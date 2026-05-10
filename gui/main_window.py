from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from spelldeck.compiler import compile_spell_pdf
from spelldeck.spells_data import DEFAULT_SPELLS_PATH
from spelldeck.spells_service import generate_spells_tex_file, parse_filter_string


class SpellDeckMainWindow(ttk.Frame):
    def __init__(self, master):
        super().__init__(master, padding=12)
        self.master = master
        self.dataset_path = tk.StringVar(value=str(DEFAULT_SPELLS_PATH))
        self.class_filter = tk.StringVar()
        self.level_filter = tk.StringVar()
        self.school_filter = tk.StringVar()
        self.name_filter = tk.StringVar()
        self.status_text = tk.StringVar(value="Ready.")
        self._build()

    def _build(self):
        self.grid(sticky="nsew")
        self.master.columnconfigure(0, weight=1)
        self.master.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        ttk.Label(self, text="Dataset JSON").grid(row=0, column=0, sticky="w", pady=(0, 8))
        ttk.Entry(self, textvariable=self.dataset_path).grid(
            row=0, column=1, sticky="ew", padx=(8, 8), pady=(0, 8)
        )
        ttk.Button(self, text="Sfoglia", command=self._choose_dataset).grid(
            row=0, column=2, sticky="ew", pady=(0, 8)
        )

        ttk.Label(self, text="Classi").grid(row=1, column=0, sticky="w", pady=4)
        ttk.Entry(self, textvariable=self.class_filter).grid(row=1, column=1, columnspan=2, sticky="ew", pady=4)

        ttk.Label(self, text="Livelli").grid(row=2, column=0, sticky="w", pady=4)
        ttk.Entry(self, textvariable=self.level_filter).grid(row=2, column=1, columnspan=2, sticky="ew", pady=4)

        ttk.Label(self, text="Scuole").grid(row=3, column=0, sticky="w", pady=4)
        ttk.Entry(self, textvariable=self.school_filter).grid(row=3, column=1, columnspan=2, sticky="ew", pady=4)

        ttk.Label(self, text="Nomi").grid(row=4, column=0, sticky="w", pady=4)
        ttk.Entry(self, textvariable=self.name_filter).grid(row=4, column=1, columnspan=2, sticky="ew", pady=4)

        hint = "Usa valori separati da virgola. Per i livelli puoi usare anche range come 1-3."
        ttk.Label(self, text=hint).grid(row=5, column=0, columnspan=3, sticky="w", pady=(4, 10))

        buttons = ttk.Frame(self)
        buttons.grid(row=6, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        buttons.columnconfigure(0, weight=1)
        buttons.columnconfigure(1, weight=1)
        ttk.Button(buttons, text="Genera TeX", command=self._generate_tex).grid(row=0, column=0, sticky="ew", padx=(0, 6))
        ttk.Button(buttons, text="Genera PDF", command=self._generate_pdf).grid(row=0, column=1, sticky="ew", padx=(6, 0))

        ttk.Label(self, text="Log").grid(row=7, column=0, sticky="w")
        self.log_widget = tk.Text(self, height=16, wrap="word")
        self.log_widget.grid(row=8, column=0, columnspan=3, sticky="nsew")
        self.rowconfigure(8, weight=1)

        ttk.Label(self, textvariable=self.status_text).grid(row=9, column=0, columnspan=3, sticky="w", pady=(10, 0))

    def _choose_dataset(self):
        selected_path = filedialog.askopenfilename(
            title="Seleziona dataset magie",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
        )
        if selected_path:
            self.dataset_path.set(selected_path)

    def _collect_filters(self):
        return {
            "dataset_path": self._resolve_dataset_path(),
            "classes": parse_filter_string(self.class_filter.get()),
            "levels": parse_filter_string(self.level_filter.get()),
            "schools": parse_filter_string(self.school_filter.get()),
            "names": parse_filter_string(self.name_filter.get()),
        }

    def _resolve_dataset_path(self):
        dataset = self.dataset_path.get().strip()
        return dataset or str(DEFAULT_SPELLS_PATH)

    def _append_log(self, message):
        self.log_widget.insert("end", message.rstrip() + "\n")
        self.log_widget.see("end")

    def _set_status(self, message):
        self.status_text.set(message)
        self._append_log(message)

    def _generate_tex(self):
        try:
            filters = self._collect_filters()
            result = generate_spells_tex_file(**filters)
        except Exception as exc:
            self._set_status(f"Errore generazione TeX: {exc}")
            messagebox.showerror("Errore", str(exc))
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
            self._set_status(f"Errore compilazione: {exc}")
            messagebox.showerror("Errore", str(exc))
            return

        if compile_result.stdout:
            self._append_log(compile_result.stdout)
        if compile_result.stderr:
            self._append_log(compile_result.stderr)

        if compile_result.succeeded:
            self._set_status(f"PDF generato: {Path(compile_result.output_pdf)}")
        else:
            self._set_status(f"Compilazione fallita con codice {compile_result.returncode}")
            messagebox.showerror("Compilazione fallita", compile_result.stderr or compile_result.stdout or "Errore LaTeX.")

