import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
from PIL import Image, ImageTk
from datetime import date, timedelta, datetime
import mysql.connector
import re


HOST = "localhost"
USER = "root"
PASSWORD = "sqldecami"
DATABASE = "restaurante_vivaldi"


CREMA = "#fbf8f1"
CREMA_CLARO = "#fbf7f1"
BEIGE = "#d9bc8c"
VERDE = "#223d2d"
VERDE_OSCURO = "#12261c"
VINO = "#6b2333"
BLANCO = "#ffffff"
GRIS = "#6f6f6f"
GRIS_CLARO = "#e8e3da"


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
            f"No se pudo conectar con la base de datos.\n\n{error}"
        )
        return None


def solo_letras(texto):
    return all(
        caracter.isalpha() or caracter.isspace()
        for caracter in texto
    )


def interfaz_recepcionista(usuario=None, rol=None):

    ventana = tk.Tk()
    ventana.title("Restaurante Vivaldi - Recepcionista")
    ventana.geometry("1100x720")
    ventana.resizable(False, False)
    ventana.configure(bg=CREMA)

    try:
        ventana.iconbitmap("vivaldi.ico")
    except:
        pass

    id_empleado = None
    id_cliente_actual = [None]

    # =========================================================
    # OBTENER ID DEL EMPLEADO
    # =========================================================

    if usuario:
        conexion = conectar()

        if conexion:
            cursor = None

            try:
                cursor = conexion.cursor()

                cursor.execute(
                    """
                    SELECT id_empleado
                    FROM Empleado
                    WHERE usuario = %s
                    """,
                    (usuario,)
                )

                resultado = cursor.fetchone()

                if resultado:
                    id_empleado = resultado[0]

            except mysql.connector.Error as error:
                messagebox.showerror(
                    "Error",
                    f"No se pudo obtener el empleado.\n\n{error}"
                )

            finally:
                if cursor:
                    cursor.close()

                conexion.close()

    # =========================================================
    # ESTILOS
    # =========================================================

    estilo = ttk.Style()

    try:
        estilo.theme_use("clam")
    except:
        pass

    estilo.configure(
        "Treeview",
        background=BLANCO,
        foreground=VERDE_OSCURO,
        rowheight=30,
        fieldbackground=BLANCO,
        font=("Arial", 9)
    )

    estilo.configure(
        "Treeview.Heading",
        background=VERDE,
        foreground=BLANCO,
        font=("Arial", 9, "bold"),
        relief="flat"
    )

    estilo.map(
        "Treeview",
        background=[("selected", BEIGE)],
        foreground=[("selected", VERDE_OSCURO)]
    )

    estilo.configure(
        "TCombobox",
        fieldbackground=BLANCO,
        background=BLANCO,
        foreground=VERDE_OSCURO,
        arrowcolor=VERDE
    )

    # =========================================================
    # CONTENEDOR PRINCIPAL
    # =========================================================

    contenedor = tk.Frame(
        ventana,
        bg=CREMA
    )

    contenedor.pack(
        fill="both",
        expand=True
    )

    # =========================================================
    # SIDEBAR
    # =========================================================

    sidebar = tk.Frame(
        contenedor,
        bg=VERDE_OSCURO,
        width=210
    )

    sidebar.pack(
        side="left",
        fill="y"
    )

    sidebar.pack_propagate(False)

    contenido_sidebar = tk.Frame(
        sidebar,
        bg=VERDE_OSCURO
    )

    contenido_sidebar.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    try:
        imagen_logo = Image.open("vivaldi_sf.png")
        imagen_logo = imagen_logo.resize((150, 150))

        logo = ImageTk.PhotoImage(
            imagen_logo
        )

        etiqueta_logo = tk.Label(
            contenido_sidebar,
            image=logo,
            bg=VERDE_OSCURO
        )

        etiqueta_logo.image = logo

        etiqueta_logo.pack(
            pady=(0, 15)
        )

    except:
        tk.Label(
            contenido_sidebar,
            text="VIVALDI",
            bg=VERDE_OSCURO,
            fg=BEIGE,
            font=("Georgia", 24, "bold")
        ).pack(
            pady=(0, 35)
        )

    tk.Label(
        contenido_sidebar,
        text="RECEPCIÓN",
        bg=VERDE_OSCURO,
        fg=BEIGE,
        font=("Georgia", 14, "bold")
    ).pack(
        pady=(0, 20)
    )

    menu_navegacion = tk.Frame(
        contenido_sidebar,
        bg=VERDE_OSCURO
    )

    menu_navegacion.pack(
        fill="x",
        padx=20
    )

    # =========================================================
    # CONTENIDO
    # =========================================================

    contenido = tk.Frame(
        contenedor,
        bg=CREMA
    )

    contenido.pack(
        side="left",
        fill="both",
        expand=True
    )

    area_central = tk.Frame(
        contenido,
        bg=CREMA
    )

    area_central.place(
        relx=0.5,
        rely=0.5,
        anchor="center",
        relwidth=0.92,
        relheight=0.94
    )

    panel_clientes = tk.Frame(
        area_central,
        bg=CREMA
    )

    panel_reservaciones = tk.Frame(
        area_central,
        bg=CREMA
    )

    panel_mesas = tk.Frame(
        area_central,
        bg=CREMA
    )

    def mostrar_panel(panel):

        for otro_panel in (
            panel_clientes,
            panel_reservaciones,
            panel_mesas
        ):
            otro_panel.pack_forget()

        panel.pack(
            fill="both",
            expand=True
        )

    def actualizar_menu(boton_activo):

        botones = [
            boton_clientes,
            boton_reservaciones,
            boton_mesas
        ]

        for boton in botones:

            boton.config(
                text=f"   {boton.texto_menu}",
                bg=VERDE_OSCURO,
                fg=CREMA_CLARO,
                font=("Arial", 10, "bold")
            )

        boton_activo.config(
            text=f"●  {boton_activo.texto_menu}",
            bg=VERDE,
            fg=BEIGE
        )

    def crear_boton_menu(texto, comando):

        boton = tk.Button(
            menu_navegacion,
            text=f"   {texto}",
            bg=VERDE_OSCURO,
            fg=CREMA_CLARO,
            activebackground=VERDE,
            activeforeground=BEIGE,
            bd=0,
            relief="flat",
            anchor="w",
            padx=10,
            pady=13,
            font=("Arial", 10, "bold"),
            cursor="hand2",
            command=comando
        )

        boton.texto_menu = texto

        boton.pack(
            fill="x",
            pady=4
        )

        return boton

    # =========================================================
    # CLIENTES
    # =========================================================

    tk.Label(
        panel_clientes,
        text="Clientes",
        bg=CREMA,
        fg=VERDE,
        font=("Georgia", 25, "bold")
    ).pack(
        anchor="w",
        pady=(5, 0)
    )

    tk.Label(
        panel_clientes,
        text="Registra y consulta la información de los clientes del restaurante.",
        bg=CREMA,
        fg=GRIS,
        font=("Arial", 10)
    ).pack(
        anchor="w",
        pady=(3, 8)
    )

    tk.Frame(
        panel_clientes,
        bg=BEIGE,
        height=2
    ).pack(
        fill="x",
        pady=(0, 12)
    )

    tarjeta_clientes = tk.Frame(
        panel_clientes,
        bg=BLANCO,
        bd=1,
        relief="solid"
    )

    tarjeta_clientes.pack(
        fill="both",
        expand=True
    )

    encabezado_clientes = tk.Frame(
        tarjeta_clientes,
        bg=VERDE
    )

    encabezado_clientes.pack(
        fill="x"
    )

    tk.Label(
        encabezado_clientes,
        text="REGISTRO DE CLIENTES",
        bg=VERDE,
        fg=BLANCO,
        font=("Arial", 11, "bold")
    ).pack(
        anchor="w",
        padx=15,
        pady=10
    )

    formulario_clientes = tk.Frame(
        tarjeta_clientes,
        bg=BLANCO
    )

    formulario_clientes.pack(
        fill="x",
        padx=18,
        pady=15
    )

    for columna in range(4):
        formulario_clientes.columnconfigure(
            columna,
            weight=1
        )

    validar_nombre = ventana.register(
        lambda texto: solo_letras(texto) or texto == ""
    )

    entrada_nombre = tk.Entry(
        formulario_clientes,
        font=("Arial", 9),
        bd=1,
        relief="solid",
        validate="key",
        validatecommand=(
            validar_nombre,
            "%P"
        )
    )

    entrada_apellido = tk.Entry(
        formulario_clientes,
        font=("Arial", 9),
        bd=1,
        relief="solid",
        validate="key",
        validatecommand=(
            validar_nombre,
            "%P"
        )
    )

    def validar_entrada_telefono(texto):
        return texto == "" or (
            texto.isdigit()
            and len(texto) <= 8
        )

    validar_telefono_entrada = ventana.register(
        validar_entrada_telefono
    )

    entrada_telefono = tk.Entry(
        formulario_clientes,
        font=("Arial", 10),
        bd=1,
        relief="solid",
        validate="key",
        validatecommand=(
            validar_telefono_entrada,
            "%P"
        )
    )

    entrada_correo = tk.Entry(
        formulario_clientes,
        font=("Arial", 10),
        bd=1,
        relief="solid"
    )

    campos_clientes = [
        ("Nombre", entrada_nombre),
        ("Apellido", entrada_apellido),
        ("Teléfono", entrada_telefono),
        ("Correo electrónico", entrada_correo)
    ]

    for columna, (texto, entrada) in enumerate(
        campos_clientes
    ):

        tk.Label(
            formulario_clientes,
            text=texto,
            bg=BLANCO,
            fg=VERDE_OSCURO,
            font=("Arial", 9, "bold")
        ).grid(
            row=0,
            column=columna,
            sticky="w",
            padx=5,
            pady=(0, 5)
        )

        entrada.grid(
            row=1,
            column=columna,
            sticky="ew",
            padx=5
        )

    def validar_telefono(telefono):
        return bool(
            re.fullmatch(
                r"[0-9]{8}",
                telefono
            )
        )

    def validar_correo(correo):
        return bool(
            re.fullmatch(
                r"[^@\s]+@[^@\s]+\.[^@\s]+",
                correo
            )
        )

    def mostrar_clientes(filtro=""):

        for item in tabla_clientes.get_children():
            tabla_clientes.delete(item)

        conexion = conectar()

        if not conexion:
            return

        cursor = None

        try:

            cursor = conexion.cursor()

            if filtro.strip():

                patron = f"%{filtro.strip()}%"

                cursor.execute(
                    """
                    SELECT id_cliente,
                           nombre,
                           apellido,
                           telefono,
                           correo_electronico,
                           fecha_registro
                    FROM Cliente
                    WHERE nombre LIKE %s
                       OR apellido LIKE %s
                       OR telefono LIKE %s
                       OR correo_electronico LIKE %s
                    ORDER BY id_cliente DESC
                    """,
                    (
                        patron,
                        patron,
                        patron,
                        patron
                    )
                )

            else:

                cursor.execute(
                    """
                    SELECT id_cliente,
                           nombre,
                           apellido,
                           telefono,
                           correo_electronico,
                           fecha_registro
                    FROM Cliente
                    ORDER BY id_cliente DESC
                    """
                )

            for cliente in cursor.fetchall():

                tabla_clientes.insert(
                    "",
                    "end",
                    values=cliente
                )

        except mysql.connector.Error as error:

            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los clientes.\n\n{error}"
            )

        finally:

            if cursor:
                cursor.close()

            conexion.close()

    def limpiar_cliente():

        id_cliente_actual[0] = None

        for entrada in (
            entrada_nombre,
            entrada_apellido,
            entrada_telefono,
            entrada_correo
        ):

            entrada.delete(
                0,
                tk.END
            )

        entrada_nombre.focus()

        for item in tabla_clientes.selection():

            tabla_clientes.selection_remove(
                item
            )

    def cargar_cliente_seleccionado(event=None):
        seleccion = tabla_clientes.selection()

        if not seleccion:
            messagebox.showwarning(
                "Cliente",
                "Selecciona un cliente para editar."
            )
            return

        valores = tabla_clientes.item(seleccion[0], "values")

        if not valores:
            return

        id_cliente_actual[0] = valores[0]

        entrada_nombre.delete(0, tk.END)
        entrada_nombre.insert(0, valores[1])

        entrada_apellido.delete(0, tk.END)
        entrada_apellido.insert(0, valores[2])

        entrada_telefono.delete(0, tk.END)
        entrada_telefono.insert(0, valores[3])

        entrada_correo.delete(0, tk.END)
        entrada_correo.insert(0, valores[4])

        entrada_nombre.focus()

    def guardar_cliente():

        nombre = entrada_nombre.get().strip()
        apellido = entrada_apellido.get().strip()
        telefono = entrada_telefono.get().strip()
        correo = entrada_correo.get().strip()

        if not all(
            (
                nombre,
                apellido,
                telefono,
                correo
            )
        ):

            messagebox.showwarning(
                "Datos incompletos",
                "Completa todos los campos del cliente."
            )

            return

        if not solo_letras(nombre) or not solo_letras(apellido):

            messagebox.showwarning(
                "Nombre inválido",
                "El nombre y apellido solo pueden contener letras."
            )

            return

        if not validar_telefono(telefono):

            messagebox.showwarning(
                "Teléfono inválido",
                "El teléfono debe contener exactamente 8 números."
            )

            return

        if not validar_correo(correo):

            messagebox.showwarning(
                "Correo inválido",
                "Ingresa un correo electrónico válido."
            )

            return

        conexion = conectar()

        if not conexion:
            return

        cursor = None

        try:

            cursor = conexion.cursor()

            cursor.execute(
                """
                SELECT id_cliente
                FROM Cliente
                WHERE telefono = %s
                   OR correo_electronico = %s
                """,
                (
                    telefono,
                    correo
                )
            )

            if cursor.fetchone():

                messagebox.showwarning(
                    "Cliente existente",
                    "Ya existe un cliente registrado con ese teléfono o correo."
                )

                return

            cursor.execute(
                """
                INSERT INTO Cliente (
                    nombre,
                    apellido,
                    telefono,
                    correo_electronico,
                    fecha_registro
                )
                VALUES (%s, %s, %s, %s, %s)
                """,
                (
                    nombre,
                    apellido,
                    telefono,
                    correo,
                    date.today()
                )
            )

            conexion.commit()

            messagebox.showinfo(
                "Cliente registrado",
                "El cliente se registró correctamente."
            )

            limpiar_cliente()
            mostrar_clientes()
            cargar_clientes_reserva()

        except mysql.connector.Error as error:

            conexion.rollback()

            messagebox.showerror(
                "Error",
                f"No se pudo registrar el cliente.\n\n{error}"
            )

        finally:

            if cursor:
                cursor.close()

            conexion.close()

    def editar_cliente():

        if id_cliente_actual[0] is None:

            messagebox.showwarning(
                "Editar cliente",
                "Primero selecciona un cliente y pulsa EDITAR."
            )

            return

        nombre = entrada_nombre.get().strip()
        apellido = entrada_apellido.get().strip()
        telefono = entrada_telefono.get().strip()
        correo = entrada_correo.get().strip()

        if not all(
            (
                nombre,
                apellido,
                telefono,
                correo
            )
        ):

            messagebox.showwarning(
                "Datos incompletos",
                "Completa todos los campos del cliente."
            )

            return

        if not solo_letras(nombre) or not solo_letras(apellido):

            messagebox.showwarning(
                "Nombre inválido",
                "El nombre y apellido solo pueden contener letras."
            )

            return

        if not validar_telefono(telefono):

            messagebox.showwarning(
                "Teléfono inválido",
                "El teléfono debe contener exactamente 8 números."
            )

            return

        if not validar_correo(correo):

            messagebox.showwarning(
                "Correo inválido",
                "Ingresa un correo electrónico válido."
            )

            return

        conexion = conectar()

        if not conexion:
            return

        cursor = None

        try:

            cursor = conexion.cursor()

            cursor.execute(
                """
                SELECT id_cliente
                FROM Cliente
                WHERE (
                    telefono = %s
                    OR correo_electronico = %s
                )
                AND id_cliente <> %s
                """,
                (
                    telefono,
                    correo,
                    id_cliente_actual[0]
                )
            )

            if cursor.fetchone():

                messagebox.showwarning(
                    "Cliente existente",
                    "Otro cliente ya tiene ese teléfono o correo."
                )

                return

            cursor.execute(
                """
                UPDATE Cliente
                SET nombre = %s,
                    apellido = %s,
                    telefono = %s,
                    correo_electronico = %s
                WHERE id_cliente = %s
                """,
                (
                    nombre,
                    apellido,
                    telefono,
                    correo,
                    id_cliente_actual[0]
                )
            )

            conexion.commit()

            messagebox.showinfo(
                "Cliente actualizado",
                "Los datos del cliente se actualizaron correctamente."
            )

            limpiar_cliente()
            mostrar_clientes()
            cargar_clientes_reserva()

        except mysql.connector.Error as error:

            conexion.rollback()

            messagebox.showerror(
                "Error",
                f"No se pudo actualizar el cliente.\n\n{error}"
            )

        finally:

            if cursor:
                cursor.close()

            conexion.close()

    marco_botones_cliente = tk.Frame(
        formulario_clientes,
        bg=BLANCO
    )

    marco_botones_cliente.grid(
        row=2,
        column=0,
        columnspan=4,
        pady=(8, 0),
        sticky="w"
    )

    tk.Button(
        marco_botones_cliente,
        text="REGISTRAR",
        command=guardar_cliente,
        bg=VERDE,
        fg=BLANCO,
        activebackground=VERDE_OSCURO,
        activeforeground=BLANCO,
        bd=0,
        padx=28,
        pady=8,
        cursor="hand2",
        font=("Arial", 9, "bold")
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        marco_botones_cliente,
        text="EDITAR",
        command=cargar_cliente_seleccionado,
        bg=VINO,
        fg=BLANCO,
        activebackground=VERDE_OSCURO,
        activeforeground=BLANCO,
        bd=0,
        padx=24,
        pady=8,
        cursor="hand2",
        font=("Arial", 9, "bold")
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        marco_botones_cliente,
        text="GUARDAR CAMBIOS",
        command=editar_cliente,
        bg=BEIGE,
        fg=VERDE_OSCURO,
        activebackground=CREMA,
        bd=0,
        padx=18,
        pady=8,
        cursor="hand2",
        font=("Arial", 9, "bold")
    ).pack(
        side="left",
        padx=5
    )

    tk.Button(
        marco_botones_cliente,
        text="LIMPIAR",
        command=limpiar_cliente,
        bg=GRIS_CLARO,
        fg=VERDE_OSCURO,
        activebackground=CREMA,
        bd=0,
        padx=18,
        pady=8,
        cursor="hand2",
        font=("Arial", 9, "bold")
    ).pack(
        side="left",
        padx=5
    )

    # =========================================================
    # BUSCADOR DE CLIENTES
    # =========================================================

    marco_busqueda_clientes = tk.Frame(
        tarjeta_clientes,
        bg=BLANCO
    )

    marco_busqueda_clientes.pack(
        fill="x",
        padx=18,
        pady=(0, 10)
    )

    tk.Label(
        marco_busqueda_clientes,
        text="Buscar cliente:",
        bg=BLANCO,
        fg=VERDE_OSCURO,
        font=("Arial", 9, "bold")
    ).pack(
        side="left",
        padx=(0, 7)
    )

    entrada_busqueda_cliente = tk.Entry(
        marco_busqueda_clientes,
        font=("Arial", 10),
        bd=1,
        relief="solid",
        width=15
    )

    entrada_busqueda_cliente.pack(
        side="left"
    )

    tk.Button(
        marco_busqueda_clientes,
        text="BUSCAR",
        command=lambda: mostrar_clientes(
            entrada_busqueda_cliente.get()
        ),
        bg=VERDE,
        fg=BLANCO,
        activebackground=VERDE_OSCURO,
        activeforeground=BLANCO,
        bd=0,
        padx=15,
        pady=6,
        cursor="hand2",
        font=("Arial", 9, "bold")
    ).pack(
        side="left",
        padx=8
    )

    tk.Button(
        marco_busqueda_clientes,
        text="MOSTRAR TODOS",
        command=lambda: (
            entrada_busqueda_cliente.delete(
                0,
                tk.END
            ),
            mostrar_clientes()
        ),
        bg=BEIGE,
        fg=VERDE_OSCURO,
        activebackground=CREMA,
        bd=0,
        padx=15,
        pady=6,
        cursor="hand2",
        font=("Arial", 9, "bold")
    ).pack(
        side="left"
    )

    entrada_busqueda_cliente.bind(
        "<Return>",
        lambda event: mostrar_clientes(
            entrada_busqueda_cliente.get()
        )
    )

    zona_tabla_clientes = tk.Frame(
        tarjeta_clientes,
        bg=BLANCO
    )

    zona_tabla_clientes.pack(
        fill="both",
        expand=True,
        padx=18
    )

    tk.Label(
        zona_tabla_clientes,
        text="CLIENTES REGISTRADOS  •  DOBLE CLIC PARA EDITAR",
        bg=BLANCO,
        fg=VERDE,
        font=("Arial", 10, "bold")
    ).pack(
        anchor="w",
        pady=(0, 7)
    )

    tabla_clientes = ttk.Treeview(
        zona_tabla_clientes,
        columns=(
            "id",
            "nombre",
            "apellido",
            "telefono",
            "correo",
            "fecha"
        ),
        show="headings"
    )

    encabezados_clientes = {
        "id": "ID",
        "nombre": "Nombre",
        "apellido": "Apellido",
        "telefono": "Teléfono",
        "correo": "Correo",
        "fecha": "Fecha"
    }

    anchos_clientes = {
        "id": 45,
        "nombre": 115,
        "apellido": 115,
        "telefono": 105,
        "correo": 180,
        "fecha": 95
    }

    for columna in encabezados_clientes:

        tabla_clientes.heading(
            columna,
            text=encabezados_clientes[columna]
        )

        tabla_clientes.column(
            columna,
            width=anchos_clientes[columna],
            anchor="center"
        )

    tabla_clientes.pack(
        fill="both",
        expand=True
    )

    tabla_clientes.bind("<Double-1>", cargar_cliente_seleccionado)

    # =========================================================
    # RESERVACIONES
    # =========================================================

    tk.Label(
        panel_reservaciones,
        text="Reservaciones",
        bg=CREMA,
        fg=VERDE,
        font=("Georgia", 25, "bold")
    ).pack(
        anchor="w",
        pady=(5, 0)
    )

    tk.Label(
        panel_reservaciones,
        text="Registra, consulta y administra las reservaciones del restaurante.",
        bg=CREMA,
        fg=GRIS,
        font=("Arial", 10)
    ).pack(
        anchor="w",
        pady=(3, 8)
    )

    tk.Frame(
        panel_reservaciones,
        bg=BEIGE,
        height=2
    ).pack(
        fill="x",
        pady=(0, 10)
    )

    tarjeta_reserva = tk.Frame(
        panel_reservaciones,
        bg=BLANCO,
        bd=1,
        relief="solid"
    )

    tarjeta_reserva.pack(
        fill="both",
        expand=True
    )

    encabezado_reserva = tk.Frame(
        tarjeta_reserva,
        bg=VERDE
    )

    encabezado_reserva.pack(
        fill="x"
    )

    tk.Label(
        encabezado_reserva,
        text="NUEVA / EDITAR RESERVACIÓN",
        bg=VERDE,
        fg=BLANCO,
        font=("Arial", 11, "bold")
    ).pack(
        anchor="w",
        padx=15,
        pady=9
    )

    formulario_reserva = tk.Frame(
        tarjeta_reserva,
        bg=BLANCO
    )

    formulario_reserva.pack(
        fill="x",
        padx=18,
        pady=10
    )

    for columna in range(4):

        formulario_reserva.columnconfigure(
            columna,
            weight=1
        )

    id_reserva_actual = [None]

    clientes_reserva = {}
    mesas_reserva = {}

    # =========================================================
    # CAMPOS RESERVACIÓN
    # =========================================================

    entrada_cliente = tk.Entry(
        formulario_reserva,
        font=("Arial", 9),
        bd=1,
        relief="solid",
        width=35
    )

    # Fecha con calendario
    marco_fecha = tk.Frame(
        formulario_reserva,
        bg=BLANCO
    )

    entrada_fecha = tk.Entry(
        marco_fecha,
        font=("Arial", 9),
        bd=1,
        relief="solid",
        state="readonly",
        width=14
    )

    entrada_fecha.pack(
        side="left",
        fill="x",
        expand=True
    )

    entrada_hora = ttk.Combobox(
        formulario_reserva,
        state="readonly",
        font=("Arial", 9)
    )

    entrada_personas = tk.Entry(
        formulario_reserva,
        font=("Arial", 9),
        bd=1,
        relief="solid"
    )

    entrada_mesa = ttk.Combobox(
        formulario_reserva,
        state="readonly",
        font=("Arial", 9)
    )

    entrada_forma_pago = ttk.Combobox(
        formulario_reserva,
        state="readonly",
        values=[
            "Efectivo",
            "Tarjeta"
        ],
        font=("Arial", 9)
    )

    entrada_estado = ttk.Combobox(
        formulario_reserva,
        state="readonly",
        values=[
            "Pendiente",
            "Confirmada",
            "Cancelada"
        ],
        font=("Arial", 9)
    )

    entrada_solicitud = tk.Entry(
        formulario_reserva,
        font=("Arial", 9),
        bd=1,
        relief="solid"
    )

    entrada_forma_pago.set(
        "Efectivo"
    )

    entrada_estado.set(
        "Pendiente"
    )

    # =========================================================
    # CLIENTE
    # =========================================================

    tk.Label(
        formulario_reserva,
        text="Cliente",
        bg=BLANCO,
        fg=VERDE_OSCURO,
        font=("Arial", 8, "bold")
    ).grid(
        row=0,
        column=0,
        sticky="w",
        padx=5,
        pady=(0, 4)
    )

    entrada_cliente.grid(
        row=1,
        column=0,
        sticky="ew",
        padx=5
    )

    # =========================================================
    # CALENDARIO
    # =========================================================

    def seleccionar_fecha():

        try:

            fecha_actual = datetime.strptime(
                entrada_fecha.get(),
                "%Y-%m-%d"
            ).date()

        except ValueError:

            fecha_actual = date.today()

        if fecha_actual < date.today():
            fecha_actual = date.today()

        ventana_calendario = tk.Toplevel(
            ventana
        )

        ventana_calendario.title(
            "Seleccionar fecha"
        )

        ventana_calendario.configure(
            bg=CREMA
        )

        ventana_calendario.resizable(
            False,
            False
        )

        ventana_calendario.transient(
            ventana
        )
        ventana_calendario.iconbitmap("vivaldi.ico")

        calendario = Calendar(
            ventana_calendario,
            selectmode="day",
            year=fecha_actual.year,
            month=fecha_actual.month,
            day=fecha_actual.day,
            mindate=date.today(),
            date_pattern="yyyy-mm-dd",
            background=VERDE,
            foreground=BLANCO,
            headersbackground=VERDE_OSCURO,
            headersforeground=BEIGE,
            selectbackground=BEIGE,
            selectforeground=VERDE_OSCURO
        )

        calendario.pack(
            padx=15,
            pady=15
        )

        def confirmar_fecha():

            fecha_seleccionada = (
                calendario.selection_get()
            )

            if fecha_seleccionada < date.today():

                messagebox.showwarning(
                    "Fecha inválida",
                    "No puedes seleccionar una fecha anterior a hoy."
                )

                return

            entrada_fecha.config(
                state="normal"
            )

            entrada_fecha.delete(
                0,
                tk.END
            )

            entrada_fecha.insert(
                0,
                fecha_seleccionada.strftime(
                    "%Y-%m-%d"
                )
            )

            entrada_fecha.config(
                state="readonly"
            )

            ventana_calendario.destroy()

            cargar_mesas()

        tk.Button(
            ventana_calendario,
            text="SELECCIONAR",
            command=confirmar_fecha,
            bg=VERDE,
            fg=BLANCO,
            activebackground=VERDE_OSCURO,
            activeforeground=BLANCO,
            bd=0,
            padx=20,
            pady=7,
            cursor="hand2",
            font=("Arial", 9, "bold")
        ).pack(
            pady=(0, 15)
        )

    tk.Label(
        formulario_reserva,
        text="Fecha",
        bg=BLANCO,
        fg=VERDE_OSCURO,
        font=("Arial", 8, "bold")
    ).grid(
        row=2,
        column=0,
        sticky="w",
        padx=5,
        pady=(6, 4)
    )

    marco_fecha.grid(
        row=3,
        column=0,
        sticky="ew",
        padx=5
    )

    tk.Button(
        marco_fecha,
        text="📅",
        command=seleccionar_fecha,
        bg=BEIGE,
        fg=VERDE_OSCURO,
        activebackground=CREMA,
        bd=0,
        width=3,
        cursor="hand2",
        font=("Arial", 9, "bold")
    ).pack(
        side="left",
        padx=(5, 0)
    )

    # =========================================================
    # CAMPOS RESTANTES
    # =========================================================

    campos_reserva = [
        ("Hora", entrada_hora, 2, 1),
        ("Personas", entrada_personas, 2, 2),
        ("Mesa disponible", entrada_mesa, 2, 3),
        ("Forma de pago", entrada_forma_pago, 4, 0),
        ("Estado", entrada_estado, 4, 1),
        ("Solicitud especial", entrada_solicitud, 4, 2)
    ]

    for texto, entrada, fila, columna in campos_reserva:

        tk.Label(
            formulario_reserva,
            text=texto,
            bg=BLANCO,
            fg=VERDE_OSCURO,
            font=("Arial", 8, "bold")
        ).grid(
            row=fila,
            column=columna,
            sticky="w",
            padx=5,
            pady=(6, 4)
        )

        entrada.grid(
            row=fila + 1,
            column=columna,
            columnspan=2 if texto == "Solicitud especial" else 1,
            sticky="ew",
            padx=5,
            pady=(0, 4)
        )

    # =========================================================
    # VALORES INICIALES
    # =========================================================

    horarios_disponibles = []

    for hora in range(11, 23):

        for minuto in (
            0,
            30
        ):

            if hora == 22 and minuto == 30:
                continue

            horarios_disponibles.append(
                f"{hora:02d}:{minuto:02d}"
            )

    entrada_fecha.config(
        state="normal"
    )

    entrada_fecha.insert(
        0,
        date.today().strftime(
            "%Y-%m-%d"
        )
    )

    entrada_fecha.config(
        state="readonly"
    )

    entrada_hora["values"] = (
        horarios_disponibles
    )

    entrada_hora.set(
        horarios_disponibles[0]
    )

    # =========================================================
    # CLIENTES PARA RESERVACIÓN
    # =========================================================

    def cargar_clientes_reserva():

        clientes_reserva.clear()

        conexion = conectar()

        if not conexion:
            return

        cursor = None

        try:

            cursor = conexion.cursor()

            cursor.execute(
                """
                SELECT id_cliente,
                       nombre,
                       apellido
                FROM Cliente
                ORDER BY nombre, apellido
                """
            )

            for id_cliente, nombre, apellido in cursor.fetchall():

                nombre_completo = (
                    f"{nombre} {apellido}"
                )

                clientes_reserva[
                    nombre_completo
                ] = id_cliente

        except mysql.connector.Error as error:

            messagebox.showerror(
                "Error",
                f"No se pudieron cargar los clientes.\n\n{error}"
            )

        finally:

            if cursor:
                cursor.close()

            conexion.close()

    def buscar_clientes_reserva():

        texto = entrada_cliente.get().strip()

        if not texto:

            messagebox.showwarning(
                "Cliente",
                "Escribe el nombre, teléfono o correo del cliente."
            )

            return

        conexion = conectar()

        if not conexion:
            return

        cursor = None

        try:

            cursor = conexion.cursor()

            patron = f"%{texto}%"

            cursor.execute(
                """
                SELECT id_cliente,
                       nombre,
                       apellido
                FROM Cliente
                WHERE nombre LIKE %s
                   OR apellido LIKE %s
                   OR CONCAT(nombre, ' ', apellido) LIKE %s
                   OR telefono LIKE %s
                   OR correo_electronico LIKE %s
                ORDER BY nombre, apellido
                """,
                (
                    patron,
                    patron,
                    patron,
                    patron,
                    patron
                )
            )

            resultados = cursor.fetchall()

            clientes_reserva.clear()

            if not resultados:

                messagebox.showwarning(
                    "Cliente no registrado",
                    "El cliente no está registrado."
                )

                return

            if len(resultados) > 1:

                messagebox.showwarning(
                    "Cliente",
                    "Se encontraron varios clientes. "
                    "Escribe un dato más específico."
                )

                return

            id_cliente, nombre, apellido = (
                resultados[0]
            )

            nombre_completo = (
                f"{nombre} {apellido}"
            )

            clientes_reserva[
                nombre_completo
            ] = id_cliente

            entrada_cliente.delete(
                0,
                tk.END
            )

            entrada_cliente.insert(
                0,
                nombre_completo
            )

        except mysql.connector.Error as error:

            messagebox.showerror(
                "Error",
                f"No se pudo buscar el cliente.\n\n{error}"
            )

        finally:

            if cursor:
                cursor.close()

            conexion.close()

    boton_buscar_cliente_reserva = tk.Button(
        formulario_reserva,
        text="BUSCAR",
        font=("Arial", 9, "bold"),
        bg=VERDE_OSCURO,
        fg=BLANCO,
        activebackground=CREMA,
        activeforeground=VERDE_OSCURO,
        bd=0,
        padx=12,
        pady=7,
        cursor="hand2",
        command=buscar_clientes_reserva
    )

    boton_buscar_cliente_reserva.grid(
        row=1,
        column=1,
        padx=(5, 0),
        sticky="w"
    )

    def obtener_id_cliente():

        valor = entrada_cliente.get().strip()

        if not valor:
            return None

        return clientes_reserva.get(
            valor
        )

    def obtener_id_mesa():

        valor = entrada_mesa.get().strip()

        if not valor:
            return None

        return mesas_reserva.get(
            valor
        )

    # =========================================================
    # CARGAR MESAS DISPONIBLES
    # =========================================================

    def cargar_mesas(id_mesa_actual=None):

        entrada_mesa["values"] = []
        mesas_reserva.clear()

        fecha = entrada_fecha.get().strip()
        hora = entrada_hora.get().strip()
        texto_personas = entrada_personas.get().strip()

        if not texto_personas:

            entrada_mesa.set("")
            return

        try:

            personas = int(
                texto_personas
            )

        except ValueError:

            entrada_mesa.set("")
            return

        if personas <= 0:

            entrada_mesa.set("")
            return

        if not fecha or not hora:
            return

        conexion = conectar()

        if not conexion:
            return

        cursor = None

        try:

            cursor = conexion.cursor()

            if id_reserva_actual[0] is not None:

                cursor.execute(
                    """
                    SELECT id_mesa
                    FROM Reserva
                    WHERE estado IN ('Pendiente', 'Confirmada')
                    AND id_reserva <> %s
                    AND TIMESTAMP(fecha, hora)
                        < TIMESTAMP(%s, %s) + INTERVAL 2 HOUR
                    AND TIMESTAMP(fecha, hora)
                        + INTERVAL 2 HOUR
                        > TIMESTAMP(%s, %s)
                    """,
                    (
                        id_reserva_actual[0],
                        fecha,
                        hora,
                        fecha,
                        hora
                    )
                )

            else:

                cursor.execute(
                    """
                    SELECT id_mesa
                    FROM Reserva
                    WHERE estado IN ('Pendiente', 'Confirmada')
                    AND TIMESTAMP(fecha, hora)
                        < TIMESTAMP(%s, %s) + INTERVAL 2 HOUR
                    AND TIMESTAMP(fecha, hora)
                        + INTERVAL 2 HOUR
                        > TIMESTAMP(%s, %s)
                    """,
                    (
                        fecha,
                        hora,
                        fecha,
                        hora
                    )
                )

            mesas_reservadas = {
                fila[0]
                for fila in cursor.fetchall()
            }

            cursor.execute(
                """
                SELECT id_mesa,
                       numero_mesa,
                       capacidad,
                       zona
                FROM Mesa
                ORDER BY capacidad, numero_mesa
                """
            )

            mesas_disponibles = []

            for (
                id_mesa,
                numero,
                capacidad,
                zona
            ) in cursor.fetchall():

                if capacidad < personas:
                    continue

                if (
                    id_mesa in mesas_reservadas
                    and id_mesa != id_mesa_actual
                ):
                    continue

                mesas_disponibles.append(
                    (
                        id_mesa,
                        numero,
                        capacidad,
                        zona
                    )
                )

            if not mesas_disponibles:

                entrada_mesa.set("")
                entrada_mesa["values"] = []

                return

            menor_capacidad = min(
                mesa[2]
                for mesa in mesas_disponibles
            )

            mesas_a_mostrar = [
                mesa
                for mesa in mesas_disponibles
                if mesa[2] == menor_capacidad
            ]

            if id_mesa_actual is not None:

                mesa_actual = next(
                    (
                        mesa
                        for mesa in mesas_disponibles
                        if mesa[0] == id_mesa_actual
                    ),
                    None
                )

                if (
                    mesa_actual
                    and mesa_actual not in mesas_a_mostrar
                ):

                    mesas_a_mostrar.append(
                        mesa_actual
                    )

            valores = []

            for (
                id_mesa,
                numero,
                capacidad,
                zona
            ) in mesas_a_mostrar:

                texto_mesa = (
                    f"Mesa {numero} - "
                    f"{capacidad} personas - "
                    f"{zona}"
                )

                mesas_reserva[
                    texto_mesa
                ] = id_mesa

                valores.append(
                    texto_mesa
                )

            entrada_mesa["values"] = valores

            if id_mesa_actual is not None:

                for valor in valores:

                    if (
                        mesas_reserva.get(valor)
                        == id_mesa_actual
                    ):

                        entrada_mesa.set(
                            valor
                        )

                        break

        except mysql.connector.Error as error:

            messagebox.showerror(
                "Error",
                f"No se pudieron cargar las mesas.\n\n{error}"
            )

        finally:

            if cursor:
                cursor.close()

            conexion.close()

    # =========================================================
    # VERIFICAR MESA
    # =========================================================

    def mesa_disponible(
        cursor,
        id_mesa,
        fecha,
        hora,
        id_reserva_excluir=None
    ):

        cursor.execute(
            """
            SELECT capacidad
            FROM Mesa
            WHERE id_mesa = %s
            """,
            (id_mesa,)
        )

        resultado = cursor.fetchone()

        if not resultado:

            return (
                False,
                "La mesa seleccionada no existe."
            )

        if id_reserva_excluir is not None:

            cursor.execute(
                """
                SELECT id_reserva
                FROM Reserva
                WHERE id_mesa = %s
                AND estado IN ('Pendiente', 'Confirmada')
                AND id_reserva <> %s
                AND TIMESTAMP(fecha, hora)
                    < TIMESTAMP(%s, %s) + INTERVAL 2 HOUR
                AND TIMESTAMP(fecha, hora)
                    + INTERVAL 2 HOUR
                    > TIMESTAMP(%s, %s)
                LIMIT 1
                """,
                (
                    id_mesa,
                    id_reserva_excluir,
                    fecha,
                    hora,
                    fecha,
                    hora
                )
            )

        else:

            cursor.execute(
                """
                SELECT id_reserva
                FROM Reserva
                WHERE id_mesa = %s
                AND estado IN ('Pendiente', 'Confirmada')
                AND TIMESTAMP(fecha, hora)
                    < TIMESTAMP(%s, %s) + INTERVAL 2 HOUR
                AND TIMESTAMP(fecha, hora)
                    + INTERVAL 2 HOUR
                    > TIMESTAMP(%s, %s)
                LIMIT 1
                """,
                (
                    id_mesa,
                    fecha,
                    hora,
                    fecha,
                    hora
                )
            )

        if cursor.fetchone():

            return (
                False,
                "La mesa ya está reservada durante ese horario."
            )

        return True, ""

    # =========================================================
    # TABLA RESERVACIONES
    # =========================================================

    zona_tabla_reservas = tk.Frame(
        tarjeta_reserva,
        bg=BLANCO
    )

    zona_tabla_reservas.pack(
        fill="both",
        expand=True,
        padx=18,
        pady=(0, 8)
    )

    tk.Label(
        zona_tabla_reservas,
        text="RESERVACIONES REGISTRADAS  •  DOBLE CLIC PARA EDITAR",
        bg=BLANCO,
        fg=VERDE,
        font=("Arial", 10, "bold")
    ).pack(
        anchor="w",
        pady=(0, 5)
    )

    marco_busqueda_reservas = tk.Frame(
        zona_tabla_reservas,
        bg=BLANCO
    )

    marco_busqueda_reservas.pack(
        fill="x",
        pady=(0, 8)
    )

    tk.Label(
        marco_busqueda_reservas,
        text="Buscar reservación:",
        bg=BLANCO,
        fg=VERDE_OSCURO,
        font=("Arial", 9, "bold")
    ).pack(
        side="left",
        padx=(0, 7)
    )

    entrada_busqueda_reserva = tk.Entry(
        marco_busqueda_reservas,
        font=("Arial", 10),
        bd=1,
        relief="solid",
        width=25
    )

    entrada_busqueda_reserva.pack(
        side="left"
    )

    # =========================================================
    # TABLA
    # =========================================================

    tabla_reservaciones = ttk.Treeview(
        zona_tabla_reservas,
        columns=(
            "id",
            "cliente",
            "fecha",
            "hora",
            "personas",
            "mesa",
            "estado",
            "solicitud"
        ),
        show="headings"
    )

    encabezados = {
        "id": "ID",
        "cliente": "Cliente",
        "fecha": "Fecha",
        "hora": "Hora",
        "personas": "Personas",
        "mesa": "Mesa",
        "estado": "Estado",
        "solicitud": "Solicitud"
    }

    anchos = {
        "id": 40,
        "cliente": 130,
        "fecha": 80,
        "hora": 55,
        "personas": 60,
        "mesa": 50,
        "estado": 90,
        "solicitud": 180
    }

    for columna in encabezados:

        tabla_reservaciones.heading(
            columna,
            text=encabezados[columna]
        )

        tabla_reservaciones.column(
            columna,
            width=anchos[columna],
            anchor="center"
        )

    tabla_reservaciones.tag_configure(
        "pendiente",
        foreground=VERDE_OSCURO
    )

    tabla_reservaciones.tag_configure(
        "confirmada",
        foreground=VERDE
    )

    tabla_reservaciones.tag_configure(
        "completada",
        foreground=GRIS
    )

    tabla_reservaciones.tag_configure(
        "cancelada",
        foreground=VINO
    )

    # =========================================================
    # ESTADOS AUTOMÁTICOS
    # =========================================================

    def actualizar_estados_automaticos():

        conexion = conectar()

        if not conexion:
            return

        cursor = None

        try:

            cursor = conexion.cursor()

            cursor.execute(
                """
                UPDATE Reserva
                SET estado = 'Completada'
                WHERE estado IN ('Pendiente', 'Confirmada')
                AND TIMESTAMP(fecha, hora)
                    + INTERVAL 2 HOUR <= NOW()
                """
            )

            cursor.execute(
                """
                UPDATE Mesa m
                SET estado = CASE
                    WHEN EXISTS (
                        SELECT 1
                        FROM Reserva r
                        WHERE r.id_mesa = m.id_mesa
                        AND r.estado IN ('Pendiente', 'Confirmada')
                        AND TIMESTAMP(r.fecha, r.hora) <= NOW()
                        AND TIMESTAMP(r.fecha, r.hora)
                            + INTERVAL 2 HOUR > NOW()
                    )
                    THEN 'Ocupada'
                    ELSE 'Disponible'
                END
                """
            )

            conexion.commit()

        except mysql.connector.Error as error:

            conexion.rollback()

            print(
                "Error al actualizar estados:",
                error
            )

        finally:

            if cursor:
                cursor.close()

            conexion.close()

    # =========================================================
    # MOSTRAR RESERVACIONES
    # =========================================================

    def mostrar_reservaciones(filtro=""):

        actualizar_estados_automaticos()

        for item in tabla_reservaciones.get_children():

            tabla_reservaciones.delete(
                item
            )

        conexion = conectar()

        if not conexion:
            return

        cursor = None

        try:

            cursor = conexion.cursor()

            if filtro.strip():

                patron = f"%{filtro.strip()}%"

                cursor.execute(
                    """
                    SELECT r.id_reserva,
                           CONCAT(c.nombre, ' ', c.apellido),
                           r.fecha,
                           r.hora,
                           r.cantidad_personas,
                           m.numero_mesa,
                           r.estado,
                           r.solicitud_adicional
                    FROM Reserva r
                    INNER JOIN Cliente c
                        ON r.id_cliente = c.id_cliente
                    INNER JOIN Mesa m
                        ON r.id_mesa = m.id_mesa
                    WHERE CAST(r.id_reserva AS CHAR) LIKE %s
                       OR c.nombre LIKE %s
                       OR c.apellido LIKE %s
                       OR CONCAT(c.nombre, ' ', c.apellido) LIKE %s
                       OR c.telefono LIKE %s
                       OR c.correo_electronico LIKE %s
                       OR CAST(r.fecha AS CHAR) LIKE %s
                       OR CAST(m.numero_mesa AS CHAR) LIKE %s
                    ORDER BY r.fecha DESC,
                             r.hora DESC,
                             r.id_reserva DESC
                    """,
                    (
                        patron,
                        patron,
                        patron,
                        patron,
                        patron,
                        patron,
                        patron,
                        patron
                    )
                )

            else:

                cursor.execute(
                    """
                    SELECT r.id_reserva,
                           CONCAT(c.nombre, ' ', c.apellido),
                           r.fecha,
                           r.hora,
                           r.cantidad_personas,
                           m.numero_mesa,
                           r.estado,
                           r.solicitud_adicional
                    FROM Reserva r
                    INNER JOIN Cliente c
                        ON r.id_cliente = c.id_cliente
                    INNER JOIN Mesa m
                        ON r.id_mesa = m.id_mesa
                    ORDER BY r.fecha DESC,
                             r.hora DESC,
                             r.id_reserva DESC
                    """
                )

            resultados = cursor.fetchall()

            for reserva in resultados:

                if reserva[6] == "Pendiente":
                    tag = "pendiente"

                elif reserva[6] == "Confirmada":
                    tag = "confirmada"

                elif reserva[6] == "Completada":
                    tag = "completada"

                else:
                    tag = "cancelada"

                tabla_reservaciones.insert(
                    "",
                    "end",
                    values=reserva,
                    tags=(tag,)
                )

            if filtro.strip() and not resultados:

                messagebox.showinfo(
                    "Reservaciones",
                    "No se encontraron reservaciones."
                )

        except mysql.connector.Error as error:

            messagebox.showerror(
                "Error",
                f"No se pudieron cargar las reservaciones.\n\n{error}"
            )

        finally:

            if cursor:
                cursor.close()

            conexion.close()

    # =========================================================
    # BUSCADOR RESERVACIONES
    # =========================================================

    tk.Button(
        marco_busqueda_reservas,
        text="BUSCAR",
        command=lambda: mostrar_reservaciones(
            entrada_busqueda_reserva.get()
        ),
        bg=VERDE,
        fg=BLANCO,
        activebackground=VERDE_OSCURO,
        activeforeground=BLANCO,
        bd=0,
        padx=15,
        pady=6,
        cursor="hand2",
        font=("Arial", 9, "bold")
    ).pack(
        side="left",
        padx=8
    )

    tk.Button(
        marco_busqueda_reservas,
        text="MOSTRAR TODAS",
        command=lambda: (
            entrada_busqueda_reserva.delete(
                0,
                tk.END
            ),
            mostrar_reservaciones()
        ),
        bg=BEIGE,
        fg=VERDE_OSCURO,
        activebackground=CREMA,
        activeforeground=VERDE_OSCURO,
        bd=0,
        padx=15,
        pady=6,
        cursor="hand2",
        font=("Arial", 9, "bold")
    ).pack(
        side="left"
    )

    entrada_busqueda_reserva.bind(
        "<Return>",
        lambda event: mostrar_reservaciones(
            entrada_busqueda_reserva.get()
        )
    )

    tabla_reservaciones.pack(
        fill="both",
        expand=True
    )

    # =========================================================
    # CARGAR RESERVACIÓN
    # =========================================================

    def cargar_reserva_por_id(id_reserva):

        actualizar_estados_automaticos()

        conexion = conectar()

        if not conexion:
            return

        cursor = None

        try:

            cursor = conexion.cursor()

            cursor.execute(
                """
                SELECT id_reserva,
                       fecha,
                       hora,
                       cantidad_personas,
                       solicitud_adicional,
                       estado,
                       forma_pago,
                       id_cliente,
                       id_mesa
                FROM Reserva
                WHERE id_reserva = %s
                """,
                (id_reserva,)
            )

            reserva = cursor.fetchone()

            if not reserva:

                messagebox.showwarning(
                    "Reservación",
                    "No se encontró la reservación."
                )

                return

            if reserva[5] in (
                "Completada",
                "Cancelada"
            ):

                messagebox.showinfo(
                    "Reservación",
                    f"Esta reservación ya está "
                    f"{reserva[5].lower()} y no puede editarse."
                )

                return

            id_reserva_actual[0] = reserva[0]

            cargar_clientes_reserva()

            cliente_encontrado = None

            for nombre_completo, id_cliente in (
                clientes_reserva.items()
            ):

                if id_cliente == reserva[7]:

                    cliente_encontrado = (
                        nombre_completo
                    )

                    break

            if cliente_encontrado:

                entrada_cliente.delete(
                    0,
                    tk.END
                )

                entrada_cliente.insert(
                    0,
                    cliente_encontrado
                )

            # Fecha
            entrada_fecha.config(
                state="normal"
            )

            entrada_fecha.delete(
                0,
                tk.END
            )

            entrada_fecha.insert(
                0,
                str(reserva[1])
            )

            entrada_fecha.config(
                state="readonly"
            )

            hora = reserva[2]

            if hasattr(
                hora,
                "strftime"
            ):

                hora = hora.strftime(
                    "%H:%M"
                )

            else:

                hora = str(hora)[:5]

            entrada_hora.set(
                hora
            )

            entrada_personas.delete(
                0,
                tk.END
            )

            entrada_personas.insert(
                0,
                str(reserva[3])
            )

            entrada_solicitud.delete(
                0,
                tk.END
            )

            if reserva[4]:

                entrada_solicitud.insert(
                    0,
                    reserva[4]
                )

            entrada_estado.set(
                reserva[5]
            )

            entrada_forma_pago.set(
                reserva[6]
            )

            cargar_mesas(
                reserva[8]
            )

        except mysql.connector.Error as error:

            messagebox.showerror(
                "Error",
                f"No se pudo cargar la reservación.\n\n{error}"
            )

        finally:

            if cursor:
                cursor.close()

            conexion.close()

    def cargar_reserva_seleccionada(event=None):

        seleccion = tabla_reservaciones.selection()

        if not seleccion:
            return

        valores = tabla_reservaciones.item(
            seleccion[0]
        ).get("values")

        if valores:

            try:

                cargar_reserva_por_id(
                    int(valores[0])
                )

            except:

                pass

    tabla_reservaciones.bind(
        "<Double-1>",
        cargar_reserva_seleccionada
    )

    # =========================================================
    # VER DETALLES
    # =========================================================

    def ver_detalles_reserva():

        seleccion = tabla_reservaciones.selection()

        if not seleccion:

            messagebox.showwarning(
                "Reservación",
                "Selecciona una reservación para ver sus detalles."
            )

            return

        valores = tabla_reservaciones.item(
            seleccion[0]
        ).get("values")

        if not valores:
            return

        id_reserva = int(
            valores[0]
        )

        conexion = conectar()

        if not conexion:
            return

        cursor = None
        reserva = None

        try:

            cursor = conexion.cursor()

            cursor.execute(
                """
                SELECT r.id_reserva,
                       CONCAT(c.nombre, ' ', c.apellido),
                       r.fecha,
                       r.hora,
                       r.cantidad_personas,
                       m.numero_mesa,
                       m.capacidad,
                       m.zona,
                       r.estado,
                       r.forma_pago,
                       r.solicitud_adicional
                FROM Reserva r
                INNER JOIN Cliente c
                    ON r.id_cliente = c.id_cliente
                INNER JOIN Mesa m
                    ON r.id_mesa = m.id_mesa
                WHERE r.id_reserva = %s
                """,
                (id_reserva,)
            )

            reserva = cursor.fetchone()

        except mysql.connector.Error as error:

            messagebox.showerror(
                "Error",
                f"No se pudieron obtener los detalles.\n\n{error}"
            )

            return

        finally:

            if cursor:
                cursor.close()

            conexion.close()

        if not reserva:

            messagebox.showerror(
                "Error",
                "No se encontró la reservación."
            )

            return

        hora_inicio = reserva[3]

        if hasattr(
            hora_inicio,
            "strftime"
        ):

            hora_inicio_texto = (
                hora_inicio.strftime(
                    "%H:%M"
                )
            )

            hora_fin = (
                datetime.combine(
                    reserva[2],
                    hora_inicio
                )
                + timedelta(hours=2)
            ).strftime(
                "%H:%M"
            )

        else:

            hora_inicio_texto = str(
                hora_inicio
            )[:5]

            hora_fin = (
                "Calculada 2 horas después"
            )

        ventana_detalles = tk.Toplevel(
            ventana
        )

        ventana_detalles.title(
            "Detalles de la reservación"
        )

        ventana_detalles.geometry(
            "500x570"
        )

        ventana_detalles.configure(
            bg=CREMA
        )

        ventana_detalles.resizable(
            False,
            False
        )

        tk.Label(
            ventana_detalles,
            text="DETALLES DE LA RESERVACIÓN",
            font=("Arial", 16, "bold"),
            bg=CREMA,
            fg=VERDE
        ).pack(
            pady=(25, 20)
        )

        datos_detalles = [
            (
                "Reservación",
                f"#{reserva[0]}"
            ),
            (
                "Cliente",
                reserva[1]
            ),
            (
                "Fecha",
                str(reserva[2])
            ),
            (
                "Hora",
                hora_inicio_texto
            ),
            (
                "Finaliza",
                hora_fin
            ),
            (
                "Personas",
                str(reserva[4])
            ),
            (
                "Mesa",
                f"Mesa {reserva[5]}"
            ),
            (
                "Capacidad",
                f"{reserva[6]} personas"
            ),
            (
                "Zona",
                reserva[7]
            ),
            (
                "Estado",
                reserva[8]
            ),
            (
                "Forma de pago",
                reserva[9]
            ),
            (
                "Solicitud",
                reserva[10] or "Ninguna"
            )
        ]

        for titulo, valor in datos_detalles:

            fila = tk.Frame(
                ventana_detalles,
                bg=CREMA
            )

            fila.pack(
                fill="x",
                padx=35,
                pady=4
            )

            tk.Label(
                fila,
                text=f"{titulo}:",
                font=("Arial", 9, "bold"),
                bg=CREMA,
                fg=VERDE
            ).pack(
                side="left"
            )

            tk.Label(
                fila,
                text=valor,
                font=("Arial", 9),
                bg=CREMA,
                fg=VERDE_OSCURO
            ).pack(
                side="left",
                padx=8
            )

        tk.Button(
            ventana_detalles,
            text="CERRAR",
            command=ventana_detalles.destroy,
            bg=GRIS_CLARO,
            fg=VERDE_OSCURO,
            font=("Arial", 9, "bold"),
            bd=0,
            padx=25,
            pady=8,
            cursor="hand2"
        ).pack(
            pady=25
        )

    # =========================================================
    # OBTENER DATOS RESERVA
    # =========================================================

    def obtener_datos_reserva():

        id_cliente = obtener_id_cliente()

        fecha = entrada_fecha.get().strip()
        hora = entrada_hora.get().strip()

        # -----------------------------------------------------
        # VALIDAR FECHA
        # -----------------------------------------------------

        try:

            fecha_seleccionada = datetime.strptime(
                fecha,
                "%Y-%m-%d"
            ).date()

        except ValueError:

            messagebox.showwarning(
                "Fecha inválida",
                "Selecciona una fecha válida."
            )

            return None

        if fecha_seleccionada < date.today():

            messagebox.showwarning(
                "Fecha inválida",
                "No puedes reservar una fecha anterior a hoy."
            )

            return None

        # -----------------------------------------------------
        # VALIDAR FECHA Y HORA
        # -----------------------------------------------------

        try:

            fecha_hora_reserva = datetime.strptime(
                f"{fecha} {hora}",
                "%Y-%m-%d %H:%M"
            )

        except ValueError:

            messagebox.showwarning(
                "Fecha u hora inválida",
                "Verifica la fecha y la hora de la reserva."
            )

            return None

        if fecha_hora_reserva <= datetime.now():

            messagebox.showwarning(
                "Hora no disponible",
                "No puedes reservar una fecha u hora que ya pasó."
            )

            return None

        texto_personas = (
            entrada_personas.get().strip()
        )

        id_mesa = obtener_id_mesa()

        estado = entrada_estado.get()

        forma_pago = entrada_forma_pago.get()

        solicitud = (
            entrada_solicitud.get().strip()
        )

        # -----------------------------------------------------
        # NUEVA RESERVA NO PUEDE SER CANCELADA
        # -----------------------------------------------------

        if (
            id_reserva_actual[0] is None
            and estado == "Cancelada"
        ):

            messagebox.showwarning(
                "Estado inválido",
                "Una nueva reservación no puede registrarse como cancelada."
            )

            return None

        if id_cliente is None:

            messagebox.showwarning(
                "Cliente",
                "El cliente no está registrado."
            )

            return None

        try:

            personas = int(
                texto_personas
            )

        except:

            messagebox.showwarning(
                "Personas",
                "La cantidad de personas debe ser un número."
            )

            return None

        if personas <= 0:

            messagebox.showwarning(
                "Personas",
                "La cantidad de personas debe ser mayor que cero."
            )

            return None

        if id_mesa is None:

            messagebox.showwarning(
                "Mesa",
                "Selecciona una mesa disponible."
            )

            return None

        if not forma_pago:

            messagebox.showwarning(
                "Forma de pago",
                "Selecciona una forma de pago."
            )

            return None

        return {
            "id_cliente": id_cliente,
            "fecha": fecha,
            "hora": hora,
            "personas": personas,
            "id_mesa": id_mesa,
            "estado": estado,
            "forma_pago": forma_pago,
            "solicitud": solicitud
        }

    # =========================================================
    # GUARDAR NUEVA RESERVA
    # =========================================================

    def guardar_reserva():

        if id_reserva_actual[0] is not None:

            messagebox.showwarning(
                "Reservación cargada",
                "Ya tienes una reservación cargada.\n\n"
                "Usa GUARDAR CAMBIOS para editarla "
                "o LIMPIAR para registrar una nueva."
            )

            return

        datos = obtener_datos_reserva()

        if datos is None:
            return

        conexion = conectar()

        if not conexion:
            return

        cursor = None

        try:

            cursor = conexion.cursor()

            cursor.execute(
                """
                SELECT capacidad
                FROM Mesa
                WHERE id_mesa = %s
                """,
                (datos["id_mesa"],)
            )

            resultado = cursor.fetchone()

            if not resultado:

                messagebox.showwarning(
                    "Mesa",
                    "La mesa seleccionada no existe."
                )

                return

            if datos["personas"] > resultado[0]:

                messagebox.showwarning(
                    "Capacidad insuficiente",
                    f"La mesa tiene capacidad para {resultado[0]} personas."
                )

                return

            disponible, mensaje = mesa_disponible(
                cursor,
                datos["id_mesa"],
                datos["fecha"],
                datos["hora"]
            )

            if not disponible:

                messagebox.showwarning(
                    "Mesa no disponible",
                    mensaje
                )

                cargar_mesas()

                return

            cursor.execute(
                """
                INSERT INTO Reserva (
                    fecha,
                    hora,
                    cantidad_personas,
                    solicitud_adicional,
                    estado,
                    forma_pago,
                    id_cliente,
                    id_mesa,
                    id_empleado
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    datos["fecha"],
                    datos["hora"],
                    datos["personas"],
                    datos["solicitud"],
                    datos["estado"],
                    datos["forma_pago"],
                    datos["id_cliente"],
                    datos["id_mesa"],
                    id_empleado
                )
            )

            conexion.commit()

            messagebox.showinfo(
                "Reservación registrada",
                "La reservación se registró correctamente."
            )

            limpiar_reserva()
            mostrar_reservaciones()
            mostrar_mesas()

        except mysql.connector.Error as error:

            conexion.rollback()

            messagebox.showerror(
                "Error",
                f"No se pudo registrar la reservación.\n\n{error}"
            )

        finally:

            if cursor:
                cursor.close()

            conexion.close()

    # =========================================================
    # CANCELAR RESERVACIÓN
    # =========================================================

    def cancelar_reserva():

        if id_reserva_actual[0] is None:
            return False

        conexion = conectar()

        if not conexion:
            return False

        cursor = None

        try:

            cursor = conexion.cursor()

            cursor.execute(
                """
                SELECT estado
                FROM Reserva
                WHERE id_reserva = %s
                """,
                (id_reserva_actual[0],)
            )

            reserva = cursor.fetchone()

            if not reserva:

                messagebox.showwarning(
                    "Reservación",
                    "La reservación ya no existe."
                )

                return False

            if reserva[0] == "Cancelada":

                messagebox.showinfo(
                    "Reservación",
                    "Esta reservación ya está cancelada."
                )

                return False

            if reserva[0] == "Completada":

                messagebox.showinfo(
                    "Reservación",
                    "Una reservación completada no puede cancelarse."
                )

                return False

            cursor.execute(
                """
                UPDATE Reserva
                SET estado = 'Cancelada'
                WHERE id_reserva = %s
                """,
                (id_reserva_actual[0],)
            )

            conexion.commit()

            return True

        except mysql.connector.Error as error:

            conexion.rollback()

            messagebox.showerror(
                "Error",
                f"No se pudo cancelar la reservación.\n\n{error}"
            )

            return False

        finally:

            if cursor:
                cursor.close()

            conexion.close()

    # =========================================================
    # EDITAR RESERVACIÓN
    # =========================================================

    def editar_reserva():

        if id_reserva_actual[0] is None:

            messagebox.showwarning(
                "Editar",
                "Primero haz doble clic sobre una reservación."
            )

            return

        # =====================================================
        # CANCELACIÓN
        # ESTA PARTE VA ANTES DE obtener_datos_reserva()
        # PARA QUE FUNCIONE AUNQUE LA HORA YA HAYA COMENZADO
        # =====================================================

        if entrada_estado.get() == "Cancelada":

            confirmar = messagebox.askyesno(
                "Cancelar reservación",
                "¿Deseas cancelar esta reservación?\n\n"
                "La reservación permanecerá en el historial."
            )

            if not confirmar:
                return

            if not cancelar_reserva():
                return

            messagebox.showinfo(
                "Reservación cancelada",
                "La reservación fue cancelada correctamente."
            )

            filtro_actual = (
                entrada_busqueda_reserva.get().strip()
            )

            limpiar_reserva()

            mostrar_reservaciones(
                filtro_actual
            )

            mostrar_mesas()

            return

        # =====================================================
        # DATOS NORMALES DE EDICIÓN
        # =====================================================

        datos = obtener_datos_reserva()

        if datos is None:
            return

        conexion = conectar()

        if not conexion:
            return

        cursor = None

        try:

            cursor = conexion.cursor()

            cursor.execute(
                """
                SELECT estado
                FROM Reserva
                WHERE id_reserva = %s
                """,
                (id_reserva_actual[0],)
            )

            reserva_actual = cursor.fetchone()

            if not reserva_actual:

                messagebox.showwarning(
                    "Reservación",
                    "La reservación ya no existe."
                )

                return

            if reserva_actual[0] in (
                "Cancelada",
                "Completada"
            ):

                messagebox.showwarning(
                    "Reservación",
                    "Esta reservación ya no puede editarse."
                )

                return

            cursor.execute(
                """
                SELECT capacidad
                FROM Mesa
                WHERE id_mesa = %s
                """,
                (datos["id_mesa"],)
            )

            capacidad = cursor.fetchone()

            if not capacidad:

                messagebox.showwarning(
                    "Mesa",
                    "La mesa no existe."
                )

                return

            if datos["personas"] > capacidad[0]:

                messagebox.showwarning(
                    "Capacidad insuficiente",
                    f"La mesa tiene capacidad para {capacidad[0]} personas."
                )

                return

            disponible, mensaje = mesa_disponible(
                cursor,
                datos["id_mesa"],
                datos["fecha"],
                datos["hora"],
                id_reserva_actual[0]
            )

            if not disponible:

                messagebox.showwarning(
                    "Mesa no disponible",
                    mensaje
                )

                return

            cursor.execute(
                """
                UPDATE Reserva
                SET fecha = %s,
                    hora = %s,
                    cantidad_personas = %s,
                    solicitud_adicional = %s,
                    estado = %s,
                    forma_pago = %s,
                    id_cliente = %s,
                    id_mesa = %s
                WHERE id_reserva = %s
                """,
                (
                    datos["fecha"],
                    datos["hora"],
                    datos["personas"],
                    datos["solicitud"],
                    datos["estado"],
                    datos["forma_pago"],
                    datos["id_cliente"],
                    datos["id_mesa"],
                    id_reserva_actual[0]
                )
            )

            conexion.commit()

            messagebox.showinfo(
                "Reservación actualizada",
                "Los cambios se guardaron correctamente."
            )

            filtro_actual = (
                entrada_busqueda_reserva.get().strip()
            )

            limpiar_reserva()

            mostrar_reservaciones(
                filtro_actual
            )

            mostrar_mesas()

        except mysql.connector.Error as error:

            conexion.rollback()

            messagebox.showerror(
                "Error",
                f"No se pudo editar la reservación.\n\n{error}"
            )

        finally:

            if cursor:
                cursor.close()

            conexion.close()

    # =========================================================
    # LIMPIAR RESERVACIÓN
    # =========================================================

    def limpiar_reserva():

        id_reserva_actual[0] = None

        entrada_cliente.delete(
            0,
            tk.END
        )

        entrada_fecha.config(
            state="normal"
        )

        entrada_fecha.delete(
            0,
            tk.END
        )

        entrada_fecha.insert(
            0,
            date.today().strftime(
                "%Y-%m-%d"
            )
        )

        entrada_fecha.config(
            state="readonly"
        )

        entrada_hora.set(
            horarios_disponibles[0]
        )

        entrada_personas.delete(
            0,
            tk.END
        )

        entrada_mesa.set("")

        entrada_estado.set(
            "Pendiente"
        )

        entrada_forma_pago.set(
            "Efectivo"
        )

        entrada_solicitud.delete(
            0,
            tk.END
        )

        cargar_clientes_reserva()
        cargar_mesas()

    # =========================================================
    # BOTONES RESERVACIÓN
    # =========================================================

    boton_ver_detalles = tk.Button(
        tarjeta_reserva,
        text="VER DETALLES",
        command=ver_detalles_reserva,
        bg=VERDE,
        fg=BLANCO,
        activebackground=VERDE_OSCURO,
        activeforeground=BLANCO,
        bd=0,
        padx=18,
        pady=7,
        cursor="hand2",
        font=("Arial", 8, "bold")
    )

    boton_ver_detalles.pack(
        pady=(0, 6)
    )

    marco_botones_reserva = tk.Frame(
        formulario_reserva,
        bg=BLANCO
    )

    marco_botones_reserva.grid(
        row=7,
        column=0,
        columnspan=4,
        pady=(8, 0)
    )

    boton_registrar = tk.Button(
        marco_botones_reserva,
        text="REGISTRAR",
        command=guardar_reserva,
        bg=BEIGE,
        fg=VERDE,
        activebackground=CREMA,
        activeforeground=VERDE,
        bd=0,
        padx=13,
        pady=7,
        cursor="hand2",
        font=("Arial", 8, "bold")
    )

    boton_registrar.pack(
        side="left",
        padx=4
    )

    boton_guardar_cambios = tk.Button(
        marco_botones_reserva,
        text="GUARDAR CAMBIOS",
        command=editar_reserva,
        bg=VERDE,
        fg=BLANCO,
        activebackground=VERDE_OSCURO,
        activeforeground=BLANCO,
        bd=0,
        padx=13,
        pady=7,
        cursor="hand2",
        font=("Arial", 8, "bold")
    )

    boton_guardar_cambios.pack(
        side="left",
        padx=4
    )

    boton_limpiar = tk.Button(
        marco_botones_reserva,
        text="LIMPIAR",
        command=limpiar_reserva,
        bg=GRIS_CLARO,
        fg=VERDE_OSCURO,
        activebackground=CREMA,
        activeforeground=VERDE_OSCURO,
        bd=0,
        padx=13,
        pady=7,
        cursor="hand2",
        font=("Arial", 8, "bold")
    )

    boton_limpiar.pack(
        side="left",
        padx=4
    )

    # =========================================================
    # EVENTOS RESERVACIÓN
    # =========================================================

    entrada_hora.bind(
        "<<ComboboxSelected>>",
        lambda event: cargar_mesas()
    )

    entrada_personas.bind(
        "<KeyRelease>",
        lambda event: cargar_mesas()
    )

    # =========================================================
    # MESAS
    # =========================================================

    tk.Label(
        panel_mesas,
        text="Mesas",
        bg=CREMA,
        fg=VERDE,
        font=("Georgia", 25, "bold")
    ).pack(
        anchor="w",
        pady=(5, 0)
    )

    tk.Label(
        panel_mesas,
        text="Consulta rápidamente las mesas según su zona, capacidad y estado.",
        bg=CREMA,
        fg=GRIS,
        font=("Arial", 10)
    ).pack(
        anchor="w",
        pady=(3, 8)
    )

    tk.Frame(
        panel_mesas,
        bg=BEIGE,
        height=2
    ).pack(
        fill="x",
        pady=(0, 12)
    )

    tarjeta_mesas = tk.Frame(
        panel_mesas,
        bg=BLANCO,
        bd=1,
        relief="solid"
    )

    tarjeta_mesas.pack(
        fill="both",
        expand=True
    )

    encabezado_mesas = tk.Frame(
        tarjeta_mesas,
        bg=VERDE
    )

    encabezado_mesas.pack(
        fill="x"
    )

    tk.Label(
        encabezado_mesas,
        text="ESTADO DE LAS MESAS",
        bg=VERDE,
        fg=BLANCO,
        font=("Arial", 11, "bold")
    ).pack(
        anchor="w",
        padx=15,
        pady=10
    )

    zona_visual_mesas = tk.Frame(
        tarjeta_mesas,
        bg=BLANCO
    )

    zona_visual_mesas.pack(
        fill="both",
        expand=True,
        padx=18,
        pady=12
    )

    frames_zonas = {}
    actualizar_scrollbars = []

    # =========================================================
    # CREAR ZONAS
    # =========================================================

    for zona in (
        "salón",
        "terraza",
        "jardín"
    ):

        frame_zona = tk.Frame(
            zona_visual_mesas,
            bg=CREMA,
            bd=1,
            relief="solid"
        )

        frame_zona.pack(
            fill="x",
            pady=4
        )

        tk.Label(
            frame_zona,
            text=zona.upper(),
            bg=VERDE_OSCURO,
            fg=BEIGE,
            font=("Arial", 9, "bold")
        ).pack(
            fill="x",
            padx=1,
            pady=1
        )

        contenedor_scroll = tk.Frame(
            frame_zona,
            bg=CREMA
        )

        contenedor_scroll.pack(
            fill="x",
            padx=8,
            pady=(8, 2)
        )

        canvas = tk.Canvas(
            contenedor_scroll,
            bg=CREMA,
            height=82,
            highlightthickness=0
        )

        canvas.pack(
            fill="x",
            expand=True
        )

        scrollbar = ttk.Scrollbar(
            contenedor_scroll,
            orient="horizontal",
            command=canvas.xview
        )

        canvas.configure(
            xscrollcommand=scrollbar.set
        )

        contenido_zona = tk.Frame(
            canvas,
            bg=CREMA
        )

        canvas.create_window(
            (0, 0),
            window=contenido_zona,
            anchor="nw"
        )

        def actualizar_scrollbar(
            event=None,
            c=canvas,
            contenido=contenido_zona,
            barra=scrollbar
        ):

            contenido.update_idletasks()
            c.update_idletasks()

            ancho_contenido = (
                contenido.winfo_reqwidth()
            )

            ancho_canvas = (
                c.winfo_width()
            )

            c.configure(
                scrollregion=c.bbox("all")
            )

            if ancho_canvas <= 1:
                return

            if ancho_contenido > ancho_canvas:

                if not barra.winfo_ismapped():

                    barra.pack(
                        fill="x"
                    )

            else:

                if barra.winfo_ismapped():

                    barra.pack_forget()

                c.xview_moveto(0)

        contenido_zona.bind(
            "<Configure>",
            actualizar_scrollbar
        )

        canvas.bind(
            "<Configure>",
            actualizar_scrollbar
        )

        actualizar_scrollbars.append(
            actualizar_scrollbar
        )

        frames_zonas[zona] = (
            contenido_zona
        )

    def revisar_scrollbars():

        for actualizar in actualizar_scrollbars:

            actualizar()

    def color_estado(estado):

        if estado == "Disponible":
            return VERDE

        if estado == "Reservada":
            return BEIGE

        return VINO

    todos_los_botones_mesa = []

    # =========================================================
    # MOSTRAR MESAS
    # =========================================================

    def mostrar_mesas():

        actualizar_estados_automaticos()

        for zona_frame in frames_zonas.values():

            for widget in zona_frame.winfo_children():

                widget.destroy()

        todos_los_botones_mesa.clear()

        conexion = conectar()

        if not conexion:
            return

        cursor = None

        try:

            cursor = conexion.cursor()

            cursor.execute(
                """
                SELECT id_mesa,
                       numero_mesa,
                       capacidad,
                       zona,
                       estado
                FROM Mesa
                ORDER BY numero_mesa
                """
            )

            mesas = cursor.fetchall()

            for (
                id_mesa,
                numero,
                capacidad,
                zona,
                estado
            ) in mesas:

                zona_normalizada = (
                    str(zona)
                    .strip()
                    .lower()
                )

                if zona_normalizada == "salón":
                    zona_clave = "salón"

                elif zona_normalizada == "terraza":
                    zona_clave = "terraza"

                elif zona_normalizada == "jardín":
                    zona_clave = "jardín"

                else:
                    continue

                if zona_clave not in frames_zonas:
                    continue

                estado_visual = estado

                cursor.execute(
                    """
                    SELECT fecha,
                           hora
                    FROM Reserva
                    WHERE id_mesa = %s
                      AND estado IN ('Pendiente', 'Confirmada')
                    ORDER BY TIMESTAMP(fecha, hora)
                    """,
                    (id_mesa,)
                )

                reservas = cursor.fetchall()

                for (
                    fecha_reserva,
                    hora_reserva
                ) in reservas:

                    cursor.execute(
                        """
                        SELECT
                            TIMESTAMP(%s, %s) <= NOW()
                            AND TIMESTAMP(%s, %s)
                                + INTERVAL 2 HOUR > NOW(),

                            TIMESTAMP(%s, %s) > NOW()
                            AND TIMESTAMP(%s, %s)
                                <= NOW() + INTERVAL 30 MINUTE
                        """,
                        (
                            fecha_reserva,
                            hora_reserva,
                            fecha_reserva,
                            hora_reserva,
                            fecha_reserva,
                            hora_reserva,
                            fecha_reserva,
                            hora_reserva
                        )
                    )

                    resultado = cursor.fetchone()

                    esta_ocupada = resultado[0]
                    esta_reservada = resultado[1]

                    if esta_ocupada:

                        estado_visual = "Ocupada"
                        break

                    if esta_reservada:

                        estado_visual = "Reservada"

                tarjeta_mesa = tk.Frame(
                    frames_zonas[zona_clave],
                    bg=BLANCO,
                    bd=1,
                    relief="flat",
                    cursor="hand2",
                    width=150,
                    height=72
                )

                tarjeta_mesa.pack_propagate(
                    False
                )

                tarjeta_mesa.pack(
                    side="left",
                    padx=5,
                    pady=4
                )

                tk.Label(
                    tarjeta_mesa,
                    text=f"MESA {numero}",
                    bg=BLANCO,
                    fg=VERDE,
                    font=("Arial", 9, "bold")
                ).pack(
                    pady=(5, 0)
                )

                tk.Label(
                    tarjeta_mesa,
                    text=f"{capacidad} personas",
                    bg=BLANCO,
                    fg=GRIS,
                    font=("Arial", 8)
                ).pack()

                tk.Label(
                    tarjeta_mesa,
                    text=estado_visual.upper(),
                    bg=BLANCO,
                    fg=color_estado(
                        estado_visual
                    ),
                    font=("Arial", 8, "bold")
                ).pack(
                    pady=(1, 4)
                )

                todos_los_botones_mesa.append(
                    tarjeta_mesa
                )

            # =====================================================
            # ZONAS SIN MESAS
            # =====================================================

            for zona, frame in frames_zonas.items():

                if not frame.winfo_children():

                    tk.Label(
                        frame,
                        text="No hay mesas registradas en esta zona.",
                        bg=CREMA,
                        fg=GRIS,
                        font=("Arial", 8)
                    ).pack(
                        pady=6
                    )

        except mysql.connector.Error as error:

            messagebox.showerror(
                "Error",
                f"No se pudieron cargar las mesas.\n\n{error}"
            )

        finally:

            if cursor:
                cursor.close()

            conexion.close()

        # =====================================================
        # REVISAR LAS BARRAS DESPUÉS DE CREAR LAS TARJETAS
        # =====================================================

        ventana.after_idle(
            revisar_scrollbars
        )

    # =========================================================
    # ACTUALIZACIÓN AUTOMÁTICA
    # =========================================================

    def revisar_estados_automaticos():

        actualizar_estados_automaticos()

        filtro_actual = (
            entrada_busqueda_reserva.get().strip()
        )

        mostrar_reservaciones(
            filtro_actual
        )

        mostrar_mesas()
        cargar_mesas()

        ventana.after(
            60000,
            revisar_estados_automaticos
        )

    # =========================================================
    # MENÚ
    # =========================================================

    boton_clientes = crear_boton_menu(
        "CLIENTES",
        lambda: (
            mostrar_clientes(),
            mostrar_panel(panel_clientes),
            actualizar_menu(boton_clientes)
        )
    )

    boton_reservaciones = crear_boton_menu(
        "RESERVACIONES",
        lambda: (
            cargar_clientes_reserva(),
            mostrar_reservaciones(),
            cargar_mesas(),
            mostrar_panel(panel_reservaciones),
            actualizar_menu(boton_reservaciones)
        )
    )

    boton_mesas = crear_boton_menu(
        "MESAS",
        lambda: (
            mostrar_mesas(),
            mostrar_panel(panel_mesas),
            actualizar_menu(boton_mesas)
        )
    )

    # =========================================================
    # CARGA INICIAL
    # =========================================================

    mostrar_clientes()

    cargar_clientes_reserva()

    mostrar_reservaciones()

    mostrar_mesas()

    cargar_mesas()

    mostrar_panel(
        panel_clientes
    )

    actualizar_menu(
        boton_clientes
    )

    ventana.after_idle(
        revisar_scrollbars
    )

    ventana.after(
        60000,
        revisar_estados_automaticos
    )

    ventana.mainloop()


if __name__ == "__main__":
    interfaz_recepcionista()