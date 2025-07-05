import tkinter as tk
from tkinter import ttk
from datetime import date
from tkcalendar import DateEntry
from tkinter import messagebox
from control import*


try:
    # Funções de cadastro e busca para interface
    def caixa_de_mensagem(mensagem):
        if mensagem["sucesso"]:
            messagebox.showinfo("Sucesso", mensagem["mensagem"])
        else:
            messagebox.showerror("Erro", mensagem["mensagem"])
           
           
           
           
        
          
    def buscar_professores_db():
        return["scsadfassd"]


    def grade():
        print("Gerar grade de presença...")



    #mascaras
    def mascarar_telefone(event):
        widget = event.widget
        texto = ''.join(filter(str.isdigit, widget.get()))
        texto = texto[:11]  # Limita a 11 dígitos

        if len(texto) >= 1:
            novo = f"({texto[:2]}"
            if len(texto) >= 3:
                novo += f") {texto[2:7]}"
            if len(texto) >= 8:
                novo += f"-{texto[7:]}"
        else:
            novo = texto

        widget.delete(0, tk.END)
        widget.insert(0, novo)

    def upper_case_entry(event):
        widget = event.widget
        texto = widget.get()
        widget.delete(0, tk.END)
        widget.insert(0, texto.upper())

    # Funções para criar componentes da interface de forma mais pratica
    def criar_frame(master, titulo):
        frame = ttk.LabelFrame(master, text=titulo)
        frame.pack(fill="both", expand=True, padx=10, pady=10)
        return frame

    def criar_label(frame, texto, linha, coluna, largura=20):
        
        label = ttk.Label(frame, text=texto, width=largura)
        label.grid(row=linha, column=coluna, sticky='w', padx=5, pady=5)
        label.config(font=("Helvetica", 10, "bold"))
        return label

    def criar_entry(frame, linha, coluna, focus=False, bind_event=None, bind_func=None, largura=70):
        entry = ttk.Entry(frame, width=largura)
        entry.grid(row=linha, column=coluna, sticky='w', padx=5, pady=5)
        
        if focus:
            entry.focus_set()
        
        if bind_event and bind_func:
            entry.bind(bind_event, bind_func)
            
        entry.configure(font=("Helvetica", 10))
        
        return entry

    def criar_combobox(frame, valores, linha, coluna, largura=30):
        combobox = ttk.Combobox(frame, values=valores, state="readonly", width=largura)
        combobox.grid(row=linha, column=coluna, sticky='w', padx=5, pady=5)
        if valores:
            combobox.current(0)  # Seleciona o primeiro item por padrão
        return combobox

    def criar_date_entry(frame, linha, coluna, largura=20):
        date_entry = DateEntry(frame, date_pattern='dd/mm/yyyy', firstweekday='sunday', width=largura)
        date_entry.grid(row=linha, column=coluna, sticky='w', padx=5, pady=5)
        date_entry.set_date(date.today())  # Define a data atual como padrão
        return date_entry

    def criar_botao_submit(frame, texto, linha, coluna, comando, largura=20):
        botao = ttk.Button(frame, text=texto, command=comando, width=largura)
        botao.grid(row=linha, column=coluna, pady=10)
        return botao

    def criar_botao_tela(frame, texto, comando, largura=20, altura=2):
        botao = tk.Button(frame, text=texto, command=comando, width=largura, height=altura)
        botao.pack(pady=10)
        return botao



    class App(tk.Tk):
        def __init__(self):
            super().__init__()

            self.title("Sistema de Controle de Presenças EDUCAR v 2.0")
            self.resizable(False, False)
            self.geometry("700x500")

            self.frames = {} 
            self.botoes_menu = {}
            self.tela_atual = None

            self._configurar_menu()
            self._configurar_container()
            self._registrar_telas()
            self.mostrar_tela(TelaCadastro)

        #Cria o frame do menu
        def _configurar_menu(self):    
            self.menu_frame = tk.Frame(self)
            self.menu_frame.pack(side="top", fill="both", padx=10, pady=10)

        #Cria o frame que conterá as telas
        def _configurar_container(self):     
            self.container = criar_frame(self, "Opções")
            self.container.pack(side="top", fill="both", expand=True, padx=10, pady=2)

        #Registra as telas e cria os botões do menu
        def _registrar_telas(self):
            self.telas = {
                "Cadastro": TelaCadastro,
                "Presenças": Telapresencas,
                "Relatórios": TelaRelatorios
            }

            for nome, TelaClasse in self.telas.items():
                # Criar botão no menu
                botao = tk.Button(
                    self.menu_frame, 
                    text=nome,
                    command=lambda t=TelaClasse: self.mostrar_tela(t),
                    height=3
                )
                botao.pack(side="left", expand=True, fill="x")
                self.botoes_menu[TelaClasse] = botao

                # Criar e armazenar o frame da tela
                frame = TelaClasse(self.container)
                self.frames[TelaClasse] = frame
                frame.grid(row=0, column=0, sticky="nsew")

        #Mostra a tela selecionada e atualiza o estado dos botões
        def mostrar_tela(self, tela):
            if self.tela_atual == tela:
                return

            self.frames[tela].tkraise()
            self.tela_atual = tela

            for TelaClasse, botao in self.botoes_menu.items():
                cor = "#ffffff" if TelaClasse == tela else "SystemButtonFace"
                botao.configure(bg=cor)



    class TelaCadastro(tk.Frame):
        def __init__(self, master):
            super().__init__(master)
            self.janela_aluno = None
            self.janela_aula = None
            self.janela_curso = None
            self.janela_turma = None

#BOTOES QUE INICIAM AS JANELAS TOPLEVEL
            criar_botao_tela(self, "Cadastrar Aluno", self.abrir_janela_aluno)
            criar_botao_tela(self, "Cadastrar Curso", self.abrir_janela_curso)
            criar_botao_tela(self, "Cadastrar Turma", self.abrir_janela_turma)
            criar_botao_tela(self, "Cadastrar Aula", self.abrir_janela_aula)


#FUNÇÕES APORA ABRIR JANELAS
        def abrir_janela_aluno(self):
            self.fechar_janela_aula()
            self.fechar_janela_curso()
            self.fechar_janela_turma()
            if self.janela_aluno is None or not self.janela_aluno.winfo_exists():
                self.janela_aluno = tk.Toplevel(self)
                self.janela_aluno.title("Cadastro de Aluno")
                self.janela_aluno.geometry("700x400")
                self.janela_aluno.resizable(False, False)
                self.janela_aluno.protocol("WM_DELETE_WINDOW", self.fechar_janela_aluno)
                self.criar_formulario_aluno(self.janela_aluno)
            else:
                self.janela_aluno.lift()

        def abrir_janela_curso(self):
            self.fechar_janela_aluno()
            self.fechar_janela_aula()
            self.fechar_janela_turma()
            if self.janela_curso is None or not self.janela_curso.winfo_exists():
                self.janela_curso = tk.Toplevel(self)
                self.janela_curso.title("Cadastro de Curso")
                self.janela_curso.geometry("700x200")
                self.janela_curso.resizable(False, False) 
                self.janela_curso.protocol("WM_DELETE_WINDOW", self.fechar_janela_curso)
                self.criar_formulario_curso(self.janela_curso)
            else:
                self.janela_curso.lift() 

        def abrir_janela_turma(self):
            self.fechar_janela_aula()
            self.fechar_janela_curso()
            self.fechar_janela_aluno()
            if self.janela_turma is None or not self.janela_turma.winfo_exists():
                self.janela_turma = tk.Toplevel(self)
                self.janela_turma.title("Cadastro de Turma")
                self.janela_turma.geometry("700x200")
                self.janela_turma.resizable(False, False) 
                self.janela_turma.protocol("WM_DELETE_WINDOW", self.fechar_janela_turma)
                self.criar_formulario_turma(self.janela_turma)
            else:
                self.janela_turma.lift() 

        def abrir_janela_aula(self):
            self.fechar_janela_aluno()
            self.fechar_janela_curso()
            self.fechar_janela_turma()
            if self.janela_aula is None or not self.janela_aula.winfo_exists():
                self.janela_aula = tk.Toplevel(self)
                self.janela_aula.title("Cadastro de Aula")
                self.janela_aula.geometry("700x400")
                self.janela_aula.resizable(False, False)
                self.janela_aula.protocol("WM_DELETE_WINDOW", self.fechar_janela_aula)
                self.criar_formulario_aula(self.janela_aula)
            else:
                self.janela_aula.lift()


#FUNÇÕES PARA FECHAR JANELAS
        def fechar_janela_aluno(self):
            if self.janela_aluno:
                self.janela_aluno.destroy()
                self.janela_aluno = None

        def fechar_janela_curso(self):
            if self.janela_curso:
                self.janela_curso.destroy()
                self.janela_curso = None

        def fechar_janela_turma(self):
            if self.janela_turma:
                self.janela_turma.destroy()
                self.janela_turma = None

        def fechar_janela_aula(self):
            if self.janela_aula:
                self.janela_aula.destroy()
                self.janela_aula = None


#FORMULARIOS DAS JANELAS (Fazem a conexão com control.py)
        def criar_formulario_aluno(self, janela):
            frame = criar_frame(janela, "Dados do Aluno")
            # Criação dos campos do formulário
    
            criar_label(frame, "Nome:", 0, 0)  
            nome_entry = criar_entry(frame, 0, 1, True)# True para definir o foco no campo de entrada
            
            criar_label(frame, "Telefone:", 1, 0) 
            telefone_entry = criar_entry(frame, 1, 1, bind_event="<FocusOut>", bind_func=mascarar_telefone)
            
            criar_label(frame, "Data de Cadastro:", 2, 0)
            data_cadastro_entry = criar_date_entry(frame, 2, 1)
            
            criar_label(frame, "Curso:", 3, 0)
            curso_entry = criar_combobox(frame, buscar_cursos_db(), 3, 1)
                    
            criar_label(frame, "Turno:", 4, 0)
            turno_entry = criar_combobox(frame, turnos(), 4, 1)

            self.campos_aluno = {
                "nome": nome_entry,
                "telefone": telefone_entry,
                "data_cadastro": data_cadastro_entry,
                "curso": curso_entry,
                "turno": turno_entry
            }
                
            criar_botao_submit(frame, "Cadastrar Aluno", 5, 0, lambda: caixa_de_mensagem(cadastrar_aluno(self.campos_aluno)))     

        def criar_formulario_curso(self, janela):
            frame = criar_frame(janela, "Dados do Curso")
            
            criar_label(frame, "Nome:", 0, 0)
            curso_entry = criar_entry(frame, 0, 1, True)
            
            self.campos_curso ={
                "curso": curso_entry
            }
            
            criar_botao_submit(frame, "Cadastrar curso", 2, 0, lambda: caixa_de_mensagem(cadastrar_curso(self.campos_curso)))

        def criar_formulario_turma(self, janela):
            frame = criar_frame(janela, "Dados da Turma")

            criar_label(frame, "Nome", 0, 0)
            nome_entry = criar_entry(frame, 0, 1, True)
            
            criar_label(frame, "Curso", 1, 0)
            curso_entry = criar_combobox(frame, buscar_cursos_db(), 1, 1)
            
            criar_label(frame, "Turno", 2, 0)
            turno_entry = criar_combobox(frame, turnos(), 2, 1)
            
            criar_label(frame, "Dia da Semana", 3, 0)
            dia_semana_entry = criar_combobox(frame, dias_semana(), 3, 1)
            
            self.campos_turma ={
                "nome":nome_entry,
                "curso":curso_entry,
                "turno":turno_entry,
                "dia_semana":dia_semana_entry
            }
            
            criar_botao_submit(frame, "Cadastrar Turma", 4, 0, lambda: caixa_de_mensagem(cadastrar_turma(self.campos_turma)))
                     
        def criar_formulario_aula(self, janela):
                frame = criar_frame(janela, "Dados da Aula")

                # Criação dos campos do formulário
                criar_label(frame, "Assunto:", 0, 0)
                assunto_entry = criar_entry(frame, 0, 1, True)
                
                criar_label(frame, "Data:", 1, 0)
                data_aula_entry = criar_date_entry(frame, 1, 1)
                           
                criar_label(frame, "Curso:", 2, 0)
                curso_entry = criar_combobox(frame, buscar_cursos_db(), 2, 1)

                criar_label(frame, "Turno:", 3, 0)
                turno_entry = criar_combobox(frame, turnos(), 3, 1, largura=10)
                
                criar_label(frame, "Professor", 4, 0)
                professor_entry = criar_combobox(frame, buscar_professores_db(), 4, 1)
                
                self.campos_aula = {
                    "data": data_aula_entry,
                    "assunto": assunto_entry,
                    "curso": curso_entry,
                    "turno": turno_entry,
                    "professor": professor_entry
                }

                criar_botao_submit(frame, "Cadastrar Aula", 5, 0, lambda: caixa_de_mensagem(cadastrar_aula(self.campos_aula)), largura=20)

                
            

    class Telapresencas(tk.Frame):
        def __init__(self, master):     
            super().__init__(master)

            self.janela_grade = None
            self.janela_consulta = None

            criar_botao_tela(self, "Gerar Grade de Presença", self.abrir_janela_grade)
            criar_botao_tela(self, "Consultar Presença", self.abrir_janela_consulta)

        # Funções para abrir as janelas de presença e consulta
        def abrir_janela_grade(self):
            self.fechar_janela_consulta()

            if self.janela_grade is None or not self.janela_grade.winfo_exists():
                self.janela_grade = tk.Toplevel(self)
                self.janela_grade.title("Gerar Grade de Presença")
                self.janela_grade.geometry("700x200")
                #self.janela_grade.resizable(False, False)
                self.janela_grade.protocol("WM_DELETE_WINDOW", self.fechar_janela_grade)
                self.criar_formulario_grade(self.janela_grade, "Gerar Grade de Presença", "Gerar Grade")
            else:
                self.janela_grade.lift()





        def abrir_janela_consulta(self):
            self.fechar_janela_grade()
            if self.janela_consulta is None or not self.janela_consulta.winfo_exists():
                self.janela_consulta = tk.Toplevel(self)
                self.janela_consulta.title("Consultar Presença")
                self.janela_consulta.geometry("700x200")
                self.janela_consulta.resizable(False, False)
                self.janela_consulta.protocol("WM_DELETE_WINDOW", self.fechar_janela_consulta)
                #self.criar_formulario(self.janela_consulta, "Consultar Presença", "Consultar Presença", gerar_grade)
            else:
                self.janela_consulta.lift()

        # Funções para fechar as janelas
        def fechar_janela_consulta(self):
            if self.janela_consulta:
                self.janela_consulta.destroy()
                self.janela_consulta = None

        def fechar_janela_grade(self):
            if self.janela_grade:
                self.janela_grade.destroy()
                self.janela_grade = None
                
                
        # Função para criar o formulário de presença
        def criar_formulario_grade(self, janela, titulo, texto_botao):
            frame = criar_frame(janela, titulo)
            self.frame_grade = criar_frame(janela,"")

            criar_label(frame, "Data:", 0, 0)
            data_entry = criar_date_entry(frame, 0, 1)

            criar_label(frame, "Curso:", 1, 0)
            curso_entry = criar_combobox(frame, buscar_cursos_db(), 1, 1, largura=30)

            criar_label(frame, "Turno:", 2, 0)
            turno_entry = criar_combobox(frame, turnos(), 2, 1, largura=10)

            self.campos_formulario = {
                "data": data_entry,
                "curso": curso_entry,
                "turno": turno_entry
            }
            
            def grade():
                resultado = gerar_grade(self.campos_formulario)
                print(resultado)
                # if isinstance(resultado, list):
                #     caixa_de_mensagem(resultado)
                # else:
                #     dados, alunos = resultado
                #     print(alunos)
                #     print(dados)
                #     self.gerar_grade_interface(dados, alunos)

                
            criar_botao_submit(frame, texto_botao, 3, 0, grade, largura=20)
          
          
          
          
        def gerar_grade_interface(self, dados, alunos):
            # Ajusta o tamanho da janela
            
            self.janela_grade.geometry("700x600")
            self.janela_grade.columnconfigure(0, weight=1)
            self.janela_grade.columnconfigure(1, weight=1)
            self.janela_grade.columnconfigure(2, weight=1)

            # Destroi qualquer conteúdo anterior
            for widget in self.frame_grade.winfo_children():
                widget.destroy()

            titulo = ttk.Frame(self.frame_grade).pack()
            # Adiciona título da seção
            ttk.Label(titulo, text= f"{dados[1]} / {dados[3]}", font=("Arial", 12, "bold"), anchor="center").grid(row=0, column=3, columnspan=3, sticky='ew')
            tk.Label(titulo, text= f"Grade do dia {dados[0]} - {dados[2]}", font=("Arial", 10), anchor="center").grid(row=1, column=3, columnspan=3, sticky='ew')
            # Cria o canvas com scrollbar
    

            lin = 2
            for aluno in alunos:
                ttk.Label(self.frame_grade, text=aluno[1], anchor="e").grid(row=lin, column=0, sticky='w', padx=5)
                ttk.Label(self.frame_grade, text= "[x]" if aluno[3] == True else "[ ]", anchor="e").grid(row=lin, column=1, sticky='w', padx=5)
                
                
                        
       
   
                # ttk.Label(self.frame_grade, text= "[x]" if aluno[3] == True else "[ ]").grid(lin,2)
                lin+=1

    


    class TelaRelatorios(tk.Frame):
        def __init__(self, master):
            super().__init__(master)
            tk.Label(self, text="Tela de Relatórios",
                    font=("Helvetica", 16)).pack(pady=20)


    print("Arquivo view.py carregado sem erros")
except Exception as e:
    print(f"Ocorreu um erro ao carregar o arquivo view.py\n Erro: {str(e)}")




        
        
        
        
