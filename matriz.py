import numpy as np
import random
import pandas as pd
from csvpandas import horarioAGRO as agro, horarioINFO as info, horarioADM as adm

professores_adm = 'professores'
professores_info = 'professores'
professores_agro = 'professores'

dias = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta"]
horarios = [
    "07:10-08:00", "08:00-08:50", "09:00-09:50",
    "10:50-11:40", "11:40-12:30", "13:50-14:40",
    "14:40-15:30", "15:50-16:40", "16:40-17:30"
]


def distribuir_disciplinas(df):
    """Distribui as disciplinas aleatoriamente na matriz."""
    matriz = np.zeros((len(dias), len(horarios)), dtype=int)
    for _, row in df.iterrows():
        codigo = int(row["Código da Disciplina"])
        aulas = int(row["Total de Aulas Semanais"])

        livres = [(i, j) for i in range(len(dias)) for j in range(len(horarios)) if matriz[i, j] == 0]
        if not livres:
            break
        escolhidos = random.sample(livres, min(aulas, len(livres)))

        for (i, j) in escolhidos:
            matriz[i, j] = codigo
    return matriz


def gerar_matrizes_por_turma(df, nome_curso, professores):
    """Cria uma matriz para cada turma e série do curso."""
    if "Série" not in df.columns or "Turma" not in df.columns:
        print(f"O DataFrame de {nome_curso} não tem colunas 'Série' e 'Turma'.")
        return []

    resultados = []
    grupos = df.groupby(["Série", "Turma"])
    for (serie, turma), grupo in grupos:
        matriz = distribuir_disciplinas(grupo)
        resultados.append((nome_curso, serie, turma, matriz, professores, grupo))
    return resultados

# ------------------------
# MAIN — Gera matrizes e exporta todas em um único CSV
# ------------------------
if __name__ == "__main__":
    todas = []
    todas += gerar_matrizes_por_turma(info, "Informática", professores_info)
    todas += gerar_matrizes_por_turma(adm, "Administração", professores_adm)
    todas += gerar_matrizes_por_turma(agro, "Agropecuária", professores_agro)

    # Cria DataFrame final e salva em CSV
    df_final = pd.DataFrame(todas)
    df_final.to_csv("matrizes_geradas.csv", index=False, encoding="utf-8-sig", sep=";")

    print(f"\n Total de matrizes geradas: {len(todas)}")
    print("Arquivo salvo como: matrizes_geradas.csv")
