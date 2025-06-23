import web
import sqlite3

urls = (
    "/", "Index",
    "/insertar","Insertar",
    )

template_globals = {
    'app_path': lambda p: web.ctx.homepath + p,
}

render = web.template.render("templates/", globals=template_globals)

#render = web.template.render("templates/")

app = web.application(urls, globals())

class Index:
    def GET(self):
        try:
            conection = sqlite3.connect("agenda.db")
            cursor = conection.cursor()
            personas = cursor.execute("select * from personas;")
            print(f"PERSONAS: {personas}")
            return render.index(personas)
        except Exception as error:
            print(f"Error 000: {error.args[0]}")
            return render.index()

class Insertar:
    def GET(self):
        try:
            return render.insertar()
        except Exception as error:
            print(f"Error 001: {error.args[0]}")
            return render.insertar()
            
    def POST(self):
        try:
            form = web.input()
            conection = sqlite3.connect("agenda.db")
            cursor = conection.cursor()
            cursor.execute(
                "insert into personas(nombre,email) values (?, ?)",
                (form.nombre, form.email),
            )
            conection.commit()
            conection.close()
            print(f"Inserted: {form.nombre}, {form.email}")
            return web.seeother("/")
        except Exception as error:
            print(f"Error 002: {error.args[0]}")
            raise web.seeother("/")

app = app.wsgifunc()

if __name__ == "__main__":
    app.run()
