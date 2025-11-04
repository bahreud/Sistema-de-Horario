import pandas as pd  # Importa biblioteca para manipulação de dados tabulares

horariosTURMAS = pd.read_csv('horariosTURMAS.csv', sep=',', encoding='utf-8-sig')  # Carrega dados do arquivo CSV

horariosTURMAS.columns = [  # Renomeia as colunas do DataFrame para português
    "Código do Curso", "Curso", "Código de Turma", "Turma",  # Colunas de identificação
    "Código da Disciplina", "Disciplina", "Código do Professor", "Professor", "Total de Aulas Semanais"  # Colunas de conteúdo
]

horariosTURMAS["Série"] = horariosTURMAS["Turma"].str.extract(r'(\d+° ano)')  # Extrai a série (ex: "1° ano") do nome da turma
horariosTURMAS["Turma_Letra"] = horariosTURMAS["Turma"].str.extract(r'- ([a-zA-Z])$')  # Extrai a letra da turma (ex: "A")

correcoes_professores = {  # Dicionário com professores substitutos para códigos específicos
    'pro041': 'Professor Substituto História',  # Mapeia código pro041 para professor de História
    'pro043': 'Professor Substituto Educação Física',  # Mapeia código pro043 para professor de Educação Física
    'pro044': 'Professor Substituto Programação',  # Mapeia código pro044 para professor de Programação
    'pro045': 'Professor Substituto Projeto Integrador'  # Mapeia código pro045 para professor de Projeto Integrador
}

for idx, row in horariosTURMAS.iterrows():  # Percorre cada linha do DataFrame
    if pd.isna(row['Professor']) or row['Professor'] == '':  # Verifica se o professor está vazio ou não definido
        cod_professor = row['Código do Professor']  # Obtém o código do professor da linha atual
        if cod_professor in correcoes_professores:  # Verifica se o código está no dicionário de correções
            horariosTURMAS.at[idx, 'Professor'] = correcoes_professores[cod_professor]  # Substitui o professor vazio pelo substituto