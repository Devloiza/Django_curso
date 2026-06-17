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

# Sección 7: Modelos y bases de datos
## Modelar datos
Es el proceso de representar estructuradamente la información de un sistema, anticipando como se ca a almacenar, consultar y relacionar la información.

### Los pasos para el diseño de una base de datos son:
1. Determinación del propósito y requisitos
2. Diseño conceptual
    a. Creación del Modelo Entidad-Relación (MER)
    b. Normalización
3. Diseño lógico
    a. Tranformación de MER a un Modelo Relacional
4. Diseño físico
5. Implenentación
6. Pruebas y evaluación
7. Mantenimiento y evaluación

## Entidad, atributo y relación
|Concepto|Definición|Ejemplo|
|:-:|:-:|:-:|
|Entidad|Objeto del mundo real representado en el sistema|Book, Author, Review|
|Atributo|Característica o propiedad de una entidad|Book.title, Author.name |
|Relación|Asociación entre entidades|Un Book está escrito por un Author|

# Sección 8: Manipulación de datos con el ORM
## ORM (Object-Relational Mapping)
Es como un traductor de un lenguaje de programación a SQL directamente.

### Para nuestro caso serán las siguientes equivalencias
* Clases - Tablas
* Atributos - Columnas
* Intancias - Filas

## Configuración de las migraciones
```
python manage.py migrate
```
Con esto se crea todo lo relacionado a los ```auth``` y ```admin``` en la base de datos.

## Uso en Django
Se debe hacer todo esto en el archivo ```models.py``` con esto se harán clases que siempre deben heredar a ```models.Model```, como ejemplo tenemos algo así sería para crear dos tablas:
```
from django.db import models

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100) # Maximo 100 letras para este campo
    birth_date = models.DateField(null=True, blank=True) # Se puede dejar vacío

class Book(models.Model):
    title = models.CharField(max_length=200)
    publicaction_date = models.DateField(null=True, blank=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name = 'books')
    pages = models.IntegerField()
    isbn = models.CharField(max_length=50)
```
Posteriormente hay que ejecutar en la terminal:
```
python manage.py makemigrations app_name
```
Esto sirve para crear la equivalencia en SQL. Es en sí un paso previo, aquí todavía no podríamos ver estas tablas en la base de datos.

Para revisar las migraciones tenemos el comando:
```
python manage.py showmigrations
```

Para ya subirlo a la base de datos se debe ejecutar:
```
python manage.py migrate
```
Básicamente teniendo doble función, para inicializar y para actualizar.

## Django shell
Es una consola integrada al proyecto, y se puede acceder a ella con esto:
```
python manage.py shell
```

### Instalación recomendada para ver mejor la terminal
```
pip install ipython
```

### Para usar el Shell
#### Creando registros:
Podemos hacer algo como lo siguiente, primero importando nuestra tabla y posteriormente creando filas:
```
from app.models import tabla

# Para crear la fila asignando valores a las columnas respectivamente
class.objects.create(col1=None, col2=None)
```
Otra forma de hacerlo es usando la instancia, o  en otras palabras, inicializamos la clase pero la guardamos hasta después:
```
variable = class(col1 = None, col2 = None)
```
Para guardarla:
```
variable.save()
```
Con esto ya se guarda directamente en la base de datos.

#### Creando regustros en lote
Se usa:
```
class.objects.bulk_create([])
```
Para esto se va a tener que instanciar la clase, aquí un ejemplo:
```
In [16]: Book.objects.bulk_create([
    ...: Book(title=" Me enamore de su software", publication_date = "2025-01-01", author = cuellar, pages = 250, isbn = "1234659845"),
    ...: Book(title="Harry Potter y el prisionero de Ecatepec", publication_date = "2025-05-11", author = cuellar, pages = 550, isbn = "165465435")])
```
Lo veo como primero, apuntar a la tabla y decir que van muchos registros. Y posteriormente creando las clases se mandan todas las variables de golpe.

**Es importante notar que se pueden usar variables, como en este caso autor ya estaba instanciado en otra variable**

#### Para crear datos de forma segura
Con segura nos referimos a evitar duplicados, para obtener o crear se usa:
```
variable = class.objects.get_or_create(col = None, defaults={"col_n": None})
```
Se puede verificar con un print (Esto hay que verificar que no sea gracias al ```__str__``` modificado).

Otra cosa que se puede hacer es actualizar o crear:
```
variable = class.objects.update_or_create(col = None, defaults={"col_n": None})
```

#### Consultas con el Shell
##### Para todo
```
class.objects.all()
```

##### Por columna específica
En este caso si se guarda en una variable obtenemos el registro en sí:
```
variable = class.objects.get(col = None)
```

##### El primero y último
```
class.objects.first()
class.objects.last()
```

#### Ordenando objectos
Se puede tanto ascendente como descendente:
```
class.objects.order_by('col_name') # Ascendente
class.objects.order_by('-col_name') # Descendente
```

Se puede por más de una columna, lo hará en orden de aparición. Se pueden usar tanto ascendentes como descendentes y sus combinaciones:
```
class.objects.order_by('col_name1', 'col_name2') 
```

Se puede ordenar al azar:
```
class.objects.order_by('?') 
```

#### Filtros
Para hacerlo se tiene que usar de la siguiente manera:
```
variable = class.objects.filter(col=None)
```
##### Campos de busqueda
Es como darle superpoderes a la busqueda, por ejemplo:
**NOTA: Se debe poner con doble guión bajo**
```
# Ejemplo
class.objects.filter(col__exact = None)

# Estructura general:
class.objects.filter(col__campo = None)
```
Aquí están todos los que se puden invocar: https://www.w3schools.com/django/django_ref_field_lookups.php **(Está bastante bien explicado en este enlace)**

Algunos de filtros vistos en la sección:
```
# Por lista
class.objects.filters(col__in = [lista])    # Devuelve aquellos dentro de la lista

# Numéricos
class.objects.filter(col__gt = numero)     # Devuelve aquellos mayores que el número umbral
class.objects.filter(col__gte = numero)    # Devuelve aquellos mayores o iguales que el número umbral
class.objects.filter(col__lt = numero)     # Devuelve aquellos menores al número umbral
class.objects.filter(col__lte = numero)    # Devuelve aquellos menores o iguales al número umbral

# Por fecha, requiere para buscar: from datetime import date
NOTA: En estos también se puede usar lo de mayor y menor que.

## Fecha completa
class.objects.filter(col__date = date(year, month, day))   # Si no es una fecha por defecto
class.objects.filter(col = date(year, month, day))         # Si es una fecha por defecto

## Por algo específico de la fecha
class.objects.filter(col__year = year)     # Busca por año específico
class.objects.filter(col__month = month)   # Busca por mes específico
class.objects.filter(col__day = day)       # Busca por día específico

```

Para encadenar filtros sólo se debe seguir poniendo en la línea de código:
```
# Con varios filtros:
class.objects.filter(col1__lt = None).filter(col2 = None)

# Combinando filtro y exclusion:
class.objects.filter(col1 = None).exclude(col2 = None)
```

Se pueden hacer list slicing:
```
# Desde el primer hasta el quinto registro
class.objects.all()[0:5]

# Desde el quinto hasta el décimo:
class.objects.all()[5:10]
```

Al final de estos se le puede añadir ```.exists()``` y nos regresa un ```bool```, por ejemplo:
```
class.objects.filter(col__strartswith = "Algo").exists()
```


##### Sensitve e insensitive
Hay dos formas de buscarlo, la sensitive, que sería tal cuál está:
```
class.objects.filter(col__cosa = None)
```
Y la insensitive, que sería más permisiva (ignora mayúsculas y minúsculas):
```
class.objects.filter(col_icosa = None)
```
##### Consulta avanzada Q (Query):
Permite usar operaciones lógicas entre la busqueda, se debe importar primero:
```
from django.db.models import Q

class.objects.filter(
    Q(col1__filtro1 = None) | Q(col2__filtro2 = None)
)
```

Ejemplo en una tabla relacional:
```
from django.db.models import Q

Book.objects.filter(Q(title__icontains = "prisionero") & Q(author__name__icontains = "Ricardo"))
```
En este ejemplo estamos filtrando que la tabla ```Book``` en la columna 'title' contenga permisivamente "prisionero" y que en la tabla ```Author``` en la columna 'name' contenga permisivamente "Ricardo". Es importante notar que la tabla ```Book``` está relacionada con la tabla ```Author```.

|Simbolo|Significado|
|:-:|:-:|
|\||or|
|&|and|


##### Consulta avanzada F (Field)
Igualmente, se debe importar primero:
```
from django.db.models import F

class.object.filter(col_1__filtro_numérico = F('colimna'))
```

#### Actualización de registros:
Se debe obtener el registro con ```get```, hacemos la modificación a la columna correspondiente y posteriormente lo guardamos.
```
variable = class.objects.get(col = None)
variable.col = None # Nuevo valor
variable.save()
```

También se pueden actualizar registros en lotes agregando al filtro ```.update()```:
```
class.objects.filter(col1 = None).update(col2 = None)
```
Esto devuelve el número de modificaciones hechas.

#### Eliminar registros:
Para eliminar de uno:
```
variable = class.objects.get(col = None)
variable.delete()
```

Para eliminar por lote:
```
class.objects.filter(col1 = None).delete()
```
**Nota: Para esto se recomienda primero hacer el filtro y despiés hacer el delete, de esta manera tenemos menos probabilidad de equivocarnos**

Para los casos en los que se borran los datos hay varias opciones pero ya dependerá de la lógica que se use para disernir cuál será la mejor opción.

Existe también el ```soft delete``` que sirve para en sí no borrar los datos pero sí ocultarlos del sistema.

#### Eliminar registros con relaciones:
Básicamente es lo mismo que obtener el registro y posteriormente usar ```delete()```. Ya dependerá de si está modelado con ```on_delete = models.CASCADE```

#### Aggregates
Son funciones adicionales a SQL, se deben importar:
```
from django.db.models import Count, Avg, Sum, Min, Max

# Se usan así:
class.objects.aggregate(col_new = Count(col1))
class.objects.aggregate(col_new = Min(col1))
```
Esto va a crear un diccionario con las keys de las ```col_new``` que utilicemos. Básicamente son como consultas de forma general.

#### Annotations
Agrega una columan virtual a cada una de las instancias de la consulta:
```
from django.db.models import Count

# Se usa asi:
variable = class.objects.annotate(col_new = Count(related_name))
```

El ```related_name``` es una variable que se asigna en el modelado de la tabla, es como una forma en la que se comunican las dos tablas relacionadas. Es como una consulta anidada.

#### Transaction Atomic
Es un conjunto de opereaciones que deben de ejecutarse todas juntas, si una falla todo se echa para atrás y no se ejecuta ninguna.

Su misión es proteger la integridad de los datos.

Se debe importar antes de usarse
```
from django.db import transaction

with transaction.atomic():
    variable = class1.objects.create(col1 = None)
    class2.objects.create(col1 = None, col2 = None, col3 = variable)


```
Este genera un ```IntegrityError``` pero si se quiere usar se debe importar como:
```
from django.db import IntegrityError
```

Se ve que es como un ```try``` pero explicitamente no lo es, incluso se puede combinar con un ```try-except```

# Sección 9. Relaciones entre modelos
## Qué es
En una base de datos relacional, una relación es una conexión lógica entre dos o más entidades, basado en datos compartidos.
Esto permite: 
- Evitar el duplicado de los datos.
- Organizar la información de forma modular.
- Consultar datos relacionados fácilmente.

## Tipos de relaciones
*Uno a Uno (1:1)*
- Cada registro de la tabla A tiene exactamente un registro de la tabla B y al revés.
- Se usa cuando se tienen datos opcionales o extendidos.

*Uno a Muchos (1:N)*
- Un registro de la tabla A puede tener muchos en la tabla B pero cada registro de B pertenece a uno sólo de A.
- Se usa cuando un dato puede tener muchas opciones de otro tipo de dato.

*Muchos a Muchos (N:M)*
- Un registro de la tabla A puede tener muchos en la tabla B y al revés. Se necesita una tabla intermedia que Django ya crea por nosotros.
- Se usa para relacionar muchos tipos de datos.

## Conceptos importantes relacionados
### Foreign Key
Campo que apunta a otro modelo y crea una relación uno a muchos.
```
class NameClass(models.Model):
    instance_relacional = models.ForeigKey(class2)
```

### on_delete
Atributo quenos ayudará a definir que sucederá cuando eliminemos un registro relacionado.
```
class NameClass(models.Model):
    instance_relacional = models.ForeigKey(class2, on_delete=models.CASCADE)
```

| Argumento | ¿Qué hace? |
|---|---|
| `CASCADE` | Elimina en cascada todos los objetos relacionados cuando se elimina el objeto referenciado. |
| `PROTECT` | Lanza una excepción `ProtectedError` e impide la eliminación si existen objetos relacionados. |
| `RESTRICT` | Similar a `PROTECT`, pero lanza `RestrictedError`. Permite la eliminación si el objeto relacionado también será eliminado en la misma operación. |
| `SET_NULL` | Establece el campo como `NULL` al eliminar el objeto referenciado. Requiere que el campo tenga `null=True`. |
| `SET_DEFAULT` | Asigna el valor por defecto del campo al eliminar el objeto referenciado. El campo debe tener un `default` definido. |
| `SET()` | Asigna un valor específico o el resultado de una función callable al eliminar el objeto referenciado. Ej: `SET(0)` o `SET(get_default)`. |
| `DO_NOTHING` | No hace nada a nivel de Django. Puede causar errores de integridad referencial en la base de datos si no se maneja a nivel de SQL. |

### related_name
Es para tener el nombre con el que accederemos desde la clase **A** a la clase **B**.
```
class NameClass(models.Model):
    instance_relacional = models.ForeigKey(class2, on_delete=models.CASCADE, related_name = "nombre_acceso")
```
*Esto es una relación uno a muchos*, en un ejemplo de uso tenemos algo asi:
De la clase ```Author``` salen ```Books```, pero para poder acceder a ```Books``` desde ```Author```
```
# Primero asignamos la fila a la variable
author = Author.objects.get(name = Autor)

# Después extraemos los libros relacionados a ese autor
author.books.all()
```

### uniques
Hace que el campo no se pueda repetir
```
class NameClass(models.Model):
    instance = models.CharField(unique = True)
```

## Relaciones
### Uno a muchos
Se usa el ForeignKey o para Django el related name. Ver más arriba en caso de dudas.
Para ejemplificarlo tenemos la siguiente tabla:
```
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_date = models.DateField(null=True, blank=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name = 'books')
    pages = models.IntegerField()
    isbn = models.CharField(max_length=50)

    def __str__(self):
        return self.title
```

### Muchos a muchos
Primero se deben crear ambas tablas para que funcione, y deben ser algo como esto:
```
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)


class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_date = models.DateField(null=True, blank=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name = 'books')
    pages = models.IntegerField()
    isbn = models.CharField(max_length=50)

    genres = models.ManyToManyField(Genre, related_name = 'books')
    def __str__(self):
        return self.title
``` 
Aquí la parte clave está en la tabla ```Book```, ya que es donde se establece la relación ```models.ManyToManyField```. Esto en la base de datos creará una nueva tabla donde se relacionarán los ```ids```.

### Uno a uno
Se puede usar para extender una tabla sin que directamente se sobrecargue, como ejemplo tenemos:
```
class BookDetail(models.Model):
    summary = models.TextField()
    cover_url = models.CharField()
    language = models.CharField()
    book = models.OneToOneField(Book, on_delete=models.CASCADE, realted_name = 'detail')
```

### select_related
**Sólo se puede usar con objetos ONE to ONE y ONE to MANY**
Para cargar los objetos relacionados en una sola consulta, optimiza las peticiones a la base de datos:
```
variable = class.objects.select_related("columna")

for var in variable:
    print(var.col.cosa)
```

### prefetch_related
**Sólo se puede usar con objetos MANY to MANY**
Es simnilar al select_related pero tiene su diferencia sobre que hay que acceder puntualmente:
```
variable = class.objects.prefetch_related("columna")

for var in variables:
    variable2 = var.col.all()
    print(variable2)
```

### Trough
Es la tabla que se crea en el intermedio de dos relaciones con los IDs, pero algunas veces querremos modificar algunas cosas:
```
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_date = models.DateField(null=True, blank=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name = 'books')
    pages = models.IntegerField()
    isbn = models.CharField(max_length=50)

    ## Modelado Muchos a Muchos
    genres = models.ManyToManyField(Genre, related_name = 'books')
    
    ## Tabla intermedia personalizada
    recommended_by = models.ManyToManyField(get_user_model(), through="Recomendation", related_name="recommendations")

    def __str__(self):
        return self.title

class Recomendation(models.Model):
    user = models.ForeignKey(get_user_model, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    recommended_at = models.DateField(auto_now_add=True)
    note = models.TextField(blank=True)

    # Esto funciona como un settings, es una clase de configuración:
    class Meta:
        unique_together = ("user", "book")
```
Hacer esto nos bloquea usar los métodos ```add()``` y ```remove()```. Ahora se usa como una tabla normal.

### Seeds
Se debe crear la carpeta ```seeds/``` con el archivo ```seed.py```.

Se debe usar este comando en windows:
```python manage.py shell -c "exec(open('seeds/seed.py', encoding='utf-8').read())```

## Modelo USER
Modelo de usuario por default de Django, se crea en automático.

Se debe acceder a él de la siguiente manera:
```
# Forma general
from django.contrib.auth.models import User

# Forma flexible para que no truene:
from django.contrib.auth import get_user_model

User = get_user_model()
```

Para inicializar el user con el hash para la contraseña se hace esto:
```
from django.contrib.auth import get_user_model

User = get_user_model()
User.objects.create_user()
```

#### Asignar y obtener valores
Se debe usar el método ```.add()```, como ejemplo tenemos una variable de la tabla ```Book``` que contiene un libro, y se le añadirán los generos ya establecidos en las variables de ```fiction``` y ```drama```, estos igual se tienen que declarar en la tabla de ```Genres```:
```
# Primero se crean o se asignan:
fiction = Genre.objects.get(name = "fiction")

# Posteriormente se relacionan con el libro
book.genres.add(fiction, drama)
```
Con esto ya podemos relacionar tanto de generos a libros como de libros a generos con su respectivo ```related_name```

# Sección 10. Django Admin
Es como un shell pero sin la parte de la terminal explícita. Se debe crear un usuario con permisos de administrador pese a que ya se incluye en la configuración básica de Django, esto se debe hacer en la terminal:
```
python manage.py createsuperuser
```
Se rellenan los campos y listo. Con esto ya se pueden manipular varias cosas.

## Usar modelos en admin
Primero debemos ir al archivo ```admin.py``` e importar los modelos que queremos usar:
```
from django.contrib import admin
from .models import Author, Genre, Book, BookDetail, Review, Loans

# Register your models here.

admin.site.register(Author)
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(BookDetail)
admin.site.register(Review)
admin.site.register(Loans)
```
Para el admin sí juega un papel importante el metodo ```__str__```, ya que así es como se nos mostrará en la parte visual.
```
class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name
```
Para la parte de darle personalización a los modelos debemos hacer algo como esto:
```
from django.contrib import admin
from .models import Author, Genre, Book, BookDetail, Review, Loans

# Register your models here.

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'pages', 'publication_date')

    # No olvidar que author es una llave foranea y que con el __ podemos acceder a ella
    search_fields = ('title', 'author__name') 
    
    list_filter = ('author', 'genres', 'publication_date')

    # Ordenar, de forma decendente (usa lista)
    ordering = ['-publication_date'] 

    date_hierarchy = 'publication_date'

# Asi se registra en el admin el modelo deseado
admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(Book, BookAdmin) # O con el decorador
admin.site.register(BookDetail)
admin.site.register(Review)
admin.site.register(Loans)
```
Para la parte del decorador (```@admin.register(Book)```), también tenemos que modificar el modelo a algo como esto:
```
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_date = models.DateField(null=True, blank=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name = 'books')
    pages = models.IntegerField()
    isbn = models.CharField(max_length=50)

    ## Modelado Muchos a Muchos
    genres = models.ManyToManyField(Genre, related_name = 'books')
    
    ## Tabla intermedia personalizada
    recommended_by = models.ManyToManyField(get_user_model(), through="Recomendation", related_name="recommendations")

    # Con esto configuramos los settings de la clase. ## ESTO ES LO QUE SE MODIFICA
    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'

    def __str__(self):
        return self.title
```

## Registros inline
Son registros relacionados. (UNO a UNO / UNO a MUCHOS (ForeignKey)), esto debe ir en ```admin.py```:
```
from django.contrib import admin
from .models import Author, Genre, Book, BookDetail, Review, Loans

# Register your models here.

## Inline One to many
class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

## Inline One to One
class BookDetailInline(admin.StackedInline):
    model = BookDetail
    can_delete = False
    verbose_name_plural = "Detalle del libro"

## Registro de modelos
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # Inline
    inlines = [ReviewInline, BookDetailInline]

    list_display = ('title', 'author', 'pages', 'publication_date')

    # No olvidar que author es una llave foranea y que con el __ podemos acceder a ella
    search_fields = ('title', 'author__name') 
    
    list_filter = ('author', 'genres', 'publication_date')

    # Ordenar, de forma decendente (usa lista)
    ordering = ['-publication_date'] 

    date_hierarchy = 'publication_date'


admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(Book, BookAdmin)

admin.site.register(BookDetail)
admin.site.register(Review)
admin.site.register(Loans)
```

## Inlines en modelos de Django
Se debe hacer algo como esto, por ejemplo para la parte del user:
```
from django.contrib import admin
from .models import Author, Genre, Book, BookDetail, Review, Loans

## Se deben importar estos de Django
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Register your models here.

## Inline a User (default de Django)
User = get_user_model()
class LoanInline(admin.TabularInline):
    model = Loans
    extra = 1

# Más modificaciones 
@admin.register(Loans)
class LoanAdmin(admin.ModelAdmin):
    readonly_fields = ("loan_date",)
    list_display = ("user", "book", "loan_date", "is_returned")


## Inline One to many
class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

## Inline One to One
class BookDetailInline(admin.StackedInline):
    model = BookDetail
    can_delete = False
    verbose_name_plural = "Detalle del libro"

## Creando el custom admin
class CustomUserAdmin(BaseUserAdmin):
    inlines = [LoanInline]
    list_display = ("username", "email")

## Registro de modelos
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    readonly_fields = ("pages",)
    # Inline
    inlines = [ReviewInline, BookDetailInline]

    list_display = ('title', 'author', 'pages', 'publication_date')

    # No olvidar que author es una llave foranea y que con el __ podemos acceder a ella
    search_fields = ('title', 'author__name') 
    
    list_filter = ('author', 'genres', 'publication_date')

    # Ordenar, de forma decendente (usa lista)
    ordering = ['-publication_date'] 

    date_hierarchy = 'publication_date'

    fieldsets = (
        ("Información general",{
            "fields": ("title", "author", "publication_date", "genres"),
        }),
        ("Detalles", {
            "fields": ("isbn", "pages"),
            "classes": ("collapse",)
        }
        )
    )

admin.site.register(Author)
admin.site.register(Genre)
# admin.site.register(Book, BookAdmin)
admin.site.register(BookDetail)
admin.site.register(Review)
# admin.site.register(Loans)

## Desregistrar y volcer a asignar
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered: 
    pass

admin.site.register(User, CustomUserAdmin)
```

## Actions
Sirve para ejecutar funciones sobre varios registros seleccionados.
Primero se debe poner el decorador ```@admin.action```:
```
# Aquí tenemos el action
@admin.action(description="Marcar préstamos como devueltos")
def mark_as_returned(modeladmin, request, queryset):
    queryset.update(is_returned = True)


class LoanInline(admin.TabularInline):
    model = Loans
    extra = 1

# Más modificaciones 
@admin.register(Loans)
class LoanAdmin(admin.ModelAdmin):
    readonly_fields = ("loan_date",)
    list_display = ("user", "book", "loan_date", "is_returned")
    actions = [mark_as_returned]
```
En la parte de hacer el action debemos forzosamente poner el ```modeladmin``` y el ```request```.

## Autocomplete Field
Sirve para generar una forma más rápida de rellenar los registros, no es directamente un autocompletado pero sí es mucho más fácil organizar entre tantas opciones:
```
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ["name"]

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ["name"]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    readonly_fields = ("pages",)
    # Inline
    inlines = [ReviewInline, BookDetailInline]

    list_display = ('title', 'author', 'pages', 'publication_date')

    # No olvidar que author es una llave foranea y que con el __ podemos acceder a ella
    search_fields = ('title', 'author__name') 
    
    list_filter = ('author', 'genres', 'publication_date')

    # Autocomplete field
    autocomplete_fields = ["author", "genres"] # Para que esto funcione debemos crear el AuthorAdmin

    # Ordenar, de forma decendente (usa lista)
    ordering = ['-publication_date'] 

    date_hierarchy = 'publication_date'

    fieldsets = (
        ("Información general",{
            "fields": ("title", "author", "publication_date", "genres"),
        }),
        ("Detalles", {
            "fields": ("isbn", "pages"),
            "classes": ("collapse",)
        }
        )
    )
```
Otra opción es usar el ```raw_id```:
```
@admin.register(Loans)
class LoanAdmin(admin.ModelAdmin):
    readonly_fields = ("loan_date",)
    list_display = ("user", "book", "loan_date", "is_returned")
    actions = [mark_as_returned]
    raw_id_fields = ["user", "book"]
```
Esto es básicamente similar pero está más aislado, creo que sólo seria conveniente si hay demasiados que de plano sea más sencillo buscarlo directamente en la base de datos.

## Seguridad, acceso y grupos
Para establecer roles, se puede hacer directo desde el admin de Django creando el usuario y posteriormente asignando los premisos a él o al grupo al que pertenecerá.
O también se puede por código, esto s recomienda especialmente si son cosas que queremos estar 100% seguros que deben ser así:
```
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    readonly_fields = ("pages",)
    # Inline
    inlines = [ReviewInline, BookDetailInline]

    list_display = ('title', 'author', 'pages', 'publication_date')

    # No olvidar que author es una llave foranea y que con el __ podemos acceder a ella
    search_fields = ('title', 'author__name') 
    
    list_filter = ('author', 'genres', 'publication_date')

    # Autocomplete field
    autocomplete_fields = ["author", "genres"] # Para que esto funcione debemos crear el AuthorAdmin

    # Ordenar, de forma decendente (usa lista)
    ordering = ['-publication_date'] 

    date_hierarchy = 'publication_date'

    fieldsets = (
        ("Información general",{
            "fields": ("title", "author", "publication_date", "genres"),
        }),
        ("Detalles", {
            "fields": ("isbn", "pages"),
            "classes": ("collapse",)
        }
        )
    )

    def has_add_permission(self, request):
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj = None):
        return request.user.is_staff
```

## Brandig personalizado
Las cosas como el idioma u hora se deben hacer directamente en el ```settings.py``` del proyecto.
Para la parte de los títulos y esas cosas relacionadas a Django:
```
from django.contrib import admin
from .models import Author, Genre, Book, BookDetail, Review, Loans

## Se deben importar estos de Django
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



# Register your models here.
admin.site.site_header = "Administrador MiniLibrary"
admin.site.site_title = "MiniLibrary panel"
admin.site.index_title = "Bienvenidos al panel de MiniLibrary"
```

Para más información se puede consultar siguiente enlace: https://docs.djangoproject.com/es/6.0/ref/django-admin/

# Algunos comandos de SQLite:
Para buscar similares:
```
SELECT * FROM tabla WHERE columna LIKE "%palabra%"
```
Los porcentajes sirven para indicar si queremos buscar entre palabras, por ejemplo en medio de, antes de o después de.

Consultas anidadas:
```
SELECT columna1 FROM tabla1 WHERE columna2 = (
    SELECT columna_relacionada FROM tabla 2 WHERE columna3 = "cosa"
);
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