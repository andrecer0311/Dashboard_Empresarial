import sqlite3

from .config import DATABASE_PATH, DEMO_RECORDS, DEMO_TRANSACTIONS, ZONES


class DashboardDatabase:
    """Persistencia local de movimientos y distribución geográfica."""

    def __init__(self, path=DATABASE_PATH):
        self.connection = sqlite3.connect(path)
        self.connection.row_factory = sqlite3.Row
        self._create_tables()
        self._seed_transactions()

    def _create_tables(self):
        self.connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                area TEXT NOT NULL,
                status TEXT NOT NULL,
                amount INTEGER NOT NULL,
                transaction_date TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS zones (
                name TEXT PRIMARY KEY,
                share INTEGER NOT NULL,
                color TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                section TEXT NOT NULL,
                name TEXT NOT NULL,
                detail TEXT NOT NULL DEFAULT '',
                value TEXT NOT NULL DEFAULT '',
                status TEXT NOT NULL DEFAULT '',
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        self.connection.executemany(
            "INSERT OR IGNORE INTO zones (name, share, color) VALUES (?, ?, ?)", ZONES
        )
        for section in {record[0] for record in DEMO_RECORDS}:
            count = self.connection.execute(
                "SELECT COUNT(*) FROM records WHERE section = ?", (section,)
            ).fetchone()[0]
            if count == 0:
                self.connection.executemany(
                    """INSERT INTO records (section, name, detail, value, status)
                       VALUES (?, ?, ?, ?, ?)""",
                    [record for record in DEMO_RECORDS if record[0] == section],
                )
        self.connection.commit()

    def _seed_transactions(self):
        count = self.connection.execute("SELECT COUNT(*) FROM transactions").fetchone()[0]
        if count == 0:
            self.connection.executemany(
                """INSERT INTO transactions
                   (title, area, status, amount, transaction_date)
                   VALUES (?, ?, ?, ?, ?)""",
                DEMO_TRANSACTIONS,
            )
            self.connection.commit()

    def get_transactions(self, search=""):
        """Consulta los movimientos y aplica el texto de búsqueda."""
        query = """SELECT title, area, status, amount, transaction_date
                   FROM transactions
                   WHERE title LIKE ? OR area LIKE ? OR status LIKE ?
                   ORDER BY transaction_date DESC, id DESC"""
        pattern = f"%{search.strip()}%"
        return self.connection.execute(query, (pattern, pattern, pattern)).fetchall()

    def get_zones(self):
        """Devuelve las zonas ordenadas por porcentaje de atención."""
        return self.connection.execute(
            "SELECT name, share, color FROM zones ORDER BY share DESC"
        ).fetchall()

    def get_records(self, section):
        """Lista los registros guardados para un apartado."""
        return self.connection.execute(
            """SELECT id, name, detail, value, status
               FROM records WHERE section = ? ORDER BY id DESC""",
            (section,),
        ).fetchall()

    def add_record(self, section, name, detail, value, status):
        """Agrega un registro al apartado indicado."""
        cursor = self.connection.execute(
            """INSERT INTO records (section, name, detail, value, status)
               VALUES (?, ?, ?, ?, ?)""",
            (section, name, detail, value, status),
        )
        self.connection.commit()
        return cursor.lastrowid

    def update_record(self, record_id, section, name, detail, value, status):
        """Actualiza un registro sin salir de su apartado."""
        cursor = self.connection.execute(
            """UPDATE records SET name = ?, detail = ?, value = ?, status = ?,
                      updated_at = CURRENT_TIMESTAMP
               WHERE id = ? AND section = ?""",
            (name, detail, value, status, record_id, section),
        )
        self.connection.commit()
        return cursor.rowcount > 0

    def delete_record(self, record_id, section):
        """Elimina un registro del apartado indicado."""
        cursor = self.connection.execute(
            "DELETE FROM records WHERE id = ? AND section = ?", (record_id, section)
        )
        self.connection.commit()
        return cursor.rowcount > 0

    def close(self):
        """Cierra la conexión local a SQLite."""
        self.connection.close()