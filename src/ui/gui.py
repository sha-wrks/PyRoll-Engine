"""PyRoll Engine — main application window with Claude-inspired UI."""

import tkinter as tk
from tkinter import ttk, messagebox

from ..database.database import Database
from ..engine.payroll import PayrollCalculator
from .theme import COLORS, FONTS, PAD


class PyRollEngine:
    """Root application window."""

    def __init__(self) -> None:
        self.db   = Database()
        self.calc = PayrollCalculator()
        self._setup_window()
        self._setup_styles()
        self._build_ui()

    # ── Window & styles ─────────────────────────────────────────────────

    def _setup_window(self) -> None:
        self.root = tk.Tk()
        self.root.title("PyRoll Engine")
        self.root.geometry("760x840")
        self.root.minsize(640, 700)
        self.root.configure(bg=COLORS["bg_primary"])
        self.root.update_idletasks()
        sw, sh = self.root.winfo_screenwidth(), self.root.winfo_screenheight()
        self.root.geometry(f"760x840+{(sw-760)//2}+{(sh-840)//2}")

    def _setup_styles(self) -> None:
        s = ttk.Style()
        s.theme_use("clam")

        s.configure("Claude.TNotebook",
            background=COLORS["bg_primary"], borderwidth=0, tabmargins=[0, 0, 0, 0])
        s.configure("Claude.TNotebook.Tab",
            background=COLORS["bg_secondary"],
            foreground=COLORS["text_secondary"],
            padding=[22, 10],
            font=FONTS["body_md"],
            borderwidth=0)
        s.map("Claude.TNotebook.Tab",
            background=[("selected", COLORS["bg_card"]),  ("active", COLORS["bg_hover"])],
            foreground=[("selected", COLORS["accent_primary"]), ("active", COLORS["text_primary"])])

        s.configure("Claude.Treeview",
            background=COLORS["bg_card"],
            foreground=COLORS["text_primary"],
            rowheight=38,
            fieldbackground=COLORS["bg_card"],
            font=FONTS["body_md"],
            borderwidth=0)
        s.configure("Claude.Treeview.Heading",
            background=COLORS["bg_secondary"],
            foreground=COLORS["text_secondary"],
            font=FONTS["label"],
            relief="flat",
            borderwidth=0)
        s.map("Claude.Treeview.Heading",
            background=[("active", COLORS["bg_hover"])])
        s.map("Claude.Treeview",
            background=[("selected", COLORS["bg_hover"])],
            foreground=[("selected", COLORS["text_primary"])])

    # ── Top-level layout ────────────────────────────────────────────────

    def _build_ui(self) -> None:
        self._build_header()
        self._build_status_bar()

        self.notebook = ttk.Notebook(self.root, style="Claude.TNotebook")
        self.notebook.pack(fill="both", expand=True)

        calc_tab = tk.Frame(self.notebook, bg=COLORS["bg_primary"])
        emp_tab  = tk.Frame(self.notebook, bg=COLORS["bg_primary"])
        self.notebook.add(calc_tab, text="  Calculate  ")
        self.notebook.add(emp_tab,  text="  Employees  ")

        self._build_calculator_tab(calc_tab)
        self._build_employees_tab(emp_tab)

    def _build_header(self) -> None:
        header = tk.Frame(self.root, bg=COLORS["bg_header"], height=68)
        header.pack(fill="x")
        header.pack_propagate(False)

        # Left accent stripe
        tk.Frame(header, bg=COLORS["accent_primary"], width=5).pack(side="left", fill="y")

        inner = tk.Frame(header, bg=COLORS["bg_header"])
        inner.pack(side="left", fill="both", expand=True, padx=PAD["xl"])

        tk.Label(inner, text="PyRoll Engine",
                 font=FONTS["heading_lg"], fg=COLORS["text_on_dark"],
                 bg=COLORS["bg_header"]).pack(side="left", pady=PAD["lg"])
        tk.Label(inner, text="  —  Payroll Management System",
                 font=FONTS["body_md"], fg=COLORS["text_muted"],
                 bg=COLORS["bg_header"]).pack(side="left")

    def _build_status_bar(self) -> None:
        bar = tk.Frame(self.root, bg=COLORS["bg_secondary"], height=30)
        bar.pack(fill="x")
        bar.pack_propagate(False)

        label = "● Redis Connected" if self.db.using_redis else "● In-Memory Mode"
        color = COLORS["success"]    if self.db.using_redis else COLORS["warning"]
        tk.Label(bar, text=label, font=FONTS["body_sm"],
                 fg=color, bg=COLORS["bg_secondary"]).pack(side="left", padx=PAD["xl"], pady=5)

    # ── Calculate tab ───────────────────────────────────────────────────

    def _build_calculator_tab(self, parent: tk.Frame) -> None:
        canvas = tk.Canvas(parent, bg=COLORS["bg_primary"], highlightthickness=0)
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=canvas.yview)
        inner = tk.Frame(canvas, bg=COLORS["bg_primary"])

        inner.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        win = canvas.create_window((0, 0), window=inner, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(win, width=e.width))
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-(e.delta // 120), "units"))

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        content = tk.Frame(inner, bg=COLORS["bg_primary"])
        content.pack(fill="both", expand=True, padx=PAD["xl"], pady=PAD["xl"])

        # Input card
        _, form = self._card(content, "Employee Details", COLORS["accent_primary"])
        self.ent_name = self._field(form, "EMPLOYEE NAME")
        self.ent_hours = self._field(form, "HOURS WORKED")
        self.ent_rate  = self._field(form, "HOURLY RATE ($)")

        # Two-column row: deductions + tax
        two = tk.Frame(form, bg=COLORS["bg_card"])
        two.pack(fill="x", pady=(0, PAD["md"]))
        self.ent_deductions = self._inline_field(two, "DEDUCTIONS ($)", side="left",  padx=(0, PAD["sm"]))
        self.ent_tax        = self._inline_field(two, "TAX RATE (%)",   side="right", padx=(PAD["sm"], 0))

        self.ent_bonus = self._field(form, "BONUS ($)")

        btns = tk.Frame(form, bg=COLORS["bg_card"])
        btns.pack(fill="x", pady=(PAD["md"], 0))
        self._btn(btns, "Calculate Salary", self._calculate,
                  COLORS["accent_primary"], COLORS["accent_hover"]).pack(side="left", padx=(0, PAD["sm"]))
        self._btn(btns, "Save Employee", self._save,
                  COLORS["btn_secondary"], COLORS["btn_secondary_hover"]).pack(side="left")

        # Results card
        _, res = self._card(content, "Calculation Results", COLORS["success"])
        self.result_text = tk.Text(
            res, height=9, font=FONTS["mono_md"],
            bg=COLORS["bg_secondary"], fg=COLORS["text_secondary"],
            relief="flat", cursor="arrow", wrap="word",
            padx=PAD["lg"], pady=PAD["md"], state="disabled")
        self.result_text.pack(fill="x")
        self._set_result("Results will appear here after calculation.")

    # ── Employees tab ───────────────────────────────────────────────────

    def _build_employees_tab(self, parent: tk.Frame) -> None:
        content = tk.Frame(parent, bg=COLORS["bg_primary"])
        content.pack(fill="both", expand=True, padx=PAD["xl"], pady=PAD["xl"])

        toolbar = tk.Frame(content, bg=COLORS["bg_primary"])
        toolbar.pack(fill="x", pady=(0, PAD["md"]))
        tk.Label(toolbar, text="All Employees", font=FONTS["heading_md"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_primary"]).pack(side="left")
        self._btn(toolbar, "Refresh", self._refresh_employees,
                  COLORS["accent_primary"], COLORS["accent_hover"],
                  small=True).pack(side="right")

        table_card = tk.Frame(content, bg=COLORS["bg_card"],
                              highlightbackground=COLORS["border_light"], highlightthickness=1)
        table_card.pack(fill="both", expand=True)
        table_card.rowconfigure(0, weight=1)
        table_card.columnconfigure(0, weight=1)

        cols = ("name", "hours", "rate", "gross", "tax", "deductions", "bonus", "net")
        self.tree = ttk.Treeview(table_card, columns=cols, show="headings",
                                 style="Claude.Treeview", selectmode="browse")

        col_defs = [
            ("name",       "Employee",        160, "w"),
            ("hours",      "Hours",             60, "e"),
            ("rate",       "Rate ($)",          80, "e"),
            ("gross",      "Gross Pay ($)",    100, "e"),
            ("tax",        "Tax ($)",           80, "e"),
            ("deductions", "Deductions ($)",   110, "e"),
            ("bonus",      "Bonus ($)",         80, "e"),
            ("net",        "Net Pay ($)",      100, "e"),
        ]
        for cid, heading, width, anchor in col_defs:
            self.tree.heading(cid, text=heading)
            self.tree.column(cid, width=width, anchor=anchor, minwidth=50)

        v_sb = ttk.Scrollbar(table_card, orient="vertical",   command=self.tree.yview)
        h_sb = ttk.Scrollbar(table_card, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_sb.set, xscrollcommand=h_sb.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        v_sb.grid(row=0, column=1, sticky="ns")
        h_sb.grid(row=1, column=0, sticky="ew")

        self.tree.tag_configure("odd",  background=COLORS["bg_card"])
        self.tree.tag_configure("even", background=COLORS["bg_primary"])

        self._refresh_employees()

    # ── Widget helpers ──────────────────────────────────────────────────

    def _card(self, parent: tk.Frame, title: str, accent: str):
        """Return (card_frame, body_frame) with a colored top stripe."""
        card = tk.Frame(parent, bg=COLORS["bg_card"],
                        highlightbackground=COLORS["border_light"], highlightthickness=1)
        card.pack(fill="x", pady=(0, PAD["lg"]))

        tk.Frame(card, bg=accent, height=3).pack(fill="x")

        body = tk.Frame(card, bg=COLORS["bg_card"])
        body.pack(fill="both", padx=PAD["xl"], pady=PAD["lg"])

        tk.Label(body, text=title, font=FONTS["heading_md"],
                 fg=COLORS["text_primary"], bg=COLORS["bg_card"]).pack(anchor="w", pady=(0, PAD["md"]))
        return card, body

    def _field(self, parent: tk.Frame, label: str) -> tk.Entry:
        """Labeled full-width input field packed into parent."""
        outer = tk.Frame(parent, bg=COLORS["bg_card"])
        outer.pack(fill="x", pady=(0, PAD["md"]))

        tk.Label(outer, text=label, font=FONTS["label"],
                 fg=COLORS["text_secondary"], bg=COLORS["bg_card"]).pack(anchor="w")

        border = tk.Frame(outer, bg=COLORS["border_light"], padx=1, pady=1)
        border.pack(fill="x", pady=(3, 0))

        entry = tk.Entry(border, font=FONTS["body_md"],
                         bg=COLORS["bg_input"], fg=COLORS["text_primary"],
                         relief="flat", insertbackground=COLORS["accent_primary"])
        entry.pack(fill="x", ipady=9, ipadx=PAD["sm"])

        entry.bind("<FocusIn>",  lambda e, b=border: b.config(bg=COLORS["accent_primary"]))
        entry.bind("<FocusOut>", lambda e, b=border: b.config(bg=COLORS["border_light"]))
        return entry

    def _inline_field(self, parent: tk.Frame, label: str,
                      side: str, padx: tuple) -> tk.Entry:
        """Half-width labeled field for the two-column row."""
        col = tk.Frame(parent, bg=COLORS["bg_card"])
        col.pack(side=side, fill="x", expand=True, padx=padx)

        tk.Label(col, text=label, font=FONTS["label"],
                 fg=COLORS["text_secondary"], bg=COLORS["bg_card"]).pack(anchor="w")

        border = tk.Frame(col, bg=COLORS["border_light"], padx=1, pady=1)
        border.pack(fill="x", pady=(3, 0))

        entry = tk.Entry(border, font=FONTS["body_md"],
                         bg=COLORS["bg_input"], fg=COLORS["text_primary"],
                         relief="flat", insertbackground=COLORS["accent_primary"])
        entry.pack(fill="x", ipady=9, ipadx=PAD["sm"])

        entry.bind("<FocusIn>",  lambda e, b=border: b.config(bg=COLORS["accent_primary"]))
        entry.bind("<FocusOut>", lambda e, b=border: b.config(bg=COLORS["border_light"]))
        return entry

    def _btn(self, parent: tk.Frame, text: str, cmd,
             bg: str, hover: str, small: bool = False) -> tk.Button:
        font = FONTS["body_sm"] if small else FONTS["body_md"]
        py   = 5 if small else 8
        btn  = tk.Button(parent, text=text, command=cmd, font=font,
                         bg=bg, fg=COLORS["text_on_accent"], relief="flat",
                         cursor="hand2", padx=PAD["md"], pady=py,
                         activebackground=hover,
                         activeforeground=COLORS["text_on_accent"], bd=0)
        btn.bind("<Enter>", lambda e: btn.config(bg=hover))
        btn.bind("<Leave>", lambda e: btn.config(bg=bg))
        return btn

    # ── Actions ─────────────────────────────────────────────────────────

    def _set_result(self, text: str, color: str | None = None) -> None:
        self.result_text.config(state="normal")
        self.result_text.delete("1.0", "end")
        self.result_text.insert("1.0", text)
        self.result_text.config(fg=color or COLORS["text_primary"])
        self.result_text.config(state="disabled")

    def _parse_inputs(self) -> tuple:
        name = self.ent_name.get().strip()
        if not name:
            raise ValueError("Employee name is required.")
        try:
            hours      = float(self.ent_hours.get()       or 0)
            rate       = float(self.ent_rate.get()        or 0)
            deductions = float(self.ent_deductions.get()  or 0)
            tax_rate   = float(self.ent_tax.get()         or 0)
            bonus      = float(self.ent_bonus.get()       or 0)
        except ValueError:
            raise ValueError("Hours, Rate, Deductions, Tax, and Bonus must be numeric values.")
        return name, hours, rate, deductions, tax_rate, bonus

    def _calculate(self) -> None:
        try:
            name, hours, rate, deductions, tax_rate, bonus = self._parse_inputs()
            gross, tax, net = self.calc.calculate_salary(hours, rate, deductions, tax_rate, bonus)
            sep = "─" * 42
            lines = [
                f"  Employee     {name}",
                f"  {sep}",
                f"  Gross Pay    ${gross:>12,.2f}",
                f"  Tax ({tax_rate:.1f}%)    ${tax:>12,.2f}",
                f"  Deductions   ${deductions:>12,.2f}",
                f"  Bonus        ${bonus:>12,.2f}",
                f"  {sep}",
                f"  Net Pay      ${net:>12,.2f}",
            ]
            self._set_result("\n".join(lines))
        except ValueError as exc:
            messagebox.showerror("Input Error", str(exc))

    def _save(self) -> None:
        try:
            name, hours, rate, deductions, tax_rate, bonus = self._parse_inputs()
            gross, tax, net = self.calc.calculate_salary(hours, rate, deductions, tax_rate, bonus)
            self.db.save_employee({
                "name": name, "hours": hours, "rate": rate,
                "deductions": deductions, "tax_rate": tax_rate,
                "bonus": bonus, "gross": gross, "tax": tax, "net_salary": net,
            })
            messagebox.showinfo("Saved", f"'{name}' has been saved successfully.")
            self._refresh_employees()
            self.notebook.select(1)
        except ValueError as exc:
            messagebox.showerror("Input Error", str(exc))

    def _refresh_employees(self) -> None:
        for item in self.tree.get_children():
            self.tree.delete(item)

        for i, emp in enumerate(self.db.get_all_employees()):
            try:
                hours      = float(emp.get("hours",      0))
                rate       = float(emp.get("rate",       0))
                deductions = float(emp.get("deductions", 0))
                tax_rate   = float(emp.get("tax_rate",   0))
                bonus      = float(emp.get("bonus",      0))
                gross, tax, net = self.calc.calculate_salary(hours, rate, deductions, tax_rate, bonus)
                tag = "odd" if i % 2 == 0 else "even"
                self.tree.insert("", "end", values=(
                    emp.get("name", "—"),
                    f"{hours:.0f}",
                    f"${rate:.2f}",
                    f"${gross:,.2f}",
                    f"${tax:,.2f}",
                    f"${deductions:,.2f}",
                    f"${bonus:,.2f}",
                    f"${net:,.2f}",
                ), tags=(tag,))
            except (ValueError, KeyError):
                continue

    def run(self) -> None:
        self.root.mainloop()
