import pandas as pd

horariosTURMAS = pd.read_csv('horariosTURMAS.csv', sep=',', encoding='utf-8-sig')

horariosTURMAS.columns = [
    "Código do Curso", "Curso", "Código de Turma", "Turma",
    "Código da Disciplina", "Disciplina", "Código do Professor", "Professor", "Total de Aulas Semanais"
]

horariosTURMAS["Série"] = horariosTURMAS["Turma"].str.extract(r'(\d+° ano)')
horariosTURMAS["Turma_Letra"] = horariosTURMAS["Turma"].str.extract(r'- ([a-zA-Z])$')