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