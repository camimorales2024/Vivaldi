import os
import tkinter as tk
from tkinter import messagebox

import mysql.connector
from PIL import Image, ImageTk


# =========================================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# =========================================================
# Puedes cambiar estos valores con variables de entorno
# (VIVALDI_DB_HOST, VIVALDI_DB_USER, VIVALDI_DB_PASSWORD,
# VIVALDI_DB_NAME) para no dejar la contraseña en el código.

HOST = os.getenv("VIVALDI_DB_HOST", "localhost")
USER = os.getenv("VIVALDI_DB_USER", "root")
PASSWORD = os.getenv("VIVALDI_DB_PASSWORD", "sqldecami")
DATABASE = os.getenv("VIVALDI_DB_NAME", "restaurante_vivaldi")


# =========================================================
# LOGOS
# =========================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOGO_PNG = os.path.join(BASE_DIR, "vivaldi.png")
LOGO_ICO = os.path.join(BASE_DIR, "vivaldi.ico")


# =========================================================
# PALETA DE COLORES - RESTAURANTE VIVALDI
# =========================================================

CREMA = "#fbf8f1"
CREMA_CLARO = "#fbf7f1"

BEIGE = "#d9bc8c"

VERDE = "#223d2d"
VERDE_OSCURO = "#12261c"

# Vino únicamente como pequeño detalle
VINO = "#6b2333"


# =========================================================
# CONEXIÓN A MYSQL
# =========================================================

def conectar():
    try:
        return mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE
        )

    except mysql.connector.Error as error:
        messagebox.showerror(
            "Error de conexión",
            f"No se pudo conectar con MySQL.\n\n{error}"
        )

        return None


# =========================================================
# ABRIR VISTA DE RECEPCIÓN
# =========================================================

def abrir_recepcion(usuario, rol):
    ventana.destroy()

    try:
        from interfaz_recepcionista import interfaz_recepcionista

        interfaz_recepcionista()

    except ImportError:
        messagebox.showerror(
            "Error",
            "No se encontró el archivo de la vista de recepción."
        )

    except Exception as error:
        messagebox.showerror(
            "Error",
            f"No se pudo abrir la vista de recepción.\n\n{error}"
        )


# =========================================================
# ABRIR VISTA DE ADMINISTRADOR
# =========================================================

def abrir_administrador(usuario, rol):
    ventana.destroy()

    try:
        from interfaz_administrador import interfaz_administrador

        interfaz_administrador()

    except ImportError:
        messagebox.showerror(
            "Error",
            "No se encontró el archivo de la vista del administrador."
        )

    except Exception as error:
        messagebox.showerror(
            "Error",
            f"No se pudo abrir la vista del administrador.\n\n{error}"
        )


# =========================================================
# ABRIR VISTA DE MESERO
# =========================================================

def abrir_mesero(usuario, rol):
    ventana.destroy()

    try:
        from interfaz_mesero import interfaz_mesero

        interfaz_mesero(usuario, rol)

    except ImportError:
        messagebox.showerror(
            "Error",
            "No se encontró el archivo de la vista de mesero."
        )

    except Exception as error:
        messagebox.showerror(
            "Error",
            f"No se pudo abrir la vista de mesero.\n\n{error}"
        )


# =========================================================
# INICIO DE SESIÓN
# =========================================================

def iniciar_sesion():
    usuario = entrada_usuario.get().strip()
    contraseña = entrada_contraseña.get()

    if usuario == "" or contraseña == "":
        messagebox.showwarning(
            "Campos incompletos",
            "Ingresa el usuario y la contraseña."
        )

        return

    conexion = conectar()

    if conexion is None:
        return

    cursor = None

    try:
        cursor = conexion.cursor(dictionary=True)

        sql = """
            SELECT usuario, contrasena_hash, rol, activo
            FROM Empleado
            WHERE usuario = %s
        """

        cursor.execute(sql, (usuario,))

        resultado = cursor.fetchone()

        if resultado is None:
            messagebox.showerror(
                "Acceso denegado",
                "El usuario no existe."
            )

            return

        if contraseña != str(resultado["contrasena_hash"]):
            messagebox.showerror(
                "Acceso denegado",
                "La contraseña es incorrecta."
            )

            return

        if not resultado["activo"]:
            messagebox.showerror(
                "Acceso denegado",
                "Este usuario está desactivado."
            )

            return

        rol = resultado["rol"]

        messagebox.showinfo(
            "Bienvenido",
            f"Inicio de sesión exitoso.\n\n"
            f"Usuario: {usuario}\n"
            f"Rol: {rol}"
        )

        if rol == "Admin":
            abrir_administrador(usuario, rol)

        elif rol == "Mesero":
            abrir_mesero(usuario, rol)

        elif rol == "Recepcionista":
            abrir_recepcion(usuario, rol)

        else:
            messagebox.showerror(
                "Error",
                "El rol del usuario no tiene una vista asignada."
            )

    except mysql.connector.Error as error:
        messagebox.showerror(
            "Error",
            f"No se pudo realizar el inicio de sesión.\n\n{error}"
        )

    finally:
        if cursor is not None:
            cursor.close()

        conexion.close()


# =========================================================
# VENTANA DE INICIO DE SESIÓN
# =========================================================

ventana = tk.Tk()

ventana.title("Restaurante Vivaldi | Inicio de sesión")

ventana.geometry("900x650")

ventana.configure(bg=CREMA)

ventana.resizable(False, False)


# =========================================================
# ICONO DE LA VENTANA
# =========================================================

try:
    ventana.iconbitmap(LOGO_ICO)

except Exception:
    pass


# =========================================================
# MARCO PRINCIPAL
# =========================================================

principal = tk.Frame(
    ventana,
    bg=CREMA
)

principal.pack(
    fill="both",
    expand=True
)


# =========================================================
# TARJETA DE LOGIN
# =========================================================

tarjeta_login = tk.Frame(
    principal,
    bg=CREMA_CLARO,
    width=500,
    height=520,
    highlightbackground=BEIGE,
    highlightthickness=1
)

tarjeta_login.place(
    relx=0.5,
    rely=0.5,
    anchor="center"
)

tarjeta_login.pack_propagate(False)


# =========================================================
# LOGO PNG TRANSPARENTE
# =========================================================

logo_tk = None

try:
    imagen = Image.open(LOGO_PNG)

    imagen.thumbnail((115, 115))

    logo_tk = ImageTk.PhotoImage(imagen)

    tk.Label(
        tarjeta_login,
        image=logo_tk,
        bg=CREMA_CLARO,
        borderwidth=0
    ).pack(
        pady=(22, 5)
    )

except Exception:
    tk.Label(
        tarjeta_login,
        text="RESTAURANTE VIVALDI",
        font=("Georgia", 18, "bold"),
        bg=CREMA_CLARO,
        fg=VERDE
    ).pack(
        pady=(35, 15)
    )


# =========================================================
# TÍTULO
# =========================================================

tk.Label(
    tarjeta_login,
    text="RESTAURANTE VIVALDI",
    font=("Georgia", 24, "bold"),
    bg=CREMA_CLARO,
    fg=VERDE_OSCURO
).pack(
    pady=(5, 3)
)


tk.Label(
    tarjeta_login,
    text="INICIO DE SESIÓN",
    font=("Segoe UI", 10, "bold"),
    bg=CREMA_CLARO,
    fg=VERDE
).pack(
    pady=(0, 22)
)


# =========================================================
# CAMPO USUARIO
# =========================================================

marco_usuario = tk.Frame(
    tarjeta_login,
    bg=CREMA,
    highlightbackground=BEIGE,
    highlightthickness=1
)

marco_usuario.pack(
    padx=55,
    fill="x",
    ipady=3
)


tk.Label(
    marco_usuario,
    text="USUARIO",
    font=("Segoe UI", 9, "bold"),
    bg=CREMA,
    fg=VERDE,
    width=10
).pack(
    side="left",
    padx=(8, 0)
)


entrada_usuario = tk.Entry(
    marco_usuario,
    font=("Segoe UI", 11),
    bg=CREMA,
    fg=VERDE_OSCURO,
    relief="flat",
    bd=0,
    insertbackground=VERDE
)

entrada_usuario.pack(
    side="left",
    fill="x",
    expand=True,
    padx=8,
    ipady=8
)


# =========================================================
# CAMPO CONTRASEÑA
# =========================================================

marco_contraseña = tk.Frame(
    tarjeta_login,
    bg=CREMA,
    highlightbackground=BEIGE,
    highlightthickness=1
)

marco_contraseña.pack(
    padx=55,
    pady=(14, 26),
    fill="x",
    ipady=3
)


tk.Label(
    marco_contraseña,
    text="CONTRASEÑA",
    font=("Segoe UI", 9, "bold"),
    bg=CREMA,
    fg=VERDE,
    width=10
).pack(
    side="left",
    padx=(8, 0)
)


entrada_contraseña = tk.Entry(
    marco_contraseña,
    font=("Segoe UI", 11),
    bg=CREMA,
    fg=VERDE_OSCURO,
    relief="flat",
    bd=0,
    show="•",
    insertbackground=VERDE
)

entrada_contraseña.pack(
    side="left",
    fill="x",
    expand=True,
    padx=8,
    ipady=8
)


# =========================================================
# BOTÓN INGRESAR
# =========================================================

boton_ingresar = tk.Button(
    tarjeta_login,
    text="INGRESAR",
    command=iniciar_sesion,
    font=("Segoe UI", 11, "bold"),
    bg=VERDE,
    fg=CREMA_CLARO,
    activebackground=VERDE_OSCURO,
    activeforeground=CREMA_CLARO,
    relief="flat",
    bd=0,
    cursor="hand2"
)

boton_ingresar.pack(
    padx=55,
    fill="x",
    ipady=11
)


# =========================================================
# TEXTO INFERIOR
# =========================================================

tk.Label(
    tarjeta_login,
    text="Sistema de gestión del restaurante",
    font=("Segoe UI", 9),
    bg=CREMA_CLARO,
    fg=VERDE
).pack(
    pady=(15, 0)
)


tk.Label(
    tarjeta_login,
    text="Restaurante Vivaldi",
    font=("Segoe UI", 9, "bold"),
    bg=CREMA_CLARO,
    fg=BEIGE
).pack(
    pady=(2, 0)
)


# =========================================================
# PEQUEÑO DETALLE VINO
# =========================================================

tk.Frame(
    tarjeta_login,
    bg=VINO,
    height=2,
    width=45
).pack(
    pady=(8, 0)
)


# =========================================================
# ENTER PARA INICIAR SESIÓN
# =========================================================

ventana.bind(
    "<Return>",
    lambda evento: iniciar_sesion()
)


entrada_usuario.focus()


# =========================================================
# EJECUTAR
# =========================================================

ventana.mainloop()