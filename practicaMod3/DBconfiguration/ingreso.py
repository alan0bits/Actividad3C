import os
import psycopg2
import getpass

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "credenciales")
DB_USER = os.getenv("DB_USER", "Admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "p4ssw0rdDB")


def conectar_db():
    try:
        return psycopg2.connect(
            host=DB_HOST, port=DB_PORT,
            database=DB_NAME, user=DB_USER, password=DB_PASSWORD
        )
    except Exception as e:
        print("Error de conexión", e)
        return None
    
def insertar_datos_usuario(name, mail, phone, date, job, username,password):
    conn = conectar_db()
    if not conn:
        return
    try:
        with conn.cursor() as cursor:
              cursor = conn.cursor()

              insert_user = """
                INSERT INTO usuarios (nombre, correo, telefono, fecha_nacimiento, id_profesion) VALUES
                (%s,%s,%s,%s,%s)
                """

              cursor.execute(insert_user, (name, mail, phone, date, job))
              user_id = cursor.fetchone()[0]

              insert_credentials = """
                INSERT INTO credenciales (id_usuario, username, password_hash)
                VALUES (%s, %s, %s);
                """
              cursor.execute(insert_credentials, (user_id, username, password))

    except Exception as e:
        print(f"[ERROR] {e}")
        conn.rollback()
    finally:
        conn.close()

              


if __name__ == "__main__":
    print("Inicio de sesión en la base de datos")
    name = input("Ingresa su nombre: ")
    mail = input("Ingrese su correo: ")
    phone = input("Ingrese telefono 10 digitos: ")
    date = input("Ingrese fecha de nacimiento con formato yyyy-mm-dd: ")
    job = input("Seleccione profesion 1-ingeniero,2-desarrollo,3-meteorologo,4-administracion,5-RH, 6-licenciado:  ")
    username = input("Ingrese nombre de usuario con 1 numero al final sin espacios: ")
    password = input("Ingrese password deseado empesando con hash sin espacios: ")
    insertar_datos_usuario(name,mail,phone,date,job,username,password)