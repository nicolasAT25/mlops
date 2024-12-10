# ------------ FastAPI ------------ #
from fastapi import FastAPI


from .routers import directories, predictions

# import subprocess

# # ------------ from Scikit-learn ------------ #
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
from .input import preprocessors as pp

# ------------------------------------------------------------------------------------ #

app = FastAPI(title='Proyecto Modelo ML\n - Nicolás Aranguren - DATAPATH')

app.include_router(predictions.router)
app.include_router(directories.router)

# models.Base.metadata.create_all(bind=engine)

# ruta_actual = os.getcwd()

# def prediccion_o_inferencia(pipeline_de_test, datos_de_test):
#     #Dropeamos
#     datos_de_test.drop('Id', axis=1, inplace=True)
#     # Cast MSSubClass as object
#     datos_de_test['MSSubClass'] = datos_de_test['MSSubClass'].astype('O')
#     datos_de_test = datos_de_test[config.FEATURES] #ESTA ES LA UNICA LINEA DIFERENTE DEL JUPYTER

#     new_vars_with_na = [
#         var for var in config.FEATURES
#         if var not in config.CATEGORICAL_VARS_WITH_NA_FREQUENT +
#         config.CATEGORICAL_VARS_WITH_NA_MISSING +
#         config.NUMERICAL_VARS_WITH_NA
#         and datos_de_test[var].isnull().sum() > 0]
    
#     datos_de_test.dropna(subset=new_vars_with_na, inplace=True)

#     #AQUI ESTOY HACIENDO LA INGENIERIA DE DATOS DE PIPELINE Y LA INFERENCIA DEL MODELO DE ML
#     predicciones = pipeline_de_test.predict(datos_de_test)
#     #ESTOY DESESCALANDO
#     predicciones_sin_escalar = np.exp(predicciones)
#     return predicciones, predicciones_sin_escalar, datos_de_test

@app.get("/") #Endpoint Raiz
def root():
    return {"mensaje": "Testando API"}

# @app.get("/ruta-actual")
# def fun_ruta_actual():
#     return {f"mensaje: {ruta_actual}"} #/usr/src/app

# #Acceso mediante: /list_files_ruta_actual
# @app.get("/list_files_ruta_actual")
# def list_files():
#     #Obtenemos el directorio actual
#     current_directory = subprocess.check_output(['pwd'], text=True).strip()
#     #Ejecutamos el comando 'ls' y capturamos la salida
#     result = subprocess.check_output(['ls'], text=True)
#     #Devolvemos el directorio actual y la lista de archivos
#     return {"directory": current_directory, "files": result.splitlines()} #requirements.txt, src

# #Acceso mediante: /rutasinofuente/list_files_ruta_actual_src
# @app.get("/list_files_ruta_actual_src")
# def list_src_files():
#     result = subprocess.check_output(['ls', 'src'], text=True)
#     return {"directory": "src", "files": result.splitlines()}

# @app.post("/obtener-datos-de-usuario-y-predecir")
# def publicar_mensaje(file: UploadFile = File(...)):

#     if file.content_type != 'text/csv':
#         raise HTTPException(status_code=400, detail="El archivo debe ser un CSV")
    
#     try:
#         # Guardar el archivo CSV subido temporalmente
#         file_location = f"{ruta_actual}/{file.filename}"
#         with open(file_location, "wb") as buffer:
#             buffer.write(file.file.read())

#         # Leer el archivo CSV
#         df_de_los_datos_subidos = pd.read_csv(file_location)

#         # Cargar el pipeline de producción desde la ruta correcta
#         # NOTA: Asegúrate de que esta ruta es donde estás copiando el archivo en el Dockerfile
#         ruta_modelo = os.path.join(ruta_actual, "src/precio_casas_pipeline.joblib")  # Actualización de la ruta
#         pipeline_de_produccion = joblib.load(ruta_modelo)

#         # Hacer la predicción
#         predicciones, predicciones_sin_escalar, datos_test_procesados = prediccion_o_inferencia(pipeline_de_produccion, df_de_los_datos_subidos)

#         # Concatenar los datos procesados y las predicciones
#         df_concatenado = pd.concat([datos_test_procesados, pd.Series(predicciones, name="Predicciones"), pd.Series(predicciones_sin_escalar, name="Predicciones_Sin_Escalar")], axis=1)

#         # Guardar el archivo de salida
#         output_file = f"{ruta_actual}/salida_datos_y_predicciones.csv"
#         df_concatenado.to_csv(output_file, index=False)

#         # Devolver el archivo resultante
#         return FileResponse(output_file, media_type="application/octet-stream", filename="salida_datos_y_predicciones.csv")

#     except pd.errors.EmptyDataError:
#         raise HTTPException(status_code=400, detail="El archivo CSV está vacío o tiene un formato incorrecto.")
#     except joblib.externals.loky.process_executor.TerminatedWorkerError:
#         raise HTTPException(status_code=500, detail="Error al cargar el modelo de predicción.")
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Error interno del servidor: {str(e)}")
