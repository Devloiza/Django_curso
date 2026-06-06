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

# Sección 5: Templates

## Para usar comando html:5
Hay que configurar en ```settings.json``` que aparezca así:
```
"emmet.includeLanguages": {
        "django-html":"html"
    }
```
Esto se puede buscar directamente en el engrane de configuración, en la barra se busca ```settings.``` y debería salir el archivo, se edita para integrar lo anterior y queda listo para usarse.

## Para acceder a las rutas de templates:
Tenemos que hacerlo en el el archivo ```settings.py``` el que le corresponde al proyecto no a la app, tiene que verse algo así para poder acceder a una ruta del template (aunque esto puede causar problemas):
```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "landing" / "templates"
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
Es mejor hacerlo directamente en el registro de la apps:
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```

## Para renderizar un html 
En lugar de mandar un string usamos ```render()``` que ya está importado por default:
```
render(request, "carpeta_app/nombre_archivo.html)
```
Obligatoriamente debemos crear la carpeta dentro de la app que se llame ```templates``` y dentro de ella otra carpeta más para poder identificar el template que deseamos, ya que se unirán al final ```templates/nombre_app```. Dentro de esta ya insertamos nuestro archivo ```.html``` que será en sí lo que se mostraría. Puede ser algo como esto al usar el comando ```html:5```:
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hola mundo</title>
</head>
<body>
    <h1>Hola mundo desde template</h1>
</body>
</html>
```

## Djando template language
### Valores dinámicos
Para enviarle valores al template sería algo como esto:
```
render(request, "nombre_app/nombre.html", {
    "name": "Ricardo",
})
```
Para usar las variables en el ```.html```:
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hola mundo</title>
</head>
<body>
    <h1>Hola mundo desde template</h1>
    <h2>{{ name }}</h2>
</body>
</html>
```

### Filtros
Som como decoradores para darle ciertas propiedades a las variables:
```
{{ variable | filter1 | filter2 | filter_n}}
```
En este enlace se encuentra toda la documentación sobre los filtros que existen en Django: https://docs.djangoproject.com/en/5.2/ref/templates/builtins/#built-in-filter-reference

### Tags
Son instrucciones que la dan más funcionalidad a los templates. Se pueden hacer cosas de lógica.
```
{% tag%} 
    {{ algo }}
{%end tag%} (algunos no necesitan el cierre)
```

#### If tag
Es muy similar a los if de MATLAB, por lo que este se usa igual que en python, pero ahora se tiene que dar explicitamente el inicio y el fin, no sólo con tabuladores, algo como esto: 
```
{% if name == "Ricardo" %}
    <h1>Hola profe</h1>
    <h2>{{ name | title}}</h2>
{% elif  name == "Fernando"%}
    <h1>Hola profe :D</h1>
{% else %}
    <h1>Hola invitado</h1>
{% endif %}
```

#### For tag
Para acceder a un elemento de la lista en los templates se debe hacer como si fuera un objeto:
```
{{lista.0}}
```
Se aplica asi y el empty sirve por si la lista se encuentra vacía no genere un error:
```
{% for tool in stack %}
    <li>{{tool}}</li>
{% empty %}
    <li>No hay tecnologías disponible</li>
{% endfor %}
```

#### URL tag
Se tiene que configurar tanto en las ```urls.py``` de la app, como esto:
```
path('stack/<str:tool>', views.stack_detail, name= "stack")
```
Y en el ```.html``` se pone como:
```
<li><a href="{% url 'alias_url' identificador %}">variable</a></li>
```
Con esto tenemos URLs dinámicas dentro del mismo ```.html```

## Herencia en los templates
Podemos heredar una plantilla para reutilizarla. Para hacer esto debemos crear una carpeta ```templates``` a nivel proyecto, se debe crear un archivo ```.html``` que recomandablemente se llame ```base.html```. Para poder poner las partes que estarán sujetas a la herencia se debe usar el tag ```{% block blockname %}```:
```
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>
    {% block blockname %}
        
    {% endblock blockname %}
    </title>
</head>
<body>
    
</body>
</html>
```
Para usarlo en otro template debemos usar el tag ```{% extends 'base.html' %}```.
Para que funciones se debe declarar en los ```settings``` del proyecto:
```
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "templates"
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]
```
## Fragmentos de templates (Include tag)
Dentro de los templates se pueden usar fragmentos para poder reciclar u optimizar la estructura, deben crearse dentro de la carpeta de la app ```templates/app_name``` o como identifiquemos nuestra carpeta de templates de la app, o también en la carpeta a nivel global de ```templates``` si es que no será exclsivo el uso en una app. Aquí se deberá crear una nueva carpeta (recmendable llamarla ```includes```) donde se guardarán estos templates. Una integración completa se vería así:
```

{% extends 'base.html' %}

{% block title %}
    Messages page
{% endblock title %}

{% block content %}
    {% include './includes/partial.html' %}
    <ul>
    {% for day in days %}
        <li><a href="{% url 'day-quote' day%}">{{day}}</a></li>
    {% empty %}

    {% endfor %}
    </ul>
    {% include './includes/endpartial.html' with days=days %}
{% endblock content %}
```
Esto también se puede usar en las plantillas generales para tener aún mejor la modulación de nuestro frontend.

## Template 404
Este template debe llamarese tal cual ```404.html``` para que al momento manejar el error con ``Http404`` se pueda desplegar el template, se debe usar así con el ```try except```:
```
raise Http404()
```
**Nota: NO funciona en modo debug, se debe poner en False esta opción en los settings, esto se retomará más adelante**

## Archivos estáticos
Son todos aquellos que se usan y no se modficarán.
Para su uso se debe crear una carpeta llamada ```static/nombre_app``` para que se pueda manejar similar a un template, para su implementación primero se debe poner en el template:
```
{% block page_style %}{% endblock page_style %}
```
Para su uso para un despligue con una app se puede hacer algo como esto:
```
{% extends 'base.html' %}

{% load static %} # Se debe cargar esto OBLIGATORIAMENTE para usar la url relativa

{% block title %}
    Messages page
{% endblock title %}

{% block page_style %}
<link rel="stylesheet" href="{% static './quotes/quotes_styles.css' %}"> # Se debe usar link para usarlo
{% endblock page_style %}

{% block content %}
    {% include './includes/partial.html' %}
    <ul>
    {% for day in days %}
        <li><a href="{% url 'day-quote' day%}">{{day}}</a></li>
    {% empty %}

    {% endfor %}
    </ul>
    {% include './includes/endpartial.html' with days=days %}
{% endblock content %}
```
Igualmente se puede usar de forma global por lo que lo común es que si se quiere usar para algun template global se pongan los statics global. Igualmente se debe agregar en ```settings``` su dirección, se debe crear una nueva variable:
```
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATICFILES_DIRS = [
    BASE_DIR / "static"
]
```

# Sección 6: Proyecto 1
## Agrupamiento de apps
Se debe crear la carpeta llamadas ```apps``` a nivel proyecto, ahí meteremos todas las apps para que quede más ordenado.
Para que funcione adecuadamente en los ```settings.py``` del proyecto debemos declarar la app pero con la carpeta incluida:
```
INSTALLED_APPS = [
    # Algo como esto:
    'apps.courses',
    'apps.dashboard',
    'apps.profiles',

    # Las que ya están por default:
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
```
E igualmente se debe configurar en los ```apps.py``` de la app:
```
class CoursesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.courses'
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