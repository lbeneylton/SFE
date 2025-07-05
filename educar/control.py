from datetime import datetime
from model import *  # Banco de Dados

# ------------------- Utilitários de Data -------------------
def br_to_iso(data_str):
    return data_str
    # try:
    #     return datetime.strptime(data_str, '%d-%m-%Y').date()
    # except ValueError:
    #     return {"sucesso": False, "mensagem": "Formato de data inválido. Use DD-MM-YYYY."}


def iso_to_br(data_str):
    try:
        data = datetime.strptime(data_str, '%Y-%m-%d').date()
        return data.strftime('%d-%m-%Y')
    except ValueError:
        return {"sucesso": False, "mensagem": "Formato de data inválido. Use YYYY-MM-DD."}

# ------------------- Operação de cadastro de Curso -------------------
def cadastrar_curso(campos):
    # Verifica se o nome do curso é válido (Diferente de vazio)
    print("\nCadastrando curso")
    try:
        nome = campos["nome"].get()

        if not nome:
            return {"sucesso": False, "mensagem": "Nome do curso é obrigatório."}

        # Normaliza os dados
        nome = nome.upper()

        # Verifica se o curso já existe
        if curso_existe(nome):
            return {"sucesso": False, "mensagem": f"Curso {nome} já cadastrado."}

        # Adiciona o curso no banco de dados
        inserir_curso_no_db(nome)
        return {"sucesso": True, "mensagem": f"Curso {nome} cadastrado com sucesso."}

    except Exception as e:
        return {"sucesso": False, "mensagem": f"Ocorreu um erro ao cadastrar o curso: {str(e)}"}

# ------------------- Operação de cadastro de Professor -------------------
def cadastrar_professor(campos):
    print("Cadastrando Professor")
    try:
        nome = campos["nome"].get()

        if not nome:
            return {"sucesso": False, "mensagem": "Nome do professor é obrigatório."}

        # Normaliza os dados
        nome = nome.upper()

        # Verifica se o curso já existe
        if professor_existe(nome):
            return {"sucesso": False, "mensagem": f"Professor {nome} já cadastrado."}

        # Adiciona o curso no banco de dados
        inserir_professor_no_db(nome)
        return {"sucesso": True, "mensagem": f"Professor {nome} cadastrado com sucesso."}
        
    except Exception as e:
        return {"Sucesso": False, "mensagem": f"Ocorreu um erro ao cadastrar o professor {str(e)}"}

# ------------------- Operação de cadastro de Turma -------------------
def cadastrar_turma(campos):
    try:
        nome = campos["nome"].get().upper()
        curso = campos["curso"].get()
        id_curso = buscar_id_curso(curso.upper())
        turno = campos["turno"].get().upper()
        dia_semana = campos["dia_semana"].get().upper()
        
        if turma_existee(id_curso, turno, dia_semana) or turma_existe(nome):
            return {"sucesso": False, "mensagem": f"Turma de {curso} no turno {turno} de {dia_semana} já existe."}
        
        
        #Adiciona a turma no banco de dados
        inserir_turma_no_db(id_curso, nome, turno, dia_semana)
        return {"sucesso": True, "mensagem": f"Turma {nome} cadastrada com sucesso."}

        
    except Exception as e:
        return {"sucesso": False, "mensagem": f"Ocorreu um erro ao cadastrar a turma: {str(e)}"}

# ------------------- Operações de cadastro de Aluno -------------------
def cadastrar_aluno(campos):
    print("Cadastrando aluno")
    try:
        # Extrai os valores dos widgets da interface
        nome = campos["nome"].get().upper()
        telefone = campos["telefone"].get()
        telefone = telefone.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
        data_cadastro = campos["data_cadastro"].get()
        data_cadastro = br_to_iso(data_cadastro)
        
        #Buscar id da turma
        turma = campos["turma"].get().upper()
        id_turma = buscar_id_turma(turma)
        
        # Verifica se o nome do aluno, o telefone são válidos (Diferente de vazio)
        if not nome or not telefone:
            return {"sucesso": False, "mensagem": "Nome e telefone são obrigatórios."}

        # Verifica duplicidade
        if aluno_existe(nome):
            return {"sucesso": False, "mensagem": f"Aluno {nome} já cadastrado."}
        

        # Insere no banco de dados
        inserir_aluno_no_db(nome, telefone, data_cadastro, id_turma)
        return {"sucesso": True, "mensagem": f"Aluno {nome} cadastrado com sucesso!"}

    except Exception as e:
        return {"sucesso": False, "mensagem": f"Ocorreu um erro ao cadastrar o aluno: {str(e)}"}

# ------------------- Operações de cadastro de Aula ------------------- 
def cadastrar_aula(campos):
    print("\nCadastrando Aula")
    try:
        # Extração dos dados
        assunto = campos["assunto"].get().upper()
        data = campos["data"].get()
        data = br_to_iso(data)

        turma = campos["turma"].get().upper()
        professor = campos["professor"].get().upper()
        
        id_turma = buscar_id_turma(turma)
        id_professor = buscar_id_professor(professor)

        # Verifica se os campos obrigatórios estão preenchidos
        if not assunto:
            return {"sucesso": False, "mensagem": "Assunto é obrigatório."}

        # Verifica se a aula já foi cadastrada
        if aula_existe(data, id_turma, assunto):
            return {"sucesso": False, "mensagem": "Aula já cadastrada."}

 
        inserir_aula_no_db(assunto, data, id_professor, id_turma)
        return {"sucesso": True, "mensagem": f"Aula {assunto} cadastrada para a turma {turma} de Curso."}

    except Exception as e:
        return {"sucesso": False, "mensagem": f"Ocorreu um erro ao cadastrar a aula {str(e)}"}


# ------------------- Operações de Presença -------------------
def retornar_dados_grade(campos):

    data = campos["data"].get()
    turma = campos["turma"].get().upper()
    turno = campos["turno"].get().upper()
    
    # Normaliza os dados
    # Converter data para o formato ISO 
    data_iso = br_to_iso(data)
    id_turma = buscar_id_turma(turma)  
    

    # Recupera o assunto da aula
    assunto = buscar_assunto_aula_por_data_e_turma(data_iso, id_turma)
    id_aula = buscar_id_aula(assunto)
 
 
    alunos_da_grade = retornar_dados_grade_db(id_aula)
    dados_aula = [data, id_turma, assunto, turno]  # Recupera os dados da aula


    # Se a grade estiver vazia, retorna uma mensagem de erro
    if not alunos_da_grade:
         return {"sucesso": False, "mensagem": "Nenhum aluno encontrado para a grade."}
     
    print(alunos_da_grade)
    return dados_aula, alunos_da_grade
    


# Função para registrar presença de aluno em uma aula
def presenca_aluno(curso, id_aula, presente):
    id_curso = buscar_id_curso(curso.upper())

    pass
    # Verifica se o aluno já está registrado nessa aula
    # if registro_existe(id_aluno, id_aula):
    #     conn.close()
    #     return {"sucesso": False, "mensagem": "Aluno já registrado nesta aula."}

    # inserir_presenca_no_db(id_aluno, id_aula, presente)
    # return {"sucesso": True, "mensagem": "Presença registrada com sucesso."}


