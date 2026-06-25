import tkinter as tk
from tkinter import messagebox

gejala = {
    "G01": "Proses booting berlangsung lama",
    "G02": "Penggunaan RAM lebih dari 90%",
    "G03": "Disk Usage mencapai 100%",
    "G04": "Banyak aplikasi berjalan saat startup",
    "G05": "Aplikasi sering mengalami freeze",
    "G06": "Membuka aplikasi terasa lambat",
    "G07": "Kapasitas penyimpanan hampir penuh",
    "G08": "Antivirus mendeteksi malware",
    "G09": "Suhu prosesor tinggi",
    "G10": "Kipas pendingin berputar sangat cepat"
}

penyebab = {
    "P01": "Penggunaan RAM Berlebihan",
    "P02": "Kapasitas Penyimpanan Hampir Penuh",
    "P03": "Terlalu Banyak Program Startup",
    "P04": "Malware",
    "P05": "Thermal Throttling"
}

prior = {"P01":0.30,"P02":0.25,"P03":0.20,"P04":0.15,"P05":0.10}

likelihood = {
    "P01":{"G01":0.50,"G02":0.90,"G03":0.20,"G04":0.30,"G05":0.60,"G06":0.80,"G07":0.10,"G08":0.03,"G09":0.27,"G10":0.33},
    "P02":{"G01":0.56,"G02":0.08,"G03":0.88,"G04":0.16,"G05":0.40,"G06":0.76,"G07":0.96,"G08":0.04,"G09":0.08,"G10":0.08},
    "P03":{"G01":0.85,"G02":0.20,"G03":0.15,"G04":0.90,"G05":0.30,"G06":0.75,"G07":0.10,"G08":0.00,"G09":0.05,"G10":0.10},
    "P04":{"G01":0.53,"G02":0.27,"G03":0.60,"G04":0.33,"G05":0.73,"G06":0.80,"G07":0.13,"G08":0.93,"G09":0.20,"G10":0.20},
    "P05":{"G01":0.20,"G02":0.10,"G03":0.10,"G04":0.10,"G05":0.60,"G06":0.70,"G07":0.00,"G08":0.00,"G09":0.90,"G10":0.90}
}

rekomendasi = {
    "P01":["Tutup aplikasi yang tidak diperlukan","Restart komputer","Upgrade RAM bila memungkinkan"],
    "P02":["Hapus file tidak penting","Gunakan Disk Cleanup","Pindahkan data ke drive lain"],
    "P03":["Nonaktifkan startup tidak penting","Kelola Startup Apps"],
    "P04":["Full scan antivirus","Update Windows Defender","Hapus malware"],
    "P05":["Bersihkan kipas","Ganti thermal paste","Perbaiki ventilasi"]
}

BG = "#1a1a1a"
CARD = "#242424"
CARD_BORDER = "#333333"
TEXT = "#e8e8e8"
TEXT_DIM = "#888888"
ACCENT = "#ffffff"
BTN_BG = "#333333"
BTN_HOVER = "#444444"
RADIUS = 16


class RoundedFrame(tk.Canvas):
    def __init__(self, parent, bg_color=CARD, border_color=CARD_BORDER, radius=RADIUS, **kw):
        super().__init__(parent, bg=BG, highlightthickness=0, **kw)
        self.bg_color = bg_color
        self.border_color = border_color
        self.radius = radius
        self.inner = tk.Frame(self, bg=bg_color)
        self._inner_id = self.create_window(0, 0, window=self.inner, anchor="nw")
        self.bind("<Configure>", self._redraw)

    def _redraw(self, e=None):
        self.delete("bg")
        w, h = self.winfo_width(), self.winfo_height()
        r = self.radius
        self._round_rect(1, 1, w-1, h-1, r, fill=self.bg_color,
                         outline=self.border_color, width=1, tags="bg")
        self.tag_lower("bg")
        self.coords(self._inner_id, r // 2, r // 2)
        self.itemconfig(self._inner_id, width=w - r, height=h - r)

    def _round_rect(self, x1, y1, x2, y2, r, **kw):
        points = [
            x1+r, y1, x2-r, y1,
            x2-r, y1, x2, y1, x2, y1+r,
            x2, y2-r, x2, y2, x2-r, y2,
            x1+r, y2, x1, y2, x1, y2-r,
            x1, y1+r, x1, y1, x1+r, y1
        ]
        return self.create_polygon(points, smooth=True, **kw)


class CustomCheckbox(tk.Canvas):
    def __init__(self, parent, text="", variable=None, bg=CARD, fg=TEXT, size=20):
        super().__init__(parent, width=size, height=size, bg=bg, highlightthickness=0)
        self._var = variable
        self._size = size
        self._bg = bg
        self._fg = fg
        self._text = text
        self._label = tk.Label(parent, text=text, font=("Segoe UI", 10),
                               bg=bg, fg=fg, cursor="hand2")
        self._draw()
        self.config(cursor="hand2")
        self.bind("<Button-1>", self._toggle)
        self._label.bind("<Button-1>", self._toggle)
        if self._var:
            self._var.trace_add("write", lambda *a: self._draw())

    def _toggle(self, e=None):
        if self._var:
            self._var.set(not self._var.get())

    def _draw(self):
        self.delete("all")
        s = self._size
        r = 4
        pts = [
            r,0, s-r,0, s-r,0, s,0, s,r,
            s,s-r, s,s, s-r,s,
            r,s, 0,s, 0,s-r,
            0,r, 0,0, r,0
        ]
        checked = self._var.get() if self._var else False
        fill = "#d0d0d0" if checked else "#3a3a3a"
        outline = "#888888" if checked else "#555555"
        self.create_polygon(pts, smooth=True, fill=fill, outline=outline)
        if checked:
            self.create_line(4, s//2, s//2-1, s-5, fill="#1a1a1a", width=2)
            self.create_line(s//2-1, s-5, s-3, 4, fill="#1a1a1a", width=2)

    def pack_row(self, **kw):
        self.pack(side="left", padx=(0, 10), **kw)
        self._label.pack(side="left")


class RoundedButton(tk.Canvas):
    def __init__(self, parent, text="", command=None, bg_color=BTN_BG,
                 fg_color=TEXT, hover_color=BTN_HOVER, font=("Segoe UI", 11),
                 btn_width=200, btn_height=44, radius=12, parent_bg=None):
        pbg = parent_bg or BG
        super().__init__(parent, width=btn_width, height=btn_height,
                         bg=pbg, highlightthickness=0)
        self.command = command
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.hover_color = hover_color
        self.radius = radius
        self._text = text
        self._font = font
        self._bw = btn_width
        self._bh = btn_height
        self.after(10, lambda: self._draw(bg_color))
        self.bind("<Enter>", lambda e: self._draw(hover_color))
        self.bind("<Leave>", lambda e: self._draw(bg_color))
        self.bind("<ButtonRelease-1>", lambda e: self.command() if self.command else None)
        self.config(cursor="hand2")

    def _draw(self, fill):
        self.delete("all")
        r = self.radius
        w, h = self._bw, self._bh
        pts = [
            r, 0, w-r, 0, w-r, 0, w, 0, w, r,
            w, h-r, w, h, w-r, h,
            r, h, 0, h, 0, h-r,
            0, r, 0, 0, r, 0
        ]
        self.create_polygon(pts, smooth=True, fill=fill, outline="")
        self.create_text(w//2, h//2, text=self._text, fill=self.fg_color, font=self._font)


class App:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Diagnosis Performa Komputer")
        self.root.geometry("660x740")
        self.root.configure(bg=BG)
        self.root.minsize(520, 600)

        self.vars_cb = {}
        self.welcome_frame = None
        self.diagnose_frame = None
        self.history = []

        self.show_welcome()
        self.root.mainloop()

    def clear_root(self):
        for w in self.root.winfo_children():
            w.destroy()

    def show_welcome(self):
        self.clear_root()

        spacer = tk.Frame(self.root, bg=BG)
        spacer.pack(expand=True)

        center = tk.Frame(self.root, bg=BG)
        center.pack()

        icon_canvas = tk.Canvas(center, width=72, height=72, bg=BG, highlightthickness=0)
        icon_canvas.pack(pady=(0, 24))
        icon_canvas.create_oval(4, 4, 68, 68, outline="#444444", width=2)
        icon_canvas.create_text(36, 32, text="⚙", font=("Segoe UI", 28), fill=TEXT)

        tk.Label(center, text="Sistem Diagnosis", font=("Segoe UI", 26, "bold"),
                 bg=BG, fg=TEXT).pack()
        tk.Label(center, text="Penurunan Performa Komputer",
                 font=("Segoe UI", 13), bg=BG, fg=TEXT_DIM).pack(pady=(4, 6))
        tk.Label(center, text="Metode Teorema Bayes",
                 font=("Segoe UI", 10), bg=BG, fg="#666666").pack(pady=(0, 32))

        RoundedButton(center, text="Mulai Diagnosa", command=self.show_diagnose,
                      bg_color=ACCENT, fg_color="#1a1a1a", hover_color="#d4d4d4",
                      font=("Segoe UI", 12, "bold"), btn_width=220, btn_height=48,
                      radius=24).pack()

        tk.Label(center, text="Pilih gejala komputer Anda untuk mendapatkan\nanalisis penyebab dan rekomendasi perbaikan",
                 font=("Segoe UI", 9), bg=BG, fg="#555555", justify="center").pack(pady=(20, 0))

        spacer2 = tk.Frame(self.root, bg=BG)
        spacer2.pack(expand=True)

    def show_diagnose(self):
        self.clear_root()
        self.vars_cb = {}

        canvas = tk.Canvas(self.root, bg=BG, highlightthickness=0)
        scrollbar = tk.Scrollbar(self.root, orient="vertical", command=canvas.yview,
                                 bg=BG, troughcolor=BG)
        canvas.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)

        container = tk.Frame(canvas, bg=BG)
        cw = canvas.create_window((0, 0), window=container, anchor="nw")
        canvas.bind("<Configure>", lambda e: canvas.itemconfig(cw, width=e.width))
        container.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        def scroll_linux(e):
            if e.num == 4: canvas.yview_scroll(-3, "units")
            elif e.num == 5: canvas.yview_scroll(3, "units")
        canvas.bind_all("<Button-4>", scroll_linux)
        canvas.bind_all("<Button-5>", scroll_linux)
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(int(-1*(e.delta/120)), "units"))

        self._canvas = canvas
        self._container = container

        header = tk.Frame(container, bg=BG)
        header.pack(fill="x", padx=28, pady=(24, 0))

        back_btn = RoundedButton(header, text="←  Kembali", command=self.show_welcome,
                                 bg_color=BTN_BG, fg_color=TEXT, hover_color=BTN_HOVER,
                                 font=("Segoe UI", 10), btn_width=110, btn_height=34, radius=10)
        back_btn.pack(anchor="w")

        tk.Label(header, text="Pilih Gejala", font=("Segoe UI", 20, "bold"),
                 bg=BG, fg=TEXT).pack(anchor="w", pady=(16, 2))
        tk.Label(header, text="Centang gejala yang dialami komputer Anda",
                 font=("Segoe UI", 10), bg=BG, fg=TEXT_DIM).pack(anchor="w", pady=(0, 16))

        card = RoundedFrame(container, height=self._calc_card_height())
        card.pack(fill="x", padx=28, pady=(0, 16))

        for i, (kode, nama) in enumerate(gejala.items()):
            v = tk.BooleanVar()
            self.vars_cb[kode] = v
            row = tk.Frame(card.inner, bg=CARD)
            row.pack(fill="x", padx=16, pady=(10 if i == 0 else 5, 10 if i == len(gejala)-1 else 5))
            cb = CustomCheckbox(row, text=nama, variable=v)
            cb.pack_row()
            if i < len(gejala) - 1:
                tk.Frame(card.inner, height=1, bg="#2e2e2e").pack(fill="x", padx=16)

        btn_row = tk.Frame(container, bg=BG)
        btn_row.pack(fill="x", padx=28, pady=(0, 16))

        RoundedButton(btn_row, text="Diagnosa", command=self._run_diagnose,
                      bg_color=ACCENT, fg_color="#1a1a1a", hover_color="#d4d4d4",
                      font=("Segoe UI", 11, "bold"), btn_width=280, btn_height=46, radius=14).pack(side="left", padx=(0, 8))

        RoundedButton(btn_row, text="Reset", command=self._reset,
                      bg_color=BTN_BG, fg_color=TEXT, hover_color=BTN_HOVER,
                      font=("Segoe UI", 11), btn_width=120, btn_height=46, radius=14).pack(side="left")

        self._result_card = None
        self._formula_card = None
        self._history_card = None

    def _calc_card_height(self):
        return len(gejala) * 42 + 30

    def _run_diagnose(self):
        selected = [k for k, v in self.vars_cb.items() if v.get()]
        if not selected:
            messagebox.showwarning("Peringatan", "Pilih minimal satu gejala.")
            return

        scores = {}
        for p in penyebab:
            s = prior[p]
            for g in selected:
                s *= likelihood[p][g]
            scores[p] = s

        total = sum(scores.values())
        posterior = {k: (v / total if total else 0) for k, v in scores.items()}
        ranking = sorted(posterior.items(), key=lambda x: x[1], reverse=True)
        best = ranking[0][0]

        from datetime import datetime
        self.history.append({
            "time": datetime.now().strftime("%H:%M:%S"),
            "gejala": [gejala[g] for g in selected],
            "result": penyebab[best],
            "prob": ranking[0][1] * 100
        })

        for card in [self._result_card, self._formula_card, self._history_card]:
            if card:
                card.destroy()

        rh = len(ranking) * 56 + len(rekomendasi[best]) * 28 + 300
        self._result_card = RoundedFrame(self._container, height=rh)
        self._result_card.pack(fill="x", padx=28, pady=(0, 16))

        inner = self._result_card.inner

        tk.Label(inner, text="HASIL DIAGNOSIS", font=("Segoe UI", 12, "bold"),
                 bg=CARD, fg=TEXT).pack(anchor="w", pady=(0, 10))
        tk.Frame(inner, height=1, bg=CARD_BORDER).pack(fill="x", pady=(0, 14))

        tk.Label(inner, text="Penyebab Utama", font=("Segoe UI", 9),
                 bg=CARD, fg=TEXT_DIM).pack(anchor="w")
        tk.Label(inner, text=penyebab[best], font=("Segoe UI", 16, "bold"),
                 bg=CARD, fg=ACCENT).pack(anchor="w", pady=(2, 10))

        prob_pct = ranking[0][1] * 100
        pf = tk.Frame(inner, bg=CARD)
        pf.pack(fill="x")
        tk.Label(pf, text="Probabilitas", font=("Segoe UI", 9),
                 bg=CARD, fg=TEXT_DIM).pack(side="left")
        tk.Label(pf, text=f"{prob_pct:.2f}%", font=("Segoe UI", 10, "bold"),
                 bg=CARD, fg=TEXT).pack(side="right")

        bar_canvas = tk.Canvas(inner, height=8, bg=CARD, highlightthickness=0)
        bar_canvas.pack(fill="x", pady=(6, 14))
        bar_canvas.update_idletasks()
        bw = bar_canvas.winfo_width() or 400
        bar_canvas.create_polygon(
            4,0, bw-4,0, bw,0, bw,4, bw,4, bw,8, bw-4,8, 4,8, 0,8, 0,4, 0,4, 0,0,
            smooth=True, fill="#333333", outline="")
        fw = max(8, int(bw * min(prob_pct / 100, 1.0)))
        bar_canvas.create_polygon(
            4,0, fw-4,0, fw,0, fw,4, fw,4, fw,8, fw-4,8, 4,8, 0,8, 0,4, 0,4, 0,0,
            smooth=True, fill="#d0d0d0", outline="")

        tk.Frame(inner, height=1, bg=CARD_BORDER).pack(fill="x", pady=(0, 12))

        tk.Label(inner, text="Ranking Penyebab", font=("Segoe UI", 11, "bold"),
                 bg=CARD, fg=TEXT).pack(anchor="w", pady=(0, 6))

        for i, (p, val) in enumerate(ranking):
            row = tk.Frame(inner, bg=CARD)
            row.pack(fill="x", pady=(4, 4))

            top = tk.Frame(row, bg=CARD)
            top.pack(fill="x")
            tk.Label(top, text=f"{i+1}.", font=("Segoe UI", 10),
                     bg=CARD, fg=TEXT_DIM).pack(side="left")
            tk.Label(top, text=penyebab[p], font=("Segoe UI", 10),
                     bg=CARD, fg=TEXT).pack(side="left", padx=(4, 0))
            tk.Label(top, text=f"{val*100:.2f}%", font=("Segoe UI", 10, "bold"),
                     bg=CARD, fg=TEXT).pack(side="right")

            bar_bg = tk.Frame(row, height=6, bg="#2e2e2e")
            bar_bg.pack(fill="x", padx=(20, 50), pady=(3, 0))
            bar_fill = tk.Frame(bar_bg, height=6, bg="#c0c0c0")
            bar_fill.place(relwidth=max(0.02, val), relheight=1.0)

        tk.Frame(inner, height=1, bg=CARD_BORDER).pack(fill="x", pady=(12, 12))

        tk.Label(inner, text="Rekomendasi", font=("Segoe UI", 11, "bold"),
                 bg=CARD, fg=TEXT).pack(anchor="w", pady=(0, 6))

        for r in rekomendasi[best]:
            row = tk.Frame(inner, bg=CARD)
            row.pack(fill="x", pady=2)
            tk.Label(row, text="→", font=("Segoe UI", 10),
                     bg=CARD, fg=TEXT_DIM).pack(side="left", padx=(0, 8))
            tk.Label(row, text=r, font=("Segoe UI", 10),
                     bg=CARD, fg=TEXT).pack(side="left")

        self._build_formula_card(selected, scores, total, posterior, ranking)
        self._build_history_card()

        self._canvas.update_idletasks()
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))
        self._canvas.yview_moveto(1.0)

    def _build_formula_card(self, selected, scores, total, posterior, ranking):
        lines = []
        lines.append("Rumus Teorema Bayes:")
        lines.append("P(Pᵢ|G) = [P(Pᵢ) × ∏P(Gⱼ|Pᵢ)] / Σ[P(Pₖ) × ∏P(Gⱼ|Pₖ)]")
        lines.append("")
        lines.append(f"Gejala dipilih: {len(selected)}")
        for g in selected:
            lines.append(f"  • {g} — {gejala[g]}")
        lines.append("")

        for p in penyebab:
            lines.append(f"── {penyebab[p]} ({p}) ──")
            lines.append(f"  Prior P({p}) = {prior[p]}")
            parts = []
            val = prior[p]
            for g in selected:
                lk = likelihood[p][g]
                parts.append(f"P({g}|{p})={lk}")
                val *= lk
            lines.append(f"  Likelihood: {' × '.join(parts)}")
            lines.append(f"  Score = {prior[p]} × {' × '.join(str(likelihood[p][g]) for g in selected)} = {scores[p]:.10f}")
            lines.append("")

        lines.append(f"Total Score = {total:.10f}")
        lines.append("")
        lines.append("Posterior (normalisasi):")
        for p, val in ranking:
            lines.append(f"  P({p}|G) = {scores[p]:.10f} / {total:.10f} = {val*100:.2f}%")

        fh = len(lines) * 18 + 60
        self._formula_card = RoundedFrame(self._container, height=fh)
        self._formula_card.pack(fill="x", padx=28, pady=(0, 16))
        fi = self._formula_card.inner

        tk.Label(fi, text="PERHITUNGAN BAYES", font=("Segoe UI", 12, "bold"),
                 bg=CARD, fg=TEXT).pack(anchor="w", pady=(0, 10))
        tk.Frame(fi, height=1, bg=CARD_BORDER).pack(fill="x", pady=(0, 10))

        for line in lines:
            if line.startswith("──"):
                tk.Label(fi, text=line, font=("Segoe UI", 10, "bold"),
                         bg=CARD, fg="#b0b0b0").pack(anchor="w", pady=(6, 2))
            elif line.startswith("Rumus") or line.startswith("Posterior"):
                tk.Label(fi, text=line, font=("Segoe UI", 10, "bold"),
                         bg=CARD, fg=TEXT).pack(anchor="w", pady=(2, 0))
            elif line == "":
                tk.Frame(fi, height=4, bg=CARD).pack()
            else:
                tk.Label(fi, text=line, font=("Consolas", 9),
                         bg=CARD, fg=TEXT_DIM).pack(anchor="w")

    def _build_history_card(self):
        if self._history_card:
            self._history_card.destroy()

        hh = len(self.history) * 60 + 60
        self._history_card = RoundedFrame(self._container, height=hh)
        self._history_card.pack(fill="x", padx=28, pady=(0, 24))
        hi = self._history_card.inner

        tk.Label(hi, text="RIWAYAT DIAGNOSIS", font=("Segoe UI", 12, "bold"),
                 bg=CARD, fg=TEXT).pack(anchor="w", pady=(0, 10))
        tk.Frame(hi, height=1, bg=CARD_BORDER).pack(fill="x", pady=(0, 10))

        for i, h in enumerate(reversed(self.history)):
            row = tk.Frame(hi, bg=CARD)
            row.pack(fill="x", pady=(4, 4))

            top = tk.Frame(row, bg=CARD)
            top.pack(fill="x")
            tk.Label(top, text=f"#{len(self.history)-i}", font=("Segoe UI", 10, "bold"),
                     bg=CARD, fg=TEXT_DIM).pack(side="left")
            tk.Label(top, text=h["result"], font=("Segoe UI", 10, "bold"),
                     bg=CARD, fg=TEXT).pack(side="left", padx=(8, 0))
            tk.Label(top, text=f"{h['prob']:.2f}%", font=("Segoe UI", 10),
                     bg=CARD, fg=TEXT_DIM).pack(side="right")
            tk.Label(top, text=h["time"], font=("Segoe UI", 9),
                     bg=CARD, fg="#555555").pack(side="right", padx=(0, 12))

            symptom_text = ", ".join(h["gejala"][:3])
            if len(h["gejala"]) > 3:
                symptom_text += f" +{len(h['gejala'])-3} lainnya"
            tk.Label(row, text=symptom_text, font=("Segoe UI", 9),
                     bg=CARD, fg="#666666").pack(anchor="w", padx=(30, 0))

            if i < len(self.history) - 1:
                tk.Frame(hi, height=1, bg="#2e2e2e").pack(fill="x", pady=(4, 0))

    def _reset(self):
        for v in self.vars_cb.values():
            v.set(False)
        for card in [self._result_card, self._formula_card, self._history_card]:
            if card:
                card.destroy()
        self._result_card = None
        self._formula_card = None
        self._history_card = None
        self._canvas.update_idletasks()
        self._canvas.configure(scrollregion=self._canvas.bbox("all"))


App()
