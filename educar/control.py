from datetime import datetime
from model import *  # Banco de Dados

def dias_semana():
    return "DOMINGO SEGUNDA-FEIRA TERÇA-FEIRA QUARTA-FEIRA QUINTA-FEIRA SEXTA-FEIRA SÁBADO".split()

def turnos():
    return "MANHÃ TARDE".split()

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
        dia_semana =campos["dia_semana"].get().upper()
        print(nome, curso, id_curso, turno, dia_semana)
        
        if turma_existe(id_curso, turno, dia_semana):
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


def gerar_grade(campos):

    data = campos["data"].get()
    curso = campos["curso"].get().upper()
    turno = campos["turno"].get().upper()

    # Validação da inserção dos campos obrigatórios
    if not curso or not curso or not turno:
        return {"sucesso": False, "mensagem": "Curso, data e turno são obrigatórios."}

    # Normaliza os dados
    # Converter data para o formato ISO
    data_iso = br_to_iso(data)
    id_curso = buscar_id_curso(curso)

    # Recupera o assunto da aula
    #assunto = buscar_assunto_aula(buscar_id_aula(turno, data))
 
 
 
    alunos_da_grade = buscar_grade_db(data_iso, id_curso, turno)



    #dados_aula = [data, curso, assunto, turno]  # Recupera os dados da aula

    print(alunos_da_grade)

    # Se a grade estiver vazia, retorna uma mensagem de erro
    if not alunos_da_grade:
        return {"sucesso": False, "mensagem": "Nenhum aluno encontrado para a grade."}

    #return dados_aula, alunos_da_grade


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


# Organziar

def buscar_alunos_sem_certificado(curso, turno=None):
    conn = conectar_db()
    cursor = conn.cursor()

    # Consulta SQL para buscar alunos sem certificado
    if turno:
        cursor.execute('''SELECT a.nome, a.telefone, a.data_cadastro 
                          FROM Alunos a 
                          JOIN Cursos c ON a.id_curso = c.id 
                          WHERE c.nome = ? AND a.certificado IS NULL AND a.turno = ?''', (curso, turno))
    else:
        cursor.execute('''SELECT a.nome, a.telefone, a.data_cadastro 
                          FROM Alunos a 
                          JOIN Cursos c ON a.id_curso = c.id 
                          WHERE c.nome = ? AND a.certificado IS NULL''', (curso,))

    alunos = cursor.fetchall()
    conn.close()

    return [{"nome": aluno[0], "telefone": aluno[1], "data_cadastro": iso_to_br(aluno[2])} for aluno in alunos]


def alunos_sem_certificado(curso, turno):
    # Verifica se o curso existe
    if not curso_existe(curso):
        return {"sucesso": False, "mensagem": "Curso não encontrado."}

    # Normaliza o nome do curso
    curso = curso.upper()
    turno = turno.upper()

    # Busca os alunos sem certificado
    alunos = buscar_alunos_sem_certificado(curso, turno)

    if not alunos:
        return {"sucesso": False, "mensagem": "Nenhum aluno encontrado sem certificado."}

    return {"sucesso": True, "alunos": alunos}


# Exemplo de dicionário com dados de alunos
alunos_dict = {
    1: {"nome": "MARCIA", "telefone": "456754549123", "data_cadastro": "24-05-2025", "curso": "CURSO DE MATEMÁTICA", "turno": "MANHÃ"},
    2: {"nome": "JOÃO", "telefone": "987654321", "data_cadastro": "25-05-2025", "curso": "CURSO DE MATEMÁTICA", "turno": "TARDE"},
    3: {"nome": "ANA", "telefone": "123456789", "data_cadastro": "26-05-2025", "curso": "CURSO DE MATEMÁTICA", "turno": "MANHÃ"}
}



