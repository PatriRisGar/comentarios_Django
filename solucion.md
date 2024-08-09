UT3.1. Formulario Básico en Django (Comentarios)

Crea una aplicación web en Django que permita a los usuarios enviar comentarios a través de un formulario en una página web. El formulario debe recopilar la siguiente información:

· Nombre
· Correo electrónico
· Comentario

Una vez que los usuarios envíen el formulario, los comentarios deben almacenarse en una base de datos (sqlite). Por ello deberás crear un modelo "comentarios" con los datos anteriores.

Crea las siguientes vistas:

· formulario: que muestre el formulario en una página web y lo procese cuando se envíe y almacene los comentarios en una base de datos.
· confirmación: Implementa una página de confirmación que muestre un mensaje de agradecimiento después de enviar el formulario.
· Lista_comentarios: crea una vista para una web que muestre un listado con todos los comentarios.

Para cada uno debe existir una url definida.

Algunas cuestiones

· Utiliza el sistema de formularios de Django para crear el formulario de comentarios.
· Define un modelo simple para almacenar los comentarios en la base de datos.
· La página de confirmación contendrá dos enlaces, uno para la creación de un nuevo comentario y otro para la lista de comentarios.
· La página de lista de comentarios contendrá un enlace para la creación de un nuevo enlace.
· Habilita para que se pueda puedan manejar los datos del modelo comentarios desde el administrador de Django.

---

PREPARANDO

Generamos nuevo entorno virtual llamado env2 mediante virtualenvwrapper.

```bash
    mkvirtualenv env2
```

Creamos un requirements.txt con contenido: Django~=3.2.10 para hacer la instalacion de Django ejecutamos en el terminal, para ello entramos en el entorno creado.

```bash
workon env2
pip install -r requirements.txt
```

Necesitamos un repositorio que en mi caso estará en comentarios-PatriciaRisGar, dentro creamos un .gitignore con el siguiente contenido:

```
    *.pyc
    *~
    __pycache__
    myvenv
    db.sqlite3
    /static
    .DS_Store
```

---

INICIAMOS NUEVO PROYECTO.

Coninuamos en la carpeta comentarios-PatriciaRisGar y vamos a crear nuestro proyecto.

```bash
    django-admin startproject mysite .
```

Se genera carpeta mysite y vamos a modificar los settings:

```
    TIME_ZONE = 'Europe/Berlin'
    LANGUAGE_CODE = ‘es-es’
```

Comprobamos que esté enlazado con la base de datos:

```
    DATABASES = {
        'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
```

Desde la terminal en env2 y la carpeta comentarios-PatriciaRisGar usamos:

```bash
    python manage.py migrate
```

Iniciamos el servidor:

```bash
    python manage.py runserver
```

En el navegador ponemos http://127.0.0.1:8000/ y veremos el cohete si ha seguido los pasos anteriores.

Hago commit para continuar despues con la creacion de la app.

---

Seguimos trabajando en env2 y la carpeta comentarios-PatriciaRisGar. Con el siguiente comando creamos la aplicacion:

```bash
    python manage.py startapp comments
```

Se nos crea una carpeta con el nombre de nuestra app, en este caso comentarios

Vamos a añadir taks a la settings.py de mysite. Para que reconozca la aplicacion.

```
    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'comments',
    ]
```

Editamos models.py de nuestra app para defirir la tabla y sus campos.

```python
from django.db import models

# Create your models here.

class Comentarios(models.Model):
    nombre = models.CharField(max_length=50)
    email = models.EmailField()
    comentario = models.TextField(max_length=200)

    def __str__(self):
        return self.nombre
```

Ahora necesitamos que sqlite genere la base de datos a partir del modelo. Para ello primero preparamos la migracion:

```bash
    python manage.py makemigrations comments
```

Despues aplicamos los cambios usando:

```bash
    python manage.py migrate comments
```

Tras ello creamos las views.

Primero creo Lista_comentarios, que devuelve listado con todos los comentarios. A continuacion defino formulario que será la que nos permita mostrar el formulario y cargar los datos introducidos en la bbdd. Por ultimo confirmacion nos visualizará la página que nos confirme la introduccion de los datos en la bbdd.

```python
from comments.forms import CommentForm
from django.shortcuts import redirect
from comments.models import Comentarios
from django.shortcuts import render

# Create your views here.

def lista_comentarios(request):
    comentarios = Comentarios.objects.all()
    return render(request, 'comments/list.html', {'comentarios': comentarios})

def formulario(request):
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('confirmacion')
    else:
        form = CommentForm()

    return render(request, 'comments/form.html', {'form' : form})

def confirmacion (request):
    return render(request, 'comments/confirmation.html')
```

Para definir nuestro formulario devemos modificar forms.py

```python
from comments.models import Comentarios
from django import forms


class CommentForm(forms.ModelForm):

    class Meta:
        model =  Comentarios
        fields = ("nombre","email","comentario",)
```

Añadamos ahora las urls.py de nuestra aplicacion comments para hacer los redireccionamientos correctamente.

```python
from . import views
from django.urls import path


urlpatterns = [
    path('', views.lista_comentarios, name='lista_comentarios'),
    path('formulario/', views.formulario, name='formulario'),
    path('confirmacion/', views.confirmacion, name='confirmacion'),
]
```

Para finalizar creamos una carpeta Templates y dentro de la misma otro directorio llamado comments. Aqui vamos a guardar los tres htmls que necesitamos para mostrar en nuestra app.

list.html

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Lista Comentarios</title>
  </head>
  <body>
    <h1>Listado de comentarios</h1>
    <a href=" {% url 'formulario' %} "> Añadir comentario</a>

    {% for coment in comentarios %}
    <article>
      <h2>{{ coment.nombre }}</h2>
      <p>{{ coment.email }}</p>
      <p>{{ coment.comentario }}</p>
    </article>
    {% endfor %}
  </body>
</html>
```

form.html

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Añadir comentario</title>
  </head>
  <body>
    <h1>Añadir comentario</h1>
    <form action=" {% url 'formulario' %}" method="post">
      {% csrf_token %} {{ form.as_p}}
      <button type="submit">Enviar</button>
    </form>
  </body>
</html>
```

confirmation.html

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Confirmacion</title>
  </head>
  <body>
    <h1>COMENTARIO ENVIADO</h1>
    <a href=" {% url 'lista_comentarios' %} "> Volver a listado comentarios</a>
  </body>
</html>
```

---

Ya hemos finalizado el ejercicio. Para comprobar el funcionamiento, vamos al terminal y volvemos a levantar nuestro servidor desde env2

```bash
python manage.py runserver
```

---

MODIFICACIÓN
Vistas basadas en clases (CRUD)

Documentacion usada

LIST:
https://docs.djangoproject.com/en/4.2/topics/class-based-views/intro/?authuser=0
https://ccbv.co.uk/projects/Django/4.2/django.views.generic.list/ListView/

DETAIL:
https://docs.djangoproject.com/en/4.2/ref/class-based-views/generic-display/
https://ccbv.co.uk/projects/Django/4.2/django.views.generic.detail/DetailView/

EDIT & DELETE:
https://docs.djangoproject.com/en/4.2/ref/class-based-views/generic-editing/
https://ccbv.co.uk/projects/Django/4.2/django.views.generic.edit/DeleteView/

Para ello hacemos las siguientes modificaciones:

views.py

```python
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from comments.models import Comentarios
from django.shortcuts import render

class Lista_comentarios (ListView):
    model = Comentarios
    template_name = 'comments/list.html'

class Formulario(CreateView):
    model = Comentarios
    fields = ["nombre","email", "comentario"]
    template_name  = 'comments/form.html'
    success_url = reverse_lazy("confirmacion")


class Confirmacion (View):
    def get(self,request):
        return render(request, 'comments/confirmation.html')
```

urls.py

```python
from django.urls import path
from comments.views import Confirmacion,Formulario, Lista_comentarios


urlpatterns = [
    path('',Lista_comentarios.as_view(), name='lista_comentarios'),
    path('formulario/', Formulario.as_view(), name='formulario'),
    path('confirmacion/', Confirmacion.as_view(), name='confirmacion'),
]
```

list.html

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Lista Comentarios</title>
  </head>
  <body>
    <h1>Listado de comentarios</h1>
    <a href=" {% url 'formulario' %} "> Añadir comentario</a>

    {% for coment in object_list %}
    <article>
      <h2>{{ coment.nombre }}</h2>
      <p>{{ coment.email }}</p>
      <p>{{ coment.comentario }}</p>
    </article>
    {% endfor %}
  </body>
</html>
```

```

```
