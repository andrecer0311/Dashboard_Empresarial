"""Permite gestionar registros de un apartado desde un Treeview."""

import tkinter as tk
from tkinter import ttk

from .components import make_button
from .config import COLORS, RECORD_FIELDS


class RecordManager(tk.Frame):
    """Muestra y edita registros sin abrir ventanas adicionales."""

    def __init__(self, parent, section, database):
        super().__init__(parent, bg=COLORS["white"])
        self.section = section
        self.database = database
        self.selected_id = None
        self.field_labels = RECORD_FIELDS[section]
        self.field_vars = [tk.StringVar(self) for _ in range(4)]
        self._build()
        self.refresh()

    def _build(self):
        """Crea la tabla, el formulario y los controles CRUD."""
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        columns = ("name", "detail", "value", "status")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=4, selectmode="browse")
        for column, label in zip(columns, self.field_labels):
            self.tree.heading(column, text=label.upper())
            self.tree.column(column, width=70, minwidth=48, stretch=True)
        self.tree.grid(row=0, column=0, sticky="ew")
        self.tree.bind("<<TreeviewSelect>>", self._load_selection)

        form = tk.Frame(self, bg=COLORS["white"])
        form.grid(row=1, column=0, sticky="ew", pady=(7, 0))
        form.grid_columnconfigure(1, weight=1)
        for row, (label, variable) in enumerate(zip(self.field_labels, self.field_vars)):
            tk.Label(form, text=label, bg=COLORS["white"], fg="#65736b",
                     font=("Segoe UI", 7)).grid(row=row, column=0, sticky="w", padx=(0, 5), pady=2)
            ttk.Entry(form, textvariable=variable).grid(row=row, column=1, sticky="ew", pady=2)

        actions = tk.Frame(self, bg=COLORS["white"])
        actions.grid(row=2, column=0, sticky="ew", pady=(7, 0))
        actions.grid_columnconfigure((0, 1), weight=1)
        make_button(actions, "Agregar", self.add).grid(row=0, column=0, sticky="ew", padx=(0, 3), pady=2)
        make_button(actions, "Actualizar", self.update_record).grid(row=0, column=1, sticky="ew", padx=(3, 0), pady=2)
        make_button(actions, "Eliminar", self.delete).grid(row=1, column=0, sticky="ew", padx=(0, 3), pady=2)
        make_button(actions, "Recargar", self.refresh).grid(row=1, column=1, sticky="ew", padx=(3, 0), pady=2)
        self.feedback = tk.Label(self, text="Selecciona una fila para editarla.", bg=COLORS["white"],
                                 fg="#89938e", anchor="w", font=("Segoe UI", 7))
        self.feedback.grid(row=3, column=0, sticky="ew", pady=(4, 0))

    def refresh(self):
        """Recarga las filas y limpia la selección activa."""
        self.tree.delete(*self.tree.get_children())
        for record in self.database.get_records(self.section):
            values = (record["name"], record["detail"], record["value"], record["status"])
            self.tree.insert("", "end", iid=str(record["id"]), values=values)
        self.selected_id = None
        self._clear_form()
        self.feedback.configure(text=f"{len(self.tree.get_children())} registros cargados.", fg="#547c60")

    def _load_selection(self, _event=None):
        """Copia la fila seleccionada al formulario."""
        selection = self.tree.selection()
        if not selection:
            return
        self.selected_id = int(selection[0])
        for variable, value in zip(self.field_vars, self.tree.item(selection[0], "values")):
            variable.set(value)
        self.feedback.configure(text="Edita los campos y pulsa Actualizar.", fg="#547c60")

    def add(self):
        """Guarda un registro nuevo en la sección activa."""
        values = self._form_values()
        if values is None:
            return
        self.database.add_record(self.section, *values)
        self.refresh()
        self.feedback.configure(text="Registro agregado.", fg="#42865d")

    def update_record(self):
        """Guarda los cambios del registro seleccionado."""
        if self.selected_id is None:
            self.feedback.configure(text="Selecciona un registro para actualizar.", fg=COLORS["coral"])
            return
        values = self._form_values()
        if values is None:
            return
        self.database.update_record(self.selected_id, self.section, *values)
        self.refresh()
        self.feedback.configure(text="Registro actualizado.", fg="#42865d")

    def delete(self):
        """Elimina el registro seleccionado de SQLite."""
        if self.selected_id is None:
            self.feedback.configure(text="Selecciona un registro para eliminar.", fg=COLORS["coral"])
            return
        self.database.delete_record(self.selected_id, self.section)
        self.refresh()
        self.feedback.configure(text="Registro eliminado.", fg="#42865d")

    def _form_values(self):
        """Valida y devuelve los datos escritos en el formulario."""
        values = [variable.get().strip() for variable in self.field_vars]
        if not values[0]:
            self.feedback.configure(text=f"Escribe un valor para {self.field_labels[0].lower()}.", fg=COLORS["coral"])
            return None
        return values

    def _clear_form(self):
        """Vacía los campos y quita la selección de la tabla."""
        for variable in self.field_vars:
            variable.set("")
        selection = self.tree.selection()
        if selection:
            self.tree.selection_remove(*selection)