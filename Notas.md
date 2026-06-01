# Sección 3: Fundamentos Django

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

# Sección 4: URLs y Views
* **URLs**: Direcciones que nos llevan a un lugar.
* **Views**: Maneja la lógica que se maneja en las URLs (métodos HTTP).

## URLs
Para esta sección se deben enlazar las urls de las apps con el archivo de ```urls.py``` de modo que se tenga algo como esto dentro de ese archivo:
```
from django.contrib import admin
from django.urls import path, include # Aquí tenemos que agregar el 'include'

urlpatterns = [
    path('admin/', admin.site.urls), # Este es el original
    path('quotes/', include("quotes.urls")) # Este es el de la app
]
```

### Rutas dinámicas
Para esto se puede hacer con una variable en este estilo, dentro de la app en su archivo personalizado:
```
from django.urls import path
from . import views

urlpatterns = [
    path("<day>", views.days_week)
]
```

Y para usarlo se tiene algo como esto, dentro del ```urls.py``` en config:
```
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quotes/', include("quotes.urls"))
]
```

### Convertidores de rutas
Es como tener un tipado para lo que se le pasará a la url dinamica:
```
urlpatterns = [
    path("<int:day>", views.days_week_num),
    path("<str:day>", views.days_week)
]
```
Nota: Es muy importante considerar que el orden de aparición sí afecta en esto, principalmente si hay un **string** primero porque aparentemente todo lo puede interpretar como string. Tal vez se pueda solucionar intentando tipar la entrada antes para especificar de origen el tipo y solo asociarlo con su url.

### Redirecciones
Se requiere importar de ```django.http``` el comando ```HttpResponseRedirect```, se tiene que usar un URL para la redirección:
```
def days_week_num(request, day):
    return HttpResponseRedirect("/quotes/sunday")
```

### HTTP Status codes más comunes
* 2xx - Success
    * 200 - Success/OK
    * 201 - Created
    * 202 - Accepted
* 3xx - Redirection
    * 301 - Permanent redirection
    * 302 - Temporary redirect
    * 303 - Not modified
* 4xx - Client Error
    * 401 - Unauthorized error
    * 403 - Forbidden
    * 404 - Not found
* 5xx - Server error
    * 501 - Not implemented
    * 502 - Bad gateway
    * 503 - Service unavailable

Para ver todos los errores aquí hay una página que los contiene: https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Status

### Named URLs
Es como tener un alias para nuestras rutas, se usa la keyword ```name``` dentro de ```path()```:

```
urlpatterns = [
    path("<int:day>", views.days_week_num),
    path("<str:day>", views.days_week, name = "day-quote")
]
```

### Función reversiva
Sirve para acceder a las rutas de forma dinámica, previniendo malas implementaciones y hardcode:
```
def days_week_num(request, day):
    days = list(days_of_week.keys())
    if day > len(days) or day == 0:
        return HttpResponseNotFound("El día no existe")
    redirect_day = days[day-1]
    redirect_path = reverse("day-quote", args = [redirect_day]) # AQUI ESTÁ
    return HttpResponseRedirect(redirect_path)
```

# Algunos comandos de terminal útiles
Para leer el txt en la terminal:
```
cat requirements.txt
```
Para crear una carpeta:
```
mkdir nombre_carpeta
```