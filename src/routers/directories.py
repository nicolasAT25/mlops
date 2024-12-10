from fastapi import APIRouter

import os
import subprocess

router = APIRouter(
    prefix="/directories",
    tags=["Directories"]
)

ruta_actual = os.getcwd()

@router.get("/ruta-actual")
def fun_ruta_actual():
    return {f"mensaje: {ruta_actual}"} #/usr/src/app

#Acceso mediante: /list_files_ruta_actual
@router.get("/list_files_ruta_actual")
def list_files():
    #Obtenemos el directorio actual
    current_directory = subprocess.check_output(['pwd'], text=True).strip()
    #Ejecutamos el comando 'ls' y capturamos la salida
    result = subprocess.check_output(['ls'], text=True)
    #Devolvemos el directorio actual y la lista de archivos
    return {"directory": current_directory, "files": result.splitlines()} #requirements.txt, src

#Acceso mediante: /rutasinofuente/list_files_ruta_actual_src
@router.get("/list_files_ruta_actual_src")
def list_src_files():
    result = subprocess.check_output(['ls', 'src'], text=True)
    return {"directory": "src", "files": result.splitlines()}