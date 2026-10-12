import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from datetime import date
import mysql.connector


# ==========================================================
# PALETA
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
# CONEXIÓN
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
            f"No fue posible conectar con MySQL.\n\n{error}"
        )

        return None


# ==========================================================
# GUARDAR
# ==========================================================

def guardar_cliente():

    nombre = nombre_entry.get().strip()
    apellido = apellido_entry.get().strip()
    telefono = telefono_entry.get().strip()
    correo = correo_entry.get().strip()

    if nombre == "":
        messagebox.showwarning(
            "Campo requerido",
            "Escribe tu nombre."
        )
        nombre_entry.focus()
        return

    if apellido == "":
        messagebox.showwarning(
            "Campo requerido",
            "Escribe tu apellido."
        )
        apellido_entry.focus()
        return

    if telefono == "":
        messagebox.showwarning(
            "Campo requerido",
            "Escribe tu teléfono."
        )
        telefono_entry.focus()
        return

    if correo == "":
        messagebox.showwarning(
            "Campo requerido",
            "Escribe tu correo electrónico."
        )
        correo_entry.focus()
        return

    conexion = conectar()

    if conexion is None:
        return

    try:

        cursor = conexion.cursor()

        consulta = """
        INSERT INTO Cliente
        (nombre, apellido, telefono, correo_electronico, fecha_registro)
        VALUES (%s, %s, %s, %s, %s)
        """

        datos = (
            nombre,
            apellido,
            telefono,
            correo,
            date.today()
        )

        cursor.execute(consulta, datos)

        conexion.commit()

        messagebox.showinfo(
            "¡Bienvenido!",
            f"Hola {nombre} 👋\n\n"
            "Tu registro en El Taco Dorado "
            "se realizó correctamente."
        )

        limpiar_campos()

    except mysql.connector.Error as error:

        messagebox.showerror(
            "Error al registrar",
            f"Ocurrió un problema al guardar tus datos.\n\n{error}"
        )

    finally:

        if conexion.is_connected():
            cursor.close()
            conexion.close()


# ==========================================================
# LIMPIAR
# ==========================================================

def limpiar_campos():

    nombre_entry.delete(0, tk.END)
    apellido_entry.delete(0, tk.END)
    telefono_entry.delete(0, tk.END)
    correo_entry.delete(0, tk.END)

    nombre_entry.focus()


# ==========================================================
# VENTANA
# ==========================================================

ventana = tk.Tk()

ventana.title("El Taco Dorado | Registro")
ventana.geometry("1150x720")
ventana.resizable(False, False)
ventana.configure(bg=AZUL_2)


# ==========================================================
# BARRA SUPERIOR
# ==========================================================

barra = tk.Frame(
    ventana,
    bg=AZUL,
    height=85
)

barra.pack(
    fill="x"
)

barra.pack_propagate(False)


tk.Label(
    barra,
    text="EL TACO",
    font=("Arial", 24, "bold"),
    bg=AZUL,
    fg=BLANCO
).pack(
    side="left",
    padx=(55, 0),
    pady=22
)


tk.Label(
    barra,
    text="DORADO",
    font=("Arial", 24, "bold"),
    bg=AZUL,
    fg=DORADO
).pack(
    side="left",
    padx=7
)


tk.Label(
    barra,
    text="REGISTRO DE CLIENTE",
    font=("Arial", 10, "bold"),
    bg=AZUL,
    fg=GRIS_3
).pack(
    side="right",
    padx=55
)


# ==========================================================
# DECORACIÓN SUPERIOR
# ==========================================================

decoracion = tk.Frame(
    ventana,
    bg=DORADO,
    height=8
)

decoracion.pack(fill="x")


# ==========================================================
# ÁREA PRINCIPAL
# ==========================================================

contenido = tk.Frame(
    ventana,
    bg=AZUL_2
)

contenido.pack(
    fill="both",
    expand=True
)


# ==========================================================
# PANEL IZQUIERDO DECORATIVO
# ==========================================================

decorativo = tk.Frame(
    contenido,
    bg=AZUL_2,
    width=350
)

decorativo.pack(
    side="left",
    fill="y"
)

decorativo.pack_propagate(False)


tk.Label(
    decorativo,
    text="🌮",
    font=("Arial", 75),
    bg=AZUL_2,
    fg=DORADO
).pack(
    pady=(85, 5)
)


tk.Label(
    decorativo,
    text="¡BIENVENIDO!",
    font=("Arial", 25, "bold"),
    bg=AZUL_2,
    fg=BLANCO
).pack()


tk.Label(
    decorativo,
    text="a la familia",
    font=("Arial", 14),
    bg=AZUL_2,
    fg=DORADO_3
).pack(
    pady=3
)


tk.Label(
    decorativo,
    text="EL TACO DORADO",
    font=("Arial", 19, "bold"),
    bg=AZUL_2,
    fg=VERDE
).pack(
    pady=(0, 25)
)


# Línea decorativa

linea = tk.Frame(
    decorativo,
    bg=ROJO,
    width=130,
    height=6
)

linea.pack()


tk.Label(
    decorativo,
    text="Regístrate para disfrutar\n"
         "de una experiencia llena\n"
         "de sabor.",
    font=("Arial", 12),
    bg=AZUL_2,
    fg=GRIS_3,
    justify="center"
).pack(
    pady=30
)


# ==========================================================
# TARJETA
# ==========================================================

tarjeta_exterior = tk.Frame(
    contenido,
    bg=AZUL_2
)

tarjeta_exterior.pack(
    side="right",
    fill="both",
    expand=True,
    padx=(10, 70),
    pady=45
)


tarjeta = tk.Frame(
    tarjeta_exterior,
    bg=BLANCO
)

tarjeta.pack(
    fill="both",
    expand=True
)


# ==========================================================
# ENCABEZADO DE TARJETA
# ==========================================================

encabezado = tk.Frame(
    tarjeta,
    bg=BLANCO,
    height=95
)

encabezado.pack(
    fill="x"
)

encabezado.pack_propagate(False)


tk.Label(
    encabezado,
    text="Crear una cuenta",
    font=("Arial", 24, "bold"),
    bg=BLANCO,
    fg=AZUL
).pack(
    anchor="w",
    padx=40,
    pady=(20, 0)
)


tk.Label(
    encabezado,
    text="Completa tus datos para comenzar",
    font=("Arial", 10),
    bg=BLANCO,
    fg=AZUL_4
).pack(
    anchor="w",
    padx=42,
    pady=3
)


# ==========================================================
# FRANJA DE COLORES
# ==========================================================

franja = tk.Frame(
    tarjeta,
    height=7
)

franja.pack(fill="x")

tk.Frame(
    franja,
    bg=ROJO,
    width=100
).pack(
    side="left",
    fill="y",
    expand=True
)

tk.Frame(
    franja,
    bg=DORADO,
    width=100
).pack(
    side="left",
    fill="y",
    expand=True
)

tk.Frame(
    franja,
    bg=VERDE,
    width=100
).pack(
    side="left",
    fill="y",
    expand=True
)


# ==========================================================
# FORMULARIO
# ==========================================================

formulario = tk.Frame(
    tarjeta,
    bg=BLANCO
)

formulario.pack(
    padx=40,
    pady=25,
    fill="both",
    expand=True
)


# ----------------------------------------------------------
# Función para campos
# ----------------------------------------------------------

def campo_formulario(parent, texto, fila, columna):

    tk.Label(
        parent,
        text=texto,
        font=("Arial", 10, "bold"),
        bg=BLANCO,
        fg=AZUL
    ).grid(
        row=fila,
        column=columna,
        sticky="w",
        padx=7,
        pady=(5, 5)
    )

    entrada = tk.Entry(
        parent,
        font=("Arial", 11),
        bg=GRIS_1,
        fg=AZUL,
        relief="flat",
        highlightthickness=2,
        highlightbackground=GRIS_3,
        highlightcolor=DORADO
    )

    entrada.grid(
        row=fila + 1,
        column=columna,
        sticky="ew",
        padx=7,
        ipady=9
    )

    return entrada


formulario.columnconfigure(0, weight=1)
formulario.columnconfigure(1, weight=1)


# Primera fila

nombre_entry = campo_formulario(
    formulario,
    "NOMBRE",
    0,
    0
)

apellido_entry = campo_formulario(
    formulario,
    "APELLIDO",
    0,
    1
)


# Segunda fila

telefono_entry = campo_formulario(
    formulario,
    "TELÉFONO",
    2,
    0
)

correo_entry = campo_formulario(
    formulario,
    "CORREO ELECTRÓNICO",
    2,
    1
)


# ==========================================================
# MENSAJE
# ==========================================================

tk.Label(
    formulario,
    text="Tus datos serán utilizados para gestionar tu experiencia como cliente.",
    font=("Arial", 9),
    bg=BLANCO,
    fg=AZUL_4
).grid(
    row=4,
    column=0,
    columnspan=2,
    pady=(25, 15)
)


# ==========================================================
# BOTONES
# ==========================================================

botones = tk.Frame(
    formulario,
    bg=BLANCO
)

botones.grid(
    row=5,
    column=0,
    columnspan=2,
    pady=10
)


btn_registrar = tk.Button(
    botones,
    text="REGISTRARME",
    font=("Arial", 11, "bold"),
    bg=VERDE_3,
    fg=BLANCO,
    activebackground=VERDE_4,
    activeforeground=BLANCO,
    relief="flat",
    cursor="hand2",
    padx=35,
    pady=12,
    command=guardar_cliente
)

btn_registrar.pack(
    side="left",
    padx=6
)


btn_limpiar = tk.Button(
    botones,
    text="LIMPIAR",
    font=("Arial", 11, "bold"),
    bg=ROJO,
    fg=BLANCO,
    activebackground=ROJO_4,
    activeforeground=BLANCO,
    relief="flat",
    cursor="hand2",
    padx=35,
    pady=12,
    command=limpiar_campos
)

btn_limpiar.pack(
    side="left",
    padx=6
)


# ==========================================================
# PIE DE TARJETA
# ==========================================================

tk.Label(
    tarjeta,
    text="EL TACO DORADO  •  SABOR QUE TE HACE VOLVER",
    font=("Arial", 9, "bold"),
    bg=AZUL,
    fg=DORADO_3
).pack(
    fill="x",
    ipady=12
)


# ==========================================================
# INICIO
# ==========================================================

nombre_entry.focus()

ventana.mainloop()