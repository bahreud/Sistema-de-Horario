from csvpandas import horariosTURMAS
from matrizGeradora import gerar_matrizes_por_turma, dias, horarios
from restricoes import (validar_restricoes, autoajustar_matriz_com_pontuacao,
                        inicializar_validador, validar_restricoes_globais,
                        validar_restricoes_com_pontuacao)
import pandas as pd


def exportar_matrizes_para_csv(todas_matrizes, arquivo_saida="horariosAjustados.csv"):
    dados_exportacao = []

    for curso, serie, turma, matriz, professores, df in todas_matrizes:
        dados_exportacao.append({
            "Turma": f"{curso} - {serie} - Turma {turma}",
            **{horario: "" for horario in horarios}
        })

        for dia_idx, dia in enumerate(dias):
            linha = {"Turma": dia}

            for horario_idx, horario in enumerate(horarios):
                cod_disc = matriz[dia_idx, horario_idx]

                if cod_disc == 0 or cod_disc == '0':
                    linha[horario] = ""
                else:
                    disciplina_info = df[df["Código da Disciplina"] == cod_disc]
                    if not disciplina_info.empty:
                        disciplina = disciplina_info["Disciplina"].iloc[0]
                        professor = professores.get(cod_disc, "Desconhecido")

                        if len(disciplina) > 20:
                            disciplina_abreviada = disciplina[:20] + "..."
                        else:
                            disciplina_abreviada = disciplina

                        if len(professor) > 15:
                            professor_abreviado = professor[:15] + "..."
                        else:
                            professor_abreviado = professor

                        linha[horario] = f"{disciplina_abreviada} ({professor_abreviado})"
                    else:
                        linha[horario] = f"ERRO: {cod_disc}"

            dados_exportacao.append(linha)

        dados_exportacao.append({"Turma": "", **{horario: "" for horario in horarios}})

    df_export = pd.DataFrame(dados_exportacao)
    df_export.to_csv(arquivo_saida, index=False, encoding="utf-8-sig", sep=";")
    print(f"✓ Matrizes exportadas para: {arquivo_saida}")
    return df_export


def main():
    print("=== SISTEMA DE GERACAO DE HORARIOS ===")
    print("Gerando matrizes de horários...")

    todas_matrizes = gerar_matrizes_por_turma(horariosTURMAS)
    inicializar_validador(todas_matrizes)

    print(f"\nTotal de matrizes geradas inicialmente: {len(todas_matrizes)}")

    matrizes_processadas = []
    estatisticas = []

    print(f"\n{'=' * 60}")
    print("PROCESSANDO E CLASSIFICANDO MATRIZES...")
    print(f"{'=' * 60}")

    for i, (curso, serie, turma, matriz, professores, df) in enumerate(todas_matrizes):
        print(f"\n▶ PROCESSANDO: {curso} | {serie} | Turma {turma}")

        erros_iniciais, pontuacao_inicial = validar_restricoes_com_pontuacao(matriz, df, curso, serie, turma)

        if pontuacao_inicial == 0:
            print(f"   ✓ Matriz inicial PERFEITA (pontuação: 0)")
            matrizes_processadas.append((curso, serie, turma, matriz, professores, df, 0))
            estatisticas.append((curso, serie, turma, 0, len(erros_iniciais), "Perfeita"))
        else:
            print(f"   ⚠ Matriz inicial com {len(erros_iniciais)} violações (pontuação: {pontuacao_inicial})")

            matriz_ajustada, sucesso, pontuacao_final = autoajustar_matriz_com_pontuacao(
                matriz, df, curso, serie, turma, max_tentativas=50
            )

            erros_finais, _ = validar_restricoes_com_pontuacao(matriz_ajustada, df, curso, serie, turma)

            if sucesso:
                status = "Perfeita"
                print(f"   ✓ Matriz ajustada para PERFEITA (pontuação: 0)")
            else:
                status = f"Melhor possível (pontuação: {pontuacao_final})"
                print(f"   ⚠ Melhor matriz encontrada com {len(erros_finais)} violações (pontuação: {pontuacao_final})")

            matrizes_processadas.append((curso, serie, turma, matriz_ajustada, professores, df, pontuacao_final))
            estatisticas.append((curso, serie, turma, pontuacao_inicial, pontuacao_final, status))

    matrizes_processadas.sort(key=lambda x: x[6])

    matrizes_perfeitas = [m for m in matrizes_processadas if m[6] == 0]
    matrizes_com_violacoes = [m for m in matrizes_processadas if m[6] > 0]

    print(f"\n{'=' * 60}")
    print("ANALISANDO RESULTADOS...")
    print(f"{'=' * 60}")

    erros_globais = validar_restricoes_globais()
    if erros_globais:
        print(f"⚠ Encontradas {len(erros_globais)} violações globais de carga horária")

    nome_arquivo = "horariosAjustados.csv"

    if matrizes_perfeitas:
        print(f"✓ Encontradas {len(matrizes_perfeitas)} matrizes PERFEITAS")
        matrizes_para_exportar = matrizes_perfeitas
        print(f"✓ Exportando matrizes perfeitas para: {nome_arquivo}")
    elif matrizes_processadas:
        print(f"⚠ Nenhuma matriz perfeita encontrada. Exportando as {len(matrizes_processadas)} melhores matrizes")
        matrizes_para_exportar = matrizes_processadas
        print(f"✓ Exportando melhores matrizes encontradas para: {nome_arquivo}")
    else:
        print("✗ NENHUMA matriz foi gerada. Verifique os dados de entrada.")
        return

    matrizes_exportacao = [(curso, serie, turma, matriz, professores, df)
                           for curso, serie, turma, matriz, professores, df, pontuacao in matrizes_para_exportar]

    print(f"\n{'=' * 60}")
    print("EXPORTANDO RESULTADOS FINAIS...")
    print(f"{'=' * 60}")

    df_export = exportar_matrizes_para_csv(matrizes_exportacao, nome_arquivo)

    print(f"\n📊 RELATÓRIO FINAL DETALHADO:")
    print(f"{'-' * 50}")

    total_turmas = len(todas_matrizes)
    turmas_perfeitas = len(matrizes_perfeitas)
    turmas_exportadas = len(matrizes_para_exportar)

    print(f"   • Total de turmas processadas: {total_turmas}")
    print(f"   • Turmas com matrizes perfeitas: {turmas_perfeitas}")
    print(f"   • Turmas exportadas: {turmas_exportadas}")
    print(f"   • Taxa de sucesso perfeito: {(turmas_perfeitas / total_turmas) * 100:.1f}%")
    print(f"   • Taxa de exportação: {(turmas_exportadas / total_turmas) * 100:.1f}%")

    if matrizes_com_violacoes and matrizes_para_exportar == matrizes_perfeitas:
        print(f"\n⚠ TURMAS COM VIOLAÇÕES (não exportadas):")
        for curso, serie, turma, pontuacao_inicial, pontuacao_final, status in estatisticas:
            if pontuacao_final > 0:
                print(f"   • {curso} - {serie} - Turma {turma}: {status}")

    print(f"\n✅ ARQUIVO GERADO: {nome_arquivo}")
    print(f"\n=== PROCESSO CONCLUÍDO ===")


if __name__ == "__main__":
    main()