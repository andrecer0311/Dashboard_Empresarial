"""Administra la ventana principal y la navegación del dashboard."""

import csv
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from .components import make_button
from .config import APP_DIR, COLORS, VIEWS
from .database import DashboardDatabase
from .section_views import DashboardSection


class ExecutiveDashboard(tk.Tk):
    """Ventana principal del dashboard empresarial."""

    def __init__(self):
        super().__init__()
        self.database = DashboardDatabase()
        self.period_var = tk.StringVar(self, "Últimos 30 días")
        self.search_var = tk.StringVar(self)
        self.current_view = None
        self.section = None
        self.title("Combarranquilla | Panel ejecutivo")
        self.geometry("1420x900")
        self.minsize(1050, 720)
        self.configure(bg=COLORS["paper"])
        self.protocol("WM_DELETE_WINDOW", self._close)
        self._configure_styles()
        self._build_layout()
        self._show_view("resumen")
        self.search_trace_id = self.search_var.trace_add("write", self._refresh_view)
        self.bind("/", lambda _event: self.search_entry.focus_set())
        self.bind("<Control-e>", lambda _event: self._export_csv())

    def _configure_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview", background=COLORS["white"], fieldbackground=COLORS["white"],
                        foreground="#58675f", rowheight=38, borderwidth=0, font=("Segoe UI", 9))
        style.configure("Treeview.Heading", background=COLORS["white"], foreground="#87938b",
                        relief="flat", font=("Segoe UI", 8, "bold"))
        style.map("Treeview", background=[("selected", "#e8f0e9")], foreground=[("selected", COLORS["forest"])])
        style.configure("TCombobox", fieldbackground=COLORS["white"], background=COLORS["white"],
                        foreground=COLORS["ink"], padding=7, arrowsize=12, bordercolor=COLORS["line"])
        style.map("TCombobox", fieldbackground=[("readonly", COLORS["white"])])

    def _build_layout(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self._build_sidebar()
        main = tk.Frame(self, bg=COLORS["paper"])
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_rowconfigure(1, weight=1)
        main.grid_columnconfigure(0, weight=1)
        self._build_topbar(main)
        self._build_viewport(main)

    def _build_sidebar(self):
        """Crea el menú que cambia la sección central."""
        sidebar = tk.Frame(self, bg=COLORS["forest"], width=230)
        sidebar.grid(row=0, column=0, sticky="ns")
        sidebar.grid_propagate(False)
        brand = tk.Frame(sidebar, bg=COLORS["forest"])
        brand.pack(fill="x", padx=20, pady=(27, 38))
        tk.Label(brand, text="C.", width=2, bg=COLORS["forest"], fg=COLORS["white"],
                 font=("Segoe UI", 21, "bold"), highlightthickness=1,
                 highlightbackground="#5a776b").pack(side="left", padx=(0, 10))
        brand_copy = tk.Frame(brand, bg=COLORS["forest"])
        brand_copy.pack(side="left")
        tk.Label(brand_copy, text="combarranquilla", bg=COLORS["forest"], fg=COLORS["white"],
                 font=("Segoe UI", 11, "bold")).pack(anchor="w")
        tk.Label(brand_copy, text="GESTIÓN EJECUTIVA", bg=COLORS["forest"], fg="#a9c0b5",
                 font=("Segoe UI", 7, "bold")).pack(anchor="w", pady=(2, 0))
        tk.Label(sidebar, text="ESPACIO DE TRABAJO", bg=COLORS["forest"], fg="#87a79a",
                 font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=22, pady=(0, 12))
        self.nav_buttons = {}
        for key, symbol in [("resumen", "▦"), ("afiliados", "◉"), ("servicios", "▤"), ("finanzas", "$"), ("informes", "≡")]:
            button = tk.Button(sidebar, text=f"  {symbol}     {VIEWS[key]['name']}", anchor="w",
                               padx=12, pady=10, relief="flat", bd=0, cursor="hand2",
                               bg=COLORS["forest"], fg="#c4d4cc", activebackground="#31584b",
                               activeforeground=COLORS["white"], font=("Segoe UI", 10),
                               command=lambda selected=key: self._show_view(selected))
            button.pack(fill="x", padx=12, pady=2)
            self.nav_buttons[key] = button
        bottom = tk.Frame(sidebar, bg=COLORS["forest"])
        bottom.pack(side="bottom", fill="x", padx=16, pady=18)
        status = tk.Frame(bottom, bg="#1e493d", padx=10, pady=11)
        status.pack(fill="x", pady=(0, 13))
        tk.Label(status, text="●", bg="#1e493d", fg="#8ed49d",
                 font=("Segoe UI", 10)).pack(side="left", padx=(0, 8))
        status_copy = tk.Frame(status, bg="#1e493d")
        status_copy.pack(side="left")
        tk.Label(status_copy, text="Operación estable", bg="#1e493d", fg=COLORS["white"],
                 font=("Segoe UI", 9, "bold")).pack(anchor="w")
        tk.Label(status_copy, text="Datos locales · SQLite", bg="#1e493d", fg="#a9c0b5",
                 font=("Segoe UI", 8)).pack(anchor="w", pady=(2, 0))
        tk.Label(bottom, text="LM   Laura Martínez\n       Dirección general", bg=COLORS["forest"],
                 fg=COLORS["white"], justify="left", font=("Segoe UI", 9)).pack(anchor="w", pady=(5, 0))

    def _build_topbar(self, parent):
        """Crea la barra superior con búsqueda y notificaciones."""
        bar = tk.Frame(parent, bg=COLORS["white"], height=62,
                       highlightthickness=1, highlightbackground=COLORS["line"])
        bar.grid(row=0, column=0, sticky="ew")
        bar.grid_propagate(False)
        breadcrumb = tk.Frame(bar, bg=COLORS["white"])
        breadcrumb.pack(side="left", padx=32, fill="y")
        tk.Label(breadcrumb, text="Gestión   ›", bg=COLORS["white"], fg="#89938e",
                 font=("Segoe UI", 9)).pack(side="left")
        self.breadcrumb_label = tk.Label(breadcrumb, text="Resumen", bg=COLORS["white"],
                                         fg="#34463e", font=("Segoe UI", 9, "bold"))
        self.breadcrumb_label.pack(side="left", padx=(7, 0))
        actions = tk.Frame(bar, bg=COLORS["white"])
        actions.pack(side="right", padx=26)
        self.search_entry = tk.Entry(actions, textvariable=self.search_var, width=28,
                                     relief="solid", bd=1, highlightthickness=0,
                                     font=("Segoe UI", 9))
        self.search_entry.pack(side="left", ipady=7, padx=(0, 12))
        self.search_entry.insert(0, "Buscar movimiento...")
        self.search_entry.configure(fg="#9aa49e")
        self.search_entry.bind("<FocusIn>", self._search_focus_in)
        self.search_entry.bind("<FocusOut>", self._search_focus_out)
        tk.Button(actions, text="◉", relief="flat", bg=COLORS["white"], fg="#596860",
                  font=("Segoe UI", 12), cursor="hand2",
                  command=self._show_notifications).pack(side="left")

    def _build_viewport(self, parent):
        """Prepara el área desplazable de contenido principal."""
        shell = tk.Frame(parent, bg=COLORS["paper"])
        shell.grid(row=1, column=0, sticky="nsew")
        shell.grid_rowconfigure(0, weight=1)
        shell.grid_columnconfigure(0, weight=1)
        self.canvas = tk.Canvas(shell, bg=COLORS["paper"], highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(shell, orient="vertical", command=self.canvas.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.canvas.configure(yscrollcommand=scrollbar.set)
        self.content = tk.Frame(self.canvas, bg=COLORS["paper"], padx=30, pady=24)
        self.content_id = self.canvas.create_window((0, 0), window=self.content, anchor="nw")
        self.content.bind("<Configure>", lambda _event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Configure>", lambda event: self.canvas.itemconfigure(self.content_id, width=event.width))
        self.canvas.bind_all("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-event.delta / 120), "units"))

    def _show_view(self, section_key):
        """Reemplaza el contenido central sin abrir otra ventana."""
        if self.section is not None:
            self.section.dispose()
            self.section.destroy()
        self.current_view = section_key
        self.breadcrumb_label.configure(text=VIEWS[section_key]["name"])
        for key, button in self.nav_buttons.items():
            active = key == section_key
            button.configure(bg="#31584b" if active else COLORS["forest"],
                             fg=COLORS["white"] if active else "#c4d4cc")
        self.section = DashboardSection(
            self.content,
            section_key,
            self.database,
            self.period_var,
            self.search_var,
            self._export_csv,
        )
        self.section.grid(row=0, column=0, sticky="nsew")
        self.content.grid_columnconfigure(0, weight=1)
        self.canvas.yview_moveto(0)

    def _refresh_view(self, *_args):
        if self.section is not None:
            self.section.refresh_table()

    def _export_csv(self):
        """Exporta los movimientos visibles a un archivo CSV."""
        path = filedialog.asksaveasfilename(
            title="Exportar movimientos",
            initialdir=str(APP_DIR),
            initialfile="movimientos-combarranquilla.csv",
            defaultextension=".csv",
            filetypes=[("Archivo CSV", "*.csv")],
        )
        if not path:
            return
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as file:
                writer = csv.writer(file)
                writer.writerow(["Actividad", "Area", "Estado", "Valor", "Fecha"])
                for row in self.database.get_transactions(self._current_search()):
                    writer.writerow([row["title"], row["area"], row["status"], row["amount"], row["transaction_date"]])
        except OSError as error:
            messagebox.showerror("No se pudo exportar", str(error), parent=self)
            return
        messagebox.showinfo("Exportación lista", "El archivo CSV se guardó correctamente.", parent=self)

    def _current_search(self):
        value = self.search_var.get().strip()
        return "" if value == "Buscar movimiento..." else value

    def _search_focus_in(self, _event):
        if self.search_entry.get() == "Buscar movimiento...":
            self.search_entry.delete(0, "end")
            self.search_entry.configure(fg=COLORS["ink"])

    def _search_focus_out(self, _event):
        if not self.search_entry.get().strip():
            self.search_var.set("")
            self.search_entry.insert(0, "Buscar movimiento...")
            self.search_entry.configure(fg="#9aa49e")

    def _show_notifications(self):
        messagebox.showinfo("Notificaciones", "No tienes notificaciones nuevas.", parent=self)

    def _close(self):
        """Libera conexiones y recursos al cerrar la aplicación."""
        self.search_var.trace_remove("write", self.search_trace_id)
        if self.section is not None:
            self.section.dispose()
        self.database.close()
        self.destroy()