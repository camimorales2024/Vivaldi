import os
import shutil
import uuid
import calendar
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation
import mysql.connector
from PIL import Image, ImageTk

HOST = "localhost"
USER = "root"
PASSWORD = "sqldecami"
DATABASE = "restaurante_vivaldi"

# =========================================================
# LOGOS
# =========================================================

LOGO_PNG = "vivaldi_sf.png"
LOGO_ICO = "vivaldi.ico"

# =========================================================
# PALETA VIVALDI
# =========================================================

CREMA = "#fbf8f1"
CREMA_CLARO = "#fbf7f1"
BEIGE = "#d9bc8c"
VERDE = "#223d2d"
VERDE_OSCURO = "#12261c"
VINO = "#6b2333"
BLANCO = "#ffffff"
GRIS = "#6f6f6f"
GRIS_CLARO = "#e8e3da"

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
# INTERFAZ DEL ADMINISTRADOR
# =========================================================

def interfaz_administrador():

    ventana = tk.Tk()
    ventana.title("Restaurante Vivaldi | Administrador")
    ventana.geometry("1100x720")
    ventana.configure(bg=CREMA)
    ventana.resizable(False, False)

    # =====================================================
    # ICONO
    # =====================================================

    try:
        ventana.iconbitmap(LOGO_ICO)
    except:
        pass

    # =====================================================
    # CONTENEDOR PRINCIPAL
    # =====================================================

    contenedor = tk.Frame(
        ventana,
        bg=CREMA
    )
    contenedor.pack(
        fill="both",
        expand=True
    )

    # =====================================================
    # SIDEBAR
    # =====================================================

    sidebar = tk.Frame(
        contenedor,
        bg=VERDE_OSCURO,
        width=230
    )
    sidebar.pack(
        side="left",
        fill="y"
    )
    sidebar.pack_propagate(False)

    # =====================================================
    # CONTENIDO DE LA SIDEBAR
    # =====================================================

    contenido_sidebar = tk.Frame(
        sidebar,
        bg=VERDE_OSCURO
    )
    contenido_sidebar.place(
        relx=0.5,
        rely=0.5,
        anchor="center"
    )

    # =====================================================
    # LOGO
    # =====================================================

    try:
        imagen_logo = Image.open(LOGO_PNG)
        imagen_logo = imagen_logo.resize((145, 145))
        logo = ImageTk.PhotoImage(imagen_logo)

        etiqueta_logo = tk.Label(
            contenido_sidebar,
            image=logo,
            bg=VERDE_OSCURO
        )

        etiqueta_logo.image = logo

        etiqueta_logo.pack(
            pady=(0, 12)
        )

    except:

        tk.Label(
            contenido_sidebar,
            text="VIVALDI",
            bg=VERDE_OSCURO,
            fg=BEIGE,
            font=("Georgia", 24, "bold")
        ).pack(
            pady=(0, 30)
        )

    # =====================================================
    # TÍTULO DE LA SIDEBAR
    # =====================================================

    tk.Label(
        contenido_sidebar,
        text="ADMINISTRACIÓN",
        bg=VERDE_OSCURO,
        fg=BEIGE,
        font=("Georgia", 13, "bold")
    ).pack(
        pady=(0, 20)
    )

    # =====================================================
    # MENÚ DE NAVEGACIÓN
    # =====================================================

    menu_navegacion = tk.Frame(
        contenido_sidebar,
        bg=VERDE_OSCURO
    )
    menu_navegacion.pack(
        fill="x",
        padx=15
    )

    # =====================================================
    # ÁREA PRINCIPAL
    # =====================================================

    contenido = tk.Frame(
        contenedor,
        bg=CREMA
    )
    contenido.pack(
        side="left",
        fill="both",
        expand=True
    )

    # =====================================================
    # ÁREA CENTRAL
    # =====================================================

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

    # =====================================================
    # TÍTULO PRINCIPAL
    # =====================================================

    titulo_principal = tk.Label(
        area_central,
        text="Panel de Administración",
        bg=CREMA,
        fg=VERDE_OSCURO,
        font=("Georgia", 23, "bold")
    )
    titulo_principal.pack(
        anchor="w",
        pady=(5, 2)
    )

    subtitulo_principal = tk.Label(
        area_central,
        text="Control general del Restaurante Vivaldi",
        bg=CREMA,
        fg=GRIS,
        font=("Segoe UI", 10)
    )
    subtitulo_principal.pack(
        anchor="w",
        pady=(0, 20)
    )

    # =====================================================
    # CONTENEDOR DE VISTAS
    # =====================================================

    vista_actual = tk.Frame(
        area_central,
        bg=CREMA
    )
    vista_actual.pack(
        fill="both",
        expand=True
    )

    # =====================================================
    # LIMPIAR VISTA
    # =====================================================

    def limpiar_vista():
        for widget in vista_actual.winfo_children():
            widget.destroy()

    # =====================================================
    # BOTONES DEL MENÚ
    # =====================================================

    botones_menu = {}

    def activar_boton(nombre):

        for texto, boton in botones_menu.items():

            boton.config(
                text=f"   {texto}",
                bg=VERDE_OSCURO,
                fg=CREMA_CLARO,
                font=("Arial", 10, "bold")
            )

        if nombre in botones_menu:

            botones_menu[nombre].config(
                text=f"●  {nombre}",
                bg=VERDE,
                fg=BEIGE,
                font=("Arial", 10, "bold")
            )

    # =====================================================
    # CREAR BOTÓN DEL MENÚ
    # =====================================================

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

        botones_menu[texto] = boton

        return boton

    # =====================================================
    # TARJETA DE RESUMEN
    # =====================================================

    def crear_tarjeta(padre, titulo, valor, descripcion):

        tarjeta = tk.Frame(
            padre,
            bg=BLANCO,
            highlightbackground=GRIS_CLARO,
            highlightthickness=1
        )

        tarjeta.pack(
            side="left",
            fill="both",
            expand=True,
            padx=5
        )

        tk.Label(
            tarjeta,
            text=titulo,
            bg=BLANCO,
            fg=GRIS,
            font=("Segoe UI", 9, "bold")
        ).pack(
            anchor="w",
            padx=15,
            pady=(14, 2)
        )

        tk.Label(
            tarjeta,
            text=valor,
            bg=BLANCO,
            fg=VERDE_OSCURO,
            font=("Georgia", 22, "bold")
        ).pack(
            anchor="w",
            padx=15
        )

        tk.Label(
            tarjeta,
            text=descripcion,
            bg=BLANCO,
            fg=GRIS,
            font=("Segoe UI", 8)
        ).pack(
            anchor="w",
            padx=15,
            pady=(0, 14)
        )

        return tarjeta

    # =====================================================
    # DASHBOARD / INICIO
    # =====================================================

    def mostrar_inicio():

        limpiar_vista()
        activar_boton("INICIO")

        # -------------------------------------------------
        # RESUMEN
        # -------------------------------------------------

        marco_resumen = tk.Frame(
            vista_actual,
            bg=CREMA
        )

        marco_resumen.pack(
            fill="x",
            pady=(0, 15)
        )

        # -------------------------------------------------
        # DATOS DE LA BASE
        # -------------------------------------------------

        total_clientes = 0
        total_mesas = 0
        total_platillos = 0
        reservas_hoy = 0

        conexion = conectar()

        if conexion:

            cursor = None

            try:

                cursor = conexion.cursor()

                cursor.execute(
                    "SELECT COUNT(*) FROM Cliente"
                )
                total_clientes = cursor.fetchone()[0]

                cursor.execute(
                    "SELECT COUNT(*) FROM Mesa"
                )
                total_mesas = cursor.fetchone()[0]

                cursor.execute(
                    "SELECT COUNT(*) FROM Platillo"
                )
                total_platillos = cursor.fetchone()[0]

                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM Reserva
                    WHERE fecha = CURDATE()
                    AND estado <> 'Cancelada'
                    """
                )

                reservas_hoy = cursor.fetchone()[0]

            except mysql.connector.Error:

                pass

            finally:

                if cursor:
                    cursor.close()

                conexion.close()

        # -------------------------------------------------
        # TARJETAS
        # -------------------------------------------------

        crear_tarjeta(
            marco_resumen,
            "RESERVACIONES",
            reservas_hoy,
            "Reservaciones para hoy"
        )

        crear_tarjeta(
            marco_resumen,
            "MESAS",
            total_mesas,
            "Mesas registradas"
        )

        crear_tarjeta(
            marco_resumen,
            "CLIENTES",
            total_clientes,
            "Clientes registrados"
        )

        crear_tarjeta(
            marco_resumen,
            "PLATILLOS",
            total_platillos,
            "Platillos registrados"
        )

        # =================================================
        # FILA INFERIOR
        # =================================================

        fila_inferior = tk.Frame(
            vista_actual,
            bg=CREMA
        )

        fila_inferior.pack(
            fill="both",
            expand=True
        )

        # =================================================
        # PRÓXIMAS RESERVACIONES
        # =================================================

        marco_reservaciones = tk.Frame(
            fila_inferior,
            bg=BLANCO,
            highlightbackground=GRIS_CLARO,
            highlightthickness=1
        )

        marco_reservaciones.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 7)
        )

        tk.Label(
            marco_reservaciones,
            text="PRÓXIMAS RESERVACIONES",
            bg=BLANCO,
            fg=VERDE_OSCURO,
            font=("Georgia", 13, "bold")
        ).pack(
            anchor="w",
            padx=18,
            pady=(16, 3)
        )

        tk.Label(
            marco_reservaciones,
            text="Reservaciones pendientes y confirmadas",
            bg=BLANCO,
            fg=GRIS,
            font=("Segoe UI", 8)
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 10)
        )

        conexion = conectar()

        if conexion:

            cursor = None

            try:

                cursor = conexion.cursor()

                cursor.execute(
                    """
                    SELECT
                        r.hora,
                        CONCAT(
                            c.nombre,
                            ' ',
                            c.apellido
                        ) AS cliente,
                        r.cantidad_personas,
                        r.estado
                    FROM Reserva r
                    LEFT JOIN Cliente c
                        ON r.id_cliente = c.id_cliente
                    WHERE r.fecha = CURDATE()
                    AND r.estado <> 'Cancelada'
                    ORDER BY r.hora
                    LIMIT 5
                    """
                )

                reservas = cursor.fetchall()

                if reservas:

                    for hora, cliente, personas, estado in reservas:

                        fila = tk.Frame(
                            marco_reservaciones,
                            bg=CREMA
                        )

                        fila.pack(
                            fill="x",
                            padx=18,
                            pady=3
                        )

                        tk.Label(
                            fila,
                            text=str(hora)[:5],
                            bg=CREMA,
                            fg=VINO,
                            font=("Segoe UI", 9, "bold"),
                            width=8
                        ).pack(
                            side="left"
                        )

                        tk.Label(
                            fila,
                            text=cliente or "Sin cliente",
                            bg=CREMA,
                            fg=VERDE_OSCURO,
                            font=("Segoe UI", 9, "bold")
                        ).pack(
                            side="left"
                        )

                        tk.Label(
                            fila,
                            text=f"{personas} personas",
                            bg=CREMA,
                            fg=GRIS,
                            font=("Segoe UI", 8)
                        ).pack(
                            side="right"
                        )

                else:

                    tk.Label(
                        marco_reservaciones,
                        text="No hay reservaciones para hoy.",
                        bg=BLANCO,
                        fg=GRIS,
                        font=("Segoe UI", 9)
                    ).pack(
                        pady=25
                    )

            except mysql.connector.Error:

                tk.Label(
                    marco_reservaciones,
                    text="No se pudieron cargar las reservaciones.",
                    bg=BLANCO,
                    fg=VINO,
                    font=("Segoe UI", 9)
                ).pack(
                    pady=25
                )

            finally:

                if cursor:
                    cursor.close()

                conexion.close()

        # =================================================
        # ESTADO DE MESAS
        # =================================================

        marco_mesas = tk.Frame(
            fila_inferior,
            bg=BLANCO,
            highlightbackground=GRIS_CLARO,
            highlightthickness=1
        )

        marco_mesas.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(7, 0)
        )

        tk.Label(
            marco_mesas,
            text="ESTADO DE MESAS",
            bg=BLANCO,
            fg=VERDE_OSCURO,
            font=("Georgia", 13, "bold")
        ).pack(
            anchor="w",
            padx=18,
            pady=(16, 3)
        )

        tk.Label(
            marco_mesas,
            text="Situación actual del restaurante",
            bg=BLANCO,
            fg=GRIS,
            font=("Segoe UI", 8)
        ).pack(
            anchor="w",
            padx=18,
            pady=(0, 12)
        )

        conexion = conectar()

        if conexion:

            cursor = None

            try:

                cursor = conexion.cursor()

                cursor.execute(
                    """
                    SELECT numero_mesa, estado
                    FROM Mesa
                    ORDER BY numero_mesa
                    """
                )

                mesas = cursor.fetchall()

                contenedor_mesas = tk.Frame(
                    marco_mesas,
                    bg=BLANCO
                )

                contenedor_mesas.pack(
                    padx=18,
                    fill="both",
                    expand=True
                )

                for indice, (numero, estado) in enumerate(mesas):

                    if estado == "Disponible":
                        color = VERDE

                    elif estado == "Ocupada":
                        color = VINO

                    else:
                        color = BEIGE

                    mesa = tk.Frame(
                        contenedor_mesas,
                        bg=CREMA,
                        highlightbackground=GRIS_CLARO,
                        highlightthickness=1,
                        width=75,
                        height=55
                    )

                    mesa.grid(
                        row=indice // 4,
                        column=indice % 4,
                        padx=4,
                        pady=4
                    )

                    mesa.grid_propagate(False)

                    tk.Label(
                        mesa,
                        text=f"● Mesa {numero}",
                        bg=CREMA,
                        fg=color,
                        font=("Segoe UI", 8, "bold")
                    ).place(
                        relx=0.5,
                        rely=0.5,
                        anchor="center"
                    )

            except mysql.connector.Error:

                tk.Label(
                    marco_mesas,
                    text="No se pudieron cargar las mesas.",
                    bg=BLANCO,
                    fg=VINO,
                    font=("Segoe UI", 9)
                ).pack(
                    pady=25
                )

            finally:

                if cursor:
                    cursor.close()

                conexion.close()

    # =====================================================
    # VISTA DE CLIENTES
    # =====================================================

    def mostrar_clientes():

        limpiar_vista()
        activar_boton("CLIENTES")

        # =================================================
        # ENCABEZADO
        # =================================================

        encabezado = tk.Frame(
            vista_actual,
            bg=CREMA
        )

        encabezado.pack(
            fill="x",
            pady=(10, 15)
        )

        tk.Label(
            encabezado,
            text="Clientes",
            bg=CREMA,
            fg=VERDE_OSCURO,
            font=("Georgia", 22, "bold")
        ).pack(
            side="left"
        )

        tk.Label(
            encabezado,
            text="Administración de clientes registrados",
            bg=CREMA,
            fg=GRIS,
            font=("Segoe UI", 9)
        ).pack(
            side="left",
            padx=15,
            pady=(8, 0)
        )

        # =================================================
        # BARRA DE ACCIONES
        # =================================================

        barra_acciones = tk.Frame(
            vista_actual,
            bg=CREMA
        )

        barra_acciones.pack(
            fill="x",
            pady=(0, 12)
        )

        tk.Label(
            barra_acciones,
            text="Buscar:",
            bg=CREMA,
            fg=VERDE_OSCURO,
            font=("Segoe UI", 9, "bold")
        ).pack(
            side="left"
        )

        entrada_busqueda = tk.Entry(
            barra_acciones,
            font=("Segoe UI", 10),
            bg=BLANCO,
            fg=VINO,
            relief="flat",
            highlightbackground=GRIS_CLARO,
            highlightthickness=1
        )

        entrada_busqueda.pack(
            side="left",
            padx=(8, 10),
            ipady=6,
            fill="x",
            expand=True
        )

        # =================================================
        # CONTENEDOR DE TABLA
        # =================================================

        marco_tabla = tk.Frame(
            vista_actual,
            bg=BLANCO,
            highlightbackground=GRIS_CLARO,
            highlightthickness=1
        )

        marco_tabla.pack(
            fill="both",
            expand=True
        )

        # =================================================
        # ESTILO DE CLIENTES
        # =================================================

        estilo = ttk.Style()

        estilo.configure(
            "Clientes.Treeview",
            background=BLANCO,
            foreground=VERDE_OSCURO,
            rowheight=34,
            fieldbackground=BLANCO,
            font=("Segoe UI", 9)
        )

        estilo.configure(
            "Clientes.Treeview.Heading",
            background=VERDE,
            foreground=VINO,
            font=("Segoe UI", 9, "bold")
        )

        estilo.map(
            "Clientes.Treeview",
            background=[
                ("selected", BEIGE)
            ],
            foreground=[
                ("selected", VERDE_OSCURO)
            ]
        )

        # =================================================
        # TABLA DE CLIENTES
        # =================================================

        columnas = (
            "id",
            "nombre",
            "apellido",
            "telefono",
            "correo",
            "fecha"
        )

        tabla = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings",
            style="Clientes.Treeview"
        )

        tabla.heading(
            "id",
            text="ID"
        )

        tabla.heading(
            "nombre",
            text="Nombre"
        )

        tabla.heading(
            "apellido",
            text="Apellido"
        )

        tabla.heading(
            "telefono",
            text="Teléfono"
        )

        tabla.heading(
            "correo",
            text="Correo"
        )

        tabla.heading(
            "fecha",
            text="Fecha de registro"
        )

        tabla.column(
            "id",
            width=55,
            anchor="center",
            stretch=False
        )

        tabla.column(
            "nombre",
            width=130,
            anchor="center",
            stretch=False
        )

        tabla.column(
            "apellido",
            width=130,
            anchor="center",
            stretch=False
        )

        tabla.column(
            "telefono",
            width=110,
            anchor="center",
            stretch=False
        )

        tabla.column(
            "correo",
            width=210,
            anchor="center",
            stretch=False
        )

        tabla.column(
            "fecha",
            width=130,
            anchor="center",
            stretch=False
        )

        # =================================================
        # BLOQUEAR REDIMENSIONAMIENTO
        # =================================================

        def bloquear_redimensionamiento_clientes(event):

            region = tabla.identify_region(
                event.x,
                event.y
            )

            if region == "separator":
                return "break"

        tabla.bind(
            "<Button-1>",
            bloquear_redimensionamiento_clientes
        )

        tabla.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # =================================================
        # SCROLLBAR
        # =================================================

        scroll = ttk.Scrollbar(
            marco_tabla,
            orient="vertical",
            command=tabla.yview
        )

        scroll.pack(
            side="right",
            fill="y",
            pady=10,
            padx=(0, 10)
        )

        tabla.configure(
            yscrollcommand=scroll.set
        )

        def desplazar_clientes(event):

            tabla.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        tabla.bind(
            "<MouseWheel>",
            desplazar_clientes
        )

        # =================================================
        # CARGAR CLIENTES
        # =================================================

        def cargar_clientes():

            for elemento in tabla.get_children():
                tabla.delete(elemento)

            conexion = conectar()

            if not conexion:
                return

            cursor = None

            try:

                cursor = conexion.cursor()

                texto = entrada_busqueda.get().strip()

                consulta = """
                    SELECT
                        id_cliente,
                        nombre,
                        apellido,
                        telefono,
                        correo_electronico,
                        fecha_registro
                    FROM Cliente
                """

                parametros = ()

                if texto:

                    consulta += """
                        WHERE
                            nombre LIKE %s
                            OR apellido LIKE %s
                            OR telefono LIKE %s
                            OR correo_electronico LIKE %s
                    """

                    busqueda = f"%{texto}%"

                    parametros = (
                        busqueda,
                        busqueda,
                        busqueda,
                        busqueda
                    )

                consulta += """
                    ORDER BY nombre, apellido
                """

                cursor.execute(
                    consulta,
                    parametros
                )

                clientes = cursor.fetchall()

                for cliente in clientes:

                    tabla.insert(
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

        # =================================================
        # FORMULARIO CLIENTE
        # =================================================

        def abrir_formulario_cliente(cliente=None):

            formulario = tk.Toplevel(ventana)

            formulario.title(
                "Nuevo cliente"
                if cliente is None
                else "Editar cliente"
            )

            formulario.geometry(
                "430x430"
            )

            formulario.configure(
                bg=CREMA
            )

            formulario.resizable(
                False,
                False
            )

            try:
                formulario.iconbitmap(
                    LOGO_ICO
                )
            except:
                pass

            formulario.transient(
                ventana
            )

            formulario.grab_set()

            # -------------------------------------------------
            # TÍTULO
            # -------------------------------------------------

            tk.Label(
                formulario,
                text=(
                    "Nuevo cliente"
                    if cliente is None
                    else "Editar cliente"
                ),
                bg=CREMA,
                fg=VERDE_OSCURO,
                font=("Georgia", 19, "bold")
            ).pack(
                pady=(25, 5)
            )

            tk.Label(
                formulario,
                text="Información del cliente",
                bg=CREMA,
                fg=GRIS,
                font=("Segoe UI", 9)
            ).pack(
                pady=(0, 20)
            )

            formulario_campos = tk.Frame(
                formulario,
                bg=CREMA
            )

            formulario_campos.pack(
                padx=40,
                fill="x"
            )

            # -------------------------------------------------
            # NOMBRE
            # -------------------------------------------------

            tk.Label(
                formulario_campos,
                text="Nombre",
                bg=CREMA,
                fg=VERDE_OSCURO,
                font=("Segoe UI", 9, "bold")
            ).pack(
                anchor="w"
            )

            entrada_nombre = tk.Entry(
                formulario_campos,
                font=("Segoe UI", 10),
                bg=BLANCO,
                fg=VERDE_OSCURO,
                relief="flat",
                highlightbackground=GRIS_CLARO,
                highlightthickness=1
            )

            entrada_nombre.pack(
                fill="x",
                ipady=6,
                pady=(3, 10)
            )

            # -------------------------------------------------
            # APELLIDO
            # -------------------------------------------------

            tk.Label(
                formulario_campos,
                text="Apellido",
                bg=CREMA,
                fg=VERDE_OSCURO,
                font=("Segoe UI", 9, "bold")
            ).pack(
                anchor="w"
            )

            entrada_apellido = tk.Entry(
                formulario_campos,
                font=("Segoe UI", 10),
                bg=BLANCO,
                fg=VERDE_OSCURO,
                relief="flat",
                highlightbackground=GRIS_CLARO,
                highlightthickness=1
            )

            entrada_apellido.pack(
                fill="x",
                ipady=6,
                pady=(3, 10)
            )

            # -------------------------------------------------
            # TELÉFONO
            # -------------------------------------------------

            tk.Label(
                formulario_campos,
                text="Teléfono",
                bg=CREMA,
                fg=VERDE_OSCURO,
                font=("Segoe UI", 9, "bold")
            ).pack(
                anchor="w"
            )

            entrada_telefono = tk.Entry(
                formulario_campos,
                font=("Segoe UI", 10),
                bg=BLANCO,
                fg=VERDE_OSCURO,
                relief="flat",
                highlightbackground=GRIS_CLARO,
                highlightthickness=1
            )

            entrada_telefono.pack(
                fill="x",
                ipady=6,
                pady=(3, 10)
            )

            # -------------------------------------------------
            # CORREO
            # -------------------------------------------------

            tk.Label(
                formulario_campos,
                text="Correo electrónico",
                bg=CREMA,
                fg=VERDE_OSCURO,
                font=("Segoe UI", 9, "bold")
            ).pack(
                anchor="w"
            )

            entrada_correo = tk.Entry(
                formulario_campos,
                font=("Segoe UI", 10),
                bg=BLANCO,
                fg=VERDE_OSCURO,
                relief="flat",
                highlightbackground=GRIS_CLARO,
                highlightthickness=1
            )

            entrada_correo.pack(
                fill="x",
                ipady=6,
                pady=(3, 10)
            )

            # -------------------------------------------------
            # DATOS PARA EDICIÓN
            # -------------------------------------------------

            if cliente:

                entrada_nombre.insert(
                    0,
                    cliente[1]
                )

                entrada_apellido.insert(
                    0,
                    cliente[2]
                )

                entrada_telefono.insert(
                    0,
                    cliente[3] or ""
                )

                entrada_correo.insert(
                    0,
                    cliente[4] or ""
                )

            # -------------------------------------------------
            # GUARDAR CLIENTE
            # -------------------------------------------------

            def guardar_cliente():

                nombre = entrada_nombre.get().strip()
                apellido = entrada_apellido.get().strip()
                telefono = entrada_telefono.get().strip()
                correo = entrada_correo.get().strip()

                if not nombre or not apellido:

                    messagebox.showwarning(
                        "Datos incompletos",
                        "El nombre y el apellido son obligatorios.",
                        parent=formulario
                    )

                    return

                conexion = conectar()

                if not conexion:
                    return

                cursor = None

                try:

                    cursor = conexion.cursor()

                    if cliente is None:

                        cursor.execute(
                            """
                            INSERT INTO Cliente (
                                nombre,
                                apellido,
                                telefono,
                                correo_electronico
                            )
                            VALUES (
                                %s,
                                %s,
                                %s,
                                %s
                            )
                            """,
                            (
                                nombre,
                                apellido,
                                telefono or None,
                                correo or None
                            )
                        )

                        mensaje = (
                            "Cliente registrado correctamente."
                        )

                    else:

                        cursor.execute(
                            """
                            UPDATE Cliente
                            SET
                                nombre = %s,
                                apellido = %s,
                                telefono = %s,
                                correo_electronico = %s
                            WHERE id_cliente = %s
                            """,
                            (
                                nombre,
                                apellido,
                                telefono or None,
                                correo or None,
                                cliente[0]
                            )
                        )

                        mensaje = (
                            "Cliente actualizado correctamente."
                        )

                    conexion.commit()

                    formulario.destroy()
                    cargar_clientes()

                    messagebox.showinfo(
                        "Operación realizada",
                        mensaje
                    )

                except mysql.connector.Error as error:

                    conexion.rollback()

                    messagebox.showerror(
                        "Error",
                        f"No se pudo guardar el cliente.\n\n{error}",
                        parent=formulario
                    )

                finally:

                    if cursor:
                        cursor.close()

                    conexion.close()

            # -------------------------------------------------
            # BOTONES DEL FORMULARIO
            # -------------------------------------------------

            tk.Button(
                formulario,
                text="Guardar",
                command=guardar_cliente,
                bg=VERDE,
                fg=BEIGE,
                activebackground=VERDE_OSCURO,
                activeforeground=BEIGE,
                relief="flat",
                bd=0,
                font=("Segoe UI", 9, "bold"),
                padx=25,
                pady=9,
                cursor="hand2"
            ).pack(
                side="left",
                padx=(40, 5),
                pady=15
            )

            tk.Button(
                formulario,
                text="Cancelar",
                command=formulario.destroy,
                bg=GRIS_CLARO,
                fg=VERDE_OSCURO,
                activebackground=GRIS_CLARO,
                activeforeground=VERDE_OSCURO,
                relief="flat",
                bd=0,
                font=("Segoe UI", 9, "bold"),
                padx=25,
                pady=9,
                cursor="hand2"
            ).pack(
                side="left",
                padx=5,
                pady=15
            )

        # =================================================
        # EDITAR CLIENTE
        # =================================================

        def editar_cliente():

            seleccion = tabla.selection()

            if not seleccion:

                messagebox.showwarning(
                    "Seleccionar cliente",
                    "Selecciona un cliente de la tabla para editarlo."
                )

                return

            datos = tabla.item(
                seleccion[0],
                "values"
            )

            abrir_formulario_cliente(
                datos
            )

        # =================================================
        # ELIMINAR CLIENTE
        # =================================================

        def eliminar_cliente():

            seleccion = tabla.selection()

            if not seleccion:

                messagebox.showwarning(
                    "Seleccionar cliente",
                    "Selecciona un cliente de la tabla para eliminarlo."
                )

                return

            datos = tabla.item(
                seleccion[0],
                "values"
            )

            id_cliente = datos[0]

            confirmar = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Deseas eliminar al cliente\n\n"
                f"{datos[1]} {datos[2]}?"
            )

            if not confirmar:
                return

            conexion = conectar()

            if not conexion:
                return

            cursor = None

            try:

                cursor = conexion.cursor()

                cursor.execute(
                    """
                    DELETE FROM Cliente
                    WHERE id_cliente = %s
                    """,
                    (id_cliente,)
                )

                conexion.commit()

                cargar_clientes()

                messagebox.showinfo(
                    "Cliente eliminado",
                    "El cliente fue eliminado correctamente."
                )

            except mysql.connector.Error:

                conexion.rollback()

                messagebox.showerror(
                    "No se puede eliminar",
                    "No se pudo eliminar este cliente.\n\n"
                    "Es posible que tenga reservaciones u órdenes "
                    "relacionadas con él."
                )

            finally:

                if cursor:
                    cursor.close()

                conexion.close()

        # =================================================
        # BÚSQUEDA AUTOMÁTICA
        # =================================================

        entrada_busqueda.bind(
            "<KeyRelease>",
            lambda event: cargar_clientes()
        )

        # =================================================
        # BOTONES INFERIORES
        # =================================================

        barra_botones = tk.Frame(
            vista_actual,
            bg=CREMA
        )

        barra_botones.pack(
            fill="x",
            pady=(12, 0)
        )

        tk.Button(
            barra_botones,
            text="+  Nuevo cliente",
            command=abrir_formulario_cliente,
            bg=VERDE,
            fg=BEIGE,
            activebackground=VERDE_OSCURO,
            activeforeground=BEIGE,
            relief="flat",
            bd=0,
            font=("Segoe UI", 9, "bold"),
            padx=16,
            pady=9,
            cursor="hand2"
        ).pack(
            side="left"
        )

        tk.Button(
            barra_botones,
            text="Editar",
            command=editar_cliente,
            bg=BEIGE,
            fg=VERDE_OSCURO,
            activebackground=BEIGE,
            activeforeground=VERDE_OSCURO,
            relief="flat",
            bd=0,
            font=("Segoe UI", 9, "bold"),
            padx=18,
            pady=9,
            cursor="hand2"
        ).pack(
            side="left",
            padx=8
        )

        tk.Button(
            barra_botones,
            text="Eliminar",
            command=eliminar_cliente,
            bg=VINO,
            fg=BLANCO,
            activebackground=VINO,
            activeforeground=BLANCO,
            relief="flat",
            bd=0,
            font=("Segoe UI", 9, "bold"),
            padx=18,
            pady=9,
            cursor="hand2"
        ).pack(
            side="left"
        )

        # =================================================
        # CARGAR CLIENTES AL ENTRAR
        # =================================================

        cargar_clientes()

    # =====================================================
    # VISTA DE RESERVACIONES
    # =====================================================

    def mostrar_reservaciones():

        limpiar_vista()
        activar_boton("RESERVACIONES")

        # =================================================
        # ENCABEZADO
        # =================================================

        encabezado = tk.Frame(
            vista_actual,
            bg=CREMA
        )

        encabezado.pack(
            fill="x",
            pady=(10, 15)
        )

        tk.Label(
            encabezado,
            text="Reservaciones",
            bg=CREMA,
            fg=VERDE_OSCURO,
            font=("Georgia", 22, "bold")
        ).pack(
            side="left"
        )

        tk.Label(
            encabezado,
            text="Administración de reservaciones del restaurante",
            bg=CREMA,
            fg=GRIS,
            font=("Segoe UI", 9)
        ).pack(
            side="left",
            padx=15,
            pady=(8, 0)
        )

        # =================================================
        # BARRA DE BÚSQUEDA
        # =================================================

        barra_busqueda = tk.Frame(
            vista_actual,
            bg=CREMA
        )

        barra_busqueda.pack(
            fill="x",
            pady=(0, 12)
        )

        tk.Label(
            barra_busqueda,
            text="Buscar:",
            bg=CREMA,
            fg=VERDE_OSCURO,
            font=("Segoe UI", 9, "bold")
        ).pack(
            side="left"
        )

        entrada_busqueda = tk.Entry(
            barra_busqueda,
            font=("Segoe UI", 10),
            bg=BLANCO,
            fg=VERDE_OSCURO,
            relief="flat",
            highlightbackground=GRIS_CLARO,
            highlightthickness=1
        )

        entrada_busqueda.pack(
            side="left",
            padx=(8, 10),
            ipady=6,
            fill="x",
            expand=True
        )

        # =================================================
        # CONTENEDOR DE TABLA
        # =================================================

        marco_tabla = tk.Frame(
            vista_actual,
            bg=BLANCO,
            highlightbackground=GRIS_CLARO,
            highlightthickness=1
        )

        marco_tabla.pack(
            fill="both",
            expand=True
        )

        # =================================================
        # ESTILO DE RESERVACIONES
        # =================================================

        estilo_reservaciones = ttk.Style()

        estilo_reservaciones.configure(
            "Reservaciones.Treeview",
            background=BLANCO,
            foreground=VERDE_OSCURO,
            rowheight=34,
            fieldbackground=BLANCO,
            font=("Segoe UI", 9)
        )

        estilo_reservaciones.configure(
            "Reservaciones.Treeview.Heading",
            background=VERDE,
            foreground=VINO,
            font=("Segoe UI", 9, "bold")
        )

        estilo_reservaciones.map(
            "Reservaciones.Treeview",
            background=[
                ("selected", BEIGE)
            ],
            foreground=[
                ("selected", VERDE_OSCURO)
            ]
        )

        # =================================================
        # TABLA
        # =================================================

        columnas = (
            "id",
            "cliente",
            "fecha",
            "hora",
            "personas",
            "mesa",
            "estado"
        )

        tabla = ttk.Treeview(
            marco_tabla,
            columns=columnas,
            show="headings",
            style="Reservaciones.Treeview"
        )

        tabla.heading(
            "id",
            text="ID"
        )

        tabla.heading(
            "cliente",
            text="Cliente"
        )

        tabla.heading(
            "fecha",
            text="Fecha"
        )

        tabla.heading(
            "hora",
            text="Hora"
        )

        tabla.heading(
            "personas",
            text="Personas"
        )

        tabla.heading(
            "mesa",
            text="Mesa"
        )

        tabla.heading(
            "estado",
            text="Estado"
        )

        tabla.column(
            "id",
            width=50,
            anchor="center",
            stretch=False
        )

        tabla.column(
            "cliente",
            width=180,
            anchor="center",
            stretch=False
        )

        tabla.column(
            "fecha",
            width=100,
            anchor="center",
            stretch=False
        )

        tabla.column(
            "hora",
            width=80,
            anchor="center",
            stretch=False
        )

        tabla.column(
            "personas",
            width=90,
            anchor="center",
            stretch=False
        )

        tabla.column(
            "mesa",
            width=80,
            anchor="center",
            stretch=False
        )

        tabla.column(
            "estado",
            width=120,
            anchor="center",
            stretch=False
        )

        # =================================================
        # BLOQUEAR REDIMENSIONAMIENTO
        # =================================================

        def bloquear_redimensionamiento_reservaciones(event):

            region = tabla.identify_region(
                event.x,
                event.y
            )

            if region == "separator":
                return "break"

        tabla.bind(
            "<Button-1>",
            bloquear_redimensionamiento_reservaciones
        )

        tabla.pack(
            side="left",
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        # =================================================
        # SCROLLBAR
        # =================================================

        scroll = ttk.Scrollbar(
            marco_tabla,
            orient="vertical",
            command=tabla.yview
        )

        scroll.pack(
            side="right",
            fill="y",
            pady=10,
            padx=(0, 10)
        )

        tabla.configure(
            yscrollcommand=scroll.set
        )

        # =================================================
        # CARGAR RESERVACIONES
        # =================================================

        def cargar_reservaciones():

            for elemento in tabla.get_children():
                tabla.delete(elemento)

            conexion = conectar()

            if not conexion:
                return

            cursor = None

            try:

                cursor = conexion.cursor()

                texto = entrada_busqueda.get().strip()

                consulta = """
                    SELECT
                        r.id_reserva,
                        CONCAT(
                            c.nombre,
                            ' ',
                            c.apellido
                        ) AS cliente,
                        r.fecha,
                        r.hora,
                        r.cantidad_personas,
                        m.numero_mesa,
                        r.estado
                    FROM Reserva r
                    INNER JOIN Cliente c
                        ON r.id_cliente = c.id_cliente
                    INNER JOIN Mesa m
                        ON r.id_mesa = m.id_mesa
                """

                parametros = ()

                if texto:

                    consulta += """
                        WHERE
                            CONCAT(
                                c.nombre,
                                ' ',
                                c.apellido
                            ) LIKE %s
                            OR r.estado LIKE %s
                            OR CAST(
                                r.fecha AS CHAR
                            ) LIKE %s
                    """

                    buscar = f"%{texto}%"

                    parametros = (
                        buscar,
                        buscar,
                        buscar
                    )

                consulta += """
                    ORDER BY
                        r.fecha ASC,
                        r.hora ASC,
                        r.id_reserva ASC
                """

                cursor.execute(
                    consulta,
                    parametros
                )

                reservaciones = cursor.fetchall()

                for reserva in reservaciones:

                    tabla.insert(
                        "",
                        "end",
                        values=(
                            reserva[0],
                            reserva[1],
                            reserva[2],
                            reserva[3],
                            reserva[4],
                            reserva[5],
                            reserva[6]
                        )
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

        # =================================================
        # BARRA DE BOTONES
        # =================================================

        barra_botones = tk.Frame(
            vista_actual,
            bg=CREMA
        )

        barra_botones.pack(
            fill="x",
            pady=(12, 0)
        )

        # -------------------------------------------------
        # NUEVA RESERVACIÓN
        # -------------------------------------------------

        tk.Button(
            barra_botones,
            text="+  Nueva reservación",
            bg=VERDE,
            fg=BEIGE,
            activebackground=VERDE_OSCURO,
            activeforeground=BEIGE,
            relief="flat",
            bd=0,
            font=("Segoe UI", 9, "bold"),
            padx=16,
            pady=9,
            cursor="hand2"
        ).pack(
            side="left"
        )

        # -------------------------------------------------
        # VER DETALLES
        # -------------------------------------------------

        tk.Button(
            barra_botones,
            text="Ver detalles",
            bg=BEIGE,
            fg=VERDE_OSCURO,
            activebackground=BEIGE,
            activeforeground=VERDE_OSCURO,
            relief="flat",
            bd=0,
            font=("Segoe UI", 9, "bold"),
            padx=18,
            pady=9,
            cursor="hand2"
        ).pack(
            side="left",
            padx=8
        )

        # -------------------------------------------------
        # ELIMINAR
        # -------------------------------------------------

        tk.Button(
            barra_botones,
            text="Eliminar",
            bg=VINO,
            fg=BLANCO,
            activebackground=VINO,
            activeforeground=BLANCO,
            relief="flat",
            bd=0,
            font=("Segoe UI", 9, "bold"),
            padx=18,
            pady=9,
            cursor="hand2"
        ).pack(
            side="left"
        )

        # -------------------------------------------------
        # ACTUALIZAR
        # -------------------------------------------------

        tk.Button(
            barra_botones,
            text="Actualizar",
            command=cargar_reservaciones,
            bg=BLANCO,
            fg=VERDE_OSCURO,
            activebackground=CREMA_CLARO,
            activeforeground=VERDE_OSCURO,
            relief="flat",
            bd=0,
            font=("Segoe UI", 9, "bold"),
            padx=18,
            pady=9,
            cursor="hand2"
        ).pack(
            side="right"
        )

        # =================================================
        # BÚSQUEDA AUTOMÁTICA
        # =================================================

        entrada_busqueda.bind(
            "<KeyRelease>",
            lambda event: cargar_reservaciones()
        )

        # =================================================
        # CARGAR DATOS
        # =================================================

        cargar_reservaciones()

    # =====================================================
    # VISTA DE MESAS
    # =====================================================

    def mostrar_mesas():

        limpiar_vista()
        activar_boton("MESAS")

        # =================================================
        # ENCABEZADO
        # =================================================

        encabezado = tk.Frame(
            vista_actual,
            bg=CREMA
        )

        encabezado.pack(
            fill="x",
            pady=(10, 15)
        )

        tk.Label(
            encabezado,
            text="Mesas",
            bg=CREMA,
            fg=VERDE_OSCURO,
            font=("Georgia", 22, "bold")
        ).pack(
            side="left"
        )

        tk.Label(
            encabezado,
            text="Administración y estado de las mesas",
            bg=CREMA,
            fg=GRIS,
            font=("Segoe UI", 9)
        ).pack(
            side="left",
            padx=15,
            pady=(8, 0)
        )

        # =================================================
        # BARRA DE BÚSQUEDA
        # =================================================

        barra_busqueda = tk.Frame(
            vista_actual,
            bg=CREMA
        )

        barra_busqueda.pack(
            fill="x",
            pady=(0, 12)
        )

        tk.Label(
            barra_busqueda,
            text="Buscar mesa:",
            bg=CREMA,
            fg=VERDE_OSCURO,
            font=("Segoe UI", 9, "bold")
        ).pack(
            side="left"
        )

        entrada_busqueda = tk.Entry(
            barra_busqueda,
            font=("Segoe UI", 10),
            bg=BLANCO,
            fg=VERDE_OSCURO,
            relief="flat",
            highlightbackground=GRIS_CLARO,
            highlightthickness=1
        )

        entrada_busqueda.pack(
            side="left",
            padx=(8, 10),
            ipady=6,
            fill="x",
            expand=True
        )

        # =================================================
        # CONTENEDOR DE MESAS
        # =================================================

        marco_mesas = tk.Frame(
            vista_actual,
            bg=BLANCO,
            highlightbackground=GRIS_CLARO,
            highlightthickness=1
        )

        marco_mesas.pack(
            fill="both",
            expand=True
        )

        # =================================================
        # ÁREA DESPLAZABLE
        # =================================================

        canvas_mesas = tk.Canvas(
            marco_mesas,
            bg=BLANCO,
            highlightthickness=0
        )

        scrollbar_mesas = ttk.Scrollbar(
            marco_mesas,
            orient="vertical",
            command=canvas_mesas.yview
        )

        canvas_mesas.configure(
            yscrollcommand=scrollbar_mesas.set
        )

        scrollbar_mesas.pack(
            side="right",
            fill="y"
        )

        canvas_mesas.pack(
            side="left",
            fill="both",
            expand=True
        )

        def desplazar_mesas(event):

            canvas_mesas.yview_scroll(
                int(-1 * (event.delta / 120)),
                "units"
            )

        canvas_mesas.bind(
            "<MouseWheel>",
            desplazar_mesas
        )

        # =================================================
        # CONTENEDOR INTERNO
        # =================================================

        contenedor_mesas = tk.Frame(
            canvas_mesas,
            bg=BLANCO
        )

        ventana_mesas = canvas_mesas.create_window(
            (0, 0),
            window=contenedor_mesas,
            anchor="nw"
        )

        # =================================================
        # AJUSTAR EL ÁREA DEL SCROLL
        # =================================================

        def actualizar_scroll(event=None):

            canvas_mesas.configure(
                scrollregion=canvas_mesas.bbox("all")
            )

        contenedor_mesas.bind(
            "<Configure>",
            actualizar_scroll
        )

        # =================================================
        # HACER QUE EL CONTENEDOR OCUPE TODO EL ANCHO
        # =================================================

        def ajustar_ancho(event):

            canvas_mesas.itemconfig(
                ventana_mesas,
                width=event.width
            )

        canvas_mesas.bind(
            "<Configure>",
            ajustar_ancho
        )

        # =================================================
        # CARGAR MESAS
        # =================================================

        def cargar_mesas():

            for widget in contenedor_mesas.winfo_children():
                widget.destroy()

            conexion = conectar()

            if not conexion:
                return

            cursor = None

            try:

                cursor = conexion.cursor()

                texto = entrada_busqueda.get().strip()

                consulta = """
                    SELECT
                        id_mesa,
                        numero_mesa,
                        capacidad,
                        zona,
                        estado
                    FROM Mesa
                """

                parametros = ()

                if texto:

                    consulta += """
                        WHERE
                            CAST(numero_mesa AS CHAR) LIKE %s
                            OR zona LIKE %s
                            OR estado LIKE %s
                    """

                    buscar = f"%{texto}%"

                    parametros = (
                        buscar,
                        buscar,
                        buscar
                    )

                consulta += """
                    ORDER BY numero_mesa
                """

                cursor.execute(
                    consulta,
                    parametros
                )

                mesas = cursor.fetchall()

                if not mesas:

                    tk.Label(
                        contenedor_mesas,
                        text="No se encontraron mesas.",
                        bg=BLANCO,
                        fg=GRIS,
                        font=("Segoe UI", 10)
                    ).pack(
                        pady=40
                    )

                    return

                # -------------------------------------------------
                # CREAR TARJETAS
                # -------------------------------------------------

                for indice, mesa in enumerate(mesas):

                    id_mesa = mesa[0]
                    numero = mesa[1]
                    capacidad = mesa[2]
                    zona = mesa[3]
                    estado = mesa[4]

                    # -------------------------------------------------
                    # COLOR SEGÚN ESTADO
                    # -------------------------------------------------

                    if estado == "Disponible":

                        color_estado = VERDE

                    elif estado == "Ocupada":

                        color_estado = VINO

                    else:

                        color_estado = BEIGE

                    # -------------------------------------------------
                    # TARJETA
                    # -------------------------------------------------

                    tarjeta = tk.Frame(
                        contenedor_mesas,
                        bg=CREMA,
                        highlightbackground=GRIS_CLARO,
                        highlightthickness=3,
                        width=180,
                        height=145
                    )

                    tarjeta.grid(
                        row=indice // 4,
                        column=indice % 4,
                        padx=8,
                        pady=8,
                        sticky="nsew"
                    )

                    tarjeta.grid_propagate(False)

                    # -------------------------------------------------
                    # NÚMERO DE MESA
                    # -------------------------------------------------

                    tk.Label(
                        tarjeta,
                        text=f"MESA {numero}",
                        bg=CREMA,
                        fg=VERDE_OSCURO,
                        font=("Georgia", 14, "bold")
                    ).pack(
                        pady=(15, 3)
                    )

                    # -------------------------------------------------
                    # CAPACIDAD
                    # -------------------------------------------------

                    tk.Label(
                        tarjeta,
                        text=f"Capacidad: {capacidad} personas",
                        bg=CREMA,
                        fg=GRIS,
                        font=("Segoe UI", 9)
                    ).pack()

                    # -------------------------------------------------
                    # ZONA
                    # -------------------------------------------------

                    tk.Label(
                        tarjeta,
                        text=f"Zona: {zona}",
                        bg=CREMA,
                        fg=GRIS,
                        font=("Segoe UI", 9)
                    ).pack(
                        pady=(3, 5)
                    )

                    # -------------------------------------------------
                    # ESTADO
                    # -------------------------------------------------

                    tk.Label(
                        tarjeta,
                        text=f"● {estado.upper()}",
                        bg=CREMA,
                        fg=color_estado,
                        font=("Segoe UI", 9, "bold")
                    ).pack()

                    # PERMITIR SELECCIONAR LA TARJETA

                    tarjeta.bind(
                        "<Button-1>",
                        lambda event,
                        datos=mesa,
                        marco=tarjeta:
                        seleccionar_mesa(datos, marco)
                    )

                    for elemento in tarjeta.winfo_children():

                        elemento.bind(
                            "<Button-1>",
                            lambda event,
                            datos=mesa,
                            marco=tarjeta:
                            seleccionar_mesa(datos, marco)
                        )

                # -------------------------------------------------
                # HACER LAS COLUMNAS UNIFORMES
                # -------------------------------------------------

                for columna in range(4):

                    contenedor_mesas.grid_columnconfigure(
                        columna,
                        weight=1
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

        # =================================================
        # FORMULARIO DE MESA
        # =================================================

        def abrir_formulario_mesa(mesa=None):

            formulario = tk.Toplevel(
                ventana
            )

            formulario.title(
                "Nueva mesa"
                if mesa is None
                else "Editar mesa"
            )

            formulario.geometry(
                "420x400"
            )

            formulario.configure(
                bg=CREMA
            )

            formulario.resizable(
                False,
                False
            )

            try:
                formulario.iconbitmap(
                    LOGO_ICO
                )
            except:
                pass

            formulario.transient(
                ventana
            )

            formulario.grab_set()

            # -------------------------------------------------
            # TÍTULO
            # -------------------------------------------------

            tk.Label(
                formulario,
                text=(
                    "Nueva mesa"
                    if mesa is None
                    else "Editar mesa"
                ),
                bg=CREMA,
                fg=VERDE_OSCURO,
                font=("Georgia", 19, "bold")
            ).pack(
                pady=(25, 5)
            )

            tk.Label(
                formulario,
                text="Información de la mesa",
                bg=CREMA,
                fg=GRIS,
                font=("Segoe UI", 9)
            ).pack(
                pady=(0, 20)
            )

            campos = tk.Frame(
                formulario,
                bg=CREMA
            )

            campos.pack(
                padx=40,
                fill="x"
            )

            # -------------------------------------------------
            # NÚMERO
            # -------------------------------------------------

            tk.Label(
                campos,
                text="Número de mesa",
                bg=CREMA,
                fg=VERDE_OSCURO,
                font=("Segoe UI", 9, "bold")
            ).pack(
                anchor="w"
            )

            entrada_numero = tk.Entry(
                campos,
                font=("Segoe UI", 10),
                bg=BLANCO,
                fg=VERDE_OSCURO,
                relief="flat",
                highlightbackground=GRIS_CLARO,
                highlightthickness=1
            )

            entrada_numero.pack(
                fill="x",
                ipady=6,
                pady=(3, 10)
            )

            # -------------------------------------------------
            # CAPACIDAD
            # -------------------------------------------------

            tk.Label(
                campos,
                text="Capacidad",
                bg=CREMA,
                fg=VERDE_OSCURO,
                font=("Segoe UI", 9, "bold")
            ).pack(
                anchor="w"
            )

            entrada_capacidad = tk.Entry(
                campos,
                font=("Segoe UI", 10),
                bg=BLANCO,
                fg=VERDE_OSCURO,
                relief="flat",
                highlightbackground=GRIS_CLARO,
                highlightthickness=1
            )

            entrada_capacidad.pack(
                fill="x",
                ipady=6,
                pady=(3, 10)
            )

            # -------------------------------------------------
            # ZONA
            # -------------------------------------------------

            tk.Label(
                campos,
                text="Zona",
                bg=CREMA,
                fg=VERDE_OSCURO,
                font=("Segoe UI", 9, "bold")
            ).pack(
                anchor="w"
            )

            zona = ttk.Combobox(
                campos,
                values=[
                    "Salón",
                    "Terraza",
                    "Jardín"
                ],
                state="readonly",
                font=("Segoe UI", 10)
            )

            zona.pack(
                fill="x",
                pady=(3, 10)
            )

            # -------------------------------------------------
            # ESTADO
            # -------------------------------------------------

            tk.Label(
                campos,
                text="Estado",
                bg=CREMA,
                fg=VERDE_OSCURO,
                font=("Segoe UI", 9, "bold")
            ).pack(
                anchor="w"
            )

            estado = ttk.Combobox(
                campos,
                values=[
                    "Disponible",
                    "Ocupada",
                    "Reservada"
                ],
                state="readonly",
                font=("Segoe UI", 10)
            )

            estado.pack(
                fill="x",
                pady=(3, 10)
            )

            # -------------------------------------------------
            # DATOS DE EDICIÓN
            # -------------------------------------------------

            if mesa:

                entrada_numero.insert(
                    0,
                    mesa[1]
                )

                entrada_capacidad.insert(
                    0,
                    mesa[2]
                )

                zona.set(
                    mesa[3]
                )

                estado.set(
                    mesa[4]
                )

            else:

                estado.set(
                    "Disponible"
                )

            # -------------------------------------------------
            # GUARDAR
            # -------------------------------------------------

            def guardar_mesa():

                numero = entrada_numero.get().strip()
                capacidad = entrada_capacidad.get().strip()
                zona_valor = zona.get()
                estado_valor = estado.get()

                if not numero or not capacidad or not zona_valor:

                    messagebox.showwarning(
                        "Datos incompletos",
                        "Completa todos los campos.",
                        parent=formulario
                    )

                    return

                try:

                    numero = int(numero)
                    capacidad = int(capacidad)

                    if numero <= 0 or capacidad <= 0:
                        raise ValueError

                except ValueError:

                    messagebox.showwarning(
                        "Datos inválidos",
                        "El número de mesa y la capacidad deben ser números positivos.",
                        parent=formulario
                    )

                    return

                conexion = conectar()

                if not conexion:
                    return

                cursor = None

                try:

                    cursor = conexion.cursor()

                    if mesa is None:

                        cursor.execute(
                            """
                            INSERT INTO Mesa (
                                numero_mesa,
                                capacidad,
                                zona,
                                estado
                            )
                            VALUES (
                                %s,
                                %s,
                                %s,
                                %s
                            )
                            """,
                            (
                                numero,
                                capacidad,
                                zona_valor,
                                estado_valor
                            )
                        )

                        mensaje = "Mesa registrada correctamente."

                    else:

                        cursor.execute(
                            """
                            UPDATE Mesa
                            SET
                                numero_mesa = %s,
                                capacidad = %s,
                                zona = %s,
                                estado = %s
                            WHERE id_mesa = %s
                            """,
                            (
                                numero,
                                capacidad,
                                zona_valor,
                                estado_valor,
                                mesa[0]
                            )
                        )

                        mensaje = "Mesa actualizada correctamente."

                    conexion.commit()

                    formulario.destroy()
                    cargar_mesas()

                    messagebox.showinfo(
                        "Operación realizada",
                        mensaje
                    )

                except mysql.connector.Error as error:

                    conexion.rollback()

                    messagebox.showerror(
                        "Error",
                        f"No se pudo guardar la mesa.\n\n{error}",
                        parent=formulario
                    )

                finally:

                    if cursor:
                        cursor.close()

                    conexion.close()

            # -------------------------------------------------
            # BOTONES
            # -------------------------------------------------

            tk.Button(
                formulario,
                text="Guardar",
                command=guardar_mesa,
                bg=VERDE,
                fg=BEIGE,
                activebackground=VERDE_OSCURO,
                activeforeground=BEIGE,
                relief="flat",
                bd=0,
                font=("Segoe UI", 9, "bold"),
                padx=25,
                pady=9,
                cursor="hand2"
            ).pack(
                side="left",
                padx=(40, 5),
                pady=15
            )

            tk.Button(
                formulario,
                text="Cancelar",
                command=formulario.destroy,
                bg=GRIS_CLARO,
                fg=VERDE_OSCURO,
                activebackground=GRIS_CLARO,
                activeforeground=VERDE_OSCURO,
                relief="flat",
                bd=0,
                font=("Segoe UI", 9, "bold"),
                padx=25,
                pady=9,
                cursor="hand2"
            ).pack(
                side="left",
                padx=5,
                pady=15
            )

        # =================================================
        # OBTENER MESA SELECCIONADA
        # =================================================

        mesa_seleccionada = [None]

        # =================================================
        # SELECCIONAR MESA
        # =================================================

        def seleccionar_mesa(mesa, tarjeta):

            mesa_seleccionada[0] = mesa

            for widget in contenedor_mesas.winfo_children():

                if isinstance(
                    widget,
                    tk.Frame
                ):

                    widget.config(
                        highlightbackground=GRIS_CLARO,
                        highlightthickness=2
                    )

            tarjeta.config(
                highlightbackground=BEIGE,
                highlightthickness=2
            )

        # =================================================
        # EDITAR MESA
        # =================================================

        def editar_mesa():

            if mesa_seleccionada[0] is None:

                messagebox.showwarning(
                    "Seleccionar mesa",
                    "Selecciona una mesa para editar."
                )

                return

            abrir_formulario_mesa(
                mesa_seleccionada[0]
            )

        # =================================================
        # ELIMINAR MESA
        # =================================================

        def eliminar_mesa():

            if mesa_seleccionada[0] is None:

                messagebox.showwarning(
                    "Seleccionar mesa",
                    "Selecciona una mesa para eliminar."
                )

                return

            mesa = mesa_seleccionada[0]

            confirmar = messagebox.askyesno(
                "Confirmar eliminación",
                f"¿Deseas eliminar la mesa {mesa[1]}?"
            )

            if not confirmar:
                return

            conexion = conectar()

            if not conexion:
                return

            cursor = None

            try:

                cursor = conexion.cursor()

                cursor.execute(
                    """
                    DELETE FROM Mesa
                    WHERE id_mesa = %s
                    """,
                    (mesa[0],)
                )

                conexion.commit()

                mesa_seleccionada[0] = None

                cargar_mesas()

                messagebox.showinfo(
                    "Mesa eliminada",
                    "La mesa fue eliminada correctamente."
                )

            except mysql.connector.Error:

                conexion.rollback()

                messagebox.showerror(
                    "No se puede eliminar",
                    "No se puede eliminar esta mesa porque tiene "
                    "reservaciones relacionadas."
                )

            finally:

                if cursor:
                    cursor.close()

                conexion.close()

        # =================================================
        # BOTONES DE ACCIONES
        # =================================================

        barra_botones = tk.Frame(
            vista_actual,
            bg=CREMA
        )

        barra_botones.pack(
            fill="x",
            pady=(12, 0)
        )

        # -------------------------------------------------
        # NUEVA MESA
        # -------------------------------------------------

        tk.Button(
            barra_botones,
            text="+ Nueva mesa",
            command=lambda: abrir_formulario_mesa(),
            bg=VERDE,
            fg=BEIGE,
            activebackground=VERDE_OSCURO,
            activeforeground=BEIGE,
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            width=14,
            height=2,
            cursor="hand2"
        ).pack(
            side="left"
        )

        # -------------------------------------------------
        # EDITAR
        # -------------------------------------------------

        tk.Button(
            barra_botones,
            text="Editar",
            command=editar_mesa,
            bg=BEIGE,
            fg=VERDE_OSCURO,
            activebackground=BEIGE,
            activeforeground=VERDE_OSCURO,
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            width=14,
            height=2,
            cursor="hand2"
        ).pack(
            side="left",
            padx=8
        )

        # -------------------------------------------------
        # ELIMINAR
        # -------------------------------------------------

        tk.Button(
            barra_botones,
            text="Eliminar",
            command=eliminar_mesa,
            bg=VINO,
            fg=BLANCO,
            activebackground=VINO,
            activeforeground=BLANCO,
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            width=14,
            height=2,
            cursor="hand2"
        ).pack(
            side="left"
        )

        # BÚSQUEDA

        entrada_busqueda.bind(
            "<KeyRelease>",
            lambda event: cargar_mesas()
        )

        # CARGAR MESAS

        cargar_mesas()

    # =====================================================
    # VISTAS PENDIENTES
    # =====================================================

    # =====================================================
    # VISTA DE PLATILLOS
    # =====================================================



    # =====================================================
    # CREACIÓN SEGURA DE TABLAS AUXILIARES
    # =====================================================
    def asegurar_tablas_administracion():
        conexion = conectar()
        if conexion is None:
            return False
        cursor = None
        try:
            cursor = conexion.cursor()
            sentencias = [
                """CREATE TABLE IF NOT EXISTS proveedor (
                    id_proveedor INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL,
                    telefono VARCHAR(15),
                    correo VARCHAR(100),
                    direccion VARCHAR(255),
                    activo TINYINT(1) NOT NULL DEFAULT 1
                )""",
                """CREATE TABLE IF NOT EXISTS ingrediente (
                    id_ingrediente INT AUTO_INCREMENT PRIMARY KEY,
                    nombre VARCHAR(100) NOT NULL UNIQUE,
                    categoria VARCHAR(50),
                    cantidad_actual DECIMAL(10,3) NOT NULL DEFAULT 0,
                    unidad_medida VARCHAR(20) NOT NULL,
                    stock_minimo DECIMAL(10,3) NOT NULL DEFAULT 0,
                    costo_unitario DECIMAL(10,2) NOT NULL DEFAULT 0,
                    id_proveedor INT NULL,
                    activo TINYINT(1) NOT NULL DEFAULT 1,
                    CONSTRAINT fk_ingrediente_proveedor_admin
                        FOREIGN KEY (id_proveedor) REFERENCES proveedor(id_proveedor)
                        ON DELETE SET NULL ON UPDATE CASCADE
                )""",
                """CREATE TABLE IF NOT EXISTS receta_ingrediente (
                    id_receta INT AUTO_INCREMENT PRIMARY KEY,
                    id_platillo INT NOT NULL,
                    id_ingrediente INT NOT NULL,
                    cantidad_necesaria DECIMAL(10,3) NOT NULL,
                    UNIQUE KEY uq_receta_platillo_ingrediente (id_platillo,id_ingrediente),
                    CONSTRAINT fk_receta_platillo_admin FOREIGN KEY (id_platillo)
                        REFERENCES platillo(id_platillo) ON DELETE CASCADE ON UPDATE CASCADE,
                    CONSTRAINT fk_receta_ingrediente_admin FOREIGN KEY (id_ingrediente)
                        REFERENCES ingrediente(id_ingrediente) ON DELETE RESTRICT ON UPDATE CASCADE
                )""",
                """CREATE TABLE IF NOT EXISTS movimiento_inventario (
                    id_movimiento INT AUTO_INCREMENT PRIMARY KEY,
                    id_ingrediente INT NOT NULL,
                    tipo ENUM('Entrada','Salida','Ajuste') NOT NULL,
                    cantidad DECIMAL(10,3) NOT NULL,
                    motivo VARCHAR(255),
                    fecha DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    id_empleado INT NULL,
                    CONSTRAINT fk_movimiento_ingrediente_admin FOREIGN KEY (id_ingrediente)
                        REFERENCES ingrediente(id_ingrediente) ON DELETE RESTRICT ON UPDATE CASCADE,
                    CONSTRAINT fk_movimiento_empleado_admin FOREIGN KEY (id_empleado)
                        REFERENCES empleado(id_empleado) ON DELETE SET NULL ON UPDATE CASCADE
                )""",
                """CREATE TABLE IF NOT EXISTS empleado_salario (
                    id_empleado INT PRIMARY KEY,
                    salario_base DECIMAL(10,2) NOT NULL DEFAULT 0,
                    actualizado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                    CONSTRAINT fk_salario_empleado_admin FOREIGN KEY (id_empleado)
                        REFERENCES empleado(id_empleado) ON DELETE CASCADE ON UPDATE CASCADE
                )""",
                """CREATE TABLE IF NOT EXISTS pago_planilla (
                    id_pago INT AUTO_INCREMENT PRIMARY KEY,
                    id_empleado INT NOT NULL,
                    periodo_inicio DATE NOT NULL,
                    periodo_fin DATE NOT NULL,
                    salario_base DECIMAL(10,2) NOT NULL DEFAULT 0,
                    bonificaciones DECIMAL(10,2) NOT NULL DEFAULT 0,
                    descuentos DECIMAL(10,2) NOT NULL DEFAULT 0,
                    total_pagado DECIMAL(10,2) NOT NULL DEFAULT 0,
                    fecha_pago DATE NOT NULL,
                    observaciones VARCHAR(255),
                    CONSTRAINT fk_pago_empleado_admin FOREIGN KEY (id_empleado)
                        REFERENCES empleado(id_empleado) ON DELETE RESTRICT ON UPDATE CASCADE
                )"""
            ]
            for sentencia in sentencias:
                cursor.execute(sentencia)
            conexion.commit()
            return True
        except mysql.connector.Error as error:
            conexion.rollback()
            messagebox.showerror(
                "Preparación de la base de datos",
                "No se pudieron preparar las tablas auxiliares.\n\n"
                f"Comprueba que DATABASE = '{DATABASE}' sea la base que contiene Platillo, Empleado y Proveedor.\n\n{error}"
            )
            return False
        finally:
            if cursor:
                cursor.close()
            conexion.close()

    # =====================================================
    # INVENTARIO FUNCIONAL
    # =====================================================
    def mostrar_inventario():
        limpiar_vista()
        activar_boton("INVENTARIO")
        if not asegurar_tablas_administracion():
            return

        tk.Label(vista_actual, text="Inventario", bg=CREMA, fg=VERDE_OSCURO,
                 font=("Georgia",  23, "bold")).pack(anchor="w", pady=(4, 2))
        tk.Label(vista_actual, text="Ingredientes, existencias y movimientos", bg=CREMA,
                 fg=GRIS, font=("Segoe UI", 9)).pack(anchor="w", pady=(0, 12))

        resumen = tk.Frame(vista_actual, bg=CREMA)
        resumen.pack(fill="x", pady=(0, 12))
        valores = {}
        for nombre, color in [("INGREDIENTES", VERDE), ("DISPONIBLES", VERDE_OSCURO),
                              ("STOCK BAJO", "#a66a00"), ("AGOTADOS", VINO)]:
            tarjeta = tk.Frame(resumen, bg=BLANCO, highlightbackground=GRIS_CLARO, highlightthickness=1)
            tarjeta.pack(side="left", fill="x", expand=True, padx=(0, 7))
            tk.Label(tarjeta, text=nombre, bg=BLANCO, fg=GRIS,
                     font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=10, pady=(9, 1))
            valores[nombre] = tk.Label(tarjeta, text="0", bg=BLANCO, fg=color,
                                       font=("Georgia", 20, "bold"))
            valores[nombre].pack(anchor="w", padx=10, pady=(0, 8))

        barra = tk.Frame(vista_actual, bg=CREMA)
        barra.pack(fill="x", pady=(0, 9))
        busqueda = tk.StringVar()
        categoria = tk.StringVar(value="Todas")
        estado = tk.StringVar(value="Todos")
        tk.Label(barra, text="Buscar:", bg=CREMA, fg=VERDE_OSCURO,
                 font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 8))
        entrada = tk.Entry(barra, textvariable=busqueda, font=("Segoe UI", 10),
                           relief="flat", bg=BLANCO, fg=VERDE_OSCURO)
        entrada.pack(side="left", fill="x", expand=True, ipady=8, padx=(0, 7))
        entrada.insert(0, "")
        combo_categoria = ttk.Combobox(barra, textvariable=categoria, values=["Todas"],
                                       state="readonly", width=15)
        combo_categoria.pack(side="left", padx=4, ipady=4)
        combo_estado = ttk.Combobox(barra, textvariable=estado,
                                    values=["Todos", "Disponible", "Stock bajo", "Agotado"],
                                    state="readonly", width=13)
        combo_estado.pack(side="left", padx=4, ipady=4)

        marco_tabla = tk.Frame(vista_actual, bg=BLANCO)
        marco_tabla.pack(fill="both", expand=True)
        columnas = ("id", "nombre", "categoria", "cantidad", "unidad", "minimo", "costo", "proveedor", "estado")
        tabla = ttk.Treeview(marco_tabla, columns=columnas, show="headings", selectmode="browse")
        titulos = {"id":"ID", "nombre":"INGREDIENTE", "categoria":"CATEGORÍA", "cantidad":"EXISTENCIA",
                   "unidad":"UNIDAD", "minimo":"STOCK MÍNIMO", "costo":"COSTO UNITARIO", "proveedor":"PROVEEDOR", "estado":"ESTADO"}
        anchos = {"id":42, "nombre":150, "categoria":95, "cantidad":78, "unidad":70, "minimo":85, "costo":90, "proveedor":125, "estado":85}
        for col in columnas:
            tabla.heading(col, text=titulos[col])
            tabla.column(col, width=anchos[col], anchor="center")
        scroll_y = ttk.Scrollbar(marco_tabla, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scroll_y.set)
        tabla.pack(side="left", fill="both", expand=True)
        scroll_y.pack(side="right", fill="y")
        tabla.tag_configure("Stock bajo", foreground="#a66a00")
        tabla.tag_configure("Agotado", foreground=VINO)
        tabla.tag_configure("Disponible", foreground=VERDE)

        registros = []
        def estado_stock(cantidad, minimo):
            cantidad, minimo = Decimal(str(cantidad)), Decimal(str(minimo))
            if cantidad <= 0:
                return "Agotado"
            if cantidad <= minimo:
                return "Stock bajo"
            return "Disponible"

        def cargar():
            for item in tabla.get_children():
                tabla.delete(item)
            conexion = conectar()
            if conexion is None:
                return
            cursor = None
            try:
                cursor = conexion.cursor(dictionary=True)
                cursor.execute("""SELECT i.id_ingrediente, i.nombre, i.categoria, i.cantidad_actual,
                    i.unidad_medida, i.stock_minimo, i.costo_unitario, i.id_proveedor,
                    COALESCE(p.nombre,'Sin proveedor') AS proveedor
                    FROM ingrediente i LEFT JOIN proveedor p ON p.id_proveedor=i.id_proveedor
                    ORDER BY i.nombre""")
                registros.clear()
                registros.extend(cursor.fetchall())
                conteo = {"INGREDIENTES":len(registros), "DISPONIBLES":0, "STOCK BAJO":0, "AGOTADOS":0}
                categorias = sorted({r["categoria"] for r in registros if r["categoria"]})
                combo_categoria["values"] = ["Todas"] + categorias
                q = busqueda.get().strip().lower()
                for r in registros:
                    est = estado_stock(r["cantidad_actual"], r["stock_minimo"])
                    conteo[{"Disponible":"DISPONIBLES", "Stock bajo":"STOCK BAJO", "Agotado":"AGOTADOS"}[est]] += 1
                    if q and q not in f"{r['nombre']} {r['categoria'] or ''} {r['proveedor']}".lower():
                        continue
                    if categoria.get() != "Todas" and r["categoria"] != categoria.get():
                        continue
                    if estado.get() != "Todos" and est != estado.get():
                        continue
                    tabla.insert("", "end", iid=str(r["id_ingrediente"]), values=(
                        r["id_ingrediente"], r["nombre"], r["categoria"] or "Sin categoría",
                        f"{Decimal(str(r['cantidad_actual'])):.3f}", r["unidad_medida"],
                        f"{Decimal(str(r['stock_minimo'])):.3f}", f"${Decimal(str(r['costo_unitario'])):.2f}",
                        r["proveedor"], est), tags=(est,))
                for k, v in conteo.items():
                    valores[k].config(text=str(v))
            except Exception as error:
                messagebox.showerror("Inventario", f"No se pudo cargar el inventario:\n\n{error}")
            finally:
                if cursor: cursor.close()
                conexion.close()

        def seleccionado():
            sel = tabla.selection()
            if not sel:
                messagebox.showwarning("Inventario", "Selecciona primero un ingrediente.")
                return None
            return next((r for r in registros if str(r["id_ingrediente"]) == sel[0]), None)

        def formulario(ing=None):
            editar = ing is not None
            w = tk.Toplevel(ventana)
            w.title("Editar ingrediente" if editar else "Nuevo ingrediente")
            w.geometry("440x590")
            w.configure(bg=CREMA)
            w.transient(ventana)
            w.grab_set()
            tk.Label(w, text="Editar ingrediente" if editar else "Registrar ingrediente",
                     bg=CREMA, fg=VERDE_OSCURO, font=("Georgia", 18, "bold")).pack(anchor="w", padx=22, pady=(18, 12))
            cuerpo = tk.Frame(w, bg=CREMA)
            cuerpo.pack(fill="both", expand=True, padx=22)
            campos = {}
            def campo(label, key, default=""):
                tk.Label(cuerpo, text=label, bg=CREMA, fg=VERDE_OSCURO,
                         font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(4, 2))
                e = tk.Entry(cuerpo, font=("Segoe UI", 10), relief="flat", bg=BLANCO)
                e.pack(fill="x", ipady=5)
                e.insert(0, str(default if default is not None else ""))
                campos[key] = e
            campo("Nombre", "nombre", ing["nombre"] if editar else "")
            campo("Categoría", "categoria", ing["categoria"] if editar else "Otros")
            campo("Cantidad actual", "cantidad", ing["cantidad_actual"] if editar else "0")
            campo("Unidad (kg, g, litros, unidades...)", "unidad", ing["unidad_medida"] if editar else "kg")
            campo("Stock mínimo", "minimo", ing["stock_minimo"] if editar else "1")
            campo("Costo por unidad ($)", "costo", ing["costo_unitario"] if editar else "0.00")
            tk.Label(cuerpo, text="Proveedor", bg=CREMA, fg=VERDE_OSCURO,
                     font=("Segoe UI", 9, "bold")).pack(anchor="w", pady=(7, 2))
            proveedores = {}
            cx = conectar()
            if cx:
                cur = None
                try:
                    cur = cx.cursor()
                    cur.execute("SELECT id_proveedor,nombre FROM proveedor WHERE activo=1 ORDER BY nombre")
                    proveedores = {nombre: ident for ident, nombre in cur.fetchall()}
                except mysql.connector.Error as error:
                    messagebox.showerror("Proveedores", str(error), parent=w)
                finally:
                    if cur: cur.close()
                    cx.close()
            combo_prov = ttk.Combobox(cuerpo, values=["Sin proveedor"] + list(proveedores), state="readonly")
            combo_prov.pack(fill="x", ipady=3)
            actual = "Sin proveedor"
            if editar and ing.get("id_proveedor"):
                actual = next((n for n, ident in proveedores.items() if ident == ing["id_proveedor"]), actual)
            combo_prov.set(actual)
            def guardar():
                nombre = campos["nombre"].get().strip()
                unidad = campos["unidad"].get().strip()
                if not nombre or not unidad:
                    messagebox.showwarning("Datos requeridos", "Nombre y unidad son obligatorios.", parent=w)
                    return
                try:
                    cantidad = Decimal(campos["cantidad"].get().strip().replace(",", "."))
                    minimo = Decimal(campos["minimo"].get().strip().replace(",", "."))
                    costo = Decimal(campos["costo"].get().strip().replace(",", "."))
                    if min(cantidad, minimo, costo) < 0:
                        raise ValueError("No se permiten valores negativos.")
                except (InvalidOperation, ValueError) as error:
                    messagebox.showerror("Datos inválidos", str(error), parent=w)
                    return
                cx = conectar()
                if cx is None: return
                cur = None
                try:
                    cur = cx.cursor()
                    prov_id = proveedores.get(combo_prov.get())
                    if editar:
                        cur.execute("""UPDATE ingrediente SET nombre=%s,categoria=%s,cantidad_actual=%s,
                            unidad_medida=%s,stock_minimo=%s,costo_unitario=%s,id_proveedor=%s
                            WHERE id_ingrediente=%s""", (nombre, campos["categoria"].get().strip() or None,
                            cantidad, unidad, minimo, costo, prov_id, ing["id_ingrediente"]))
                        if cantidad != Decimal(str(ing["cantidad_actual"])):
                            cur.execute("INSERT INTO movimiento_inventario(id_ingrediente,tipo,cantidad,motivo) VALUES(%s,'Ajuste',%s,%s)",
                                        (ing["id_ingrediente"], cantidad, "Ajuste desde edición del ingrediente"))
                    else:
                        cur.execute("""INSERT INTO ingrediente(nombre,categoria,cantidad_actual,unidad_medida,
                            stock_minimo,costo_unitario,id_proveedor) VALUES(%s,%s,%s,%s,%s,%s,%s)""",
                            (nombre, campos["categoria"].get().strip() or None, cantidad, unidad, minimo, costo, prov_id))
                        nuevo = cur.lastrowid
                        if cantidad > 0:
                            cur.execute("INSERT INTO movimiento_inventario(id_ingrediente,tipo,cantidad,motivo) VALUES(%s,'Entrada',%s,%s)",
                                        (nuevo, cantidad, "Existencia inicial"))
                    cx.commit()
                    w.destroy()
                    cargar()
                    messagebox.showinfo("Inventario", "Ingrediente guardado correctamente.")
                except mysql.connector.Error as error:
                    cx.rollback()
                    messagebox.showerror("No se pudo guardar", str(error), parent=w)
                finally:
                    if cur: cur.close()
                    cx.close()
            tk.Button(w, text="Guardar", command=guardar, bg=VERDE, fg=BLANCO,
                      activebackground=VERDE_OSCURO, relief="flat", font=("Segoe UI", 10, "bold"),
                      cursor="hand2", pady=8).pack(fill="x", padx=22, pady=18)

        def movimiento():
            ing = seleccionado()
            if not ing: return
            w = tk.Toplevel(ventana)
            w.title("Movimiento de inventario")
            w.geometry("390x340")
            w.configure(bg=CREMA)
            w.transient(ventana); w.grab_set()
            tk.Label(w, text=ing["nombre"], bg=CREMA, fg=VERDE_OSCURO,
                     font=("Georgia", 16, "bold")).pack(anchor="w", padx=20, pady=(18, 4))
            tk.Label(w, text=f"Existencia: {ing['cantidad_actual']} {ing['unidad_medida']}",
                     bg=CREMA, fg=GRIS).pack(anchor="w", padx=20, pady=(0, 12))
            tipo = ttk.Combobox(w, values=["Entrada", "Salida", "Ajuste"], state="readonly")
            tipo.pack(fill="x", padx=20, pady=5); tipo.set("Entrada")
            cantidad = tk.Entry(w); cantidad.pack(fill="x", padx=20, pady=5); cantidad.insert(0, "1")
            motivo = tk.Entry(w); motivo.pack(fill="x", padx=20, pady=5); motivo.insert(0, "Compra / uso / ajuste")
            def guardar_mov():
                try:
                    cant = Decimal(cantidad.get().strip().replace(",", "."))
                    if cant <= 0: raise ValueError("La cantidad debe ser mayor que cero.")
                except (InvalidOperation, ValueError) as error:
                    messagebox.showerror("Cantidad inválida", str(error), parent=w); return
                cx = conectar()
                if cx is None: return
                cur = None
                try:
                    cur = cx.cursor()
                    cur.execute("SELECT cantidad_actual FROM ingrediente WHERE id_ingrediente=%s FOR UPDATE", (ing["id_ingrediente"],))
                    fila = cur.fetchone()
                    if not fila: raise ValueError("El ingrediente ya no existe.")
                    anterior = Decimal(str(fila[0]))
                    if tipo.get() == "Entrada": nueva = anterior + cant
                    elif tipo.get() == "Salida":
                        nueva = anterior - cant
                        if nueva < 0: raise ValueError("No hay existencia suficiente para esa salida.")
                    else: nueva = cant
                    cur.execute("UPDATE ingrediente SET cantidad_actual=%s WHERE id_ingrediente=%s", (nueva, ing["id_ingrediente"]))
                    cur.execute("INSERT INTO movimiento_inventario(id_ingrediente,tipo,cantidad,motivo) VALUES(%s,%s,%s,%s)",
                                (ing["id_ingrediente"], tipo.get(), cant, motivo.get().strip() or None))
                    cx.commit(); w.destroy(); cargar()
                    messagebox.showinfo("Inventario", f"Movimiento registrado. Existencia: {nueva} {ing['unidad_medida']}.")
                except Exception as error:
                    cx.rollback(); messagebox.showerror("Movimiento", str(error), parent=w)
                finally:
                    if cur: cur.close()
                    cx.close()
            tk.Button(w, text="Registrar movimiento", command=guardar_mov, bg=VERDE, fg=BLANCO,
                      relief="flat", pady=8).pack(fill="x", padx=20, pady=15)

        def receta():
            ing = seleccionado()
            if not ing: return
            cx = conectar()
            if cx is None: return
            cur = None
            try:
                cur = cx.cursor()
                cur.execute("SELECT id_platillo,nombre,categoria FROM platillo ORDER BY categoria,nombre")
                plats = cur.fetchall()
            except mysql.connector.Error as error:
                messagebox.showerror("Menú", str(error)); return
            finally:
                if cur: cur.close()
                cx.close()
            if not plats:
                messagebox.showinfo("Menú", "Primero registra platillos en el menú."); return
            w = tk.Toplevel(ventana); w.title("Ingrediente por platillo"); w.geometry("430x280"); w.configure(bg=CREMA); w.transient(ventana); w.grab_set()
            tk.Label(w, text=f"Vincular: {ing['nombre']}", bg=CREMA, fg=VERDE_OSCURO,
                     font=("Georgia", 15, "bold")).pack(anchor="w", padx=20, pady=(20, 12))
            nombres = [f"{p[1]} — {p[2] or 'Sin categoría'}" for p in plats]
            combo = ttk.Combobox(w, values=nombres, state="readonly"); combo.pack(fill="x", padx=20, pady=7); combo.current(0)
            cantidad = tk.Entry(w); cantidad.pack(fill="x", padx=20, pady=7); cantidad.insert(0, "0.100")
            tk.Label(w, text=f"Cantidad por porción ({ing['unidad_medida']})", bg=CREMA, fg=GRIS).pack(anchor="w", padx=20)
            def guardar_receta():
                try:
                    cant = Decimal(cantidad.get().strip().replace(",", "."))
                    if cant <= 0: raise ValueError("Debe ser mayor que cero.")
                except (InvalidOperation, ValueError) as error:
                    messagebox.showerror("Cantidad", str(error), parent=w); return
                cx2 = conectar()
                if cx2 is None: return
                c2 = None
                try:
                    c2 = cx2.cursor()
                    c2.execute("""INSERT INTO receta_ingrediente(id_platillo,id_ingrediente,cantidad_necesaria)
                        VALUES(%s,%s,%s) ON DUPLICATE KEY UPDATE cantidad_necesaria=VALUES(cantidad_necesaria)""",
                        (plats[combo.current()][0], ing["id_ingrediente"], cant))
                    cx2.commit(); w.destroy(); messagebox.showinfo("Receta", "Ingrediente vinculado al platillo.")
                except mysql.connector.Error as error:
                    cx2.rollback(); messagebox.showerror("Receta", str(error), parent=w)
                finally:
                    if c2: c2.close()
                    cx2.close()
            tk.Button(w, text="Guardar relación", command=guardar_receta, bg=VERDE, fg=BLANCO,
                      relief="flat", pady=8).pack(fill="x", padx=20, pady=15)

        def historial():
            ing = seleccionado()
            if not ing: return
            w = tk.Toplevel(ventana); w.title("Historial de movimientos"); w.geometry("760x390"); w.configure(bg=CREMA)
            tk.Label(w, text=f"Historial: {ing['nombre']}", bg=CREMA, fg=VERDE_OSCURO,
                     font=("Georgia", 17, "bold")).pack(anchor="w", padx=18, pady=15)
            t = ttk.Treeview(w, columns=("tipo", "cantidad", "motivo", "fecha"), show="headings")
            for col, title, width in [("tipo","TIPO",100),("cantidad","CANTIDAD",100),("motivo","MOTIVO",300),("fecha","FECHA",170)]:
                t.heading(col, text=title); t.column(col, width=width)
            t.pack(fill="both", expand=True, padx=18, pady=(0,18))
            cx = conectar()
            if cx is None: return
            cur = None
            try:
                cur = cx.cursor()
                cur.execute("SELECT tipo,cantidad,motivo,fecha FROM movimiento_inventario WHERE id_ingrediente=%s ORDER BY fecha DESC,id_movimiento DESC", (ing["id_ingrediente"],))
                for row in cur.fetchall(): t.insert("", "end", values=(row[0], row[1], row[2] or "—", row[3].strftime("%d/%m/%Y %H:%M") if row[3] else ""))
            except mysql.connector.Error as error:
                messagebox.showerror("Historial", str(error), parent=w)
            finally:
                if cur: cur.close()
                cx.close()

        def eliminar():
            ing = seleccionado()
            if not ing: return
            if not messagebox.askyesno("Eliminar ingrediente", f"¿Eliminar {ing['nombre']}? Si tiene historial o recetas asociadas, MySQL impedirá la eliminación."):
                return
            cx = conectar()
            if cx is None: return
            cur = None
            try:
                cur = cx.cursor(); cur.execute("DELETE FROM ingrediente WHERE id_ingrediente=%s", (ing["id_ingrediente"],)); cx.commit(); cargar()
            except mysql.connector.Error as error:
                cx.rollback(); messagebox.showerror("No se puede eliminar", f"Conservaremos el ingrediente porque tiene relaciones o movimientos.\n\n{error}")
            finally:
                if cur: cur.close()
                cx.close()

        botones = tk.Frame(vista_actual, bg=CREMA); botones.pack(fill="x", pady=(10, 0))
        acciones = [("+ Ingrediente", lambda: formulario(), VERDE), ("Editar", lambda: formulario(seleccionado()) if tabla.selection() else messagebox.showwarning("Inventario", "Selecciona un ingrediente."), BEIGE),
                    ("Movimiento", movimiento, VINO), ("Vincular menú", receta, VERDE_OSCURO), ("Historial", historial, VINO), ("Eliminar", eliminar, GRIS)]
        for texto, cmd, color in acciones:
            tk.Button(botones, text=texto, command=cmd, bg=color, fg=BLANCO if color != BEIGE else VERDE_OSCURO,
                      relief="flat", cursor="hand2", font=("Segoe UI", 8, "bold"), padx=8, pady=8).pack(side="left", padx=(0, 5))
        tk.Button(botones, text="Actualizar", command=cargar, bg=BEIGE, fg=VERDE_OSCURO,
                  relief="flat", cursor="hand2", font=("Segoe UI", 8, "bold"), padx=8, pady=8).pack(side="right")
        busqueda.trace_add("write", lambda *_: cargar())
        combo_categoria.bind("<<ComboboxSelected>>", lambda _e: cargar())
        combo_estado.bind("<<ComboboxSelected>>", lambda _e: cargar())
        cargar()

    # =====================================================
    # PROVEEDORES FUNCIONAL
    # =====================================================
    def mostrar_proveedores():
        limpiar_vista(); activar_boton("PROVEEDORES")
        if not asegurar_tablas_administracion(): return
        tk.Label(vista_actual, text="Proveedores", bg=CREMA, fg=VERDE_OSCURO,
                 font=("Georgia", 23, "bold")).pack(anchor="w", pady=(4, 2))
        tk.Label(vista_actual, text="Administración de proveedores y contacto", bg=CREMA,
                 fg=GRIS, font=("Segoe UI", 9)).pack(anchor="w", pady=(0, 12))
        barra = tk.Frame(vista_actual, bg=CREMA); barra.pack(fill="x", pady=(0, 10))
        busqueda = tk.StringVar()
        tk.Label(barra, text="Buscar:", bg=CREMA, fg=VERDE_OSCURO,
                 font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 8))
        e = tk.Entry(barra, textvariable=busqueda, relief="flat", bg=BLANCO, font=("Segoe UI", 10)); e.pack(side="left", fill="x", expand=True, ipady=8)
        tabla = ttk.Treeview(vista_actual, columns=("id","nombre","telefono","correo","direccion","estado"), show="headings", selectmode="browse")
        for c, title, width in [("id","ID",45),("nombre","PROVEEDOR",170),("telefono","TELÉFONO",105),("correo","CORREO",180),("direccion","DIRECCIÓN",240),("estado","ESTADO",90)]:
            tabla.heading(c,text=title); tabla.column(c,width=width,anchor="center" if c in ("id","estado") else "w")
        tabla.pack(fill="both", expand=True)
        def cargar():
            tabla.delete(*tabla.get_children()); cx=conectar()
            if cx is None:return
            cur=None
            try:
                cur=cx.cursor(); cur.execute("SELECT id_proveedor,nombre,telefono,correo,direccion,activo FROM proveedor WHERE nombre LIKE %s OR telefono LIKE %s OR correo LIKE %s ORDER BY nombre", tuple([f"%{busqueda.get().strip()}%"]*3))
                for row in cur.fetchall(): tabla.insert("","end",iid=str(row[0]),values=(row[0],row[1],row[2] or "—",row[3] or "—",row[4] or "—","Activo" if row[5] else "Inactivo"))
            except mysql.connector.Error as error: messagebox.showerror("Proveedores",str(error))
            finally:
                if cur:cur.close()
                cx.close()
        def formulario(row=None):
            w=tk.Toplevel(ventana); w.title("Editar proveedor" if row else "Nuevo proveedor"); w.geometry("440x430"); w.configure(bg=CREMA); w.transient(ventana); w.grab_set()
            tk.Label(w,text="Editar proveedor" if row else "Registrar proveedor",bg=CREMA,fg=VERDE_OSCURO,font=("Georgia",18,"bold")).pack(anchor="w",padx=22,pady=18)
            fields={}
            for key,label in [("nombre","Nombre"),("telefono","Teléfono"),("correo","Correo electrónico"),("direccion","Dirección")]:
                tk.Label(w,text=label,bg=CREMA,fg=VERDE_OSCURO,font=("Segoe UI",9,"bold")).pack(anchor="w",padx=22,pady=(5,2))
                x=tk.Entry(w,bg=BLANCO,relief="flat",font=("Segoe UI",10)); x.pack(fill="x",padx=22,ipady=6); x.insert(0,(row[fields_order.index(key)+1] or "") if row else ""); fields[key]=x
            activo=tk.IntVar(value=int(row[5]) if row else 1)
            tk.Checkbutton(w,text="Proveedor activo",variable=activo,bg=CREMA,fg=VERDE_OSCURO,activebackground=CREMA).pack(anchor="w",padx=22,pady=10)
            def guardar():
                nombre=fields["nombre"].get().strip()
                if not nombre: messagebox.showwarning("Datos requeridos","El nombre es obligatorio.",parent=w); return
                cx=conectar()
                if cx is None:return
                cur=None
                try:
                    cur=cx.cursor()
                    vals=(nombre,fields["telefono"].get().strip() or None,fields["correo"].get().strip() or None,fields["direccion"].get().strip() or None,activo.get())
                    if row: cur.execute("UPDATE proveedor SET nombre=%s,telefono=%s,correo=%s,direccion=%s,activo=%s WHERE id_proveedor=%s",vals+(row[0],))
                    else: cur.execute("INSERT INTO proveedor(nombre,telefono,correo,direccion,activo) VALUES(%s,%s,%s,%s,%s)",vals)
                    cx.commit(); w.destroy(); cargar()
                except mysql.connector.Error as error: cx.rollback(); messagebox.showerror("Proveedor",str(error),parent=w)
                finally:
                    if cur:cur.close()
                    cx.close()
            tk.Button(w,text="Guardar proveedor",command=guardar,bg=VERDE,fg=BLANCO,relief="flat",pady=8).pack(fill="x",padx=22,pady=15)
        fields_order=["id","nombre","telefono","correo","direccion","activo"]
        def obtener():
            sel=tabla.selection()
            if not sel: messagebox.showwarning("Proveedores","Selecciona un proveedor."); return None
            vals=tabla.item(sel[0],"values")
            cx=conectar()
            if cx is None:return None
            cur=None
            try:
                cur=cx.cursor();cur.execute("SELECT id_proveedor,nombre,telefono,correo,direccion,activo FROM proveedor WHERE id_proveedor=%s",(vals[0],));return cur.fetchone()
            finally:
                if cur:cur.close()
                cx.close()
        def desactivar():
            row=obtener()
            if not row:return
            if not messagebox.askyesno("Desactivar proveedor",f"¿Desactivar a {row[1]}? Los ingredientes conservarán la relación."):return
            cx=conectar()
            if cx is None:return
            cur=None
            try:cur=cx.cursor();cur.execute("UPDATE proveedor SET activo=0 WHERE id_proveedor=%s",(row[0],));cx.commit();cargar()
            except mysql.connector.Error as error:cx.rollback();messagebox.showerror("Proveedores",str(error))
            finally:
                if cur:cur.close()
                cx.close()
        botones=tk.Frame(vista_actual,bg=CREMA);botones.pack(fill="x",pady=12)
        for texto,cmd,color in [("+ Nuevo",lambda:formulario(),VERDE),("Editar",lambda:formulario(obtener()) if tabla.selection() else messagebox.showwarning("Proveedores","Selecciona un proveedor."),BEIGE),("Desactivar",desactivar,VINO),("Actualizar",cargar,VERDE_OSCURO)]:
            tk.Button(botones,text=texto,command=cmd,bg=color,fg=BLANCO if color!=BEIGE else VERDE_OSCURO,relief="flat",padx=12,pady=8).pack(side="left",padx=(0,7))
        busqueda.trace_add("write",lambda *_:cargar());cargar()

    # =====================================================
    # PLANILLA FUNCIONAL
    # =====================================================
    def mostrar_planilla():
        limpiar_vista(); activar_boton("PLANILLA")
        if not asegurar_tablas_administracion(): return
        tk.Label(vista_actual,text="Planilla",bg=CREMA,fg=VERDE_OSCURO,font=("Georgia",23,"bold")).pack(anchor="w",pady=(4,2))
        tk.Label(vista_actual,text="Empleados, salarios y registro de pagos",bg=CREMA,fg=GRIS,font=("Segoe UI",9)).pack(anchor="w",pady=(0,12))
        barra=tk.Frame(vista_actual,bg=CREMA);barra.pack(fill="x",pady=(0,8));busqueda=tk.StringVar()
        tk.Label(barra,text="Buscar:",bg=CREMA,fg=VERDE_OSCURO,font=("Segoe UI",9,"bold")).pack(side="left",padx=(0,8))
        e=tk.Entry(barra,textvariable=busqueda,bg=BLANCO,relief="flat",font=("Segoe UI",10));e.pack(fill="x",expand=True,side="left",ipady=8)
        tabla=ttk.Treeview(vista_actual,columns=("id","nombre","usuario","rol","turno","salario","activo","contratacion"),show="headings",selectmode="browse")
        for c,t,w in [("id","ID",42),("nombre","EMPLEADO",155),("usuario","USUARIO",90),("rol","ROL",100),("turno","TURNO",85),("salario","SALARIO BASE",100),("activo","ESTADO",80),("contratacion","CONTRATACIÓN",105)]:tabla.heading(c,text=t);tabla.column(c,width=w,anchor="center")
        tabla.pack(fill="both",expand=True)
        def cargar():
            tabla.delete(*tabla.get_children());cx=conectar()
            if cx is None:return
            cur=None
            try:
                cur=cx.cursor();q="""SELECT e.id_empleado,CONCAT(e.nombre,' ',e.apellido),e.usuario,e.rol,e.turno,
                    COALESCE(s.salario_base,0),e.activo,e.fecha_contratacion
                    FROM empleado e LEFT JOIN empleado_salario s ON s.id_empleado=e.id_empleado
                    WHERE CONCAT(e.nombre,' ',e.apellido) LIKE %s OR e.usuario LIKE %s OR e.rol LIKE %s ORDER BY e.apellido,e.nombre"""
                term=f"%{busqueda.get().strip()}%";cur.execute(q,(term,term,term))
                for r in cur.fetchall():tabla.insert("","end",iid=str(r[0]),values=(r[0],r[1],r[2],r[3],r[4] or "—",f"${Decimal(str(r[5])):.2f}","Activo" if r[6] else "Inactivo",r[7] or "—"))
            except mysql.connector.Error as error:messagebox.showerror("Planilla",str(error))
            finally:
                if cur:cur.close()
                cx.close()
        def empleado_id():
            sel=tabla.selection()
            if not sel:messagebox.showwarning("Planilla","Selecciona un empleado.");return None
            return int(sel[0])
        def configurar_salario():
            ident=empleado_id()
            if ident is None:return
            w=tk.Toplevel(ventana);w.title("Salario base");w.geometry("360x220");w.configure(bg=CREMA);w.transient(ventana);w.grab_set()
            tk.Label(w,text="Actualizar salario base",bg=CREMA,fg=VERDE_OSCURO,font=("Georgia",16,"bold")).pack(pady=(20,12))
            x=tk.Entry(w,font=("Segoe UI",11));x.pack(fill="x",padx=22,ipady=7)
            cx=conectar();cur=None
            if cx:
                try:cur=cx.cursor();cur.execute("SELECT salario_base FROM empleado_salario WHERE id_empleado=%s",(ident,));r=cur.fetchone();x.insert(0,str(r[0]) if r else "0.00")
                finally:
                    if cur:cur.close()
                    cx.close()
            def guardar():
                try:sueldo=Decimal(x.get().strip().replace(",","."));
                except InvalidOperation:messagebox.showerror("Salario","Ingresa un monto válido.",parent=w);return
                if sueldo<0:messagebox.showerror("Salario","No se permite un salario negativo.",parent=w);return
                c=conectar()
                if c is None:return
                cu=None
                try:cu=c.cursor();cu.execute("INSERT INTO empleado_salario(id_empleado,salario_base) VALUES(%s,%s) ON DUPLICATE KEY UPDATE salario_base=VALUES(salario_base)",(ident,sueldo));c.commit();w.destroy();cargar()
                except mysql.connector.Error as error:c.rollback();messagebox.showerror("Salario",str(error),parent=w)
                finally:
                    if cu:cu.close()
                    c.close()
            tk.Button(w,text="Guardar salario",command=guardar,bg=VERDE,fg=BLANCO,relief="flat",pady=8).pack(fill="x",padx=22,pady=15)
        def pagar():
            ident=empleado_id()
            if ident is None:return
            w=tk.Toplevel(ventana);w.title("Registrar pago de planilla");w.geometry("430x440");w.configure(bg=CREMA);w.transient(ventana);w.grab_set()
            tk.Label(w,text="Registrar pago",bg=CREMA,fg=VERDE_OSCURO,font=("Georgia",17,"bold")).pack(anchor="w",padx=22,pady=(18,12))
            campos={}
            for key,label,default in [("inicio","Inicio del período (AAAA-MM-DD),",date.today().replace(day=1).isoformat()),("fin","Fin del período (AAAA-MM-DD)",date.today().isoformat()),("bono","Bonificaciones", "0.00"),("descuento","Descuentos","0.00"),("fecha","Fecha de pago (AAAA-MM-DD)",date.today().isoformat()),("obs","Observaciones","Pago de planilla")]:
                tk.Label(w,text=label,bg=CREMA,fg=VERDE_OSCURO,font=("Segoe UI",9,"bold")).pack(anchor="w",padx=22,pady=(4,1));x=tk.Entry(w);x.pack(fill="x",padx=22,ipady=4);x.insert(0,default);campos[key]=x
            cx=conectar();cur=None;sueldo=Decimal("0")
            if cx:
                try:cur=cx.cursor();cur.execute("SELECT salario_base FROM empleado_salario WHERE id_empleado=%s",(ident,));r=cur.fetchone();sueldo=Decimal(str(r[0])) if r else Decimal("0")
                finally:
                    if cur:cur.close()
                    cx.close()
            tk.Label(w,text=f"Salario base: ${sueldo:.2f}",bg=CREMA,fg=VERDE,font=("Segoe UI",10,"bold")).pack(anchor="w",padx=22,pady=5)
            def guardar_pago():
                try:
                    inicio=date.fromisoformat(campos["inicio"].get().strip());fin=date.fromisoformat(campos["fin"].get().strip());fp=date.fromisoformat(campos["fecha"].get().strip());bono=Decimal(campos["bono"].get().strip().replace(",","."));desc=Decimal(campos["descuento"].get().strip().replace(",","."))
                    if fin<inicio or min(bono,desc)<0:raise ValueError("Revisa las fechas y los montos.")
                except (ValueError,InvalidOperation) as error:messagebox.showerror("Pago inválido",str(error),parent=w);return
                total=sueldo+bono-desc
                if total<0:messagebox.showerror("Pago inválido","El total no puede ser negativo.",parent=w);return
                c=conectar()
                if c is None:return
                cu=None
                try:
                    cu=c.cursor();cu.execute("INSERT INTO pago_planilla(id_empleado,periodo_inicio,periodo_fin,salario_base,bonificaciones,descuentos,total_pagado,fecha_pago,observaciones) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)",(ident,inicio,fin,sueldo,bono,desc,total,fp,campos["obs"].get().strip() or None));c.commit();w.destroy();messagebox.showinfo("Planilla",f"Pago registrado: ${total:.2f}")
                except mysql.connector.Error as error:c.rollback();messagebox.showerror("Planilla",str(error),parent=w)
                finally:
                    if cu:cu.close()
                    c.close()
            tk.Button(w,text="Guardar pago",command=guardar_pago,bg=VERDE,fg=BLANCO,relief="flat",pady=8).pack(fill="x",padx=22,pady=12)
        def historial_pagos():
            ident=empleado_id()
            if ident is None:return
            w=tk.Toplevel(ventana);w.title("Historial de pagos");w.geometry("850x390");w.configure(bg=CREMA)
            tk.Label(w,text="Historial de pagos",bg=CREMA,fg=VERDE_OSCURO,font=("Georgia",17,"bold")).pack(anchor="w",padx=18,pady=15)
            t=ttk.Treeview(w,columns=("periodo","base","bono","desc","total","fecha"),show="headings")
            for c,title,width in [("periodo","PERÍODO",180),("base","BASE",90),("bono","BONOS",80),("desc","DESCUENTOS",90),("total","TOTAL",90),("fecha","FECHA DE PAGO",130)]:t.heading(c,text=title);t.column(c,width=width,anchor="center")
            t.pack(fill="both",expand=True,padx=18,pady=(0,18));cx=conectar()
            if cx is None:return
            cur=None
            try:
                cur=cx.cursor();cur.execute("SELECT periodo_inicio,periodo_fin,salario_base,bonificaciones,descuentos,total_pagado,fecha_pago FROM pago_planilla WHERE id_empleado=%s ORDER BY fecha_pago DESC",(ident,))
                for r in cur.fetchall():t.insert("","end",values=(f"{r[0]} a {r[1]}",f"${r[2]:.2f}",f"${r[3]:.2f}",f"${r[4]:.2f}",f"${r[5]:.2f}",str(r[6])))
            except mysql.connector.Error as error:messagebox.showerror("Planilla",str(error),parent=w)
            finally:
                if cur:cur.close()
                cx.close()
        botones=tk.Frame(vista_actual,bg=CREMA);botones.pack(fill="x",pady=12)
        for text,cmd,color in [("Definir salario",configurar_salario,BEIGE),("Registrar pago",pagar,VERDE),("Historial de pagos",historial_pagos,VINO),("Actualizar",cargar,VERDE_OSCURO)]:tk.Button(botones,text=text,command=cmd,bg=color,fg=VERDE_OSCURO if color==BEIGE else BLANCO,relief="flat",padx=12,pady=8).pack(side="left",padx=(0,7))
        busqueda.trace_add("write",lambda *_:cargar());cargar()

    # =====================================================
    # REPORTES CON DATOS REALES
    # =====================================================
    def mostrar_reportes():
        limpiar_vista();activar_boton("REPORTES")
        tk.Label(vista_actual,text="Reportes",bg=CREMA,fg=VERDE_OSCURO,font=("Georgia",23,"bold")).pack(anchor="w",pady=(4,2))
        tk.Label(vista_actual,text="Ventas, reservas y platillos más vendidos",bg=CREMA,fg=GRIS,font=("Segoe UI",9)).pack(anchor="w",pady=(0,12))
        barra=tk.Frame(vista_actual,bg=CREMA);barra.pack(fill="x",pady=(0,12))
        periodo=tk.StringVar(value="Este mes")
        combo=ttk.Combobox(barra,textvariable=periodo,values=["Hoy","Esta semana","Este mes","Este año"],state="readonly",width=16);combo.pack(side="left",ipady=5)
        tarjetas=tk.Frame(vista_actual,bg=CREMA);tarjetas.pack(fill="x",pady=(0,14))
        datos={}
        for label in ["INGRESOS PAGADOS","FACTURAS PAGADAS","RESERVAS","ÓRDENES ENTREGADAS"]:
            card=tk.Frame(tarjetas,bg=BLANCO,highlightbackground=GRIS_CLARO,highlightthickness=1);card.pack(side="left",fill="x",expand=True,padx=(0,7))
            tk.Label(card,text=label,bg=BLANCO,fg=GRIS,font=("Segoe UI",8,"bold")).pack(anchor="w",padx=10,pady=(9,2))
            datos[label]=tk.Label(card,text="—",bg=BLANCO,fg=VERDE_OSCURO,font=("Georgia",17,"bold"));datos[label].pack(anchor="w",padx=10,pady=(0,9))
        tk.Label(vista_actual,text="PLATILLOS MÁS VENDIDOS",bg=CREMA,fg=VERDE_OSCURO,font=("Georgia",13,"bold")).pack(anchor="w",pady=(4,7))
        tabla=ttk.Treeview(vista_actual,columns=("platillo","cantidad","ventas"),show="headings")
        for c,t,w in [("platillo","PLATILLO",360),("cantidad","UNIDADES VENDIDAS",150),("ventas","VENTAS GENERADAS",160)]:tabla.heading(c,text=t);tabla.column(c,width=w,anchor="center" if c!="platillo" else "w")
        tabla.pack(fill="both",expand=True)
        def fechas():
            hoy=date.today();p=periodo.get()
            if p=="Hoy":return hoy,hoy
            if p=="Esta semana":return hoy-timedelta(days=hoy.weekday()),hoy
            if p=="Este año":return date(hoy.year,1,1),hoy
            return date(hoy.year,hoy.month,1),hoy
        def cargar(_event=None):
            tabla.delete(*tabla.get_children());inicio,fin=fechas();cx=conectar()
            if cx is None:return
            cur=None
            try:
                cur=cx.cursor()
                cur.execute("SELECT COALESCE(SUM(total),0),COUNT(*) FROM factura WHERE estado_pago='Pagado' AND DATE(fecha) BETWEEN %s AND %s",(inicio,fin));ingresos,facturas=cur.fetchone()
                cur.execute("SELECT COUNT(*) FROM reserva WHERE fecha BETWEEN %s AND %s AND estado<>'Cancelada'",(inicio,fin));reservas=cur.fetchone()[0]
                cur.execute("SELECT COUNT(*) FROM orden WHERE fecha BETWEEN %s AND %s AND estado='Entregado'",(inicio,fin));ordenes=cur.fetchone()[0]
                datos["INGRESOS PAGADOS"].config(text=f"${Decimal(str(ingresos)):.2f}");datos["FACTURAS PAGADAS"].config(text=str(facturas));datos["RESERVAS"].config(text=str(reservas));datos["ÓRDENES ENTREGADAS"].config(text=str(ordenes))
                cur.execute("""SELECT p.nombre,SUM(d.cantidad) AS unidades,SUM(d.subtotal) AS ventas
                    FROM detalle_orden d JOIN orden o ON o.id_orden=d.id_orden
                    JOIN platillo p ON p.id_platillo=d.id_platillo
                    JOIN factura f ON f.id_orden=o.id_orden
                    WHERE f.estado_pago='Pagado' AND DATE(f.fecha) BETWEEN %s AND %s
                    GROUP BY p.id_platillo,p.nombre ORDER BY unidades DESC LIMIT 10""",(inicio,fin))
                for r in cur.fetchall():tabla.insert("","end",values=(r[0],r[1],f"${Decimal(str(r[2])):.2f}"))
                if not tabla.get_children():tabla.insert("","end",values=("Sin ventas pagadas en este período",0,"$0.00"))
            except mysql.connector.Error as error:messagebox.showerror("Reportes",f"No se pudieron cargar los reportes.\n\n{error}")
            finally:
                if cur:cur.close()
                cx.close()
        combo.bind("<<ComboboxSelected>>",cargar)
        tk.Button(barra,text="Actualizar",command=cargar,bg=VERDE,fg=BLANCO,relief="flat",padx=14,pady=7).pack(side="left",padx=10)
        cargar()

    # =====================================================
    # VISTA TEMPORAL
    # =====================================================

    def vista_pendiente(nombre):

        limpiar_vista()
        activar_boton(nombre)

        tk.Label(
            vista_actual,
            text=nombre.title(),
            bg=CREMA,
            fg=VERDE_OSCURO,
            font=("Georgia", 22, "bold")
        ).pack(
            anchor="w",
            pady=(20, 5)
        )

        tk.Label(
            vista_actual,
            text="Esta sección se desarrollará a continuación.",
            bg=CREMA,
            fg=GRIS,
            font=("Segoe UI", 10)
        ).pack(
            anchor="w"
        )

    # =====================================================
    # MENÚ LATERAL
    # =====================================================

    crear_boton_menu(
        "INICIO",
        mostrar_inicio
    )

    crear_boton_menu(
        "CLIENTES",
        mostrar_clientes
    )

    crear_boton_menu(
        "RESERVACIONES",
        mostrar_reservaciones
    )

    crear_boton_menu(
        "MESAS",
        mostrar_mesas
    )

    crear_boton_menu(
        "MENÚ",
        mostrar_platillos
    )

    crear_boton_menu(
        "INVENTARIO",
        mostrar_inventario
    )

    crear_boton_menu(
        "PROVEEDORES",
        mostrar_proveedores
    )

    crear_boton_menu(
        "PLANILLA",
        mostrar_planilla
    )

    crear_boton_menu(
        "REPORTES",
        mostrar_reportes
    )

    # =====================================================
    # MOSTRAR INICIO AL ABRIR
    # =====================================================

    mostrar_inicio()

    # =====================================================
    # EJECUTAR VENTANA
    # =====================================================

    ventana.mainloop()


# =========================================================
# EJECUTAR ARCHIVO
# =========================================================

if __name__ == "__main__":
    interfaz_administrador()