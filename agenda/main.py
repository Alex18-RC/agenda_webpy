import web
import sqlite3

urls = (
    "/", "Index",
    "/insertar", "Insertar",
    r"/detalle/(\d+)", "Detalle",
    r"/editar/(\d+)", "Editar",
    r"/borrar/(\d+)", "Borrar",
)

web.template.Template.globals.clear()
render = web.template.render("templates/")

class Index:
    def GET(self):
        conn = sqlite3.connect('agenda.db')
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM personas")
        rows = cursor.fetchall()
        personas = [tuple(row) for row in rows]  # <-- Conversión aquí
        conn.close()
        return render.index(personas)


class Insertar:
    def GET(self):
        return render.insertar()

    def POST(self):
        data = web.input()
        nombre = data.get('nombre')
        email = data.get('email')
        conn = sqlite3.connect('agenda.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO personas (nombre, email) VALUES (?, ?)", (nombre, email))
        conn.commit()
        conn.close()
        raise web.seeother('/')


class Detalle:
    def GET(self, id):
        try:
            conn = sqlite3.connect("agenda.db")
            conn.row_factory = sqlite3.Row 
            cur = conn.cursor()
            cur.execute("SELECT * FROM personas WHERE id = ?", (id,))
            persona = cur.fetchone()
            conn.close()

            if persona:
                return render.detalle({"persona": dict(persona), "error": None})
            else:
                return render.detalle({"persona": None, "error": "Persona no encontrada"})
        except Exception as e:
            return render.detalle({"persona": None, "error": str(e)})
        


class Editar:
    def GET(self, id):
        try:
            conn = sqlite3.connect("agenda.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM personas WHERE id = ?", (id,))
            persona = cursor.fetchone()
            conn.close()

            if persona:
                return render.editar(persona=dict(persona), error=None)
            else:
                return render.editar(persona=None, error="Persona no encontrada")
        except Exception as e:
            return render.editar(persona=None, error=str(e))

    def POST(self, id):
        data = web.input()
        nombre = data.get('nombre')
        email = data.get('email')

        try:
            conn = sqlite3.connect("agenda.db")
            cursor = conn.cursor()
            cursor.execute("UPDATE personas SET nombre = ?, email = ? WHERE id = ?", (nombre, email, id))
            conn.commit()
            conn.close()
            raise web.seeother("/")
        except Exception as e:
            return render.editar(persona={"id": id, "nombre": nombre, "email": email}, error=str(e))


        


class Borrar:
    def GET(self, id):
        try:
            conn = sqlite3.connect("agenda.db")
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM personas WHERE id = ?", (id,))
            persona = cursor.fetchone()
            conn.close()

            if persona:
                return render.borrar({"persona": dict(persona)})
            else:
                return render.borrar({"persona": None, "error": "Persona no encontrada"})
        except Exception as e:
            return render.borrar({"persona": None, "error": str(e)})

    def POST(self, id):
        try:
            conn = sqlite3.connect("agenda.db")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM personas WHERE id = ?", (id,))
            conn.commit()
            conn.close()
            raise web.seeother("/")
        except Exception as e:
            return f"Error al borrar: {str(e)}"






if __name__ == "__main__":
    app = web.application(urls, globals())
    app.run()
