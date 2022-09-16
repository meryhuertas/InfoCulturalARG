"""El siguiente programa extrae informacion cultural de argentina desde sitio web oficial
procesa la informacion y la carga a una base en postgresql"""
import os  # libreria para interaccion con el sistema operativo (crear y modificar carpetas)
from datetime import date  # libreria para identificar fecha actual
import logging # libreria para la creacion de logs en info_cultural.log
import requests  # libreria para extraccion info de pagina web
import pandas as pd # libreria para procesamiento de datos
import numpy as np # libreria para calculos matematicos
from decouple import config # config de las var de entorno para la conexion con postgresql
import sqlalchemy # libreria para conexion con postgresql
from sqlalchemy import create_engine # herramienta para conexion con postgresql
from sqlalchemy.orm import sessionmaker # herramienta para crear la sesion con postgresql
from sqlalchemy_utils import database_exists, create_database # creacion de la base en postgresql

def main():
    # Configuracion logging, se puede cambiar el filename si se desea
    logging.basicConfig(filename="info_cultural.log",level=logging.DEBUG)

    # Colocar la ruta del entorno virtual
    local_route=input("Por favor indica la ruta local donde se descargarán los archivos de la web :")

    # Relacionar las url de los archivos csv a descargar
    link_1 = "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/4207def0-2ff7-41d5-9095-d42ae8207a5d/download/museos_datosabiertos.csv"
    link_2 = "https://datos.cultura.gob.ar/dataset/37305de4-3cce-4d4b-9d9a-fec3ca61d09f/resource/01c6c048-dbeb-44e0-8efa-6944f73715d7/download/biblioteca_popular.csv"
    link_3 = "https://datos.cultura.gob.ar/dataset/0560ef96-55ca-4026-b70a-d638e1541c05/resource/b8bf0459-16a5-430b-b8e1-4fb786572469/download/salas_cine.csv"
    # creacion de diccionarios
    # month_dict es el diccionario que relaciona el mes de la libreria time, con
    # numero y texto en español
    month_dict = {
        1: {
            "num": "01",
            "name": "enero"},
        2: {
            "num": "02",
            "name": "febrero"},
        3: {
            "num": "03",
            "name": "marzo"},
        4: {
            "num": "04",
            "name": "abril"},
        5: {
            "num": "05",
            "name": "mayo"},
        6: {
            "num": "06",
            "name": "junio"},
        7: {
            "num": "07",
            "name": "julio"},
        8: {
            "num": "08",
            "name": "agosto"},
        9: {
            "num": "09",
            "name": "septiembre"},
        10: {
            "num": "10",
            "name": "octubre"},
        11: {
            "num": "11",
            "name": "noviembre"},
        12: {
            "num": "12",
            "name": "diciembre"},
    }
    final_columns={ #diccionario con las columnas de interes para el final_file
    "cod_localidad":["cod_localidad","Cod_Loc"],
    "id_provincia":["id_provincia","IdProvincia","Id_Provincia"],
    "id_departamento":["id_departamento","IdDepartamento","Id_Departamento"],
    "categoria":["categoría","Categoría","categoria","Categoria"],
    "provincia":["provincia","Provincia"],
    "localidad":["localidad","Localidad"],
    "nombre":["nombre","Nombre"],
    "domicilio":["domicilio","Domicilio"],
    "codigo_postal":["CP","cp","código_postal","Código_postal"],
    "numero_de_telefono":["Teléfono","telefono"],
    "mail":["mail","Mail"],
    "web": ["web","Web"]
    }
    # determinacion de variables de tiempo, segun fecha actual
    today = date.today()  # fecha actual
    day_num=today.day #dia en numero
    month=today.month #mes en formato M
    year=today.year #año en formato YYYY
    # buscar llave month en month_dict y extrae el mes en texto español
    month_name = month_dict[month]["name"]
    # buscar llave month en month_dict y extrae el mes en numero
    month_num = month_dict[month]["num"]
    #obtencion de la informacion web
    download_list = [link_1, link_2, link_3]
    get_files(download_list,year,month_name,day_num,month_num,local_route)
    #procesamiento de los datos
    final_file = data_processing(final_columns,year,month_name,day_num,month_num,today,local_route)
    #conexion con postgresql
    engine = get_engine(
    user=config("pguser"),
    passwd=config("pgpasswd"),
    host=config("pghost"),
    port=int(config("pgport")),
    db=config("pgdb")
    )
    get_session(engine)
    #cargue de info en postgresql
    file_upload(final_file,engine)
    print("Done") #mensaje al finalizar la ejecución

#Utilizar request para obtener la info y guardar localmente
def get_files(download_list,year,month_name,day_num,month_num,local_route):
    for link in download_list:
        r = requests.get(link)
        if "museos" in link:
            category = "museos"  # category igual a museos, si el link contiene la palabra museos
        elif "biblioteca" in link:
            # category igual a bibliotecas, si el link contiene la palabra
            # bibliotecas
            category = "bibliotecas"
        elif "salas_cine" in link:
            # category igual a salas_cine, si el link contiene la palabra
            # salas_cine
            category = "salas_cine"
    # indicar la ruta donde se guardaran los archivos csv
        newpath = f'{local_route}{category}/{year}-{month_name}'
        if not os.path.exists(newpath):
            os.makedirs(newpath)  # si el directorio no existe, entonces crear uno
    # guardar en el directorio creado / especificado anteriormente, el archivo
    # con el nombre modificado y extension csv
        open(f"{local_route}{category}/{year}-{month_name}/{category}-{int(day_num):02}-{month_num}-{year}.csv","wb").write(r.content)
        logging.info(f"Archivo '{category}' guardado localmente")

#funcion que permite procesar los archivos y compilarlos en un solo dataframe
def data_processing(final_columns,year,month_name,day_num,month_num,today,local_route):
    columns_keys = list(final_columns.keys())
    #info de museos
    df_museos = pd.read_csv(f"{local_route}museos/{year}-{month_name}/museos-{int(day_num):02}-{month_num}-{year}.csv", sep=",")  
    for column in df_museos.columns:
        new_column = return_key(column,final_columns)
        df_museos.rename(columns={column:new_column}, inplace=True)
    df_museos_subset = df_museos[np.intersect1d(df_museos.columns, columns_keys)]
    #info de bibliotecas
    df_bibliotecas = pd.read_csv(f"{local_route}bibliotecas/{year}-{month_name}/bibliotecas-{int(day_num):02}-{month_num}-{year}.csv", sep=",")
    for column in df_bibliotecas.columns:
        new_column = return_key(column, final_columns)
        df_bibliotecas.rename(columns={column:new_column}, inplace=True)
    df_bibliotecas_subset = df_bibliotecas[np.intersect1d(df_bibliotecas.columns, columns_keys)]
    df_bibliotecas_subset = df_bibliotecas_subset.astype({"web":str})
    #info de salas de cine
    df_salas_cine = pd.read_csv(f"{local_route}salas_cine/{year}-{month_name}/salas_cine-{int(day_num):02}-{month_num}-{year}.csv", sep=",")  
    for column in df_salas_cine.columns:
        new_column = return_key(column, final_columns)
        df_salas_cine.rename(columns={column:new_column}, inplace=True)
    df_salas_cine_subset = df_salas_cine[np.intersect1d(df_salas_cine.columns, columns_keys)]
    df_salas_cine_subset = df_salas_cine_subset.astype({"codigo_postal":str})
    #creacion de una sola tabla que compila la info de los anteriores subsets
    df_info_cultural =pd.concat([df_museos_subset,df_bibliotecas_subset, df_salas_cine_subset],
                        axis = 0)
    #creacion de columna con la fecha de carga
    df_info_cultural = df_info_cultural.assign(fecha_carga = today)
    df_info_cultural["fecha_carga"] = pd.to_datetime(df_info_cultural["fecha_carga"])
    return df_info_cultural

#funcion para encontrar column en los valores del dict final_columns
#retona la llave o nombre de columna estandarizada
def return_key (column,final_columns): # column es un string
    for key, value in final_columns.items():
        if column in value:
            return key
    return column

#funcion que retorna la conexion con postgresql
def get_engine(user, passwd, host, port, db):
    url = f"postgresql://{user}:{passwd}@{host}:{port}/{db}"
    if not database_exists(url):
        create_database(url)
    engine=create_engine(url, echo=False)
    return engine

#funcion que retorna la sesion de postgresql
def get_session(engine):
    session = sessionmaker(bind=engine)()
    return session

#funcion que carga el final_file en postgresql
#devuelve las columnas cargadas y tipo de datos en info_cultural.log
def file_upload(final_file,engine):
    sql_tabla = "info_cultural" #nombre de la tabla a crear en postgresql
    final_file.to_sql(sql_tabla, con=engine, if_exists="replace")
    logging.info(f"Se ha cargado el dataframe a la tabla {sql_tabla} en postgresql")
    for i in engine.execute(
        "SELECT TABLE_NAME,COLUMN_NAME,DATA_TYPE FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME='info_cultural'"
        ):
        logging.debug(i)

if __name__ == "__main__":
    main()
