# ------------ FastAPI ------------ #
from fastapi import UploadFile, File, HTTPException, status, APIRouter
from fastapi.responses import FileResponse

# ------------ Basic libraries ------------ #
import os
import pandas as pd
import numpy as np

import joblib
from src.configuraciones import config

# ------------ from Scikit-learn ------------ #
# from sklearn.linear_model import Lasso
# from sklearn.metrics import mean_squared_error, r2_score
# from sklearn.model_selection import train_test_split
# from sklearn.pipeline import Pipeline
# from sklearn.preprocessing import MinMaxScaler, Binarizer

# # ------------ from feature-engine ------------ #
# from feature_engine.imputation import (
#     AddMissingIndicator,
#     MeanMedianImputer,
#     CategoricalImputer,
# )

# from feature_engine.encoding import (
#     RareLabelEncoder,
#     OrdinalEncoder,
# )

# from feature_engine.transformation import LogTransformer

# from feature_engine.selection import DropFeatures
# from feature_engine.wrappers import SklearnTransformerWrapper

# ------------ from .src.input ------------ #
from src.input import preprocessors as pp


router = APIRouter(
    prefix="/obtener-datos-de-usuario-y-predecir",
    tags=["Prediction"]
)

ruta_actual = os.getcwd()

def prediccion_o_inferencia(pipeline_de_test, datos_de_test):
    #Dropeamos
    datos_de_test.drop('Id', axis=1, inplace=True)
    # Cast MSSubClass as object
    datos_de_test['MSSubClass'] = datos_de_test['MSSubClass'].astype('O')
    datos_de_test = datos_de_test[config.FEATURES] #ESTA ES LA UNICA LINEA DIFERENTE DEL JUPYTER

    new_vars_with_na = [
        var for var in config.FEATURES
        if var not in config.CATEGORICAL_VARS_WITH_NA_FREQUENT +
        config.CATEGORICAL_VARS_WITH_NA_MISSING +
        config.NUMERICAL_VARS_WITH_NA
        and datos_de_test[var].isnull().sum() > 0]
    
    datos_de_test.dropna(subset=new_vars_with_na, inplace=True)

    #AQUI ESTOY HACIENDO LA INGENIERIA DE DATOS DE PIPELINE Y LA INFERENCIA DEL MODELO DE ML
    predicciones = pipeline_de_test.predict(datos_de_test)
    #ESTOY DESESCALANDO
    predicciones_sin_escalar = np.exp(predicciones)
    return predicciones, predicciones_sin_escalar, datos_de_test

@router.post("/")
def publicar_mensaje(file: UploadFile = File(...)):

    if file.content_type != 'text/csv':
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El archivo debe ser un CSV")
    
    try:
        # Guardar el archivo CSV subido temporalmente
        file_location = f"{ruta_actual}/{file.filename}"
        with open(file_location, "wb") as buffer:
            buffer.write(file.file.read())

        # Leer el archivo CSV
        df_de_los_datos_subidos = pd.read_csv(file_location)

        # Cargar el pipeline de producción desde la ruta correcta
        # NOTA: Asegúrate de que esta ruta es donde estás copiando el archivo en el Dockerfile
        ruta_modelo = os.path.join(ruta_actual, "src/precio_casas_pipeline.joblib")  # Actualización de la ruta
        pipeline_de_produccion = joblib.load(ruta_modelo)

        # Hacer la predicción
        predicciones, predicciones_sin_escalar, datos_test_procesados = prediccion_o_inferencia(pipeline_de_produccion, df_de_los_datos_subidos)

        # Concatenar los datos procesados y las predicciones
        df_concatenado = pd.concat([datos_test_procesados, pd.Series(predicciones, name="Predicciones"), pd.Series(predicciones_sin_escalar, name="Predicciones_Sin_Escalar")], axis=1)

        # Guardar el archivo de salida
        output_file = f"{ruta_actual}/salida_datos_y_predicciones.csv"
        df_concatenado.to_csv(output_file, index=False)

        # Devolver el archivo resultante
        return FileResponse(output_file, media_type="application/octet-stream", filename="salida_datos_y_predicciones.csv")

    except pd.errors.EmptyDataError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El archivo CSV está vacío o tiene un formato incorrecto.")
    except joblib.externals.loky.process_executor.TerminatedWorkerError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al cargar el modelo de predicción.")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error interno del servidor: {str(e)}")