from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from spelldeck.compiler import (
    compile_items_pdf,
    compile_single_page_items_pdf,
    compile_spell_pdf,
)
from spelldeck.items_data import DEFAULT_ITEMS_PATH
from spelldeck.items_service import generate_items_tex_file, preview_items
from spelldeck.spells_data import DEFAULT_SPELLS_PATH
from spelldeck.spells_service import (
    analyze_spells_dataset,
    generate_spells_tex_file,
    parse_filter_string,
    preview_spells,
)


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

    def _show_preview_popup(self, title, names):
        preview_window = tk.Toplevel(self)
        preview_window.title(title)
        preview_window.minsize(420, 360)
        preview_window.transient(self.winfo_toplevel())
        preview_window.grab_set()
        preview_window.columnconfigure(0, weight=1)
        preview_window.rowconfigure(1, weight=1)

        ttk.Label(
            preview_window,
            text=f"Elementi selezionati: {len(names)}",
            padding=(12, 12, 12, 6),
        ).grid(row=0, column=0, sticky="w")

        list_frame = ttk.Frame(preview_window, padding=(12, 0, 12, 12))
        list_frame.grid(row=1, column=0, sticky="nsew")
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        listbox = tk.Listbox(list_frame)
        listbox.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        listbox.configure(yscrollcommand=scrollbar.set)

        for name in names:
            listbox.insert("end", name)

        ttk.Button(preview_window, text="Chiudi", command=preview_window.destroy).grid(
            row=2, column=0, sticky="e", padx=12, pady=(0, 12)
        )


class SpellsTab(BaseGeneratorTab):
    dataset_label = "Dataset magie"
    browse_title = "Seleziona dataset magie"
    hint_text = "Usa valori separati da virgola. Per i livelli puoi usare anche range come 1-3."

    def __init__(self, master):
        self.class_filter = tk.StringVar()
        self.level_filter = tk.StringVar()
        self.school_filter = tk.StringVar()
        self.name_filter = tk.StringVar()
        self.analysis_text = tk.StringVar(value="Analisi dataset non ancora eseguita.")
        self.class_listbox = None
        self.school_listbox = None
        super().__init__(master, DEFAULT_SPELLS_PATH)

    def _build_form(self):
        actions = ttk.Frame(self)
        actions.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(0, 8))
        actions.columnconfigure(0, weight=0)
        actions.columnconfigure(1, weight=1)
        ttk.Button(actions, text="Analizza", command=self._analyze_dataset).grid(
            row=0, column=0, sticky="w"
        )
        ttk.Label(actions, textvariable=self.analysis_text).grid(
            row=0, column=1, sticky="w", padx=(12, 0)
        )

        ttk.Label(self, text="Classi").grid(row=2, column=0, sticky="w", pady=4)
        ttk.Entry(self, textvariable=self.class_filter).grid(
            row=2, column=1, columnspan=2, sticky="ew", pady=4
        )

        ttk.Label(self, text="Scuole").grid(row=3, column=0, sticky="w", pady=4)
        ttk.Entry(self, textvariable=self.school_filter).grid(
            row=3, column=1, columnspan=2, sticky="ew", pady=4
        )

        analysis_frame = ttk.Frame(self)
        analysis_frame.grid(row=4, column=0, columnspan=3, sticky="nsew", pady=(4, 10))
        analysis_frame.columnconfigure(0, weight=1)
        analysis_frame.columnconfigure(1, weight=1)

        class_frame = ttk.LabelFrame(analysis_frame, text="Classi trovate")
        class_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 6))
        class_frame.columnconfigure(0, weight=1)
        class_frame.rowconfigure(0, weight=1)
        self.class_listbox = tk.Listbox(class_frame, selectmode="extended", exportselection=False, height=6)
        self.class_listbox.grid(row=0, column=0, sticky="nsew")
        class_scrollbar = ttk.Scrollbar(class_frame, orient="vertical", command=self.class_listbox.yview)
        class_scrollbar.grid(row=0, column=1, sticky="ns")
        self.class_listbox.configure(yscrollcommand=class_scrollbar.set)
        self.class_listbox.bind("<<ListboxSelect>>", self._on_class_select)

        school_frame = ttk.LabelFrame(analysis_frame, text="Scuole trovate")
        school_frame.grid(row=0, column=1, sticky="nsew", padx=(6, 0))
        school_frame.columnconfigure(0, weight=1)
        school_frame.rowconfigure(0, weight=1)
        self.school_listbox = tk.Listbox(school_frame, selectmode="extended", exportselection=False, height=6)
        self.school_listbox.grid(row=0, column=0, sticky="nsew")
        school_scrollbar = ttk.Scrollbar(school_frame, orient="vertical", command=self.school_listbox.yview)
        school_scrollbar.grid(row=0, column=1, sticky="ns")
        self.school_listbox.configure(yscrollcommand=school_scrollbar.set)
        self.school_listbox.bind("<<ListboxSelect>>", self._on_school_select)

        ttk.Label(self, text="Livelli").grid(row=5, column=0, sticky="w", pady=4)
        ttk.Entry(self, textvariable=self.level_filter).grid(
            row=5, column=1, columnspan=2, sticky="ew", pady=4
        )

        ttk.Label(self, text="Nomi").grid(row=6, column=0, sticky="w", pady=4)
        ttk.Entry(self, textvariable=self.name_filter).grid(
            row=6, column=1, columnspan=2, sticky="ew", pady=4
        )

        ttk.Label(self, text=self.hint_text).grid(row=7, column=0, columnspan=3, sticky="w", pady=(4, 10))

        buttons = ttk.Frame(self)
        buttons.grid(row=8, column=0, columnspan=3, sticky="ew", pady=(0, 10))
        buttons.columnconfigure(0, weight=1)
        buttons.columnconfigure(1, weight=1)
        buttons.columnconfigure(2, weight=1)
        ttk.Button(buttons, text="Preview", command=self._preview).grid(
            row=0, column=0, sticky="ew", padx=(0, 6)
        )
        ttk.Button(buttons, text="Genera TeX", command=self._generate_tex).grid(
            row=0, column=1, sticky="ew", padx=6
        )
        ttk.Button(buttons, text="Genera PDF", command=self._generate_pdf).grid(
            row=0, column=2, sticky="ew", padx=(6, 0)
        )

    def _collect_filters(self):
        return {
            "dataset_path": self._resolve_dataset_path(DEFAULT_SPELLS_PATH),
            "classes": parse_filter_string(self.class_filter.get()),
            "levels": parse_filter_string(self.level_filter.get()),
            "schools": parse_filter_string(self.school_filter.get()),
            "names": parse_filter_string(self.name_filter.get()),
        }

    def _analyze_dataset(self):
        try:
            result = analyze_spells_dataset(self._resolve_dataset_path(DEFAULT_SPELLS_PATH))
        except Exception as exc:
            self._show_error("Errore", f"Errore analisi dataset: {exc}")
            return

        self.class_listbox.delete(0, "end")
        self.school_listbox.delete(0, "end")

        for value in result.classes:
            self.class_listbox.insert("end", value)
        for value in result.schools:
            self.school_listbox.insert("end", value)

        self._apply_existing_multiselect_filters()
        self.analysis_text.set(
            f"Dataset analizzato: {result.spell_count} magie | classi: {len(result.classes)} | scuole: {len(result.schools)}"
        )
        self._set_status("Analisi dataset magie completata.")

    def _apply_existing_multiselect_filters(self):
        selected_classes = set(parse_filter_string(self.class_filter.get()) or [])
        selected_schools = set(parse_filter_string(self.school_filter.get()) or [])

        for index in range(self.class_listbox.size()):
            if self.class_listbox.get(index).lower() in selected_classes:
                self.class_listbox.selection_set(index)

        for index in range(self.school_listbox.size()):
            if self.school_listbox.get(index).lower() in selected_schools:
                self.school_listbox.selection_set(index)

    def _on_class_select(self, _event=None):
        selected = [self.class_listbox.get(index) for index in self.class_listbox.curselection()]
        self.class_filter.set(", ".join(selected))

    def _on_school_select(self, _event=None):
        selected = [self.school_listbox.get(index) for index in self.school_listbox.curselection()]
        self.school_filter.set(", ".join(selected))

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

    def _preview(self):
        try:
            result = preview_spells(**self._collect_filters())
        except Exception as exc:
            self._show_error("Errore", f"Errore preview: {exc}")
            return

        self._set_status(f"Preview magie: {result.spell_count} elementi")
        self._show_preview_popup("Preview magie", result.names)

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
        buttons.columnconfigure(3, weight=1)
        ttk.Button(buttons, text="Preview", command=self._preview).grid(
            row=0, column=0, sticky="ew", padx=(0, 6)
        )
        ttk.Button(buttons, text="Genera TeX", command=self._generate_tex).grid(
            row=0, column=1, sticky="ew", padx=6
        )
        ttk.Button(buttons, text="Genera PDF", command=self._generate_pdf).grid(
            row=0, column=2, sticky="ew", padx=6
        )
        ttk.Button(buttons, text="Genera PDF 9 copie", command=self._generate_single_page_pdf).grid(
            row=0, column=3, sticky="ew", padx=(6, 0)
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

    def _preview(self):
        try:
            result = preview_items(**self._collect_filters())
        except Exception as exc:
            self._show_error("Errore", f"Errore preview: {exc}")
            return

        self._set_status(f"Preview oggetti: {result.item_count} elementi")
        self._show_preview_popup("Preview oggetti", result.names)

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
