import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import date
import mysql.connector


# ==========================================================
# PALETA DE COLORES
# ==========================================================

DORADO = "#BC9755"
DORADO_2 = "#C5A46D"
DORADO_3 = "#D0B384"
DORADO_4 = "#DCC39A"

VERDE = "#7FB328"
VERDE_2 = "#6FA121"
VERDE_3 = "#5D8C1A"
VERDE_4 = "#4C7712"

ROJO = "#8B1E22"
ROJO_2 = "#7D1B1E"
ROJO_3 = "#6E181A"
ROJO_4 = "#5F1517"

AZUL = "#1A2530"
AZUL_2 = "#202D3A"
AZUL_3 = "#273545"
AZUL_4 = "#2E3D50"

BLANCO = "#FFFFFF"
GRIS_1 = "#F5F5F5"
GRIS_2 = "#EDEDED"
GRIS_3 = "#E5E5E5"


# ==========================================================
# CONEXIÓN A MYSQL
# ==========================================================

def conectar():
    try:
        return mysql.connector.connect(
            host="localhost",
            user="root",
            password="sqldecami",
            database="restaurante_taco"
        )
    except mysql.connector.Error as error:
        messagebox.showerror(
            "Error de conexión",
            f"No se pudo conectar con la base de datos.\n\n{error}"
        )
        return None


# ==========================================================
# LIMPIAR CAMPOS
# ==========================================================

def limpiar():
    entrada_nombre.delete(0, tk.END)
    entrada_apellido.delete(0, tk.END)
    entrada_telefono.delete(0, tk.END)
    entrada_correo.delete(0, tk.END)

    entrada_nombre.focus()


# ==========================================================
# GUARDAR CLIENTE
# ==========================================================

def guardar():

    nombre = entrada_nombre.get().strip()
    apellido = entrada_apellido.get().strip()
    telefono = entrada_telefono.get().strip()
    correo = entrada_correo.get().strip()

    if not nombre or not apellido or not telefono or not correo:
        messagebox.showwarning(
            "Campos incompletos",
            "Por favor completa todos los campos."
        )
        return

    conexion = conectar()

    if conexion is None:
        return

    try:

        cursor = conexion.cursor()

        sql = """
        INSERT INTO Cliente
        (nombre, apellido, telefono, correo_electronico, fecha_registro)
        VALUES (%s, %s, %s, %s, %s)
        """

        valores = (
            nombre,
            apellido,
            telefono,
            correo,
            date.today()
        )

        cursor.execute(sql, valores)

        conexion.commit()

        messagebox.showinfo(
            "¡Registro exitoso!",
            f"¡Bienvenido/a {nombre}!\n\n"
            "Tu cuenta ha sido registrada correctamente "
            "en El Taco Dorado."
        )

        limpiar()

    except mysql.connector.Error as error:

        messagebox.showerror(
            "Error",
            f"No se pudo registrar el cliente.\n\n{error}"
        )

    finally:

        if conexion.is_connected():
            cursor.close()
            conexion.close()


# ==========================================================
# VENTANA PRINCIPAL
# ==========================================================

ventana = tk.Tk()

ventana.title("El Taco Dorado - Registro de Cliente")
ventana.geometry("1100x700")
ventana.resizable(False, False)
ventana.configure(bg=AZUL)


# ==========================================================
# PANEL IZQUIERDO
# ==========================================================

panel_izquierdo = tk.Frame(
    ventana,
    bg=AZUL,
    width=430,
    height=700
)

panel_izquierdo.pack(side="left", fill="y")
panel_izquierdo.pack_propagate(False)


# Franja dorada

tk.Frame(
    panel_izquierdo,
    bg=DORADO,
    height=10
).pack(fill="x")


# Logo

try:

    imagen = Image.open("logo_restaurante.jpg")
    imagen = imagen.resize((190, 190))

    logo = ImageTk.PhotoImage(imagen)

    tk.Label(
        panel_izquierdo,
        image=logo,
        bg=AZUL
    ).pack(pady=(75, 20))

except:

    tk.Label(
        panel_izquierdo,
        text="🌮",
        font=("Arial", 80),
        bg=AZUL,
        fg=DORADO
    ).pack(pady=(80, 20))


tk.Label(
    panel_izquierdo,
    text="EL TACO DORADO",
    font=("Arial", 27, "bold"),
    bg=AZUL,
    fg=DORADO
).pack()


tk.Label(
    panel_izquierdo,
    text="SABOR QUE TE HACE VOLVER",
    font=("Arial", 11, "bold"),
    bg=AZUL,
    fg=BLANCO
).pack(pady=(8, 30))


# Decoración verde

tk.Frame(
    panel_izquierdo,
    bg=VERDE,
    width=150,
    height=5
).pack()


tk.Label(
    panel_izquierdo,
    text="Crea tu cuenta y disfruta\n"
         "de nuestros deliciosos tacos.",
    font=("Arial", 13),
    bg=AZUL,
    fg=GRIS_3,
    justify="center"
).pack(pady=30)


# ==========================================================
# PANEL DERECHO
# ==========================================================

panel_derecho = tk.Frame(
    ventana,
    bg=GRIS_1
)

panel_derecho.pack(
    side="right",
    fill="both",
    expand=True
)


# Encabezado

encabezado = tk.Frame(
    panel_derecho,
    bg=BLANCO,
    height=105
)

encabezado.pack(fill="x")
encabezado.pack_propagate(False)


tk.Label(
    encabezado,
    text="CREAR CUENTA",
    font=("Arial", 25, "bold"),
    bg=BLANCO,
    fg=AZUL
).pack(anchor="w", padx=55, pady=(25, 0))


tk.Label(
    encabezado,
    text="Regístrate como cliente de El Taco Dorado",
    font=("Arial", 11),
    bg=BLANCO,
    fg=AZUL_4
).pack(anchor="w", padx=57, pady=5)


# Línea decorativa

tk.Frame(
    panel_derecho,
    bg=VERDE,
    height=6
).pack(fill="x")


# ==========================================================
# FORMULARIO
# ==========================================================

formulario = tk.Frame(
    panel_derecho,
    bg=GRIS_1
)

formulario.pack(
    padx=55,
    pady=35,
    fill="both",
    expand=True
)


def crear_campo(parent, texto, fila):

    tk.Label(
        parent,
        text=texto,
        font=("Arial", 11, "bold"),
        bg=GRIS_1,
        fg=AZUL
    ).grid(
        row=fila,
        column=0,
        sticky="w",
        pady=(8, 5)
    )

    campo = tk.Entry(
        parent,
        font=("Arial", 12),
        bg=BLANCO,
        fg=AZUL,
        relief="flat",
        highlightthickness=2,
        highlightbackground=GRIS_3,
        highlightcolor=DORADO,
        width=39
    )

    campo.grid(
        row=fila + 1,
        column=0,
        sticky="ew",
        ipady=9
    )

    return campo


entrada_nombre = crear_campo(
    formulario,
    "Nombre",
    0
)

entrada_apellido = crear_campo(
    formulario,
    "Apellido",
    2
)

entrada_telefono = crear_campo(
    formulario,
    "Teléfono",
    4
)

entrada_correo = crear_campo(
    formulario,
    "Correo electrónico",
    6
)


# ==========================================================
# BOTONES
# ==========================================================

zona_botones = tk.Frame(
    formulario,
    bg=GRIS_1
)

zona_botones.grid(
    row=8,
    column=0,
    sticky="ew",
    pady=(35, 0)
)


boton_guardar = tk.Button(
    zona_botones,
    text="CREAR CUENTA",
    font=("Arial", 12, "bold"),
    bg=ROJO,
    fg=BLANCO,
    activebackground=ROJO_3,
    activeforeground=BLANCO,
    relief="flat",
    cursor="hand2",
    padx=30,
    pady=12,
    command=guardar
)

boton_guardar.pack(
    side="left",
    padx=(0, 12)
)


boton_limpiar = tk.Button(
    zona_botones,
    text="LIMPIAR",
    font=("Arial", 12, "bold"),
    bg=DORADO,
    fg=BLANCO,
    activebackground=DORADO_3,
    activeforeground=AZUL,
    relief="flat",
    cursor="hand2",
    padx=28,
    pady=12,
    command=limpiar
)

boton_limpiar.pack(
    side="left"
)


# Pie

tk.Label(
    formulario,
    text="Al registrarte podrás disfrutar de la experiencia de El Taco Dorado.",
    font=("Arial", 9),
    bg=GRIS_1,
    fg=AZUL_4
).grid(
    row=9,
    column=0,
    pady=25
)


entrada_nombre.focus()

ventana.mainloop()