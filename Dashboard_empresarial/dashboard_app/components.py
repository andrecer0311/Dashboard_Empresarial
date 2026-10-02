import tkinter as tk
from tkinter import ttk

from .config import COLORS, PERIODS


def format_number(value):
    """Formatea cifras con separador de miles colombiano."""
    return f"{value:,}".replace(",", ".")


def make_panel(parent, **kwargs):
    """Crea un panel con fondo y borde del diseño actual."""
    return tk.Frame(
        parent,
        bg=COLORS["white"],
        padx=kwargs.get("padx", 17),
        pady=kwargs.get("pady", 15),
        highlightthickness=1,
        highlightbackground=COLORS["line"],
    )


def make_button(parent, label, command, primary=False, flat=False):
    """Construye un botón con el estilo compartido del dashboard."""
    if primary:
        bg, fg, active = COLORS["forest"], COLORS["white"], COLORS["forest_dark"]
    elif flat:
        bg, fg, active = parent.cget("bg"), "#52654b", parent.cget("bg")
    else:
        bg, fg, active = COLORS["white"], COLORS["ink"], "#f3f6f2"
    return tk.Button(
        parent,
        text=label,
        command=command,
        relief="flat",
        bd=0,
        cursor="hand2",
        bg=bg,
        fg=fg,
        activebackground=active,
        activeforeground=fg,
        padx=11,
        pady=7,
        font=("Segoe UI", 8, "bold"),
    )


def make_metric_card(parent, metric, column, total_columns=4):
    """Muestra una tarjeta con un indicador y su variación."""
    label, value, trend, note, icon = metric
    palette = {
        "people": (COLORS["forest"], COLORS["green_light"], "◉"),
        "activity": (COLORS["coral"], COLORS["coral_light"], "⌁"),
        "money": ("#9c782a", COLORS["yellow_light"], "$"),
        "heart": ("#547c90", COLORS["blue_light"], "♡"),
        "company": (COLORS["green"], COLORS["green_light"], "▤"),
    }
    icon_color, icon_bg, symbol = palette.get(icon, palette["activity"])
    card = tk.Frame(
        parent,
        bg=COLORS["white"],
        padx=13,
        pady=11,
        highlightthickness=1,
        highlightbackground=COLORS["line"],
    )
    card.grid(
        row=0,
        column=column,
        sticky="nsew",
        padx=(0 if column == 0 else 5, 0 if column == total_columns - 1 else 5),
    )
    top = tk.Frame(card, bg=COLORS["white"])
    top.pack(fill="x")
    tk.Label(
        top,
        text=label,
        bg=COLORS["white"],
        fg="#77837c",
        anchor="w",
        font=("Segoe UI", 8, "bold"),
    ).pack(side="left", fill="x", expand=True)
    tk.Label(
        top,
        text=symbol,
        width=2,
        bg=icon_bg,
        fg=icon_color,
        font=("Segoe UI", 10, "bold"),
    ).pack(side="right", ipady=3)
    tk.Label(
        card,
        text=value,
        bg=COLORS["white"],
        fg=COLORS["ink"],
        anchor="w",
        font=("Segoe UI", 17, "bold"),
    ).pack(fill="x", pady=(7, 2))
    foot = tk.Frame(card, bg=COLORS["white"])
    foot.pack(fill="x")
    tk.Label(
        foot, text=f"↑ {trend}", bg=COLORS["white"], fg="#42865d",
        font=("Segoe UI", 8, "bold")
    ).pack(side="left")
    tk.Label(
        foot, text=note, bg=COLORS["white"], fg="#8a958e", font=("Segoe UI", 7)
    ).pack(side="left", padx=(5, 0))
    return card


def make_section_heading(parent, eyebrow, title, description=None):
    """Dibuja el encabezado reutilizable de una sección."""
    tk.Label(parent, text=eyebrow.upper(), bg=COLORS["white"], fg="#8a968e",
             font=("Segoe UI", 7, "bold")).pack(anchor="w")
    tk.Label(parent, text=title, bg=COLORS["white"], fg=COLORS["ink"],
             font=("Segoe UI", 11, "bold")).pack(anchor="w", pady=(3, 0))
    if description:
        tk.Label(parent, text=description, bg=COLORS["white"], fg="#87928b",
                 font=("Segoe UI", 8)).pack(anchor="w", pady=(4, 0))


def draw_line_chart(canvas, view, period_name):
    """Dibuja la tendencia del área para el periodo seleccionado."""
    canvas.delete("all")
    period = PERIODS[period_name]
    values = [round(value * period["scale"]) for value in view["trend"]]
    width = max(canvas.winfo_width(), 360)
    height = max(canvas.winfo_height(), 160)
    left, right, top, bottom = 38, width - 7, 10, height - 21
    plot_height = bottom - top
    max_value = max(values) * 1.18
    for index in range(5):
        y = top + plot_height * index / 4
        axis_value = round(max_value * (4 - index) / 4)
        label = f"{axis_value // 1000}k" if axis_value >= 1000 else str(axis_value)
        canvas.create_text(left - 8, y, text=label, anchor="e", fill="#9aa49d", font=("Segoe UI", 7))
        canvas.create_line(left, y, right, y, fill="#edf0ec", width=1)
    points = []
    for index, value in enumerate(values):
        x = left + (right - left) * index / (len(values) - 1)
        y = bottom - (value / max_value) * plot_height
        points.extend((x, y))
    canvas.create_polygon([left, bottom, *points, right, bottom], fill="#e4efe5", outline="", smooth=True)
    canvas.create_line(*points, fill=COLORS["forest"], width=2, smooth=True)
    for index in range(0, len(points), 2):
        canvas.create_oval(points[index] - 3, points[index + 1] - 3,
                           points[index] + 3, points[index + 1] + 3,
                           fill=COLORS["white"], outline=COLORS["forest"], width=2)
    labels = period["labels"]
    for index, label in enumerate(labels):
        if label:
            x = left + (right - left) * index / (len(labels) - 1)
            canvas.create_text(x, height - 5, text=label, fill="#99a39d", font=("Segoe UI", 7))
    return values


def draw_zone_chart(canvas, zone_rows):
    """Dibuja el gráfico circular de participación por zona."""
    canvas.delete("all")
    start = 90
    for zone in zone_rows:
        extent = -3.6 * zone["share"]
        canvas.create_arc(9, 9, 121, 121, start=start, extent=extent,
                          style="pieslice", fill=zone["color"], outline=COLORS["white"], width=2)
        start += extent
    canvas.create_oval(36, 36, 94, 94, fill=COLORS["white"], outline=COLORS["white"])
    canvas.create_text(65, 57, text=str(len(zone_rows)), fill=COLORS["ink"], font=("Segoe UI", 16, "bold"))
    canvas.create_text(65, 74, text="zonas", fill=COLORS["muted"], font=("Segoe UI", 7))


def make_transactions_table(parent, database, search_value, height=5):
    """Crea una tabla y su función de actualización desde SQLite."""
    columns = ("activity", "area", "status", "amount")
    table = ttk.Treeview(parent, columns=columns, show="headings", height=height)
    table.heading("activity", text="ACTIVIDAD")
    table.heading("area", text="ÁREA")
    table.heading("status", text="ESTADO")
    table.heading("amount", text="VALOR", anchor="e")
    table.column("activity", width=205, minwidth=150, stretch=True)
    table.column("area", width=95, minwidth=75, stretch=True)
    table.column("status", width=95, minwidth=83, stretch=False)
    table.column("amount", width=115, minwidth=95, stretch=False, anchor="e")
    table.tag_configure("pending", foreground="#a77b2f")
    table.tag_configure("done", foreground="#4e805d")

    def refresh(*_args):
        query = search_value.get().strip()
        if query == "Buscar movimiento...":
            query = ""
        rows = database.get_transactions(query)
        table.delete(*table.get_children())
        for row in rows:
            tag = "pending" if row["status"] != "Procesado" else "done"
            table.insert("", "end", values=(
                row["title"], row["area"], row["status"], f"${format_number(row['amount'])}"
            ), tags=(tag,))
        return len(rows)

    refresh()
    return table, refresh