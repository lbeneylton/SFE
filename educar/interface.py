from control import *
from tkcalendar import DateEntry
from datetime import date
import tkinter as tk
from tkinter import ttk, messagebox



def mascarar_telefone(event):
    widget = event.widget
    texto = widget.get()
    texto = ''.join(filter(str.isdigit, texto))
    texto = texto[:11]

    novo = ""
    if len(texto) >= 1:
        novo += f"({texto[:2]}"
    if len(texto) >= 3:
        novo += f") {texto[2:7]}"
    if len(texto) >= 8:
        novo += f"-{texto[7:]}"

    widget.delete(0, tk.END)
    widget.insert(0, novo)

def upper_case_entry(event):
    widget = event.widget
    texto = widget.get()
    widget.delete(0, tk.END)
    widget.insert(0, texto.upper())





class Interface():
    #Janela principal da interface
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Frequência EDUCAR - v1.2")
        self.root.geometry('700x500')
        self.root.resizable(False, False)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True)

        self.criar_abas()

    #incluir as abas na interface
    def criar_abas(self):
        self.criar_aba_aluno()


    def criar_aba_aluno(self):
        self.frame_aluno = ttk.Frame(self.notebook)
        self.notebook.add(self.frame_aluno, text="Cadastrar Aluno")

        ttk.Label(self.frame_aluno, text="Nome:").grid( row=0, column=0, sticky='e', pady=5)
        self.nome_entry = ttk.Entry(self.frame_aluno, width=80)
        self.nome_entry.grid(row=0, column=1, pady=5)

        ttk.Label(self.frame_aluno, text="Telefone:").grid(
            row=1, column=0, sticky='e', pady=5)
        self.telefone_entry = ttk.Entry(self.frame_aluno, width=25)
        self.telefone_entry.grid(row=1, column=1, sticky='w', pady=5)
        self.telefone_entry.bind("<FocusOut>", mascarar_telefone)

        ttk.Label(self.frame_aluno, text="Data de Matrícula:").grid(
            row=2, column=0, sticky='e')
        self.data_matricula = DateEntry(
            self.frame_aluno, date_pattern='dd/mm/yyyy', firstweekday='sunday')
        self.data_matricula.grid(row=2, column=1, sticky='w', pady=5)
        self.data_matricula.set_date(date.today())

        ttk.Label(self.frame_aluno, text="Turno:").grid(
            row=3, column=0, sticky='e', pady=5)
        self.turno_entry = ttk.Combobox(
            self.frame_aluno, values=["Manhã", "Tarde"], state="readonly")
        self.turno_entry.grid(row=3, column=1, sticky='w', pady=5)
        self.turno_entry.current(0)

        ttk.Button(self.frame_aluno, text="Cadastrar Aluno",
                command=lambda: cadastrar_aluno(
                    self.nome_entry.get(), self.telefone_entry.get(), self.data_matricula.get(), self.turno_entry.get())
                ).grid(row=4, columnspan=2)




        # Implementar campos e botões para registrar presença





    def cadastrar_curso(self):
        nome_curso = self.nome_curso_entry.get().strip()
        if not nome_curso:
            messagebox.showerror("Erro", "O nome do curso não pode ser vazio.")
            return
        resultado = cadastrar_curso(nome_curso)
        messagebox.showinfo("Resultado", resultado["mensagem"])




app = Interface()
app.root.mainloop()



   