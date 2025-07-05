import sqlite3


def conectar_db():
    # Conexão com o banco de dados SQLite
    return sqlite3.connect('frequencia.db')
    # return sqlite3.connect(r'C:\EDUCAR\FREQUENCIAS\frequencia.db')


# Cria as tabelas no banco de dados

def criar_tabela_alunos():
    conn = conectar_db()
    cursor = conn.cursor()
    # Criação da tabela Alunos
    print('\nCriando tabela Alunos...')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Alunos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT,
        telefone TEXT,
        data_cadastro DATE,
        id_turma INTEGER,
        certificado BOOLEAN DEFAULT 0,
        FOREIGN KEY(id_turma) REFERENCES Turmas(id)
    )''')

    print('Tabela Alunos criada com sucesso!')

    conn.commit()
    conn.close()

def criar_tabela_cursos():
    conn = conectar_db()
    cursor = conn.cursor()
    # Criação da tabela Cursos
    print('\nCriando tabela Cursos...')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Cursos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    )''')

    print('Tabela Cursos criada com sucesso!')

    conn.commit()
    conn.close()

def criar_tabela_turmas():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS Turmas(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        id_curso INTEGER,
        turno TEXT,
        dia_semana TEXT,
        FOREIGN KEY(id_curso) REFERENCES Cursos(id)      
        )''')

def criar_tabela_aulas():
    conn = conectar_db()
    cursor = conn.cursor()
    # Criação da tabela Aulas
    print('\nCriando tabela Aulas...')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Aulas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        assunto TEXT NOT NULL UNIQUE,
        data DATE,
        id_professor INTEGER,
        id_turma INTEGER NOT NULL,
        FOREIGN KEY(id_turma) REFERENCES Turmas(id),
        FOREIGN KEY (id_professor) REFERENCES Professores(id)
    )''')

    print('Tabela Aulas criada com sucesso!')

    conn.commit()
    conn.close()

def criar_tabela_professores():
    conn = conectar_db()
    cursor = conn.cursor()
    # Criação da tabela Professores
    print('\nCriando tabela Professores...')
    cursor.execute('''CREATE TABLE IF NOT EXISTS Professores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL UNIQUE
    )
    ''')

    print('Tabela Professores criada com sucesso!')

    conn.commit()
    conn.close()

def criar_tabela_presencas():
    conn = conectar_db()
    cursor = conn.cursor()
    # Criação da tabela Presenças
    print('\nCriando tabela Presenças...')

    cursor.execute('''CREATE TABLE IF NOT EXISTS Presencas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        id_aluno INTEGER,
        id_aula INTEGER,
        presente INTEGER,
        UNIQUE(id_aluno, id_aula),
        FOREIGN KEY(id_aluno) REFERENCES Alunos(id),
        FOREIGN KEY(id_aula) REFERENCES Aulas(id)
    )
    ''')

    print('Tabela Presenças criada com sucesso!')

    conn.commit()
    conn.close()

# Função para criar todas as tabelas

def criar_tabelas():

    print('\nCRIANDO TABELAS...\n')
    criar_tabela_alunos()
    criar_tabela_cursos()
    criar_tabela_turmas()
    criar_tabela_aulas()
    criar_tabela_professores()
    criar_tabela_presencas()
    
    print('\nTABELAS CRIADAS COM SUCESSO!\n')


# Funções para verificar se valores existem no banco de dados
def aluno_existe(nome):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT 1 FROM Alunos WHERE nome = ?''', (nome,))
    existe = cursor.fetchone() is not None
    conn.close()
    return existe

def curso_existe(nome):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT 1 FROM Cursos WHERE nome = ?''', (nome,))
    existe = cursor.fetchone() is not None
    conn.close()
    return existe

#-->Verificar se da pra torcar todos argumento só pelo nome da turma
def turma_existe(id_curso, turno, dia_semana):
    conn = conectar_db()
    cursor =conn.cursor()
    cursor.execute(
        '''SELECT 1 FROM Turmas WHERE id_curso = ? AND turno = ? AND dia_semana = ?''',(id_curso, turno, dia_semana,))
    existe = cursor.fetchone() is not None
    conn.close()
    return existe
        
def aula_existe(data, turma, assunto=None):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT 1 FROM Aulas WHERE data = ?  AND turma = ? AND assunto = ?''', (data, turma, assunto))
    existe = cursor.fetchone() is not None
    conn.close()
    return existe

def registro_existe(id_aluno, id_aula):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute(
        '''SELECT 1 FROM Presencas WHERE id_aluno = ? AND id_aula = ?''', (id_aluno, id_aula))
    existe = cursor.fetchone() is not None
    conn.close()
    return existe


# Funções de inserção no banco de dados
def inserir_aluno_no_db(nome, telefone, data_cadastro, id_turma):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO Alunos (nome, telefone, data_cadastro, id_turma, certificado) VALUES (?, ?, ?, ?, ?)''',
                   (nome, telefone, data_cadastro, id_turma, False))
    conn.commit()
    conn.close()

def inserir_curso_no_db(nome_curso):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO Cursos (nome) VALUES (?)''', (nome_curso,))
    conn.commit()
    conn.close()

def inserir_turma_no_db(id_curso, nome, turno, dia_semana):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO Turmas (id_curso, nome, turno, dia_semana) VALUES (?, ?, ?, ?)''', (id_curso, nome, turno, dia_semana,))
    conn.commit()
    conn.close()

def inserir_aula_no_db(assunto, data, id_turma, professor):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO Aulas (assunto, data, professor, id_turma) VALUES (?, ?, ?, ?)''',
                   (assunto, data, professor, id_turma,))
    conn.commit()
    conn.close()

def inserir_presenca_no_db(id_aluno, id_aula, presente):
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Presencas (id_aluno, id_aula, presente)
        VALUES (?, ?, ?)
    ''', (id_aluno, id_aula, presente))

    conn.commit()
    conn.close()


# Funções de busca de id no banco de dados
def buscar_id_aluno(nome_aluno):
    nome_aluno = nome_aluno.upper()
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('''SELECT id FROM Alunos WHERE nome = ?''', (nome_aluno,))
    resultado = cursor.fetchone()
    conn.close()

    return resultado[0] if resultado else None

def buscar_id_curso(nome_curso):
    nome_curso = nome_curso.upper()
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('''SELECT id FROM Cursos WHERE nome = ?''', (nome_curso,))
    resultado = cursor.fetchone()
    conn.close()

    return resultado[0] if resultado else None

def buscar_id_turma(id_curso, turno):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('''SELECT id FROM Turmas WHERE id_curso = ? AND turno = ?''', (id_curso, turno,))
    resultado = cursor.fetchone()
    conn.close()

    return resultado[0] if resultado else None

def buscar_id_turma_pelo_nome(nome):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('''SELECT id FROM Turmas WHERE nome = ? ''', (nome,))
    resultado = cursor.fetchone()
    conn.close()

    return resultado[0] if resultado else None


def buscar_id_aula(turno, data):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute(
        '''SELECT id FROM Aulas WHERE turno = ? AND data = ?''', (turno, data,))
    resultado = cursor.fetchone()
    conn.close()

    return resultado[0] if resultado else None


# Funções de busca de nome no banco de dados
def buscar_nome_curso(id_curso):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute('''SELECT nome FROM Cursos WHERE id = ?''', (id_curso,))
    resultado = cursor.fetchone()
    conn.close()

    return resultado[0] if resultado else None

def buscar_assunto_aula(id_aula):
    conn = conectar_db()
    cursor = conn.cursor()

    cursor.execute(
        '''SELECT assunto FROM Aulas WHERE id = ?''', (id_aula))
    resultado = cursor.fetchone()
    conn.close()

    return resultado[0] if resultado else None

def buscar_cursos_db():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT nome FROM Cursos''')
    cursos = cursor.fetchall()
    conn.close()
    return [curso[0] for curso in cursos]

def buscar_turmas_db():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT nome FROM Turmas''')
    professores = cursor.fetchall()
    conn.close()
    return [professor[0] for professor in professores]

def buscar_professores_db():
    conn = conectar_db()
    cursor = conn.cursor()
    cursor.execute('''SELECT nome FROM Professores''')
    professores = cursor.fetchall()
    conn.close()
    return [professor[0] for professor in professores]


def buscar_grade_db(data, id_curso, turno):
    id_turma = buscar_id_turma(id_curso,turno)
    
    with conectar_db() as conn:
        cursor = conn.cursor()

        cursor.execute('''
            SELECT
                Alunos.id,
                Alunos.nome,
                Alunos.telefone,
                Presencas.presente 
            FROM Turmas
            JOIN Alunos ON Alunos.id_turma = Aulas.id_turma
            LEFT JOIN Presencas ON Presencas.id_aula = Aulas.id AND Presencas.id_aluno = Alunos.id 
            WHERE Aulas.data = ? AND Aulas.id_turma = ?
            GROUP BY Alunos.id
                       ''', (data, id_turma))

        alunos_com_presenca = cursor.fetchall()

    return alunos_com_presenca




def buscar_nome_turma():
    pass






        
        
        
        
        
        

