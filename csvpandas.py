import pandas as pd

HoraINFO = pd.read_csv('HoraINFO.csv',
                         sep=';',
                         encoding='utf-8',
                     names=["Curso", "Código do Curso", "Turma", "Código da Turma", "Disciplina", "Código da Disciplina", "Professor", "Código do Professor", "Dia", "Horário"],
                         header=0)

print(HoraINFO)


HoraAGRO = pd.read_csv('HoraAGRO.csv',
                       sep=';',
                       encoding='utf-8',
                       names=["Curso", "Código do Curso", "Turma", "Código da Turma", "Disciplina", "Código da Disciplina", "Professor", "Código do Professor", "Dia", "Horário"],
                       header=0)
print(HoraAGRO)


HoraADM = pd.read_csv('HoraADM.csv',
                       sep=';',
                       encoding='utf-8',
                       names=["Curso", "Código do Curso", "Turma", "Código da Turma", "Disciplina", "Código da Disciplina", "Professor", "Código do Professor", "Dia", "Horário"],
                       header=0)
print(HoraADM)