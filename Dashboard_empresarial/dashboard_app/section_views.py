"""Construye las secciones dentro del panel de la ventana principal."""

import tkinter as tk
from tkinter import ttk

from .components import draw_line_chart, draw_zone_chart, format_number, make_button, make_metric_card, make_panel, make_section_heading, make_transactions_table
from .config import COLORS, PERIODS, RECORD_FIELDS, SERVICES, VIEWS
from .record_manager import RecordManager


class DashboardSection(tk.Frame):
    """Muestra una sección en el espacio compartido del dashboard."""

    def __init__(self, parent, section_key, database, period_var, search_var, export_command):
        super().__init__(parent, bg=COLORS["paper"])
        self.section_key = section_key
        self.view = VIEWS[section_key]
        self.database = database
        self.period_var = period_var
        self.search_var = search_var
        self.export_command = export_command
        self._build()
        self.period_trace_id = self.period_var.trace_add("write", self.refresh_chart)
        self.refresh_chart()

    def _build(self):
        """Organiza los indicadores y paneles del área activa."""
        self.grid_columnconfigure(0, weight=1)
        heading = tk.Frame(self, bg=COLORS["paper"])
        heading.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        title_area = tk.Frame(heading, bg=COLORS["paper"])
        title_area.pack(side="left", fill="x", expand=True)
        tk.Label(title_area, text=f"━  PANEL DE CONTROL · {self.view['name'].upper()}",
                 bg=COLORS["paper"], fg="#738179", font=("Segoe UI", 8, "bold")).pack(anchor="w")
        tk.Label(title_area, text=self.view["title"], bg=COLORS["paper"], fg=COLORS["ink"],
                 font=("Segoe UI", 21, "bold")).pack(anchor="w", pady=(5, 1))
        tk.Label(title_area, text=self.view["description"], bg=COLORS["paper"], fg="#7a8780",
                 font=("Segoe UI", 9)).pack(anchor="w")
        controls = tk.Frame(heading, bg=COLORS["paper"])
        controls.pack(side="right", anchor="s")
        ttk.Combobox(controls, textvariable=self.period_var, values=list(PERIODS),
                     state="readonly", width=19).pack(side="left", padx=(0, 8), ipady=2)
        make_button(controls, "Exportar CSV", self.export_command, primary=True).pack(side="left")

        notice = tk.Frame(self, bg="#f1f4e9", highlightthickness=1, highlightbackground="#e6ead9")
        notice.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        tk.Label(notice, text="i", width=2, bg="#86976d", fg=COLORS["white"],
                 font=("Segoe UI", 8, "bold")).pack(side="left", padx=(9, 8), pady=7)
        tk.Label(notice, text="Vista de demostración · cifras ilustrativas, no corresponden a datos reales",
                 bg="#f1f4e9", fg="#697663", font=("Segoe UI", 8)).pack(side="left", pady=7)

        metrics = tk.Frame(self, bg=COLORS["paper"])
        metrics.grid(row=2, column=0, sticky="ew", pady=(0, 16))
        for column in range(4):
            metrics.grid_columnconfigure(column, weight=1, uniform="section-metrics")
        for index, metric in enumerate(self.view["metrics"]):
            make_metric_card(metrics, metric, index)

        analytics = tk.Frame(self, bg=COLORS["paper"])
        analytics.grid(row=3, column=0, sticky="ew", pady=(0, 16))
        analytics.grid_columnconfigure(0, weight=7, uniform="section-analytics")
        analytics.grid_columnconfigure(1, weight=3, uniform="section-analytics")
        self._build_chart(analytics)
        self._build_overview(analytics)

        details = tk.Frame(self, bg=COLORS["paper"])
        details.grid(row=4, column=0, sticky="ew", pady=(0, 12))
        details.grid_columnconfigure(0, weight=7, uniform="section-details")
        details.grid_columnconfigure(1, weight=3, uniform="section-details")
        self._build_transactions(details)
        if self.section_key in RECORD_FIELDS:
            self._build_record_manager(details)
        else:
            self._build_service_demand(details)
        tk.Label(self, text="Combarranquilla · Inteligencia de gestión · Prototipo con información ilustrativa",
                 bg=COLORS["paper"], fg="#9aa49d", font=("Segoe UI", 8)).grid(
                     row=5, column=0, sticky="w", pady=(4, 0)
                 )

    def _build_chart(self, parent):
        panel = make_panel(parent)
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 9))
        heading = tk.Frame(panel, bg=COLORS["white"])
        heading.pack(fill="x")
        make_section_heading(heading, "Tendencia", self.view["chart_title"])
        self.period_label = tk.Label(heading, text="", bg=COLORS["white"], fg="#9ba59e",
                                     font=("Segoe UI", 8))
        self.period_label.pack(side="right", anchor="n")
        summary = tk.Frame(panel, bg=COLORS["white"])
        summary.pack(fill="x", pady=(11, 0))
        self.chart_total = tk.Label(summary, text="", bg=COLORS["white"], fg="#253a31",
                                    font=("Segoe UI", 15, "bold"))
        self.chart_total.pack(side="left")
        tk.Label(summary, text=self.view["chart_unit"], bg=COLORS["white"], fg="#8b968f",
                 font=("Segoe UI", 8)).pack(side="left", padx=(8, 0), pady=(5, 0))
        self.chart = tk.Canvas(panel, height=165, bg=COLORS["white"], highlightthickness=0)
        self.chart.pack(fill="x", expand=True, pady=(5, 0))
        self.chart.bind("<Configure>", self.refresh_chart)

    def _build_overview(self, parent):
        panel = make_panel(parent)
        panel.grid(row=0, column=1, sticky="nsew", padx=(9, 0))
        if self.section_key == "resumen":
            make_section_heading(panel, "Distribución", "Impacto por zona",
                                 "Participación de atenciones según ubicación.")
            row = tk.Frame(panel, bg=COLORS["white"])
            row.pack(fill="x", expand=True, pady=(8, 0))
            donut = tk.Canvas(row, width=132, height=132, bg=COLORS["white"], highlightthickness=0)
            donut.pack(side="left", padx=(0, 7))
            zones = self.database.get_zones()
            draw_zone_chart(donut, zones)
            legend = tk.Frame(row, bg=COLORS["white"])
            legend.pack(side="left", fill="x", expand=True)
            for zone in zones:
                item = tk.Frame(legend, bg=COLORS["white"])
                item.pack(fill="x", pady=5)
                tk.Label(item, text="■", bg=COLORS["white"], fg=zone["color"],
                         font=("Segoe UI", 9)).pack(side="left", padx=(0, 4))
                tk.Label(item, text=zone["name"], bg=COLORS["white"], fg="#77837b",
                         font=("Segoe UI", 8)).pack(side="left", fill="x", expand=True)
                tk.Label(item, text=f"{zone['share']}%", bg=COLORS["white"], fg="#46584e",
                         font=("Segoe UI", 8, "bold")).pack(side="right")
            return

        if self.section_key == "afiliados":
            heading = ("Composición", "Afiliación y cobertura", "Indicadores de la población afiliada.")
            items = [("Afiliados activos", "184.260", COLORS["forest"]),
                     ("Empresas afiliadas", "6.382", COLORS["coral"]),
                     ("Grupo familiar", "312.540", COLORS["yellow"])]
        elif self.section_key == "servicios":
            heading = ("Oferta social", "Servicios con mayor demanda", "Participación en las atenciones.")
            items = [(name, f"{share}% · {format_number(amount)}", color)
                     for name, share, amount, color in SERVICES]
        elif self.section_key == "finanzas":
            heading = ("Resumen financiero", "Ingresos y ejecución", "Valores ilustrativos en pesos colombianos.")
            items = [("Ingresos recaudados", "$8.420 M", COLORS["forest"]),
                     ("Aportes del periodo", "$6.180 M", COLORS["coral"]),
                     ("Ejecución presupuestal", "68,4%", COLORS["yellow"]),
                     ("Cartera al día", "96,8%", COLORS["blue"])]
        else:
            heading = ("Cumplimiento", "Estado de indicadores", "Seguimiento de objetivos institucionales.")
            items = [("Metas cumplidas", "18 de 24", COLORS["forest"]),
                     ("Áreas reportando", "12 de 12", COLORS["coral"]),
                     ("Alertas abiertas", "3", COLORS["yellow"])]
        make_section_heading(panel, *heading)
        list_frame = tk.Frame(panel, bg=COLORS["white"])
        list_frame.pack(fill="both", expand=True, pady=(10, 0))
        for label, value, color in items:
            row = tk.Frame(list_frame, bg=COLORS["white"])
            row.pack(fill="x", pady=7)
            tk.Label(row, text="●", bg=COLORS["white"], fg=color,
                     font=("Segoe UI", 9)).pack(side="left", padx=(0, 7))
            tk.Label(row, text=label, bg=COLORS["white"], fg="#58675f", anchor="w",
                     font=("Segoe UI", 8)).pack(side="left", fill="x", expand=True)
            tk.Label(row, text=value, bg=COLORS["white"], fg=COLORS["ink"],
                     font=("Segoe UI", 8, "bold")).pack(side="right")
            ttk.Separator(list_frame, orient="horizontal").pack(fill="x")

    def _build_transactions(self, parent):
        panel = make_panel(parent)
        panel.grid(row=0, column=0, sticky="nsew", padx=(0, 9))
        heading = tk.Frame(panel, bg=COLORS["white"])
        heading.pack(fill="x", pady=(0, 11))
        make_section_heading(heading, "Seguimiento", "Movimientos recientes")
        self.table, self._table_refresh = make_transactions_table(
            panel, self.database, self.search_var, height=5
        )
        self.table.pack(fill="x", expand=True)

    def _build_record_manager(self, parent):
        """Muestra el Treeview CRUD compacto en el extremo inferior derecho."""
        panel = make_panel(parent)
        panel.grid(row=0, column=1, sticky="nsew", padx=(9, 0))
        make_section_heading(panel, "Gestión", f"Editar {self.view['name'].lower()}")
        self.record_manager = RecordManager(panel, self.section_key, self.database)
        self.record_manager.pack(fill="both", expand=True, pady=(9, 0))

    def _build_service_demand(self, parent):
        """Muestra la demanda de servicios en el resumen ejecutivo."""
        panel = make_panel(parent)
        panel.grid(row=0, column=1, sticky="nsew", padx=(9, 0))
        make_section_heading(panel, "Top de servicios", "Mayor demanda",
                             "Servicios con más actividad en el periodo.")
        for name, share, amount, color in SERVICES:
            row = tk.Frame(panel, bg=COLORS["white"])
            row.pack(fill="x", pady=(10, 0))
            labels = tk.Frame(row, bg=COLORS["white"])
            labels.pack(fill="x")
            tk.Label(labels, text=name, bg=COLORS["white"], fg="#42534a",
                     font=("Segoe UI", 8, "bold")).pack(side="left")
            tk.Label(labels, text=f"{share}%", bg=COLORS["white"], fg="#67766c",
                     font=("Segoe UI", 8, "bold")).pack(side="right")
            track = tk.Canvas(row, height=5, bg="#edf0ec", highlightthickness=0)
            track.pack(fill="x", pady=(5, 3))
            track.bind("<Configure>", lambda event, canvas=track, pct=share, fill=color:
                       canvas.create_rectangle(0, 0, event.width * pct / 45, 5, fill=fill, outline=""))
            tk.Label(row, text=f"{format_number(amount)} atenciones", bg=COLORS["white"],
                     fg="#97a19a", font=("Segoe UI", 7)).pack(anchor="w")

    def refresh_chart(self, *_args):
        """Actualiza la gráfica según el periodo elegido."""
        if not self.winfo_exists() or not hasattr(self, "chart") or not self.chart.winfo_exists():
            return
        values = draw_line_chart(self.chart, self.view, self.period_var.get())
        period = self.period_var.get()
        self.period_label.configure(text={
            "Últimos 30 días": "30 días",
            "Últimos 90 días": "90 días",
            "Año 2026": "Año 2026",
        }.get(period, period))
        if self.section_key == "finanzas":
            total = f"${format_number(sum(values))} M"
        elif self.section_key == "informes":
            total = f"{values[-1]}%"
        else:
            total = format_number(sum(values))
        self.chart_total.configure(text=total)

    def refresh_table(self):
        """Actualiza los movimientos con el filtro de búsqueda."""
        if self.winfo_exists() and self.table.winfo_exists():
            self._table_refresh()

    def dispose(self):
        """Retira los eventos asociados antes de cambiar de sección."""
        self.period_var.trace_remove("write", self.period_trace_id)