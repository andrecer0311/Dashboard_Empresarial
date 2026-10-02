"""Pruebas CRUD para los registros de cada área."""

import tempfile
import unittest
from pathlib import Path

from dashboard_app.database import DashboardDatabase


class DashboardRecordsTests(unittest.TestCase):
    def setUp(self):
        self.temp_directory = tempfile.TemporaryDirectory()
        self.database = DashboardDatabase(Path(self.temp_directory.name) / "test.sqlite3")

    def tearDown(self):
        self.database.close()
        self.temp_directory.cleanup()

    def test_add_update_and_delete_record_for_each_section(self):
        for section in ("afiliados", "servicios", "finanzas", "informes"):
            record_id = self.database.add_record(
                section, f"Prueba {section}", "Detalle", "Valor inicial", "Activo"
            )
            self.assertTrue(
                self.database.update_record(
                    record_id, section, f"Editado {section}", "Detalle editado", "Nuevo valor", "Actualizado"
                )
            )
            record = next(row for row in self.database.get_records(section) if row["id"] == record_id)
            self.assertEqual(record["name"], f"Editado {section}")
            self.assertEqual(record["value"], "Nuevo valor")
            self.assertTrue(self.database.delete_record(record_id, section))
            self.assertFalse(any(row["id"] == record_id for row in self.database.get_records(section)))

    def test_update_and_delete_are_scoped_to_the_section(self):
        record_id = self.database.add_record("afiliados", "Persona", "Empresa", "A", "Activo")
        self.assertFalse(
            self.database.update_record(record_id, "servicios", "Cambio", "", "", "")
        )
        self.assertFalse(self.database.delete_record(record_id, "servicios"))
        self.assertEqual(self.database.get_records("afiliados")[0]["name"], "Persona")

    def test_demo_records_exist_for_all_editable_sections(self):
        for section in ("afiliados", "servicios", "finanzas", "informes"):
            with self.subTest(section=section):
                self.assertGreater(len(self.database.get_records(section)), 0)


if __name__ == "__main__":
    unittest.main()
