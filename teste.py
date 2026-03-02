import tkinter as tk
import json
import termo

vocabulario=set()
entrada="res/lexico-5-letras"
with open(entrada, "r", encoding="utf-8") as arquivo:
    for linha in arquivo:
        palavras = linha.split()
        vocabulario.update(palavras)
COLORS = [
    ("#3a3a3c", "white"),   # 0 - cinza
    ("#c9b458", "black"),   # 1 - bege
    ("#538d4e", "white"),   # 2 - verde
]

BACKGROUND = "#000000"
BLUE = "#4ea1ff"

class TermoUI:
    def __init__(self, root, vocabulario):
        self.voc=vocabulario
        self.tempvoc=vocabulario
        self.root = root
        self.root.title("Resolvedor de Termo")
        self.root.configure(bg=BACKGROUND)

        self.states = [0] * 5
        self.entries = []
        self.history = []

        self.main_frame = tk.Frame(root, bg=BACKGROUND)
        self.main_frame.pack(padx=20, pady=20)

        self.create_grid()
        self.create_top15_panel(None)

        self.root.bind("<Return>", self.save_attempt)

    # ================= GRID =================
    def create_grid(self):
        frame = tk.Frame(self.main_frame, bg=BACKGROUND)
        frame.grid(row=0, column=0, padx=20)

        for i in range(5):
            entry = tk.Entry(
                frame,
                width=2,
                font=("Helvetica", 32),
                justify="center",
                bg=COLORS[0][0],
                fg=COLORS[0][1],
                insertbackground="white",
                relief="solid",
                bd=2
            )
            entry.grid(row=0, column=i, padx=6)
            entry.bind("<KeyRelease>", lambda e, idx=i: self.limit_char(idx))
            entry.bind("<Button-1>", lambda e, idx=i: self.toggle_color(idx))

            self.entries.append(entry)

    # ================= TOP 15 =================
    def create_top15_panel(self,top):
        if hasattr(self, "top15_frame"):
            self.top15_frame.destroy()

        frame = tk.Frame(self.main_frame, bg=BACKGROUND)
        frame.grid(row=0, column=1, sticky="n")

        title = tk.Label(
            frame,
            text="TOP 15 MELHORES ",
            font=("Segoe UI", 16, "bold"),
            fg=BLUE,
            bg=BACKGROUND
        )
        title.pack(pady=(0, 10))

        self.top15_labels = []
        if top is None:
            try:
                with open("res/top15.json", "r", encoding="utf-8") as f:
                    top15 = json.load(f)
            except FileNotFoundError:
                top15 = []
        else: 
            top15=top

        for i, item in enumerate(top15[:15], start=1):
            info = item[0]
            palavra = item[1]
            label = tk.Label(
                frame,
                text=f"{i:2d}. {palavra}  ({info:.2f} bits)",
                font=("Segoe UI", 16),
                fg=BLUE,
                bg=BACKGROUND,
                anchor="w"
            )
            label.pack(fill="x")
            self.top15_labels.append(label)
    def limit_char(self, idx):
        text = self.entries[idx].get().upper()
        self.entries[idx].delete(0, tk.END)
        self.entries[idx].insert(0, text[:1])

        if text and idx < 4:
            self.entries[idx + 1].focus()

    def toggle_color(self, idx):
        self.states[idx] = (self.states[idx] + 1) % 3
        bg, fg = COLORS[self.states[idx]]
        self.entries[idx].config(bg=bg, fg=fg)

    def save_attempt(self, event=None):
        word = "".join(e.get() for e in self.entries)

        if len(word) != 5 or not word.isalpha():
            return
        print(word)
        self.history.append((word, self.states.copy()))
        print(self.states)
        word=word.lower()
        newvoc=termo.gerar_vocabulario_possivel(word,self.states.copy(),self.tempvoc)
        self.tempvoc=newvoc
        top15=sorted( 
            termo.calcular_todos(newvoc),
            key=lambda x: x[0],
            reverse=True
            )[:15]
        print(top15)
        self.create_top15_panel(top15)
        print("Tentativa salva:", self.history[-1])
        
        self.clear_row()


    def clear_row(self):
        self.states = [0] * 5
        for entry in self.entries:
            entry.delete(0, tk.END)
            entry.config(bg=COLORS[0][0], fg=COLORS[0][1])
        self.entries[0].focus()


if __name__ == "__main__":
    vocabulario=set()
    entrada="lexico-5-letras"
    with open(entrada, "r", encoding="utf-8") as arquivo:
        for linha in arquivo:
            palavras = linha.split()
            vocabulario.update(palavras)
    root = tk.Tk()
    app = TermoUI(root,vocabulario)
    root.mainloop()
