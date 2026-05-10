from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from spelldeck.compiler import (
    compile_items_pdf,
    compile_single_page_items_pdf,
    compile_spell_pdf,
)
from spelldeck.items_data import DEFAULT_ITEMS_PATH
from spelldeck.items_service import generate_items_tex_file
from spelldeck.spells_data import DEFAULT_SPELLS_PATH
from spelldeck.spells_service import generate_spells_tex_file, parse_filter_string


class BaseGeneratorTab(ttk.Frame):
    dataset_label = "Dataset JSON"
    browse_title = "Seleziona dataset"
    hint_text = ""

    def __init__(self, master, default_dataset):
        super().__init__(master, padding=12)
        self.dataset_path = tk.StringVar(value=str(default_dataset))
        self.status_text = tk.StringVar(value="Ready.")
        self.log_widget = None
        self._build()

    def _build(self):
        self.columnconfigure(1, weight=1)

        ttk.Label(self, text=self.dataset_label).grid(row=0, column=0, sticky="w", pady=(0, 8))
        ttk.Entry(self, textvariable=self.dataset_path).grid(
            row=0, column=1, sticky="ew", padx=(8, 8), pady=(0, 8)
        )
        ttk.Button(self, text="Sfoglia", command=self._choose_dataset).grid(
            row=0, column=2, sticky="ew", pady=(0, 8)
        )

        self._build_form()

        ttk.Label(self, text="Log").grid(row=90, column=0, sticky="w", pady=(8, 0))
        self.log_widget = tk.Text(self, height=14, wrap="word")
        self.log_widget.grid(row=91, column=0, columnspan=3, sticky="nsew")
        self.rowconfigure(91, weight=1)

        ttk.Label(self, textvariable=self.status_text).grid(
            row=92, column=0, columnspan=3, sticky="w", pady=(10, 0)
        )

    def _build_form(self):
        raise NotImplementedError

    def _choose_dataset(self):
        selected_path = filedialog.askopenfilename(
            title=self.browse_title,
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if selected_path:
            self.dataset_path.set(selected_path)

    def _resolve_dataset_path(self, default_path):
        dataset = self.dataset_path.get().strip()
        return dataset or str(default_path)

    def _append_log(self, message):
        self.log_widget.insert("end", message.rstrip() + "\n")
        self.log_widget.see("end")

    def _set_status(self, message):
        self.status_text.set(message)
        self._append_log(message)

    def _show_error(self, title, message):
        self._set_status(message)
        messagebox.showerror(title, message)

    def _log_compile_result(self, compile_result):
        if compile_result.stdout:
            self._append_log(compile_result.stdout)
        if compile_result.stderr:
            self._append_log(compile_result.stderr)


class SpellsTab(BaseGeneratorTab):
    dataset_label = "Dataset magie"
    browse_title = "Seleziona dataset magie"
    hint_text = "Usa valori separati da virgola. Per i livelli puoi usare anche range come 1-3."

    def __init__(self, master):
        self.class_filter = tk.StringVar()
        self.level_filter = tk.StringVar()
        self.school_filter = tk.StringVar()
        self.name_filter = tk.StringVar()
        super().__init__(master, DEFAULT_SPELLS_PATH)

    def _build_form(self):
        ttk.Label(self, text="Classi").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(self, textvariable=self.class_filter).grid(
            row=1, column=1, columnspan=2, sticky="ew", pady=4
        )

        ttk.Label(self, text="Livelli").grid(row=2, column=0, sticky="w", pady=4)
        ttk.Entry(self, textvariable=self.level_filter).grid(
            row=2, column=1, columnspan=2, sticky="ew", pady=4
        )

        ttk.Label(self, text="Scuole").grid(row=3, column=0, sticky="w", pady=4)
        ttk.Entry(self, textvariable=self.school_filter).grid(
            row=3, column=1, columnspan=2, sticky="ew", pady=4
        )

        ttk.Label(self, text="Nomi").grid(row=4, column=0, sticky="w", pady=4)
        ttk.Entry(self, textvariable=self.name_filter).grid(
            row=4, column=1, columnspan=2, sticky="ew", pady=4
        )

        ttk.Label(self, text=self.hint_text).grid(row=5, column=0, columnspan=3, sticky="w", pady=(4, 10))

        buttons = ttk.Frame(self)
        buttons.grid(row=6, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        buttons.columnconfigure(0, weight=1)
        buttons.columnconfigure(1, weight=1)
        ttk.Button(buttons, text="Genera TeX", command=self._generate_tex).grid(
            row=0, column=0, sticky="ew", padx=(0, 6)
        )
        ttk.Button(buttons, text="Genera PDF", command=self._generate_pdf).grid(
            row=0, column=1, sticky="ew", padx=(6, 0)
        )

    def _collect_filters(self):
        return {
            "dataset_path": self._resolve_dataset_path(DEFAULT_SPELLS_PATH),
            "classes": parse_filter_string(self.class_filter.get()),
            "levels": parse_filter_string(self.level_filter.get()),
            "schools": parse_filter_string(self.school_filter.get()),
            "names": parse_filter_string(self.name_filter.get()),
        }

    def _generate_tex(self):
        try:
            result = generate_spells_tex_file(**self._collect_filters())
        except Exception as exc:
            self._show_error("Errore", f"Errore generazione TeX: {exc}")
            return None

        self._set_status(
            f"TeX generato: {result.output_path} | magie: {result.spell_count} | troncate: {result.truncated_count}"
        )
        return result

    def _generate_pdf(self):
        generation_result = self._generate_tex()
        if generation_result is None:
            return

        try:
            compile_result = compile_spell_pdf()
        except Exception as exc:
            self._show_error("Errore", f"Errore compilazione: {exc}")
            return

        self._log_compile_result(compile_result)
        if compile_result.succeeded:
            self._set_status(f"PDF generato: {Path(compile_result.output_pdf)}")
        else:
            self._set_status(f"Compilazione fallita con codice {compile_result.returncode}")
            messagebox.showerror(
                "Compilazione fallita",
                compile_result.stderr or compile_result.stdout or "Errore LaTeX.",
            )


class ItemsTab(BaseGeneratorTab):
    dataset_label = "Dataset oggetti"
    browse_title = "Seleziona dataset oggetti"
    hint_text = "Usa valori separati da virgola. Il filtro principale per gli oggetti e' il nome."

    def __init__(self, master):
        self.name_filter = tk.StringVar()
        self.class_filter = tk.StringVar()
        super().__init__(master, DEFAULT_ITEMS_PATH)

    def _build_form(self):
        ttk.Label(self, text="Nomi").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(self, textvariable=self.name_filter).grid(
            row=1, column=1, columnspan=2, sticky="ew", pady=4
        )

        ttk.Label(self, text="Classi legacy").grid(row=2, column=0, sticky="w", pady=4)
        ttk.Entry(self, textvariable=self.class_filter).grid(
            row=2, column=1, columnspan=2, sticky="ew", pady=4
        )

        ttk.Label(self, text=self.hint_text).grid(row=3, column=0, columnspan=3, sticky="w", pady=(4, 10))

        buttons = ttk.Frame(self)
        buttons.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        buttons.columnconfigure(0, weight=1)
        buttons.columnconfigure(1, weight=1)
        buttons.columnconfigure(2, weight=1)
        ttk.Button(buttons, text="Genera TeX", command=self._generate_tex).grid(
            row=0, column=0, sticky="ew", padx=(0, 6)
        )
        ttk.Button(buttons, text="Genera PDF", command=self._generate_pdf).grid(
            row=0, column=1, sticky="ew", padx=6
        )
        ttk.Button(buttons, text="Genera PDF 9 copie", command=self._generate_single_page_pdf).grid(
            row=0, column=2, sticky="ew", padx=(6, 0)
        )

    def _collect_filters(self):
        return {
            "dataset_path": self._resolve_dataset_path(DEFAULT_ITEMS_PATH),
            "names": parse_filter_string(self.name_filter.get()),
            "classes": parse_filter_string(self.class_filter.get()),
        }

    def _generate_tex(self):
        try:
            result = generate_items_tex_file(**self._collect_filters())
        except Exception as exc:
            self._show_error("Errore", f"Errore generazione TeX: {exc}")
            return None

        truncated_suffix = ""
        if result.truncated_names:
            truncated_suffix = f" | nomi troncati: {', '.join(result.truncated_names)}"

        self._set_status(
            f"TeX generato: {result.output_path} | oggetti: {result.item_count} | troncati: {result.truncated_count}{truncated_suffix}"
        )
        return result

    def _generate_pdf(self):
        generation_result = self._generate_tex()
        if generation_result is None:
            return

        try:
            compile_result = compile_items_pdf()
        except Exception as exc:
            self._show_error("Errore", f"Errore compilazione: {exc}")
            return

        self._log_compile_result(compile_result)
        if compile_result.succeeded:
            self._set_status(f"PDF oggetti generato: {Path(compile_result.output_pdf)}")
        else:
            self._set_status(f"Compilazione oggetti fallita con codice {compile_result.returncode}")
            messagebox.showerror(
                "Compilazione fallita",
                compile_result.stderr or compile_result.stdout or "Errore LaTeX.",
            )

    def _generate_single_page_pdf(self):
        generation_result = self._generate_tex()
        if generation_result is None:
            return

        try:
            compile_result = compile_single_page_items_pdf()
        except Exception as exc:
            self._show_error("Errore", f"Errore compilazione: {exc}")
            return

        self._log_compile_result(compile_result)
        if compile_result.succeeded:
            self._set_status(f"PDF oggetti one-page generato: {Path(compile_result.output_pdf)}")
        else:
            self._set_status(f"Compilazione one-page fallita con codice {compile_result.returncode}")
            messagebox.showerror(
                "Compilazione fallita",
                compile_result.stderr or compile_result.stdout or "Errore LaTeX.",
            )


class SpellDeckMainWindow(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=12)
        self.master = master
        self._build()

    def _build(self):
        self.grid(sticky="nsew")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        notebook = ttk.Notebook(self)
        notebook.grid(row=0, column=0, sticky="nsew")

        spells_tab = SpellsTab(notebook)
        items_tab = ItemsTab(notebook)

        notebook.add(spells_tab, text="Magie")
        notebook.add(items_tab, text="Oggetti")
