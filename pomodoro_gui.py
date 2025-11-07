import tkinter as tk
from tkinter import messagebox
import time
import threading

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⏱️ Pomodoro Timer")
        self.root.geometry("360x420")
        self.root.resizable(False, False)

        # ======= VARIÁVEIS =======
        self.tempo_foco = 25 * 60
        self.tempo_pausa = 5 * 60
        self.em_pausa = False
        self.rodando = False
        self.ciclo = 1
        self.total_ciclos = 4

        # ======= CORES =======
        self.cor_foco = "#1E90FF"   # Azul
        self.cor_pausa = "#32CD32"  # Verde
        self.root.configure(bg=self.cor_foco)

        # ======= TÍTULO =======
        self.label_titulo = tk.Label(
            root,
            text="Pomodoro Timer",
            font=("Arial", 22, "bold"),
            bg=self.cor_foco,
            fg="white"
        )
        self.label_titulo.pack(pady=10)

        # ======= ENTRADAS =======
        frame_config = tk.Frame(root, bg=self.cor_foco)
        frame_config.pack(pady=10)

        tk.Label(frame_config, text="Tempo de Foco (min):", bg=self.cor_foco, fg="white").grid(row=0, column=0, padx=5, pady=5)
        self.input_foco = tk.Entry(frame_config, width=5, justify="center")
        self.input_foco.insert(0, "25")
        self.input_foco.grid(row=0, column=1)

        tk.Label(frame_config, text="Tempo de Pausa (min):", bg=self.cor_foco, fg="white").grid(row=1, column=0, padx=5, pady=5)
        self.input_pausa = tk.Entry(frame_config, width=5, justify="center")
        self.input_pausa.insert(0, "5")
        self.input_pausa.grid(row=1, column=1)

        # ======= LABEL DO TEMPO =======
        self.label_tempo = tk.Label(
            root,
            text="25:00",
            font=("Arial", 50, "bold"),
            bg=self.cor_foco,
            fg="white"
        )
        self.label_tempo.pack(pady=20)

        # ======= BOTÕES =======
        frame_botoes = tk.Frame(root, bg=self.cor_foco)
        frame_botoes.pack(pady=10)

        self.botao_iniciar = tk.Button(frame_botoes, text="▶️ Iniciar", command=self.iniciar, width=10, bg="#00FA9A", fg="black", font=("Arial", 10, "bold"))
        self.botao_iniciar.grid(row=0, column=0, padx=5)

        self.botao_resetar = tk.Button(frame_botoes, text="🔁 Resetar", command=self.resetar, width=10, bg="#FFD700", fg="black", font=("Arial", 10, "bold"))
        self.botao_resetar.grid(row=0, column=1, padx=5)

        # ======= STATUS E CICLO =======
        self.label_status = tk.Label(root, text="Modo: Foco", font=("Arial", 12, "bold"), bg=self.cor_foco, fg="white")
        self.label_status.pack(pady=5)

        self.label_ciclo = tk.Label(root, text="Ciclo 1 de 4", font=("Arial", 12, "bold"), bg=self.cor_foco, fg="white")
        self.label_ciclo.pack(pady=5)

    def atualizar_cor(self):
        """Atualiza a cor da interface conforme o modo (foco/pausa)"""
        nova_cor = self.cor_pausa if self.em_pausa else self.cor_foco
        self.root.configure(bg=nova_cor)
        self.label_titulo.configure(bg=nova_cor)
        self.label_tempo.configure(bg=nova_cor)
        self.label_status.configure(bg=nova_cor)
        self.label_ciclo.configure(bg=nova_cor)
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.configure(bg=nova_cor)
                for child in widget.winfo_children():
                    if isinstance(child, tk.Label):
                        child.configure(bg=nova_cor, fg="white")

    def iniciar(self):
        if not self.rodando:
            try:
                foco_min = int(self.input_foco.get())
                pausa_min = int(self.input_pausa.get())
                self.tempo_foco = foco_min * 60
                self.tempo_pausa = pausa_min * 60
            except ValueError:
                messagebox.showerror("Erro", "Digite valores numéricos válidos!")
                return

            self.rodando = True
            threading.Thread(target=self.contagem_regressiva).start()

    def resetar(self):
        self.rodando = False
        self.em_pausa = False
        self.ciclo = 1
        self.atualizar_cor()
        self.label_tempo.config(text=f"{int(self.input_foco.get()):02d}:00")
        self.label_status.config(text="Modo: Foco")
        self.label_ciclo.config(text=f"Ciclo {self.ciclo} de {self.total_ciclos}")

    def contagem_regressiva(self):
        tempo = self.tempo_pausa if self.em_pausa else self.tempo_foco

        while tempo > 0 and self.rodando:
            minutos, segundos = divmod(tempo, 60)
            self.label_tempo.config(text=f"{minutos:02d}:{segundos:02d}")
            time.sleep(1)
            tempo -= 1

        if self.rodando:
            if self.em_pausa:
                self.ciclo += 1
                if self.ciclo > self.total_ciclos:
                    messagebox.showinfo("Pomodoro", "🎉 Todos os ciclos concluídos! Ótimo trabalho!")
                    self.resetar()
                    return

            self.em_pausa = not self.em_pausa
            modo = "Pausa" if self.em_pausa else "Foco"
            self.label_status.config(text=f"Modo: {modo}")
            self.label_ciclo.config(text=f"Ciclo {self.ciclo} de {self.total_ciclos}")
            self.atualizar_cor()
            messagebox.showinfo("Pomodoro", f"⏰ Tempo de {modo.lower()} iniciado!")
            self.contagem_regressiva()  # inicia o próximo ciclo automaticamente


if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroApp(root)
    root.mainloop()
