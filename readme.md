# Información Cultural de Argentina 🎞️📖🖼️
El directorio cultural de Argentina ha sido dispuesto para el alcance de todos a través de [Datos abiertos Ministerio Cultura](https://datos.cultura.gob.ar/ "Datos abiertos Ministerio Cultura").
Mediante este programa desarrollado en Python se obtiene, procesa y luego carga esta información en una tabla en postgresql.
### Nota de versión
> Por el momento solo se extraen y cargan los datos de museos, bibliotecas y salas de cine, para 12 columnas de interés más una columna con la fecha de cargue.
Sigo trabajando en el mejoramiento del contenido para ampliar su alcance y optimizar su funcionamiento (16/09/2022) 👩‍💻

## Contenido
Este proyecto contiene los siguientes archivos:
1. **web_info.py** en el cual reposa todo el código que permite hacer la extracción, procesamiento y cargue de información en postgresql.
2. **InstalledPackages.txt** donde se listan las librerías usadas y su versión.

## Logging
El programa creará un archivo llamado **"info_cultural.log"** con los logs relevantes durante su ejecución. Este archivo se guardará en el entorno virtual.

## Checklist de los requerimientos previos
- Instalar Python en tu equipo.
- Crear y activar un entorno virtual para la utilización de este proyecto.
- Descargar y guardar el archivo "web_info.py" en la carpeta del entorno virtual.
- Instalar las librerias requeridas de Python.
- Configurar tus credenciales de acceso a postgresql en archivo .env

Veamos a continuación el detalle de cada uno de estos puntos🔎 :

### Instalación de Python
Para la ejecución del archivo **web_info.py**, es necesario que tu entorno virtual pueda ejecutar código de python. Te recomiendo este tutorial en español del canal en Youtube **Roelcode** para descargar **python 3**.
En el tutorial también te enseñan a configurar VS Code en tu equipo *(este último es **opcional**, ya que puedes ejecutar el archivo desde la consola de windows o usar la terminal de tu IDE favorito. En el paso a paso de este readme mostraré como ejecutar todo desde la consola de windows).*

[Tutorial descargar Python 3](https://www.youtube.com/watch?v=m5i-Pq-z9w8 "Tutorial descargar Python 3")

### Creación del entorno virtual
Un entorno virtual es :
> "un directorio que contiene una instalación de Python de una versión en particular, además de unos cuantos paquetes adicionales"[ Python.org - ](https://docs.python.org/es/3/tutorial/venv.html " Python.org - ")

Para ello:
1. **Identifica** la carpeta donde quieres que se instale tu entorno virtual. Por ejemplo:
`		"C:\Users\User\Desktop\Proyecto>" `
2. **Abre** la aplicación cmd en tu equipo (Windows). Puedes usar el buscador en tu equipo y digitar *cmd* para encontrarla fácilmente.
3. **Crea** la carpeta, en caso de que no la hayas creado aún. Por ejemplo:
`mkdir Proyecto`
4. **Dirigete** a la carpeta creada con el comando "*cd*". Por ejemplo:
`cd Proyecto`
5. **Ejecuta** el siguiente código para crear tu entorno virtual en la carpeta donde estás ubicado:
`		 python3 -m venv tutorial-env`
	o también:
`		py -m venv tutorial-env`

Donde:
- **tutorial-env** es el nombre del entorno virtual a crear. Puedes colocar el nombre de tu preferencia.
- **venv **es el módulo de python que ejecuta esta acción.


¡Tu entorno virtual ha sido creado!
Allí encontrarás carpetas como *"Include"*, *"Lib"*, *"Scripts"* y archivos como *"pyenv.cfg"* que sirven de base para el correcto funcionamiento del entorno virtual.

### Activación del entorno virtual

Nuevamente desde cmd y desde la carpeta raiz de tu entorno virtual ("*Proyecto*" en el caso de este ejemplo), debes ingresar lo siguiente:

`		tutorial-env\Scripts\activate`

Donde: 
- **tutorial-env** es el nombre del entorno virtual creado
- **Scripts** es una carpeta generada automaticamente cuando se creó el entorno virtual
- **activate** es uno de los archivos existentes dentro de la carpeta scripts que permite "activar" el entorno virtual

Una vez ejecutado debes poder ver algo asi:

`		 (tutorial-env) C:\Users\User\Desktop\Proyecto>`

A la izquierda y en paréntesis podrás observar el nombre del entorno virtual, si ha sido activado correctamente. De no ser así, por favor repite los pasos de activación del entorno virtual.

### Instalación de las librerías requeridas
Para garantizar que la ejecución del programa sea el apropiado, debes instalar las siguientes librerías:

	requests
	pandas
	sqlalchemy
	sqlalchemy_utils
	psycopg2
	python-decouple
	python-dotenv

Para instalarlas digita el siguiente comando en cmd (windows), **con el entorno virtual activo**:
`		pip install NombreLibreria`
Por ejemplo, para instalar python-decouple sería: 
`pip install python-decouple`

Una vez instaladas todas las librerías, debes validar que estén completas digitando en cmd(windows) el comando:
` 		pip list`

Notarás que la terminal despliega un listado de las librerías disponibles **y que en dicha lista habrán muchas más que las descritas anteriormente**.
Esto sucede porque las librerias mencionadas se instalarán junto con otras por defecto, ya que se requieren para su correcto funcionamiento.

Por ejemplo, la instalación de pandas conlleva automaticamente la instalación de numpy.
Por esta razón, se recomienda validar usando ***pip list ***que **también** estén presentes las siguientes librerias. Si no están en la lista, debes instalarlas.

	certifi
	charset-normalizer
	idna
	numpy
	python-dateutil
	pytz
	six
	urllib3

Si al finalizar las instalaciones se muestra un mensaje indicando nuevas versiones disponibles, recomiendo usar el comando que el mismo mensaje expresa, para así tener todo actualizado :tw-26a1:
Al final verás que se instalaron las siguientes **18 librerías**:

	certifi
	charset-normalizer
	greenlet
	idna
	numpy
	pandas
	pip
	python-dateutil
	python-decouple
	python-dotenv
	pytz
	psycopg2
	requests
	setuptools
	six
	SQLAlchemy
	sqlalchemy_utils
	urllib3

### Configuración de las credenciales de acceso para postgresql
Desde cmd digita el siguiente comando,  para crear un archivo .env, guardado en la carpeta de tu entorno virtual.

`		code .env`

En este archivo deberás colocar la información necesaria para la conexión a tu base postgresql:

		DEBUG=True
		TEMPLATE_DEBUG=True
		pghost="coloca el host de tu administrador postgresql"
		pgport="coloca el puerto de tu administrador postgresql"
		pguser="coloca el usuario de tu administrador postgresql"
		pgpasswd="coloca la contraseña de tu administrador postgresql"
		pgdb="coloca el nombre de la base de datos de tu administrador postgresql en donde vas a cargar la información"

La libreria **python-decouple** se encargará de tomar esta información y asignarla a los campos relacionados en **web_info.py** de forma automática.

## Ejecución del programa
Para ejecutar el programa debes:
1. **Guardar** el archivo ***web_info.py*** en la carpeta de tu entorno virtual (Siguiendo el ejemplo, se guardaría ***web_info.py*** en la carpeta ***tutorial-env***)

2. En cmd(windows) **con el entorno virtual activado**, debes **dirigirte** a la carpeta de tu entorno virtual usando el comando cd. Cuando ya te encuentres en la carpeta donde está guardado el archivo ***web_info.py***, verás una ruta similar a la siguiente:

		(tutorial-env) PS C:\Users\User\Desktop\Proyecto\tutorial-env>

3. **Ejecutar** el archivo ***web_info.py***, mediante el siguiente comando en cmd:
`python web_info.py`
4. El programa te solicitará escribir la ruta de la carpeta local donde se guardarán los archivos descargados de la página del Ministerio de Cultura, con el mensaje: ***"Por favor indica la ruta local donde se descargarán los archivos de la web"***. 
Debes colocar una ruta local con una estructura similar a la siguiente:
		C:/Users/User/Desktop/Proyecto/

Con estos pasos, el programa se ejecutará y mostrará **"Done"** cuando haya finalizado
