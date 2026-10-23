import os
import subprocess
import sys
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime, timedelta
from decimal import Decimal

import mysql.connector

try:
    from PIL import Image, ImageTk
except ImportError:
    Image = None
    ImageTk = None

HOST = "localhost"
USER = "root"
PASSWORD = "sqldecami"
DATABASE = "restaurante_vivaldi"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


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
            "No se pudo conectar con MySQL.\n\n"
            f"{error}\n\n"
            "Revisa HOST, USER, PASSWORD y DATABASE."
        )
        return None

CREMA = "#fbf8f1"
CREMA_CLARO = "#fbf7f1"
BEIGE = "#d9bc8c"
VERDE = "#223d2d"
VERDE_OSCURO = "#12261c"
VINO = "#6b2333"
VINO_OSCURO = "#561b28"
BLANCO = "#ffffff"
GRIS = "#6f6f6f"
GRIS_CLARO = "#e8e3da"

def interfaz_mesero(usuario=None, rol=None):

    ventana = tk.Tk()
    ventana.state("zoomed")
    ventana.title("Restaurante Vivaldi | Mesero")
    ventana.configure(bg=CREMA)
    ventana.iconbitmap("vivaldi.ico")
    ventana.geometry("1100x720")
    ventana.resizable(False, False)

    id_empleado = None
    nombre_mesero = usuario or "Mesero"

    if usuario:
        conexion = conectar()

        if conexion:
            cursor = None

            try:
                cursor = conexion.cursor()

                cursor.execute(
                    """
                    SELECT id_empleado, nombre, apellido
                    FROM Empleado
                    WHERE usuario = %s
                      AND rol = 'Mesero'
                      AND activo = 1
                    """,
                    (usuario,)
                )

                empleado = cursor.fetchone()

                if empleado:
                    id_empleado = empleado[0]
                    nombre_mesero = (
                        f"{empleado[1]} {empleado[2]}"
                    )
                else:
                    messagebox.showerror(
                        "Acceso no válido",
                        "No se encontró un empleado activo "
                        "con el rol Mesero para este usuario."
                    )
                    ventana.destroy()
                    conexion.close()
                    return

            except mysql.connector.Error as error:
                messagebox.showerror(
                    "Error",
                    f"No se pudo identificar al mesero.\n\n{error}"
                )
                ventana.destroy()
                conexion.close()
                return

            finally:
                if cursor:
                    cursor.close()

            conexion.close()

    orden_actual = [None]
    mesa_actual = [None]
    cliente_actual = [None]

    estilo = ttk.Style(ventana)
    estilo.theme_use("clam")

    estilo.configure(
        "Treeview",
        background=BLANCO,
        foreground=VERDE_OSCURO,
        fieldbackground=BLANCO,
        rowheight=29,
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

    # =====================================================
    # ESTRUCTURA PRINCIPAL Y SIDEBAR
    # =====================================================

    contenedor = tk.Frame(
        ventana,
        bg=CREMA
    )
    contenedor.pack(fill="both", expand=True)

    sidebar = tk.Frame(
        contenedor,
        bg=VERDE_OSCURO,
        width=210
    )
    sidebar.pack(side="left", fill="y")
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
        if Image is None:
            raise ImportError

        imagen_logo = Image.open(
            os.path.join(BASE_DIR, "vivaldi_sf.png")
        )
        imagen_logo = imagen_logo.resize((150, 150))
        logo = ImageTk.PhotoImage(imagen_logo)

        etiqueta_logo = tk.Label(
            contenido_sidebar,
            image=logo,
            bg=VERDE_OSCURO
        )
        etiqueta_logo.image = logo
        etiqueta_logo.pack(pady=(0, 15))

    except Exception:
        tk.Label(
            contenido_sidebar,
            text="VIVALDI",
            bg=VERDE_OSCURO,
            fg=BEIGE,
            font=("Georgia", 24, "bold")
        ).pack(pady=(0, 35))

    tk.Label(
        contenido_sidebar,
        text="MESERO",
        bg=VERDE_OSCURO,
        fg=BEIGE,
        font=("Georgia", 14, "bold")
    ).pack(pady=(0, 8))

    menu_navegacion = tk.Frame(
        contenido_sidebar,
        bg=VERDE_OSCURO
    )
    menu_navegacion.pack(fill="x", padx=20)

    contenido = tk.Frame(
        contenedor,
        bg=CREMA
    )
    contenido.pack(side="left", fill="both", expand=True)

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

    panel_inicio = tk.Frame(area_central, bg=CREMA)
    panel_mesas = tk.Frame(area_central, bg=CREMA)
    panel_menu = tk.Frame(area_central, bg=CREMA)
    panel_cuenta = tk.Frame(area_central, bg=CREMA)

    def mostrar_panel(panel):
        for otro_panel in (
            panel_inicio,
            panel_mesas,
            panel_menu,
            panel_cuenta
        ):
            otro_panel.pack_forget()

        panel.pack(fill="both", expand=True)

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
        boton.pack(fill="x", pady=4)

        return boton

    # Los botones se asignan después de crear las funciones.
    boton_inicio = None
    boton_mesas = None
    boton_menu = None
    boton_cuenta = None

    def actualizar_menu(boton_activo):
        botones = [
            boton_inicio,
            boton_mesas,
            boton_menu,
            boton_cuenta
        ]

        for boton in botones:
            if boton is not None:
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

    # =====================================================
    # FUNCIONES VISUALES REUTILIZABLES
    # =====================================================

    def preparar_panel(panel, titulo, subtitulo):
        tk.Label(
            panel,
            text=titulo,
            bg=CREMA,
            fg=VERDE,
            font=("Georgia", 25, "bold")
        ).pack(anchor="w", pady=(5, 0))

        tk.Label(
            panel,
            text=subtitulo,
            bg=CREMA,
            fg=GRIS,
            font=("Arial", 10)
        ).pack(anchor="w", pady=(3, 8))

        tk.Frame(
            panel,
            bg=BEIGE,
            height=2
        ).pack(fill="x", pady=(0, 12))

    def crear_tarjeta(panel, titulo):
        tarjeta = tk.Frame(
            panel,
            bg=BLANCO,
            bd=1,
            relief="solid"
        )
        tarjeta.pack(fill="both", expand=True)

        encabezado = tk.Frame(
            tarjeta,
            bg=VERDE
        )
        encabezado.pack(fill="x")

        tk.Label(
            encabezado,
            text=titulo,
            bg=VERDE,
            fg=BLANCO,
            font=("Arial", 11, "bold")
        ).pack(anchor="w", padx=15, pady=10)

        return tarjeta

    def crear_boton(parent, texto, comando, color=VERDE):
        return tk.Button(
            parent,
            text=texto,
            command=comando,
            bg=color,
            fg=BLANCO,
            activebackground=VERDE_OSCURO,
            activeforeground=BLANCO,
            bd=0,
            relief="flat",
            font=("Arial", 9, "bold"),
            padx=12,
            pady=8,
            cursor="hand2"
        )

    # =====================================================
    # CONSULTAS A LA BASE DE DATOS
    # =====================================================

    def consultar(sql, parametros=()):
        conexion = conectar()

        if not conexion:
            return None

        cursor = None

        try:
            cursor = conexion.cursor()
            cursor.execute(sql, parametros)
            return cursor.fetchall()

        except mysql.connector.Error as error:
            messagebox.showerror(
                "Error de base de datos",
                str(error)
            )
            return None

        finally:
            if cursor:
                cursor.close()
            conexion.close()

    # =====================================================
    # INICIO
    # =====================================================

    preparar_panel(
        panel_inicio,
        "Panel del Mesero",
        "Consulta tus mesas y administra los pedidos del restaurante."
    )

    tarjeta_inicio = crear_tarjeta(
        panel_inicio,
        "RESUMEN DE SERVICIO"
    )

    cuerpo_inicio = tk.Frame(
        tarjeta_inicio,
        bg=BLANCO
    )
    cuerpo_inicio.pack(
        fill="both",
        expand=True,
        padx=20,
        pady=20
    )

    franja_bienvenida = tk.Frame(cuerpo_inicio, bg=VERDE_OSCURO)
    franja_bienvenida.pack(fill="x", pady=(0, 16))

    tk.Frame(
        franja_bienvenida,
        bg=BEIGE,
        width=6
    ).pack(side="left", fill="y")

    texto_bienvenida = tk.Frame(franja_bienvenida, bg=VERDE_OSCURO)
    texto_bienvenida.pack(side="left", fill="x", expand=True, padx=16, pady=14)

    etiqueta_bienvenida = tk.Label(
        texto_bienvenida,
        text=f"Bienvenido/a, {nombre_mesero}",
        bg=VERDE_OSCURO,
        fg=CREMA_CLARO,
        font=("Georgia", 19, "bold")
    )
    etiqueta_bienvenida.pack(anchor="w", pady=(0, 4))

    tk.Label(
        texto_bienvenida,
        text="Organiza tus mesas, continúa pedidos y revisa las cuentas activas.",
        bg=VERDE_OSCURO,
        fg=BEIGE,
        font=("Arial", 10)
    ).pack(anchor="w")

    etiqueta_fecha = tk.Label(
        cuerpo_inicio,
        text=f"Fecha de servicio: {date.today():%d/%m/%Y}",
        bg=BLANCO,
        fg=GRIS,
        font=("Arial", 10)
    )
    etiqueta_fecha.pack(anchor="w", pady=(0, 18))

    resumen_mesas = tk.Label(
        cuerpo_inicio,
        text="RESERVAS ATENDIDAS     —",
        bg=CREMA_CLARO,
        fg=VERDE,
        font=("Arial", 12, "bold"),
        padx=14,
        pady=12,
        anchor="w"
    )
    resumen_mesas.pack(fill="x", pady=6)

    resumen_pedidos = tk.Label(
        cuerpo_inicio,
        text="TUS PEDIDOS ACTIVOS     —",
        bg=CREMA_CLARO,
        fg=VERDE,
        font=("Arial", 12, "bold"),
        padx=14,
        pady=12,
        anchor="w"
    )
    resumen_pedidos.pack(fill="x", pady=6)

    def actualizar_inicio():
        reservas = consultar(
            """
            SELECT COUNT(*)
            FROM Orden
            WHERE id_empleado = %s
              AND fecha = %s
            """,
            (id_empleado, date.today())
        ) if id_empleado is not None else [(0,)]

        if reservas is not None:
            resumen_mesas.config(
                text=f"RESERVAS ATENDIDAS     {reservas[0][0]}"
            )

        if id_empleado is not None:
            pedidos = consultar(
                """
                SELECT COUNT(*)
                FROM Orden
                WHERE id_empleado = %s
                  AND fecha = %s
                  AND estado IN ('Pendiente', 'Preparando', 'Entregado')
                  AND pedido_finalizado = 0
                """,
                (id_empleado, date.today())
            )

            if pedidos is not None:
                cantidad = min(pedidos[0][0], 2)
                resumen_pedidos.config(
                    text=f"TUS PEDIDOS ACTIVOS     {cantidad} / 2"
                )

    crear_boton(
        cuerpo_inicio,
        "VER MESAS Y RESERVAS",
        lambda: cambiar_seccion("MESAS")
    ).pack(anchor="w", pady=(22, 0))

    # =====================================================
    # MESAS Y RESERVAS
    # =====================================================

    preparar_panel(
        panel_mesas,
        "Mesas y reservas",
        "Selecciona una reserva confirmada para comenzar a atender."
    )

    tarjeta_mesas = crear_tarjeta(
        panel_mesas,
        "RESERVAS DEL DÍA"
    )

    cuerpo_mesas = tk.Frame(
        tarjeta_mesas,
        bg=BLANCO
    )
    cuerpo_mesas.pack(
        fill="both",
        expand=True,
        padx=12,
        pady=12
    )

    columnas_reservas = (
        "id_reserva", "hora", "cliente",
        "mesa", "personas", "estado", "forma_pago"
    )

    tabla_reservas = ttk.Treeview(
        cuerpo_mesas,
        columns=columnas_reservas,
        show="headings",
        height=12
    )

    encabezados_reservas = {
        "id_reserva": ("Reserva", 65),
        "hora": ("Hora", 75),
        "cliente": ("Cliente", 190),
        "mesa": ("Mesa", 70),
        "personas": ("Personas", 75),
        "estado": ("Estado", 105),
        "forma_pago": ("Forma de pago", 115)

    }

    for columna, (texto, ancho) in encabezados_reservas.items():
        tabla_reservas.heading(columna, text=texto)
        tabla_reservas.column(
            columna,
            width=ancho,
            anchor="center"
        )

    tabla_reservas.pack(
        fill="both",
        expand=True
    )

    tk.Label(
        cuerpo_mesas,
        text=(
            "Selecciona una fila y pulsa «Atender reserva». "
            "Las reservas canceladas no se muestran."
        ),
        bg=BLANCO,
        fg=GRIS,
        font=("Arial", 9)
    ).pack(anchor="w", pady=(10, 5))

    def cargar_reservas():
        for fila in tabla_reservas.get_children():
            tabla_reservas.delete(fila)

        resultados = consultar(
            """
            SELECT
                r.id_reserva,
                r.hora,
                c.nombre,
                c.apellido,
                m.numero_mesa,
                r.cantidad_personas,
                r.estado,
                r.forma_pago
            FROM Reserva r
            INNER JOIN Cliente c
                ON c.id_cliente = r.id_cliente
            INNER JOIN Mesa m
                ON m.id_mesa = r.id_mesa
            WHERE r.fecha = %s
              AND r.estado = 'Confirmada'
            ORDER BY r.hora, m.numero_mesa
            """,
            (date.today(),)
        )

        if resultados is None:
            return

        for fila in resultados:
            (
                id_reserva,
                hora,
                nombre,
                apellido,
                numero_mesa,
                personas,
                estado,
                forma_pago
            ) = fila

            if isinstance(hora, timedelta):
                hora = (datetime.min + hora).time()

            hora_texto = (
                hora.strftime("%H:%M")
                if hasattr(hora, "strftime")
                else str(hora)[:5]
            )

            tabla_reservas.insert(
                "",
                "end",
                values=(
                    id_reserva,
                    hora_texto,
                    f"{nombre} {apellido}",
                    numero_mesa,
                    personas,
                    estado,
                    forma_pago or "Efectivo"

                )
            )

    def atender_reserva():
        seleccion = tabla_reservas.selection()

        if not seleccion:
            messagebox.showwarning(
                "Selecciona una reserva",
                "Primero selecciona una reserva de la tabla."
            )
            return

        valores = tabla_reservas.item(
            seleccion[0],
            "values"
        )

        id_reserva = int(valores[0])

        if id_empleado is None:
            messagebox.showerror(
                "Sesión no identificada",
                "No se puede asociar la orden a un mesero. "
                "Debes abrir esta vista desde el inicio de sesión "
                "pasando el nombre de usuario."
            )
            return

        conexion = conectar()

        if not conexion:
            return

        cursor = None

        try:
            cursor = conexion.cursor()
            conexion.start_transaction()

            # Bloquea la fila de la reserva mientras se comprueba
            # si otro mesero ya inició un pedido en esa mesa.
            cursor.execute(
                """
                SELECT r.id_cliente, r.id_mesa, r.hora,
                    m.numero_mesa, c.nombre, c.apellido
                FROM Reserva r
                INNER JOIN Mesa m
                    ON m.id_mesa = r.id_mesa
                INNER JOIN Cliente c
                    ON c.id_cliente = r.id_cliente
                WHERE r.id_reserva = %s
                  AND r.fecha = %s
                  AND r.estado = 'Confirmada'
                FOR UPDATE
                """,
                (id_reserva, date.today())
            )

            reserva = cursor.fetchone()

            if not reserva:
                conexion.rollback()
                messagebox.showwarning(
                    "Reserva no disponible",
                    "La reserva ya no está confirmada. "
                    "Actualiza la lista e inténtalo de nuevo."
                )
                return

            (
                id_cliente,
                id_mesa,
                hora_reserva,
                numero_mesa,
                nombre,
                apellido
            ) = reserva

            # MySQL devuelve las columnas TIME como timedelta.
            if isinstance(hora_reserva, timedelta):
                hora_reserva = (datetime.min + hora_reserva).time()

            # Comprobar que ya llegó la hora de la reserva.
            hora_actual = datetime.now().time().replace(microsecond=0)

            if hora_actual < hora_reserva:
                conexion.rollback()

                messagebox.showwarning(
                    "Reserva todavía no disponible",
                    f"La reserva de la mesa {numero_mesa} "
                    f"está programada para las "
                    f"{hora_reserva.strftime('%H:%M')}.\n\n"
                    "Podrás comenzar a tomar el pedido "
                    "cuando llegue la hora de la reserva."
                )
                return

            cursor.execute(
                """
                SELECT id_mesa
                FROM Mesa
                WHERE id_mesa = %s
                FOR UPDATE
                """,
                (id_mesa,)
            )
            cursor.fetchone()

            cursor.execute(
                """
                SELECT id_orden, id_empleado
                FROM Orden
                WHERE id_reserva = %s
                  AND estado IN ('Pendiente', 'Preparando', 'Entregado')
                  AND pedido_finalizado = 0
                LIMIT 1
                FOR UPDATE
                """,
                (id_reserva,)
            )

            orden_existente = cursor.fetchone()

            if orden_existente:
                id_orden_existente, empleado_existente = orden_existente

                if empleado_existente != id_empleado:
                    conexion.rollback()
                    messagebox.showwarning(
                        "Mesa atendida",
                        "Otro mesero ya tiene una orden activa "
                        "para esta reserva."
                    )
                    return

                conexion.commit()

                orden_actual[0] = id_orden_existente
                mesa_actual[0] = id_mesa
                cliente_actual[0] = f"{nombre} {apellido}"

                cambiar_seccion("MENU")

                messagebox.showinfo(
                    "Orden recuperada",
                    f"Continúas atendiendo la mesa {numero_mesa}."
                )
                return

            # Comprobar si la mesa tiene otra orden activa,
            # aunque pertenezca a una reserva diferente.
            cursor.execute(
                """
                SELECT id_orden
                FROM Orden
                WHERE id_mesa = %s
                  AND estado IN ('Pendiente', 'Preparando', 'Entregado')
                  AND pedido_finalizado = 0
                  AND (id_reserva IS NULL OR id_reserva != %s)
                LIMIT 1
                FOR UPDATE
                """,
                (id_mesa, id_reserva)
            )

            otra_orden = cursor.fetchone()

            if otra_orden:
                conexion.rollback()
                messagebox.showwarning(
                    "Mesa con una orden activa",
                    "Esta mesa tiene otra orden pendiente. "
                    "Revisa su estado antes de atender la reserva."
                )
                return

            ahora = datetime.now()

            cursor.execute(
                """
                INSERT INTO Orden (
                    fecha,
                    hora,
                    tipo_pedido,
                    estado,
                    id_cliente,
                    id_mesa,
                    id_empleado,
                    id_reserva
                )
                VALUES (%s, %s, 'Local', 'Pendiente', %s, %s, %s, %s)
                """,
                (
                    ahora.date(),
                    ahora.time().replace(microsecond=0),
                    id_cliente,
                    id_mesa,
                    id_empleado,
                    id_reserva
                )
            )

            nuevo_id_orden = cursor.lastrowid

            # Marcar la mesa como ocupada.
            cursor.execute(
                """
                UPDATE Mesa
                SET estado = 'Ocupada'
                WHERE id_mesa = %s
                  AND estado IN ('Disponible', 'Reservada')
                """,
                (id_mesa,)
            )

            if cursor.rowcount != 1:
                conexion.rollback()
                messagebox.showwarning(
                    "Mesa no disponible",
                    "No se pudo ocupar la mesa. "
                    "Actualiza las reservas e inténtalo nuevamente."
                )
                return

            conexion.commit()

            orden_actual[0] = nuevo_id_orden
            mesa_actual[0] = id_mesa
            cliente_actual[0] = f"{nombre} {apellido}"

            cargar_reservas()
            actualizar_inicio()
            cambiar_seccion("MENU")

            messagebox.showinfo(
                "Orden iniciada",
                f"Orden #{nuevo_id_orden}\n"
                f"Cliente: {nombre} {apellido}\n"
                f"Mesa: {numero_mesa}"
            )

        except mysql.connector.Error as error:
            conexion.rollback()
            messagebox.showerror(
                "Error al asignar la mesa",
                "No se pudo iniciar la orden.\n\n"
                f"{error}"
            )

        finally:
            if cursor:
                cursor.close()
            conexion.close()

    crear_boton(
        cuerpo_mesas,
        "ATENDER RESERVA",
        atender_reserva
    ).pack(anchor="e", pady=(10, 0))

    # =====================================================
    # MENÚ DE PLATILLOS - VISTA DEL MESERO
    # =====================================================

    categorias_menu = [
        "Antipasti",
        "Primi",
        "Secondi",
        "Dolci & Vini"
    ]

    platillo_seleccionado = [None]

    # Caché de fotos: evita releer las imágenes del disco cada vez
    # que se abre el menú, y mantiene viva la referencia de Tkinter.
    cache_fotos = {}

    tarjetas_menu = {}
    botones_seleccion_menu = {}

    preparar_panel(
        panel_menu,
        "Menú del Restaurante",
        "Explora nuestras especialidades y agrégalas a la cuenta de tu mesa."
    )

    tarjeta_menu = crear_tarjeta(
        panel_menu,
        "NUESTRAS ESPECIALIDADES"
    )

    cuerpo_menu = tk.Frame(
        tarjeta_menu,
        bg=BLANCO
    )
    cuerpo_menu.pack(
        fill="both",
        expand=True,
        padx=12,
        pady=10
    )

    etiqueta_orden = tk.Label(
        cuerpo_menu,
        text="Primero selecciona una reserva en MESAS.",
        bg=BLANCO,
        fg=VINO,
        font=("Arial", 10, "bold"),
        anchor="w"
    )
    etiqueta_orden.pack(fill="x", pady=(0, 8))

    # Área desplazable de tarjetas.
    marco_lista_menu = tk.Frame(
        cuerpo_menu,
        bg=CREMA
    )
    marco_lista_menu.pack(
        fill="both",
        expand=True
    )

    canvas_menu = tk.Canvas(
        marco_lista_menu,
        bg=CREMA,
        highlightthickness=0
    )

    barra_scroll_menu = ttk.Scrollbar(
        marco_lista_menu,
        orient="vertical",
        command=canvas_menu.yview
    )

    canvas_menu.configure(
        yscrollcommand=barra_scroll_menu.set
    )

    barra_scroll_menu.pack(side="right", fill="y")
    canvas_menu.pack(side="left", fill="both", expand=True)

    marco_tarjetas_menu = tk.Frame(
        canvas_menu,
        bg=CREMA
    )

    ventana_tarjetas_menu = canvas_menu.create_window(
        (0, 0),
        window=marco_tarjetas_menu,
        anchor="nw"
    )

    def actualizar_scroll_menu(event=None):
        canvas_menu.configure(
            scrollregion=canvas_menu.bbox("all")
        )

    def ajustar_ancho_menu(event):
        canvas_menu.itemconfigure(
            ventana_tarjetas_menu,
            width=event.width
        )

    marco_tarjetas_menu.bind(
        "<Configure>",
        actualizar_scroll_menu
    )

    canvas_menu.bind(
        "<Configure>",
        ajustar_ancho_menu
    )

    # Rueda del ratón compatible con Windows, macOS y Linux.
    def desplazar_menu(event):
        if event.num == 4:
            pasos = -1
        elif event.num == 5:
            pasos = 1
        else:
            pasos = -1 if event.delta > 0 else 1

        canvas_menu.yview_scroll(pasos, "units")

    def activar_scroll_menu(event):
        canvas_menu.bind_all("<MouseWheel>", desplazar_menu)
        canvas_menu.bind_all("<Button-4>", desplazar_menu)
        canvas_menu.bind_all("<Button-5>", desplazar_menu)

    def desactivar_scroll_menu(event):
        canvas_menu.unbind_all("<MouseWheel>")
        canvas_menu.unbind_all("<Button-4>")
        canvas_menu.unbind_all("<Button-5>")

    canvas_menu.bind("<Enter>", activar_scroll_menu)
    canvas_menu.bind("<Leave>", desactivar_scroll_menu)

    # Seleccionar una tarjeta sin agregarla todavía a la cuenta.
    def seleccionar_platillo(id_platillo):
        platillo_seleccionado[0] = id_platillo

        for id_tarjeta, tarjeta in tarjetas_menu.items():
            seleccionado = id_tarjeta == id_platillo

            tarjeta.configure(
                highlightbackground=(
                    VINO if seleccionado else GRIS_CLARO
                ),
                highlightthickness=(
                    3 if seleccionado else 1
                )
            )

        for id_tarjeta, boton in botones_seleccion_menu.items():
            if id_tarjeta == id_platillo:
                boton.configure(
                    text="SELECCIONADO",
                    bg=VINO
                )
            else:
                boton.configure(
                    text="SELECCIONAR",
                    bg=VERDE
                )

    def obtener_foto(imagen_url):
        """Devuelve la foto (PhotoImage) del platillo o None."""
        if not imagen_url or Image is None or ImageTk is None:
            return None

        # imagen_url es una ruta de archivo dentro del proyecto,
        # por ejemplo "imagenes_menu/foto.jpg" (no una URL de internet).
        ruta_imagen = str(imagen_url).strip()

        if not os.path.isabs(ruta_imagen):
            ruta_imagen = os.path.join(BASE_DIR, ruta_imagen)

        if ruta_imagen in cache_fotos:
            return cache_fotos[ruta_imagen]

        if not os.path.isfile(ruta_imagen):
            return None

        try:
            imagen = Image.open(ruta_imagen).convert("RGB")
            imagen.thumbnail((100, 105))
            foto = ImageTk.PhotoImage(imagen)
        except (OSError, ValueError):
            return None

        cache_fotos[ruta_imagen] = foto
        return foto

    # Cargar los platillos disponibles desde la base de datos.
    def cargar_menu():

        for widget in marco_tarjetas_menu.winfo_children():
            widget.destroy()

        tarjetas_menu.clear()
        botones_seleccion_menu.clear()
        platillo_seleccionado[0] = None

        resultados = consultar(
            """
            SELECT
                id_platillo,
                nombre,
                descripcion,
                precio,
                categoria,
                imagen_url,
                vegetariano,
                sin_gluten,
                distintivo
            FROM Platillo
            WHERE disponibilidad = 'Disponible'
            ORDER BY nombre
            """
        )

        if resultados is None:
            return

        if not resultados:
            tk.Label(
                marco_tarjetas_menu,
                text="No hay platillos disponibles por el momento.",
                font=("Arial", 12),
                bg=CREMA,
                fg=GRIS,
                pady=30
            ).pack(fill="x")

            actualizar_scroll_menu()
            return

        # -------------------------------------------------
        # AGRUPAR LOS PLATILLOS POR CATEGORÍA
        # -------------------------------------------------

        agrupados = {
            categoria: [] for categoria in categorias_menu
        }

        for platillo in resultados:

            categoria_bd = (
                str(platillo[4] or "").strip().casefold()
            )

            for categoria in categorias_menu:

                if categoria_bd == categoria.casefold():
                    agrupados[categoria].append(platillo)
                    break

        # -------------------------------------------------
        # MOSTRAR CADA CATEGORÍA
        # -------------------------------------------------

        for categoria in categorias_menu:

            lista = agrupados[categoria]

            if not lista:
                continue

            # Encabezado de categoría.
            encabezado = tk.Frame(
                marco_tarjetas_menu,
                bg=CREMA
            )
            encabezado.pack(
                fill="x",
                padx=12,
                pady=(16, 5)
            )

            tk.Label(
                encabezado,
                text=categoria,
                font=("Georgia", 19, "bold"),
                bg=CREMA,
                fg=VERDE_OSCURO
            ).pack(side="left")

            tk.Frame(
                encabezado,
                bg=BEIGE,
                height=2
            ).pack(
                side="left",
                fill="x",
                expand=True,
                padx=(12, 0),
                pady=7
            )

            # Dos tarjetas por fila.
            fila_tarjetas = tk.Frame(
                marco_tarjetas_menu,
                bg=CREMA
            )
            fila_tarjetas.pack(
                fill="x",
                padx=6
            )

            fila_tarjetas.grid_columnconfigure(0, weight=1)
            fila_tarjetas.grid_columnconfigure(1, weight=1)

            for indice, platillo in enumerate(lista):

                (
                    id_platillo,
                    nombre,
                    descripcion,
                    precio,
                    categoria_bd,
                    imagen_url,
                    vegetariano,
                    sin_gluten,
                    distintivo
                ) = platillo

                tarjeta = tk.Frame(
                    fila_tarjetas,
                    bg=BLANCO,
                    highlightbackground=GRIS_CLARO,
                    highlightthickness=1,
                    padx=9,
                    pady=9
                )

                tarjeta.grid(
                    row=indice // 2,
                    column=indice % 2,
                    padx=5,
                    pady=5,
                    sticky="nsew"
                )

                tarjetas_menu[id_platillo] = tarjeta

                # ---------------------------------------------
                # FOTOGRAFÍA DEL PLATILLO
                # ---------------------------------------------

                marco_foto = tk.Frame(
                    tarjeta,
                    bg=CREMA_CLARO,
                    width=100,
                    height=105
                )
                marco_foto.pack(
                    side="left",
                    padx=(0, 9)
                )
                marco_foto.pack_propagate(False)

                foto = obtener_foto(imagen_url)

                if foto is not None:
                    tk.Label(
                        marco_foto,
                        image=foto,
                        bg=CREMA_CLARO
                    ).pack(expand=True)
                else:
                    tk.Label(
                        marco_foto,
                        text="Sin imagen",
                        bg=CREMA_CLARO,
                        fg=GRIS,
                        font=("Arial", 9)
                    ).pack(
                        expand=True,
                        fill="both"
                    )

                # ---------------------------------------------
                # INFORMACIÓN DEL PLATILLO
                # ---------------------------------------------

                info = tk.Frame(
                    tarjeta,
                    bg=BLANCO
                )
                info.pack(
                    side="left",
                    fill="both",
                    expand=True
                )

                tk.Label(
                    info,
                    text=nombre,
                    font=("Arial", 10, "bold"),
                    bg=BLANCO,
                    fg=VERDE_OSCURO,
                    anchor="w",
                    justify="left",
                    wraplength=175
                ).pack(fill="x")

                tk.Label(
                    info,
                    text=(
                        descripcion
                        if descripcion
                        else "Especialidad de la casa"
                    ),
                    font=("Arial", 8),
                    bg=BLANCO,
                    fg=GRIS,
                    anchor="w",
                    justify="left",
                    wraplength=175
                ).pack(
                    fill="x",
                    pady=(4, 5)
                )

                # ---------------------------------------------
                # ETIQUETAS
                # ---------------------------------------------

                etiquetas = []

                if vegetariano:
                    etiquetas.append("Vegetariano")

                if sin_gluten:
                    etiquetas.append("Sin gluten")

                if distintivo:
                    etiquetas.append(str(distintivo))

                if etiquetas:
                    tk.Label(
                        info,
                        text=" · ".join(etiquetas),
                        font=("Arial", 8, "bold"),
                        bg=BLANCO,
                        fg=VINO,
                        anchor="w",
                        justify="left",
                        wraplength=175
                    ).pack(
                        fill="x",
                        pady=(0, 4)
                    )

                # ---------------------------------------------
                # PRECIO
                # ---------------------------------------------

                tk.Label(
                    info,
                    text=f"${Decimal(str(precio)):.2f}",
                    font=("Georgia", 13, "bold"),
                    bg=BLANCO,
                    fg=VINO,
                    anchor="w"
                ).pack(
                    fill="x",
                    pady=(2, 6)
                )

                # ---------------------------------------------
                # BOTÓN SELECCIONAR
                # ---------------------------------------------

                boton_seleccionar = tk.Button(
                    info,
                    text="SELECCIONAR",
                    bg=VERDE,
                    fg=BLANCO,
                    activebackground=VERDE_OSCURO,
                    activeforeground=BLANCO,
                    font=("Arial", 8, "bold"),
                    relief="flat",
                    bd=0,
                    padx=8,
                    pady=6,
                    cursor="hand2",
                    command=lambda pid=id_platillo:
                    seleccionar_platillo(pid)
                )
                boton_seleccionar.pack(anchor="w")

                botones_seleccion_menu[id_platillo] = boton_seleccionar

        actualizar_scroll_menu()

    # Cantidad y botón para agregar a la cuenta.
    marco_agregar = tk.Frame(
        cuerpo_menu,
        bg=BLANCO
    )
    marco_agregar.pack(fill="x", pady=(9, 0))

    tk.Label(
        marco_agregar,
        text="Cantidad:",
        bg=BLANCO,
        fg=VERDE_OSCURO,
        font=("Arial", 9, "bold")
    ).pack(side="left", padx=(0, 7))

    cantidad_platillo = tk.IntVar(value=1)

    selector_cantidad = tk.Spinbox(
        marco_agregar,
        from_=1,
        to=20,
        width=4,
        textvariable=cantidad_platillo,
        font=("Arial", 10)
    )
    selector_cantidad.pack(side="left")

    def agregar_platillo():
        if orden_actual[0] is None:
            messagebox.showwarning(
                "Sin orden activa",
                "Primero selecciona una reserva en MESAS."
            )
            return

        if platillo_seleccionado[0] is None:
            messagebox.showwarning(
                "Selecciona un platillo",
                "Pulsa SELECCIONAR en el platillo que deseas agregar."
            )
            return

        if id_empleado is None:
            messagebox.showerror(
                "Sesión no identificada",
                "No se pudo identificar al mesero."
            )
            return

        try:
            cantidad = int(cantidad_platillo.get())

            if cantidad < 1:
                raise ValueError

        except (ValueError, tk.TclError):
            messagebox.showwarning(
                "Cantidad inválida",
                "Introduce una cantidad entera mayor que cero."
            )
            return

        id_platillo = platillo_seleccionado[0]

        conexion = conectar()

        if not conexion:
            return

        cursor = None

        try:
            cursor = conexion.cursor()
            conexion.start_transaction()

            cursor.execute(
                """
                SELECT id_orden
                FROM Orden
                WHERE id_orden = %s
                  AND id_empleado = %s
                  AND estado IN ('Pendiente', 'Preparando')
                  AND pedido_finalizado = 0
                FOR UPDATE
                """,
                (orden_actual[0], id_empleado)
            )

            orden = cursor.fetchone()

            if not orden:
                conexion.rollback()
                messagebox.showwarning(
                    "Orden no disponible",
                    "La orden ya no está activa o no pertenece "
                    "al mesero que inició sesión."
                )
                return

            cursor.execute(
                """
                SELECT precio
                FROM Platillo
                WHERE id_platillo = %s
                  AND disponibilidad = 'Disponible'
                """,
                (id_platillo,)
            )

            platillo = cursor.fetchone()

            if not platillo:
                conexion.rollback()

                messagebox.showwarning(
                    "Platillo no disponible",
                    "Este platillo ya no está disponible."
                )

                cargar_menu()
                return

            precio = Decimal(str(platillo[0]))
            subtotal = precio * cantidad

            # Si el platillo ya está en la cuenta, se suma a la
            # fila existente en lugar de crear una fila repetida.
            cursor.execute(
                """
                SELECT id_detalle
                FROM Detalle_Orden
                WHERE id_orden = %s
                  AND id_platillo = %s
                LIMIT 1
                FOR UPDATE
                """,
                (orden_actual[0], id_platillo)
            )

            detalle_existente = cursor.fetchone()

            if detalle_existente:
                cursor.execute(
                    """
                    UPDATE Detalle_Orden
                    SET cantidad = cantidad + %s,
                        subtotal = subtotal + %s
                    WHERE id_detalle = %s
                    """,
                    (cantidad, subtotal, detalle_existente[0])
                )
            else:
                cursor.execute(
                    """
                    INSERT INTO Detalle_Orden (
                        cantidad,
                        subtotal,
                        id_orden,
                        id_platillo
                    )
                    VALUES (%s, %s, %s, %s)
                    """,
                    (
                        cantidad,
                        subtotal,
                        orden_actual[0],
                        id_platillo
                    )
                )

            conexion.commit()

            cargar_detalles_orden()

            messagebox.showinfo(
                "Platillo agregado",
                f"Se agregaron {cantidad} unidad(es) "
                "a la cuenta correctamente."
            )

        except mysql.connector.Error as error:
            conexion.rollback()

            messagebox.showerror(
                "Error",
                f"No se pudo agregar el platillo.\n\n{error}"
            )

        finally:
            if cursor:
                cursor.close()

            conexion.close()

    crear_boton(
        marco_agregar,
        "AGREGAR A LA CUENTA",
        agregar_platillo,
        color=VINO
    ).pack(side="right")

    # =====================================================
    # MI CUENTA
    # =====================================================

    preparar_panel(
        panel_cuenta,
        "Mi cuenta",
        "Consulta los platillos registrados en la orden actual."
    )

    tarjeta_cuenta = crear_tarjeta(
        panel_cuenta,
        "DETALLE DE LA ORDEN"
    )

    cuerpo_cuenta = tk.Frame(
        tarjeta_cuenta,
        bg=BLANCO
    )
    cuerpo_cuenta.pack(
        fill="both",
        expand=True,
        padx=12,
        pady=12
    )

    etiqueta_cliente_cuenta = tk.Label(
        cuerpo_cuenta,
        text="Cliente: —     Mesa: —     Orden: —",
        bg=BLANCO,
        fg=VERDE_OSCURO,
        font=("Arial", 10, "bold")
    )
    etiqueta_cliente_cuenta.pack(
        anchor="w",
        pady=(0, 10)
    )

    columnas_detalle = (
        "id_detalle",
        "platillo",
        "cantidad",
        "subtotal"
    )

    tabla_detalle = ttk.Treeview(
        cuerpo_cuenta,
        columns=columnas_detalle,
        show="headings",
        height=11
    )

    encabezados_detalle = {
        "id_detalle": ("Detalle", 65),
        "platillo": ("Platillo", 300),
        "cantidad": ("Cantidad", 100),
        "subtotal": ("Subtotal", 120)
    }

    for columna, (texto, ancho) in encabezados_detalle.items():
        tabla_detalle.heading(columna, text=texto)
        tabla_detalle.column(
            columna,
            width=ancho,
            anchor="center"
        )

    tabla_detalle.pack(
        fill="both",
        expand=True
    )

    barra_inferior_cuenta = tk.Frame(
        cuerpo_cuenta,
        bg=BLANCO
    )
    barra_inferior_cuenta.pack(
        fill="x",
        pady=(15, 5)
    )

    boton_quitar_platillo = crear_boton(
        barra_inferior_cuenta,
        "QUITAR PLATILLO",
        lambda: quitar_platillo(),
        color=VINO
    )
    boton_quitar_platillo.pack(side="left")

    boton_cobrar = crear_boton(
        barra_inferior_cuenta,
        "COBRAR CUENTA",
        lambda: cobrar_cuenta(),
        color=VINO
    )
    boton_cobrar.pack(side="left", padx=(8, 0))

    etiqueta_total = tk.Label(
        barra_inferior_cuenta,
        text="TOTAL: $0.00",
        bg=BLANCO,
        fg=VERDE,
        font=("Georgia", 18, "bold")
    )
    etiqueta_total.pack(side="right")

    def actualizar_seleccion():
        if orden_actual[0] is None:
            etiqueta_orden.config(
                text="Primero selecciona una reserva en MESAS."
            )
            etiqueta_cliente_cuenta.config(
                text="Cliente: —     Mesa: —     Orden: —"
            )
            return

        numero_mesa = consultar(
            """
            SELECT numero_mesa
            FROM Mesa
            WHERE id_mesa = %s
            """,
            (mesa_actual[0],)
        )

        numero = numero_mesa[0][0] if numero_mesa else "—"

        etiqueta_orden.config(
            text=(
                f"Orden #{orden_actual[0]}  |  "
                f"Mesa {numero}  |  Cliente: {cliente_actual[0]}"
            )
        )

        etiqueta_cliente_cuenta.config(
            text=(
                f"Cliente: {cliente_actual[0]}     "
                f"Mesa: {numero}     "
                f"Orden: #{orden_actual[0]}"
            )
        )

        estado_orden = consultar(
            "SELECT estado FROM Orden WHERE id_orden = %s AND id_empleado = %s",
            (orden_actual[0], id_empleado)
        )

        se_puede_quitar = bool(
            estado_orden and estado_orden[0][0] == "Pendiente"
        )

        if se_puede_quitar:
            if not boton_quitar_platillo.winfo_manager():
                boton_quitar_platillo.pack(side="left")
        else:
            boton_quitar_platillo.pack_forget()

    def cargar_detalles_orden():
        for fila in tabla_detalle.get_children():
            tabla_detalle.delete(fila)

        if orden_actual[0] is None:
            etiqueta_total.config(text="TOTAL: $0.00")
            actualizar_seleccion()
            return

        resultados = consultar(
            """
            SELECT
                d.id_detalle,
                p.nombre,
                d.cantidad,
                d.subtotal
            FROM Detalle_Orden d
            INNER JOIN Platillo p
                ON p.id_platillo = d.id_platillo
            WHERE d.id_orden = %s
            ORDER BY d.id_detalle
            """,
            (orden_actual[0],)
        )

        if resultados is None:
            return

        total = Decimal("0.00")

        for id_detalle, nombre, cantidad, subtotal in resultados:
            subtotal = Decimal(str(subtotal))
            total += subtotal

            tabla_detalle.insert(
                "",
                "end",
                values=(
                    id_detalle,
                    nombre,
                    cantidad,
                    f"${subtotal:.2f}"
                )
            )

        etiqueta_total.config(
            text=f"TOTAL: ${total:.2f}"
        )

        actualizar_seleccion()

    def cobrar_cuenta():
        # Comprobar que se seleccionó una orden.
        if orden_actual[0] is None:
            messagebox.showwarning(
                "Sin cuenta seleccionada",
                "Selecciona una cuenta activa antes de cobrar."
            )
            return

        if id_empleado is None:
            messagebox.showerror(
                "Error",
                "No se pudo identificar al mesero."
            )
            return

        id_orden = orden_actual[0]

        # Consultar la orden, su reserva y la forma de pago.
        datos = consultar(
            """
            SELECT o.id_orden, o.id_mesa, o.id_reserva,
                o.pedido_finalizado, o.estado,
                COALESCE(r.forma_pago, 'Efectivo'),
                COALESCE(r.cobro_extra, 0),
                r.solicitud_adicional
            FROM Orden o
            LEFT JOIN Reserva r
                ON r.id_reserva = o.id_reserva
            WHERE o.id_orden = %s
              AND o.id_empleado = %s
            """,
            (id_orden, id_empleado)
        )

        if not datos:
            messagebox.showerror(
                "Orden no encontrada",
                "No se encontró la orden seleccionada."
            )
            return

        (id_orden, id_mesa, id_reserva, pedido_finalizado,
            estado_orden, forma_pago, cobro_extra, solicitud
        ) = datos[0]

        if pedido_finalizado:
            messagebox.showwarning(
                "Cuenta finalizada",
                "Esta orden ya fue cobrada o finalizada."
            )
            return

        # Obtener los platillos que pertenecen a la orden.
        detalles = consultar(
            """
            SELECT p.nombre, d.cantidad, d.subtotal
            FROM Detalle_Orden d
            INNER JOIN Platillo p
                ON p.id_platillo = d.id_platillo
            WHERE d.id_orden = %s
            ORDER BY d.id_detalle
            """,
            (id_orden,)
        )

        if detalles is None:
            messagebox.showerror(
                "Error",
                "No se pudieron consultar los platillos."
            )
            return

        subtotal = sum(
            (Decimal(str(fila[2])) for fila in detalles),
            Decimal("0.00")
        )

        extra = Decimal(str(cobro_extra or 0))

        if not detalles or subtotal <= 0:
            messagebox.showwarning(
                "Cuenta vacía",
                "Agrega al menos un platillo antes de cobrar."
            )
            return

        # Comprobar si ya existe una factura pagada.
        facturas = consultar(
            """
            SELECT id_factura
            FROM Factura
            WHERE id_orden = %s
              AND estado_pago = 'Pagado'
            LIMIT 1
            """,
            (id_orden,)
        )

        if facturas is None:
            messagebox.showerror(
                "Error",
                "No se pudo comprobar el estado de la factura."
            )
            return

        if facturas:
            messagebox.showwarning(
                "Cobro duplicado",
                "Esta orden ya tiene una factura pagada."
            )
            return

        # Ventana de cobro.
        ventana_cobro = tk.Toplevel(ventana)
        ventana_cobro.title(f"Cobrar orden #{id_orden}")
        ventana_cobro.configure(bg=CREMA)
        ventana_cobro.transient(ventana)
        ventana_cobro.grab_set()
        ventana_cobro.resizable(False, False)
        ventana_cobro.iconbitmap("vivaldi.ico")

        marco = tk.Frame(
            ventana_cobro,
            bg=BLANCO,
            padx=24,
            pady=20
        )
        marco.pack(fill="both", expand=True, padx=12, pady=12)

        tk.Label(
            marco,
            text=f"COBRO DE LA ORDEN #{id_orden}",
            bg=BLANCO,
            fg=VERDE,
            font=("Georgia", 16, "bold")
        ).pack(anchor="w", pady=(0, 12))

        # Mostrar el detalle de los platillos.
        for nombre, cantidad, importe in detalles:
            tk.Label(
                marco,
                text=f"{cantidad} x {nombre}  —  ${Decimal(str(importe)):.2f}",
                bg=BLANCO,
                fg=VERDE_OSCURO,
                font=("Arial", 10),
                wraplength=430,
                justify="left"
            ).pack(anchor="w", pady=2)

        tk.Label(
            marco,
            text=f"\nSubtotal de platillos: ${subtotal:.2f}",
            bg=BLANCO,
            fg=VERDE_OSCURO,
            font=("Arial", 11)
        ).pack(anchor="w")

        tk.Label(
            marco,
            text=f"Cobro extra de reserva: ${extra:.2f}",
            bg=BLANCO,
            fg=VERDE_OSCURO,
            font=("Arial", 11)
        ).pack(anchor="w", pady=3)

        tk.Label(
            marco,
            text=f"Forma de pago: {forma_pago}",
            bg=BLANCO,
            fg=VERDE,
            font=("Arial", 11, "bold")
        ).pack(anchor="w", pady=5)

        if solicitud:
            tk.Label(
                marco,
                text=f"Solicitud: {solicitud}",
                bg=BLANCO,
                fg=GRIS,
                font=("Arial", 9),
                wraplength=430,
                justify="left"
            ).pack(anchor="w", pady=3)

        tk.Label(
            marco,
            text="Propina (opcional):",
            bg=BLANCO,
            fg=VERDE_OSCURO,
            font=("Arial", 10, "bold")
        ).pack(anchor="w", pady=(12, 4))

        variable_propina = tk.StringVar(value="0.00")

        entrada_propina = tk.Entry(
            marco,
            textvariable=variable_propina,
            font=("Arial", 11),
            width=18
        )
        entrada_propina.pack(anchor="w")

        etiqueta_total_cobro = tk.Label(
            marco,
            text=f"TOTAL: ${subtotal + extra:.2f}",
            bg=BLANCO,
            fg=VINO,
            font=("Georgia", 17, "bold")
        )
        etiqueta_total_cobro.pack(anchor="w", pady=12)

        def actualizar_total(*args):
            try:
                propina = Decimal(
                    variable_propina.get().strip() or "0"
                )

                if not propina.is_finite() or propina < 0:
                    raise ValueError

                total = subtotal + extra + propina

                etiqueta_total_cobro.config(
                    text=f"TOTAL: ${total:.2f}"
                )

            except (ValueError, ArithmeticError):
                etiqueta_total_cobro.config(
                    text="Revisa el valor de la propina."
                )

        variable_propina.trace_add("write", actualizar_total)

        cobro_en_proceso = [False]

        def confirmar_cobro():
            if not ventana_cobro.winfo_exists():
                return

            if cobro_en_proceso[0]:
                return

            try:
                propina = Decimal(
                    variable_propina.get().strip() or "0"
                ).quantize(Decimal("0.01"))

                if not propina.is_finite() or propina < 0:
                    raise ValueError

            except (ValueError, ArithmeticError):
                messagebox.showwarning(
                    "Propina inválida",
                    "Introduce una cantidad válida, por ejemplo 0.00.",
                    parent=ventana_cobro
                )
                return

            if forma_pago not in ("Efectivo", "Tarjeta"):
                messagebox.showerror(
                    "Forma de pago inválida",
                    "La reserva no contiene una forma de pago válida.",
                    parent=ventana_cobro
                )
                return

            total = (subtotal + extra + propina).quantize(
                Decimal("0.01")
            )

            if not messagebox.askyesno(
                    "Confirmar cobro",
                    f"Subtotal: ${subtotal:.2f}\n"
                    f"Extra: ${extra:.2f}\n"
                    f"Propina: ${propina:.2f}\n"
                    f"TOTAL: ${total:.2f}\n\n"
                    f"Forma de pago: {forma_pago}\n\n"
                    "¿Confirmas el pago?",
                    parent=ventana_cobro
            ):
                return

            cobro_en_proceso[0] = True
            conexion_pago = conectar()

            if not conexion_pago:
                cobro_en_proceso[0] = False
                return

            cursor_pago = None

            try:
                cursor_pago = conexion_pago.cursor()
                conexion_pago.start_transaction()

                cursor_pago.execute(
                    """
                    SELECT id_orden, id_mesa, id_reserva,
                           pedido_finalizado
                    FROM Orden
                    WHERE id_orden = %s
                      AND id_empleado = %s
                    FOR UPDATE
                    """,
                    (id_orden, id_empleado)
                )

                orden_bloqueada = cursor_pago.fetchone()

                if not orden_bloqueada:
                    raise ValueError(
                        "La orden ya no existe o no pertenece al mesero."
                    )

                if orden_bloqueada[3]:
                    raise ValueError(
                        "Esta orden ya fue finalizada."
                    )

                cursor_pago.execute("""
                    SELECT id_factura
                    FROM Factura
                    WHERE id_orden = %s
                      AND estado_pago = 'Pagado'
                    LIMIT 1
                """, (id_orden,))

                factura_pagada = cursor_pago.fetchone()

                if factura_pagada:
                    conexion_pago.rollback()

                    messagebox.showwarning(
                        "Cuenta ya pagada",
                        "Esta orden ya tiene una factura pagada.\n"
                        "No se realizará otro cobro.",
                        parent=ventana_cobro
                    )

                    if ventana_cobro.winfo_exists():
                        ventana_cobro.destroy()

                    return

                # Actualizar una factura pendiente si existe.
                cursor_pago.execute(
                    """
                    SELECT id_factura
                    FROM Factura
                    WHERE id_orden = %s
                      AND estado_pago = 'Pendiente'
                    ORDER BY id_factura DESC
                    LIMIT 1
                    FOR UPDATE
                    """,
                    (id_orden,)
                )

                factura_pendiente = cursor_pago.fetchone()

                servicio_extra = (
                    f"Cobro extra de reserva: ${extra:.2f}"
                    if extra else None
                )

                if solicitud:
                    texto_solicitud = f"Solicitud: {solicitud}"
                    servicio_extra = (
                        f"{servicio_extra} | {texto_solicitud}"
                        if servicio_extra
                        else texto_solicitud
                    )

                if factura_pendiente:
                    cursor_pago.execute(
                        """
                        UPDATE Factura
                        SET servicio_extra = %s,
                            subtotal = %s,
                            propina = %s,
                            total = %s,
                            metodo_pago = %s,
                            estado_pago = 'Pagado'
                        WHERE id_factura = %s
                        """,
                        (
                            servicio_extra,
                            subtotal,
                            propina,
                            total,
                            forma_pago,
                            factura_pendiente[0]
                        )
                    )
                else:
                    cursor_pago.execute(
                        """
                        INSERT INTO Factura (
                            servicio_extra,
                            subtotal,
                            propina,
                            total,
                            metodo_pago,
                            estado_pago,
                            id_orden
                        )
                        VALUES (%s, %s, %s, %s, %s, 'Pagado', %s)
                        """,
                        (
                            servicio_extra,
                            subtotal,
                            propina,
                            total,
                            forma_pago,
                            id_orden
                        )
                    )

                # Finalizar la orden.
                cursor_pago.execute(
                    """
                    UPDATE Orden
                    SET pedido_finalizado = 1
                    WHERE id_orden = %s
                      AND id_empleado = %s
                    """,
                    (id_orden, id_empleado)
                )

                # Completar la reserva asociada, si corresponde.
                id_reserva_pago = orden_bloqueada[2]

                if id_reserva_pago:
                    cursor_pago.execute(
                        """
                        UPDATE Reserva
                        SET estado = 'Completada'
                        WHERE id_reserva = %s
                        """,
                        (id_reserva_pago,)
                    )

                # No liberar una mesa que tenga otras órdenes activas.
                id_mesa_pago = orden_bloqueada[1]

                cursor_pago.execute(
                    """
                    SELECT COUNT(*)
                    FROM Orden
                    WHERE id_mesa = %s
                      AND id_orden <> %s
                      AND estado IN (
                          'Pendiente', 'Preparando', 'Entregado'
                      )
                      AND pedido_finalizado = 0
                    """,
                    (id_mesa_pago, id_orden)
                )

                otras_ordenes = cursor_pago.fetchone()[0]

                # Mantener la mesa reservada si hay una reserva futura.
                cursor_pago.execute(
                    """
                    SELECT COUNT(*)
                    FROM Reserva
                    WHERE id_mesa = %s
                      AND estado = 'Confirmada'
                      AND (
                          fecha > %s
                          OR (fecha = %s AND hora > %s)
                      )
                    """,
                    (
                        id_mesa_pago,
                        date.today(),
                        date.today(),
                        datetime.now().time().replace(microsecond=0)
                    )
                )

                reservas_futuras = cursor_pago.fetchone()[0]

                if otras_ordenes:
                    estado_mesa = "Ocupada"
                elif reservas_futuras:
                    estado_mesa = "Reservada"
                else:
                    estado_mesa = "Disponible"

                cursor_pago.execute(
                    """
                    UPDATE Mesa
                    SET estado = %s
                    WHERE id_mesa = %s
                    """,
                    (estado_mesa, id_mesa_pago)
                )

                conexion_pago.commit()


            except Exception as error:
                try:
                    conexion_pago.rollback()
                except mysql.connector.Error:
                    pass

                messagebox.showerror(
                    "No se pudo completar el cobro",
                    "No se confirmó el pago.\n\n"
                    f"Detalle del error:\n{error}",

                    parent=(
                        ventana_cobro
                        if ventana_cobro.winfo_exists()
                        else ventana

                    )
                )

                return

            finally:
                if cursor_pago:
                    cursor_pago.close()
                    cobro_en_proceso[0] = False

                conexion_pago.close()

            # Actualizar las vistas después de confirmar la transacción.
            ventana_cobro.destroy()

            orden_actual[0] = None
            mesa_actual[0] = None
            cliente_actual[0] = None

            cargar_reservas()
            cargar_detalles_orden()
            actualizar_inicio()
            cambiar_seccion("CUENTA")

            messagebox.showinfo(
                "Pago registrado",
                f"Factura pagada correctamente.\n\n"
                f"Orden: #{id_orden}\n"
                f"Total: ${total:.2f}\n"
                f"Forma de pago: {forma_pago}"
            )

        crear_boton(
            marco,
            "CONFIRMAR COBRO",
            confirmar_cobro,
            color=VERDE
        ).pack(fill="x", pady=(8, 0))

        ventana_cobro.update_idletasks()

        x = ventana.winfo_rootx() + (
                ventana.winfo_width() - ventana_cobro.winfo_width()
        ) // 2

        y = ventana.winfo_rooty() + (
                ventana.winfo_height() - ventana_cobro.winfo_height()
        ) // 2

        ventana_cobro.geometry(
            f"+{max(x, 0)}+{max(y, 0)}"
        )

    def quitar_platillo():
        if orden_actual[0] is None:
            messagebox.showwarning(
                "Sin orden activa",
                "Primero selecciona una reserva en MESAS."
            )
            return

        seleccion = tabla_detalle.selection()

        if not seleccion:
            messagebox.showwarning(
                "Selecciona un platillo",
                "Selecciona en la tabla el platillo que deseas quitar."
            )
            return

        if id_empleado is None:
            messagebox.showerror(
                "Sesión no identificada",
                "No se pudo identificar al mesero."
            )
            return

        valores = tabla_detalle.item(seleccion[0], "values")
        id_detalle = int(valores[0])

        if not messagebox.askyesno(
            "Quitar platillo",
            f"¿Quitar «{valores[1]}» de la cuenta?"
        ):
            return

        conexion = conectar()

        if not conexion:
            return

        cursor = None

        try:
            cursor = conexion.cursor()
            conexion.start_transaction()

            # Solo se puede quitar de una orden propia que todavía
            # esté Pendiente (aún no pasó a cocina).
            cursor.execute(
                """
                DELETE d
                FROM Detalle_Orden d
                INNER JOIN Orden o
                    ON o.id_orden = d.id_orden
                WHERE d.id_detalle = %s
                  AND d.id_orden = %s
                  AND o.id_empleado = %s
                  AND o.estado = 'Pendiente'
                """,
                (id_detalle, orden_actual[0], id_empleado)
            )

            if cursor.rowcount != 1:
                conexion.rollback()
                messagebox.showwarning(
                    "No se pudo quitar",
                    "El platillo ya no está en la cuenta o la orden "
                    "ya no está pendiente."
                )
                return

            conexion.commit()

        except mysql.connector.Error as error:
            conexion.rollback()
            messagebox.showerror(
                "Error",
                f"No se pudo quitar el platillo.\n\n{error}"
            )

        finally:
            if cursor:
                cursor.close()
            conexion.close()

        cargar_detalles_orden()


    # =====================================================
    # NAVEGACIÓN LATERAL
    # =====================================================

    def cambiar_seccion(seccion):
        if seccion == "INICIO":
            actualizar_inicio()
            mostrar_panel(panel_inicio)
            actualizar_menu(boton_inicio)

        elif seccion == "MESAS":
            cargar_reservas()
            mostrar_panel(panel_mesas)
            actualizar_menu(boton_mesas)

        elif seccion == "MENU":
            cargar_menu()
            actualizar_seleccion()
            mostrar_panel(panel_menu)
            actualizar_menu(boton_menu)

        elif seccion == "CUENTA":
            cargar_detalles_orden()
            mostrar_panel(panel_cuenta)
            actualizar_menu(boton_cuenta)

    boton_inicio = crear_boton_menu(
        "INICIO",
        lambda: cambiar_seccion("INICIO")
    )

    boton_mesas = crear_boton_menu(
        "MESAS",
        lambda: cambiar_seccion("MESAS")
    )

    boton_menu = crear_boton_menu(
        "MENÚ",
        lambda: cambiar_seccion("MENU")
    )

    boton_cuenta = crear_boton_menu(
        "MI CUENTA",
        lambda: cambiar_seccion("CUENTA")
    )

    def cerrar_sesion():
        respuesta = messagebox.askyesno(
            "Cerrar sesión",
            "¿Deseas cerrar sesión?"
        )

        if not respuesta:
            return

        try:
            ruta_login = os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "inicio_sistema.py"
            )

            subprocess.Popen([
                r"C:\Users\moral\AppData\Local\Programs\Python\Python313\python.exe",
                ruta_login
            ])

            ventana.destroy()

        except Exception as error:
            messagebox.showerror(
                "Error al cerrar sesión",
                f"No se pudo volver al inicio de sesión:\n{error}"
            )

    tk.Frame(
        menu_navegacion,
        bg=BEIGE,
        height=1
    ).pack(fill="x", pady=(18, 10))

    tk.Button(
        menu_navegacion,
        text="CERRAR SESIÓN",
        bg=VERDE_OSCURO,
        fg=CREMA_CLARO,
        activebackground=CREMA_CLARO,
        activeforeground=BLANCO,
        bd=0,
        relief="flat",
        anchor="w",
        padx=10,
        pady=13,
        font=("Arial", 10, "bold"),
        cursor="hand2",
        command=cerrar_sesion
    ).pack(fill="x", pady=4)

    cambiar_seccion("INICIO")
    ventana.mainloop()

if __name__ == "__main__":
    interfaz_mesero()