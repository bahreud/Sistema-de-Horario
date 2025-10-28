import numpy as np
import random
import pandas as pd
from csvpandas import horariosTURMAS

dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
horarios = [
    "07:10-08:00", "08:00-08:50", "09:00-09:50",
    "10:50-11:40", "11:40-12:30", "13:50-14:40",
    "14:40-15:30", "15:50-16:40", "16:40-17:30"
]


def distribuir_disciplinas(df, max_tentativas=50):
    for tentativa in range(max_tentativas):
        matriz = np.zeros((len(dias), len(horarios)), dtype=object)
        professores_dict = dict(zip(df["Código da Disciplina"], df["Professor"]))
        sucesso = True

        for _, row in df.iterrows():
            codigo = row["Código da Disciplina"]
            aulas = int(row["Total de Aulas Semanais"])

            posicoes_encontradas = []
            for _ in range(aulas * 3):  # Dar mais chances
                livres = [(i, j) for i in range(len(dias)) for j in range(len(horarios)) if matriz[i, j] == 0]
                if not livres:
                    sucesso = False
                    break

                pos = random.choice(livres)
                posicoes_encontradas.append(pos)

            if not sucesso or len(posicoes_encontradas) < aulas:
                sucesso = False
                break

            escolhidos = posicoes_encontradas[:aulas]

            for (i, j) in escolhidos:
                matriz[i, j] = codigo

        if sucesso:
            return matriz, professores_dict

    print("Aviso: Distribuição não ideal após várias tentativas")
    return matriz, professores_dict


def gerar_matrizes_por_turma(df):
    if "Série" not in df.columns or "Turma_Letra" not in df.columns:
        print("O DataFrame não tem colunas 'Série' e 'Turma_Letra'.")
        return []

    resultados = []
    grupos = df.groupby(["Curso", "Série", "Turma_Letra"])

    for (curso, serie, turma), grupo in grupos:
        print(f"Gerando matriz para {curso} - {serie} - Turma {turma}")
        matriz, professores = distribuir_disciplinas(grupo)
        resultados.append((curso, serie, turma, matriz, professores, grupo))

    return resultados


if __name__ == "__main__":
    todas_matrizes = gerar_matrizes_por_turma(horariosTURMAS)
    print(f"\nTotal de matrizes geradas: {len(todas_matrizes)}")