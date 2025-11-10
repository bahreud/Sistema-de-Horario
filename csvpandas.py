import pandas as pd  # Importa biblioteca para manipulação de dados tabulares

horariosTURMAS = pd.read_csv('horariosTURMAS.csv', sep=',', encoding='utf-8-sig')  # Carrega dados do arquivo CSV

horariosTURMAS.columns = [  # Renomeia as colunas do DataFrame para português
    "Código do Curso", "Curso", "Código de Turma", "Turma",  # Colunas de identificação
    "Código da Disciplina", "Disciplina", "Código do Professor", "Professor", "Total de Aulas Semanais"  # Colunas de conteúdo
]

horariosTURMAS["Série"] = horariosTURMAS["Turma"].str.extract(r'(\d+° ano)')  # Extrai a série (ex: "1° ano") do nome da turma
horariosTURMAS["Turma_Letra"] = horariosTURMAS["Turma"].str.extract(r'- ([a-zA-Z])$')  # Extrai a letra da turma (ex: "A")
