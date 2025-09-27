import numpy as np
import pandas as pd
from csvpandas import HoraADM, HoraINFO, HoraAGRO

# Definição dos dias e horários
dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
horarios = [
    "07:10-08:00", "08:00-08:50", "09:00-09:50", "09:50-10:40",
    "10:50-11:40", "11:40-12:30", "12:30-13:50",  # almoço
    "13:50-14:40", "14:40-15:30", "15:50-16:40", "16:40-17:30",
    "17:30-19:00",  # descanso
    "19:00-19:50", "19:50-20:40" "20:50-21:40", "21:40-22:30"
]

def criar_matriz(df):
    matriz = np.zeros((len(dias), len(horarios)), dtype=np.int64)
    for _, row in df.iterrows():
        if row["Dia"] in dias and row["Horário"]in horarios:
            i = dias.index(row["Dia"])
            j = horarios.index(row["Horário"])
            # Preenche com código da disciplina
            try:
                matriz[i, j] = int(row["Código da Disciplina"])
            except:
                matriz[i, j] = 0
    return matriz

# Criar as matrizes a partir dos dataframes que você já tem
matrizADM = criar_matriz(HoraADM)
matrizINFO = criar_matriz(HoraINFO)
matrizAGRO = criar_matriz(HoraAGRO)

print("Matriz Administração:\n", matrizADM)
print("Matriz Informática:\n", matrizINFO)
print("Matriz Agropecuária:\n", matrizAGRO)

