import pandas as pd

horarioINFO = pd.read_csv('horarioINFO.csv', sep=',', encoding='utf-8-sig',
                          names=["Código do Curso", "Curso", "Código da Série", "Série",
                             "Código da Turma", "Turma", "Código da Disciplina",
                             "Disciplina", "Professor", "Código do Professor", "Total de Aulas Semanais"],
                          header=0)

horarioAGRO = pd.read_csv('horarioAGRO.csv', sep=',', encoding='utf-8-sig',
                          names=["Código do Curso", "Curso", "Código da Série", "Série",
                                 "Código da Turma", "Turma", "Código da Disciplina",
                                 "Disciplina", "Professor", "Código do Professor", "Total de Aulas Semanais"],
                          header=0)

horarioADM = pd.read_csv('horarioADM.csv', sep=',', encoding='utf-8-sig',
                         names=["Código do Curso", "Curso", "Código da Série", "Série",
                             "Código da Turma", "Turma", "Código da Disciplina",
                             "Disciplina", "Professor", "Código do Professor", "Total de Aulas Semanais"],
                         header=0)

print(horarioINFO.head())
print(horarioAGRO.head())
print(horarioADM.head())
