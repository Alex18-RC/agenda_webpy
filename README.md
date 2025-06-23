# agenda_webpy
Ejemplo de una aplicacion web con SQLite3 y web.py


## 1. Instalar gunicorn

**gunicorn** es WSGI HTTP Server para UNIX/Linux


gunicorn -b 0.0.0.0:8080 main:app

sudo gunicorn -b 0.0.0.0:80 main:app

python3 main.py 8080

sudo python3 main.py 80

Set-ExecutionPolicy Unrestricted -Scope Process



waitress-serve --listen=*:8080 main:app


$ detalle = '/detalle/%s' % persona[0]
                    $ editar = '/editar/%s' % persona[0]
                    $ borrar = '/borrar/%s' % persona[0]