import web
import sqlite3

urls = (
    "/", "Index",
    "/insertar", "Insertar",
    r"/detalle/(\d+)", "Detalle",
)

render = web.template.render("templates/")

app = web.application(urls, globals())

class Index:
    def GET(self):
        try:
            conection = sqlite3.connect("agenda.db")
            cursor = conection.cursor()
            cursor.execute("SELECT * FROM personas;")
            personas = cursor.fetchall()  # <-- Cambia esto
            print("Consulta ejecutada correctamente")
            return render.index(personas)
        except Exception as error:
            print("===== ERROR DETALLADO =====")
            import traceback
            traceback.print_exc()
            print("===== FIN ERROR =====")
            return "Error: " + str(error)

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
            conection.commit()
            last_id = cursor.lastrowid  # ID autoincremental recién generado
            conection.close()
            return web.seeother(f"/detalle/{last_id}")
        except sqlite3.OperationalError as error:
            print(f"Error 002: {error.args[0]}")
            return web.seeother("/")
        except Exception as error:
            print(f"Error 003: {error.args[0]}")
            return web.seeother("/")

class Detalle:
    def GET(self, id):
        try:
            con = sqlite3.connect("agenda.db")
            cursor = con.cursor()
            cursor.execute("SELECT id, nombre, email FROM personas WHERE id = ?;", (id,))
            row = cursor.fetchone()
            con.close()
            if row:
                persona = {'id': row[0], 'nombre': row[1], 'email': row[2]}
                return render.detalle(persona)
            else:
                return "Persona no encontrada"
        except Exception as error:
            print("Error en Detalle:", error)
            return "Error al mostrar el detalle"
        

application = app.wsgifunc()

if __name__ == "__main__":
    app.run()
