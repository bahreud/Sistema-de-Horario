import numpy as np
import pandas as pd
from csvpandas import HoraAGRO, HoraADM, HoraINFO

# Definição dos dias e horários
dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
horarios = [
    "07:10-08:00", "08:00-08:50", "09:00-09:50", "09:50-10:40",
    "10:50-11:40", "11:40-12:30",
    "12:30-13:50",  # almoço
    "13:50-14:40", "14:40-15:30", "15:50-16:40", "16:40-17:30",
    "17:30-19:00",  # descanso
    "19:00-19:50", "19:50-20:40", "20:50-21:40", "21:40-22:30"
]

def criar_matriz_organizada(df):
    matriz = np.zeros((len(dias), len(horarios)), dtype=np.int64)

    # Lista de índices dos horários proibidos (almoço e descanso)
    indices_proibidos = [horarios.index("12:30-13:50"), horarios.index("17:30-19:00")]

    for i, dia in enumerate(dias):
        for j, horario in enumerate(horarios):
            if j in indices_proibidos:
                matriz[i, j] = 0
                continue

            # Filtra todas as aulas desse dia e horário
            aulas = df[(df["Dia"] == dia) & (df["Horário"] == horario)]
            if not aulas.empty:
                # Evita duplicidade de professor na mesma hora
                professores_usados = set()
                turmas_usadas = set()
                for _, aula in aulas.iterrows():
                    cod_prof = aula["Código do Professor"]
                    cod_turma = aula["Código da Turma"]

                    if cod_prof not in professores_usados and cod_turma not in turmas_usadas:
                        matriz[i, j] = aula["Código da Disciplina"]
                        professores_usados.add(cod_prof)
                        turmas_usadas.add(cod_turma)
                        break  # preenche apenas uma disciplina por horário

    # Garantir que não haja vaga na manhã exceto nos dois últimos horários
    manha_indices = list(range(0, 6))  # 07:10-12:30
    for i in range(len(dias)):
        for j in manha_indices[:-2]:
            if matriz[i, j] == 0:
                disciplinas_dia = df[df["Dia"] == dias[i]]["Código da Disciplina"].unique()
                if len(disciplinas_dia) > 0:
                    matriz[i, j] = int(disciplinas_dia[0])

    return matriz

# Criar matrizes organizadas para todos os cursos
matrizAGRO = criar_matriz_organizada(HoraAGRO)
matrizADM = criar_matriz_organizada(HoraADM)
matrizINFO = criar_matriz_organizada(HoraINFO)

print("Matriz Agropecuária:\n", matrizAGRO)
print("Matriz Administração:\n", matrizADM)
print("Matriz Informática:\n", matrizINFO)
