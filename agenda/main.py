import web
import sqlite3

urls = (
    "/", "Index",
    "/insertar","Insertar",
    )

render = web.template.render("templates/")

app = web.application(urls, globals())

class Index:
    def GET(self):
        try:
            conection = sqlite3.connect("agenda.db")
            cursor = conection.cursor()
            personas = cursor.execute("select * from personas;")
            print(f"Consulta ejecutada correctamente")
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
            print(f"Form data: {form}")
            conection = sqlite3.connect("agenda.db")
            cursor = conection.cursor()
            sql = "INSERT INTO personas(nombre, email) VALUES (?, ?);"
            data = (form.nombre, form.email)
            cursor.execute(sql, data)
            print("Executed SQL query successfully.")
            conection.commit()
            conection.close()
            return web.seeother("/")
        except sqlite3.OperationalError as error:
            print(f"Error 002: {error.args[0]}")
            return web.seeother("/")
        except Exception as error:
            print(f"Error 003: {error.args[0]}")
            return web.seeother("/")

application = app.wsgifunc()


if __name__ == "__main__":
    app.run()
