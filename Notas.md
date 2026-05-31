# Notas

## Qué es django
* Es un framework de desarrollo web de alto nivel para python.
* Baterías incluidas.
    * Tiene de casi todo para montarlo rápido.

## Para instalar de forma global
_Esto se tiene que hacer en Powershell_
```
python pip install Django
```

## Para instalarlo con venv
Para crearlo:
```
python -m venv nombre_venv
```
Para activarlo:
```
venv\Scripts\activate
```
Para dejar el archivo de requerimientos:
```
pip freeze > requirements.txt
```

## Para crear un proyecto en Django
Desde cero:
```
django-admin startproject nombre_proyecto
```
Desde una carpeta existente (debemos estar dentro de la carpeta): _Esto es lo más recomendado_
```
django-admin startproject nombre_proyecto .
```
_Se recomienda llamarle config a esta carpeta dentro del proyecto_

### Para crear nuestro servidor de desarrollo
*Tenemos que estar en la carpeta del proyecto para que se ejecute adecuadamente*
```
python manage.py runserver
```

### Para crear nuestras apps (paquetes) con Django
```
python manage.py startapp nombre_app
```


## Algunos comandos de terinal útiles
Para leer el txt en la terminal:
```
cat requirements.txt
```
Para crear una carpeta:
```
mkdir nombre_carpeta
```