from pathlib import Path


APP_DIR = Path(__file__).resolve().parent.parent
DATABASE_PATH = APP_DIR / "combarranquilla.db"

COLORS = {
    "forest": "#153c32",
    "forest_dark": "#102f28",
    "green": "#477a58",
    "green_light": "#eaf3e9",
    "ink": "#192c27",
    "muted": "#78847e",
    "line": "#e5ebe5",
    "paper": "#f6f8f4",
    "white": "#ffffff",
    "coral": "#e9765c",
    "coral_light": "#fff0ec",
    "yellow": "#d6ac43",
    "yellow_light": "#fbf3df",
    "blue": "#6e9ab0",
    "blue_light": "#eaf2f5",
}

VIEWS = {
    "resumen": {
        "name": "Resumen",
        "title": "Resumen ejecutivo",
        "description": "Una mirada clara al impacto social y el ritmo de la operación.",
        "chart_title": "Actividad de servicios",
        "chart_unit": "atenciones registradas",
        "metrics": [
            ("Afiliados activos", "184.260", "+4,8%", "vs. periodo anterior", "people"),
            ("Atenciones del periodo", "18.420", "+8,6%", "vs. periodo anterior", "activity"),
            ("Ingresos recaudados", "$8.420 M", "+3,2%", "vs. periodo anterior", "money"),
            ("Satisfacción", "92,4%", "+1,6 pts", "vs. periodo anterior", "heart"),
        ],
        "trend": [1120, 1320, 1260, 1490, 1420, 1640, 1530, 1810, 1680, 1930, 1840, 2380],
    },
    "afiliados": {
        "name": "Afiliados",
        "title": "Gestión de afiliados",
        "description": "Composición, crecimiento y acompañamiento de la población afiliada.",
        "chart_title": "Nuevas afiliaciones",
        "chart_unit": "afiliaciones registradas",
        "metrics": [
            ("Afiliados activos", "184.260", "+4,8%", "vs. periodo anterior", "people"),
            ("Nuevas afiliaciones", "2.846", "+6,1%", "vs. periodo anterior", "activity"),
            ("Empresas afiliadas", "6.382", "+2,4%", "vs. periodo anterior", "company"),
            ("Grupo familiar", "312.540", "+3,7%", "vs. periodo anterior", "heart"),
        ],
        "trend": [150, 174, 188, 201, 216, 232, 248, 263, 249, 276, 291, 318],
    },
    "servicios": {
        "name": "Servicios",
        "title": "Desempeño de servicios",
        "description": "Uso de programas y alcance de la oferta social en el territorio.",
        "chart_title": "Atenciones por servicio",
        "chart_unit": "atenciones registradas",
        "metrics": [
            ("Atenciones del periodo", "18.420", "+8,6%", "vs. periodo anterior", "activity"),
            ("Servicios activos", "42", "+3", "nuevos este trimestre", "company"),
            ("Ocupación promedio", "78,2%", "+5,3 pts", "vs. periodo anterior", "people"),
            ("Satisfacción", "92,4%", "+1,6 pts", "vs. periodo anterior", "heart"),
        ],
        "trend": [1180, 1390, 1330, 1580, 1510, 1720, 1630, 1920, 1790, 2040, 1950, 2380],
    },
    "finanzas": {
        "name": "Finanzas",
        "title": "Panorama financiero",
        "description": "Ingresos, ejecución presupuestal y sostenibilidad de los programas.",
        "chart_title": "Ingresos recaudados",
        "chart_unit": "millones de pesos",
        "metrics": [
            ("Ingresos recaudados", "$8.420 M", "+3,2%", "vs. periodo anterior", "money"),
            ("Ejecución presupuestal", "68,4%", "+2,1 pts", "del presupuesto anual", "activity"),
            ("Aportes del periodo", "$6.180 M", "+4,6%", "vs. periodo anterior", "company"),
            ("Cartera al día", "96,8%", "+0,8 pts", "vs. periodo anterior", "heart"),
        ],
        "trend": [540, 610, 585, 680, 655, 715, 690, 760, 735, 790, 780, 880],
    },
    "informes": {
        "name": "Informes",
        "title": "Informes de gestión",
        "description": "Indicadores consolidados para orientar decisiones y prioridades.",
        "chart_title": "Evolución de indicadores",
        "chart_unit": "metas cumplidas",
        "metrics": [
            ("Indicadores en seguimiento", "24", "+2", "actualizados este mes", "activity"),
            ("Metas cumplidas", "18 / 24", "75%", "avance acumulado", "heart"),
            ("Áreas reportando", "12", "100%", "reporte al día", "company"),
            ("Alertas abiertas", "03", "−2", "vs. periodo anterior", "people"),
        ],
        "trend": [48, 52, 51, 57, 59, 63, 61, 66, 70, 72, 73, 75],
    },
}

PERIODS = {
    "Últimos 30 días": {
        "labels": ["1 sep", "4 sep", "7 sep", "10 sep", "13 sep", "16 sep", "19 sep", "22 sep", "25 sep", "28 sep", "30 sep", ""],
        "scale": 1,
    },
    "Últimos 90 días": {
        "labels": ["4 jul", "13 jul", "22 jul", "31 jul", "9 ago", "18 ago", "27 ago", "5 sep", "14 sep", "23 sep", "1 oct", ""],
        "scale": 2.65,
    },
    "Año 2026": {
        "labels": ["ene", "feb", "mar", "abr", "may", "jun", "jul", "ago", "sep", "oct", "nov", "dic"],
        "scale": 5.8,
    },
}

ZONES = [
    ("Norte", 42, COLORS["forest"]),
    ("Centro", 28, COLORS["coral"]),
    ("Sur", 19, COLORS["yellow"]),
    ("Soledad", 11, COLORS["blue"]),
]

DEMO_TRANSACTIONS = [
    ("Subsidio familiar", "Afiliaciones", "Procesado", 248600000, "2026-10-01"),
    ("Jornada de salud preventiva", "Bienestar", "En curso", 42800000, "2026-09-30"),
    ("Matrículas educativas", "Educación", "Procesado", 86250000, "2026-09-29"),
    ("Fondo de vivienda", "Vivienda", "En revisión", 315000000, "2026-09-28"),
    ("Actividades recreativas", "Recreación", "Procesado", 18640000, "2026-09-27"),
]

SERVICES = [
    ("Vivienda", 32, 5894, COLORS["coral"]),
    ("Salud y bienestar", 27, 4973, COLORS["green"]),
    ("Educación", 23, 4237, COLORS["yellow"]),
    ("Recreación", 18, 3316, COLORS["blue"]),
]

RECORD_FIELDS = {
    "afiliados": ("Afiliado", "Empresa", "Categoría", "Estado"),
    "servicios": ("Servicio", "Categoría", "Atenciones", "Estado"),
    "finanzas": ("Concepto", "Tipo", "Valor", "Estado"),
    "informes": ("Indicador", "Área", "Avance", "Estado"),
}

DEMO_RECORDS = [
    ("afiliados", "Ana Martínez", "Empresa: Grupo Norte", "Categoría A", "Activo"),
    ("afiliados", "Carlos Pérez", "Empresa: Soluciones Caribe", "Categoría B", "Activo"),
    ("afiliados", "Diana Gómez", "Empresa: Logística Atlántico", "Categoría C", "Pendiente"),
    ("servicios", "Vivienda", "Subsidios", "5.894", "Activo"),
    ("servicios", "Salud y bienestar", "Atención integral", "4.973", "Activo"),
    ("servicios", "Educación", "Formación", "4.237", "Activo"),
    ("finanzas", "Aportes del periodo", "Ingreso", "$6.180 M", "Registrado"),
    ("finanzas", "Subsidio familiar", "Egreso", "$2.480 M", "Aprobado"),
    ("finanzas", "Fondo de vivienda", "Ejecución", "$315 M", "En revisión"),
    ("informes", "Metas cumplidas", "Gestión social", "75%", "En seguimiento"),
    ("informes", "Áreas reportando", "Gestión interna", "100%", "Al día"),
    ("informes", "Satisfacción", "Experiencia", "92,4%", "Al día"),
]