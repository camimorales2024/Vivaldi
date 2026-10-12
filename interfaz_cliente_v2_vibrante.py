"""
====================================================================
 EL TACO DORADO - Sistema de Gestion de Restaurante
 PROPUESTA 2: Interfaz de Cliente - Estilo "Vibrante con Pestanas"
====================================================================
 Instituto Nacional Gral. Francisco Menendez
 Desarrollo de Software - Modulo 3.1
 Campos basados en la entidad Cliente de la base de datos:
   id_cliente, nombre, apellido, telefono, correo_electronico,
   fecha_registro

 NOTA: Para usar el logo real, coloque un archivo llamado
 "logo.ico" y/o "logo.png" en la misma carpeta que este script.
====================================================================
"""

import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date
import os

# --------------------------------------------------------------
# PALETA DE COLORES OFICIAL "EL TACO DORADO"
# --------------------------------------------------------------
GOLD_1 = "#BC9755"
GOLD_2 = "#C5A46D"
GOLD_3 = "#DCC39A"
GREEN_1 = "#7FB328"
GREEN_2 = "#6FA121"
GREEN_3 = "#4C7712"
RED_1 = "#8B1E22"
RED_2 = "#7D1B1E"
RED_3 = "#5F1517"
BLUEBLACK_1 = "#1A2530"
BLUEBLACK_2 = "#273545"
WHITE_1 = "#FFFFFF"
WHITE_2 = "#F5F5F5"
WHITE_3 = "#EDEDED"


class ClienteAppVibrante(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("El Taco Dorado | Registro de Clientes")
        self.geometry("1020x680")
        self.configure(bg=WHITE_2)

        self.clientes = []
        self.contador_id = 1

        self._cargar_icono_ventana()
        self._crear_banner()
        self._crear_notebook()

    # ------------------------------------------------------------------
    def _cargar_icono_ventana(self):
        try:
            if os.path.exists("logo_restaurante.ico"):
                self.iconbitmap("logo_restaurante.ico")
        except Exception:
            pass

    # ------------------------------------------------------------------
    def _crear_banner(self):
        """Banner superior colorido con degradado simulado mediante bandas."""
        banner = tk.Canvas(self, height=130, bg=WHITE_2, highlightthickness=0)
        banner.pack(fill="x")

        # Bandas de color tipo "degradado" con la paleta oficial
        colores_banda = [GREEN_3, GREEN_1, GOLD_1, GOLD_2, RED_1, RED_3]
        ancho_banda = 1200 / len(colores_banda)
        for i, c in enumerate(colores_banda):
            banner.create_rectangle(i * ancho_banda, 0, (i + 1) * ancho_banda, 130,
                                     fill=c, outline="")

        # Circulo decorativo tipo "taco" estilizado (simple)
        banner.create_oval(30, 25, 110, 105, fill=WHITE_1, outline=GOLD_1, width=4)
        self.logo_img = None
        try:
            if os.path.exists("logo_restaurante.png"):
                self.logo_img = tk.PhotoImage(file="logo_restaurante.png")
                banner.create_image(70, 65, image=self.logo_img)
            else:
                banner.create_text(70, 65, text="El taco Dorado", fill=GOLD_1,
                                    font=("Segoe UI", 9, "bold"), justify="center")
        except Exception:
            banner.create_text(70, 65, text="El taco Dorado", fill=GOLD_1,
                                font=("Segoe UI", 9, "bold"), justify="center")

        banner.create_text(160, 45, anchor="w", text="EL TACO DORADO",
                            fill=WHITE_1, font=("Georgia", 24, "bold"))
        banner.create_text(160, 80, anchor="w", text="Sistema de Clientes  -  Registro rapido y colorido",
                            fill=WHITE_1, font=("Segoe UI", 11, "italic"))
        banner.create_rectangle(0, 126, 1200, 130, fill=BLUEBLACK_1, outline="")
        self.banner = banner

    # ------------------------------------------------------------------
    def _crear_notebook(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=WHITE_2, borderwidth=0)
        style.configure("TNotebook.Tab", background=GOLD_3, foreground=BLUEBLACK_1,
                         font=("Segoe UI", 11, "bold"), padding=[20, 10])
        style.map("TNotebook.Tab", background=[("selected", RED_1)],
                  foreground=[("selected", "white")])

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=15, pady=15)

        tab_registro = tk.Frame(notebook, bg=WHITE_2)
        tab_lista = tk.Frame(notebook, bg=WHITE_2)
        notebook.add(tab_registro, text="  Registrar Cliente  ")
        notebook.add(tab_lista, text="  Clientes Registrados  ")

        self._construir_tab_registro(tab_registro)
        self._construir_tab_lista(tab_lista)

    # ------------------------------------------------------------------
    def _construir_tab_registro(self, parent):
        contenedor = tk.Frame(parent, bg=WHITE_2)
        contenedor.pack(expand=True, pady=20)

        # Tarjeta con borde grueso simulando "no minimalismo"
        card_borde = tk.Frame(contenedor, bg=GREEN_1, padx=6, pady=6)
        card_borde.pack()
        card = tk.Frame(card_borde, bg=WHITE_1, padx=30, pady=25,
                         highlightbackground=GOLD_1, highlightthickness=4)
        card.pack()

        tk.Label(card, text="Nuevo Registro de Cliente", font=("Georgia", 17, "bold"),
                 fg=RED_1, bg=WHITE_1).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        self.entries = {}
        campos = [
            ("ID Cliente", "id_cliente", True, GOLD_1),
            ("Nombre", "nombre", False, GREEN_1),
            ("Apellido", "apellido", False, GREEN_1),
            ("Telefono", "telefono", False, RED_1),
            ("Correo Electronico", "correo", False, RED_1),
            ("Fecha de Registro", "fecha", True, GOLD_1),
        ]

        for i, (label, key, readonly, color) in enumerate(campos, start=1):
            tk.Label(card, text=label, font=("Segoe UI", 10, "bold"), fg=BLUEBLACK_1,
                     bg=WHITE_1).grid(row=i, column=0, sticky="w", pady=9, padx=(0, 15))
            entry = tk.Entry(card, font=("Segoe UI", 11), width=28,
                              highlightbackground=color, highlightthickness=2,
                              relief="flat", bd=4)
            entry.grid(row=i, column=1, pady=9)
            if key == "id_cliente":
                entry.insert(0, str(self.contador_id))
                entry.config(state="disabled")
            if key == "fecha":
                entry.insert(0, date.today().isoformat())
                entry.config(state="disabled")
            self.entries[key] = entry

        btns = tk.Frame(card, bg=WHITE_1)
        btns.grid(row=8, column=0, columnspan=2, pady=(20, 0))

        self._boton_redondeado(btns, "REGISTRAR", RED_1, RED_2, self.guardar_cliente).grid(
            row=0, column=0, padx=6)
        self._boton_redondeado(btns, "LIMPIAR", GREEN_1, GREEN_3, self.limpiar_campos).grid(
            row=0, column=1, padx=6)
        self._boton_redondeado(btns, "PEDIR COMIDA", GOLD_1, GOLD_2,
                                lambda: messagebox.showinfo(
                                    "Pedido", "Aqui se abriria el modulo de Pedidos / Menu.")
                                ).grid(row=0, column=2, padx=6)

    def _boton_redondeado(self, parent, texto, color, color_hover, comando):
        btn = tk.Button(parent, text=texto, font=("Segoe UI", 10, "bold"), bg=color,
                         fg="white", activebackground=color_hover, relief="flat",
                         padx=16, pady=9, bd=0, cursor="hand2", command=comando)
        return btn

    # ------------------------------------------------------------------
    def _construir_tab_lista(self, parent):
        top = tk.Frame(parent, bg=RED_1, padx=10, pady=10)
        top.pack(fill="x", padx=15, pady=(15, 0))
        tk.Label(top, text="Buscar cliente:", bg=RED_1, fg="white",
                 font=("Segoe UI", 10, "bold")).pack(side="left", padx=(5, 10))
        self.buscar_var = tk.StringVar()
        buscar_entry = tk.Entry(top, textvariable=self.buscar_var, font=("Segoe UI", 10),
                                 width=30, highlightbackground=GOLD_1, highlightthickness=2,
                                 relief="flat")
        buscar_entry.pack(side="left")
        buscar_entry.bind("<KeyRelease>", self.filtrar_tabla)

        tabla_frame = tk.Frame(parent, bg=WHITE_2)
        tabla_frame.pack(fill="both", expand=True, padx=15, pady=15)

        cols = ("id", "nombre", "apellido", "telefono", "correo", "fecha")
        headers = ("ID", "Nombre", "Apellido", "Telefono", "Correo", "Fecha Registro")

        style = ttk.Style()
        style.configure("Vibrante.Treeview.Heading", background=GREEN_1, foreground="white",
                         font=("Segoe UI", 10, "bold"))
        style.configure("Vibrante.Treeview", rowheight=28, font=("Segoe UI", 10))

        self.tree = ttk.Treeview(tabla_frame, columns=cols, show="headings",
                                  style="Vibrante.Treeview")
        for c, h in zip(cols, headers):
            self.tree.heading(c, text=h)
            self.tree.column(c, width=115, anchor="center")
        self.tree.tag_configure("par", background=GOLD_3)
        self.tree.tag_configure("impar", background=WHITE_1)
        self.tree.pack(fill="both", expand=True)

    # ------------------------------------------------------------------
    def guardar_cliente(self):
        nombre = self.entries["nombre"].get().strip()
        apellido = self.entries["apellido"].get().strip()
        telefono = self.entries["telefono"].get().strip()
        correo = self.entries["correo"].get().strip()
        fecha = self.entries["fecha"].get().strip()

        if not nombre or not apellido:
            messagebox.showwarning("Campos incompletos", "Nombre y Apellido son obligatorios.")
            return

        id_cliente = self.contador_id
        tag = "par" if id_cliente % 2 == 0 else "impar"
        self.tree.insert("", "end", values=(id_cliente, nombre, apellido, telefono, correo, fecha),
                          tags=(tag,))
        self.clientes.append((id_cliente, nombre, apellido, telefono, correo, fecha))
        self.contador_id += 1

        self.limpiar_campos()
        messagebox.showinfo("Registrado", f"Cliente '{nombre} {apellido}' registrado con exito.")

    def limpiar_campos(self):
        for key, entry in self.entries.items():
            if key == "id_cliente":
                entry.config(state="normal")
                entry.delete(0, "end")
                entry.insert(0, str(self.contador_id))
                entry.config(state="disabled")
            elif key == "fecha":
                entry.config(state="normal")
                entry.delete(0, "end")
                entry.insert(0, date.today().isoformat())
                entry.config(state="disabled")
            else:
                entry.delete(0, "end")

    def filtrar_tabla(self, event=None):
        texto = self.buscar_var.get().lower()
        for item in self.tree.get_children():
            valores = [str(v).lower() for v in self.tree.item(item, "values")]
            visible = any(texto in v for v in valores)
            if not visible and texto != "":
                self.tree.detach(item)
            else:
                self.tree.reattach(item, "", "end")


if __name__ == "__main__":
    app = ClienteAppVibrante()
    app.mainloop()
