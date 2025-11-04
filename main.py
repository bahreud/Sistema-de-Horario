from csvpandas import horariosTURMAS  # Pega os dados das turmas que já foram preparados
from matrizGeradora import gerar_matrizes_por_turma, dias, horarios  # Pega funções para gerar horários
from restricoes import (validar_restricoes, autoajustar_matriz_com_pontuacao,  # Pega funções para verificar e ajustar horários
                        inicializar_validador, validar_restricoes_globais,
                        validar_restricoes_com_pontuacao)
import pandas as pd  # Importa biblioteca para trabalhar com planilhas


def exportar_matrizes_para_csv(todas_matrizes, arquivo_saida="horariosAjustados.csv"):  # Salva os horários em arquivo
    dados_exportacao = []  # Lista vazia para dados que serão salvos

    for curso, serie, turma, matriz, professores, df in todas_matrizes:  # Para cada turma
        dados_exportacao.append({  # Adiciona uma linha com o nome da turma
            "Turma": f"{curso} - {serie} - Turma {turma}",  # Nome completo da turma
            **{horario: "" for horario in horarios}  # Colunas vazias para cada horário
        })

        for dia_idx, dia in enumerate(dias):  # Para cada dia da semana
            linha = {"Turma": dia}  # Cria uma linha com o nome do dia

            for horario_idx, horario in enumerate(horarios):  # Para cada horário
                cod_disc = matriz[dia_idx, horario_idx]  # Pega a matéria neste horário

                if cod_disc == 0 or cod_disc == '0':  # Se não tem aula
                    linha[horario] = ""  # Deixa vazio
                else:  # Se tem aula
                    # Busca informações sobre esta matéria
                    disciplina_info = df[df["Código da Disciplina"] == cod_disc]
                    if not disciplina_info.empty:  # Se encontrou a matéria
                        disciplina = disciplina_info["Disciplina"].iloc[0]  # Pega o nome da matéria
                        professor = professores.get(cod_disc, "Desconhecido")  # Pega o nome do professor

                        if len(disciplina) > 20:  # Se o nome da matéria é muito longo
                            disciplina_abreviada = disciplina[:20] + "..."  # Encurta o nome
                        else:  # Se o nome é normal
                            disciplina_abreviada = disciplina  # Usa o nome completo

                        if len(professor) > 15:  # Se o nome do professor é muito longo
                            professor_abreviado = professor[:15] + "..."  # Encurta o nome
                        else:  # Se o nome é normal
                            professor_abreviado = professor  # Usa o nome completo

                        # Coloca no formato: "Matéria (Professor)"
                        linha[horario] = f"{disciplina_abreviada} ({professor_abreviado})"
                    else:  # Se não encontrou a matéria
                        linha[horario] = f"ERRO: {cod_disc}"  # Mostra erro

            dados_exportacao.append(linha)  # Adiciona a linha do dia

        # Adiciona uma linha em branco entre turmas
        dados_exportacao.append({"Turma": "", **{horario: "" for horario in horarios}})

    # Cria uma planilha com todos os dados
    df_export = pd.DataFrame(dados_exportacao)
    # Salva a planilha em arquivo CSV
    df_export.to_csv(arquivo_saida, index=False, encoding="utf-8-sig", sep=";")
    print(f"✓ Horários salvos em: {arquivo_saida}")  # Mensagem de confirmação
    return df_export  # Retorna a planilha criada


def main():  # Função principal que coordena tudo
    print("=== SISTEMA DE GERAÇÃO DE HORÁRIOS ===")  # Título do sistema
    print("REGRAS APLICADAS:")  # Lista de regras usadas
    print("✓ Prioridade de colocar aulas na manhã")  # Regra 1
    print("✓ Professor não pode estar em duas turmas ao mesmo tempo")  # Regra 2
    print("✓ Dois professores não podem estar na mesma turma ao mesmo tempo")  # Regra 3
    print("✓ Respeito ao horário de funcionamento dos cursos")  # Regra 4
    print("✓ Máximo 2 dias com aulas no período da tarde")  # Regra 5
    print("Gerando horários...")  # Mensagem

    # Gera os horários iniciais para todas as turmas
    todas_matrizes = gerar_matrizes_por_turma(horariosTURMAS)
    # Prepara o validador com todos os horários gerados
    inicializar_validador(todas_matrizes)

    print(f"\nTotal de horários gerados inicialmente: {len(todas_matrizes)}")  # Mostra quantos horários foram feitos

    matrizes_processadas = []  # Lista para horários depois de verificados e ajustados
    estatisticas = []  # Lista para guardar informações sobre cada turma

    print(f"\n{'=' * 60}")  # Linha de separação
    print("VERIFICANDO E CLASSIFICANDO HORÁRIOS...")  # Título
    print(f"{'=' * 60}")  # Linha de separação

    for i, (curso, serie, turma, matriz, professores, df) in enumerate(todas_matrizes):  # Para cada turma
        print(f"\n▶ PROCESSANDO: {curso} | {serie} | Turma {turma}")  # Mostra qual turma está sendo processada

        # Verifica se o horário desta turma está bom
        erros_iniciais, pontuacao_inicial = validar_restricoes_com_pontuacao(matriz, df, curso, serie, turma)

        if pontuacao_inicial == 0:  # Se o horário já está perfeito
            print(f"   ✅ Horário inicial PERFEITO (pontuação: 0)")  # Mensagem
            # Guarda este horário como bom
            matrizes_processadas.append((curso, serie, turma, matriz, professores, df, 0))
            estatisticas.append((curso, serie, turma, 0, 0, "Perfeita"))  # Guarda estatística

            # Conta aulas na manhã e tarde
            aulas_manha = sum(1 for dia in range(len(dias)) for hora in [0, 1, 2, 3, 4] if matriz[dia, hora] != 0)
            aulas_tarde = sum(1 for dia in range(len(dias)) for hora in [5, 6, 7, 8] if matriz[dia, hora] != 0)
            print(f"   📊 Estatísticas: {aulas_manha} aulas manhã, {aulas_tarde} aulas tarde")  # Mostra
        else:  # Se o horário tem problemas
            print(f"   ⚠ Horário inicial com {len(erros_iniciais)} problemas (pontuação: {pontuacao_inicial})")  # Avisa

            # Mostra os primeiros 3 problemas
            for erro in erros_iniciais[:3]:
                print(f"      • {erro}")  # Mostra cada problema
            if len(erros_iniciais) > 3:  # Se tem mais problemas
                print(f"      ... e mais {len(erros_iniciais) - 3} problemas")  # Mostra quantos

            print(f"   🔄 Tentando ajustar automaticamente...")  # Mensagem
            # Tenta melhorar o horário
            matriz_ajustada, sucesso, pontuacao_final = autoajustar_matriz_com_pontuacao(
                matriz, df, curso, serie, turma, max_tentativas=50  # Tenta 50 vezes melhorar
            )

            # Verifica o horário ajustado
            erros_finais, _ = validar_restricoes_com_pontuacao(matriz_ajustada, df, curso, serie, turma)

            if sucesso:  # Se conseguiu deixar perfeito
                status = "Perfeita"  # Marca como perfeito
                print(f"   ✅ Horário ajustado para PERFEITO (pontuação: 0)")  # Mensagem

                # Conta aulas na manhã e tarde do horário ajustado
                aulas_manha = sum(
                    1 for dia in range(len(dias)) for hora in [0, 1, 2, 3, 4] if matriz_ajustada[dia, hora] != 0)
                aulas_tarde = sum(
                    1 for dia in range(len(dias)) for hora in [5, 6, 7, 8] if matriz_ajustada[dia, hora] != 0)
                print(f"   📊 Estatísticas: {aulas_manha} aulas manhã, {aulas_tarde} aulas tarde")  # Mostra
            else:  # Se não conseguiu deixar perfeito
                status = f"Melhor possível (pontuação: {pontuacao_final})"  # Marca como o melhor possível
                print(f"   ⚠ Melhor horário encontrado com {len(erros_finais)} problemas (pontuação: {pontuacao_final})")  # Mensagem

                # Mostra os principais problemas que sobraram
                for erro in erros_finais[:2]:
                    print(f"      • {erro}")  # Mostra cada problema

            # Guarda o horário ajustado
            matrizes_processadas.append((curso, serie, turma, matriz_ajustada, professores, df, pontuacao_final))
            estatisticas.append((curso, serie, turma, pontuacao_inicial, pontuacao_final, status))  # Guarda estatística

    # Ordena os horários do melhor para o pior (menor pontuação primeiro)
    matrizes_processadas.sort(key=lambda x: x[6])

    # Separa horários perfeitos dos que têm problemas
    matrizes_perfeitas = [m for m in matrizes_processadas if m[6] == 0]  # Só os perfeitos
    matrizes_com_violacoes = [m for m in matrizes_processadas if m[6] > 0]  # Os com problemas

    print(f"\n{'=' * 60}")  # Linha de separação
    print("ANALISANDO RESULTADOS FINAIS...")  # Título
    print(f"{'=' * 60}")  # Linha de separação

    # Verifica problemas entre todas as turmas juntas
    erros_globais = validar_restricoes_globais()
    if erros_globais:  # Se encontrou problemas globais
        print(f"⚠ Encontrados {len(erros_globais)} problemas entre turmas:")  # Avisa
        for erro in erros_globais:  # Para cada problema
            print(f"   • {erro}")  # Mostra o problema

    nome_arquivo = "horariosAjustados.csv"  # Nome do arquivo onde será salvo

    # Decide quais horários salvar
    if matrizes_perfeitas:  # Se tem horários perfeitos
        print(f"✅ Encontrados {len(matrizes_perfeitas)} horários PERFEITOS")  # Mostra quantos
        matrizes_para_exportar = matrizes_perfeitas  # Vai salvar só os perfeitos
        print(f"📤 Salvando horários perfeitos em: {nome_arquivo}")  # Mensagem
    elif matrizes_processadas:  # Se não tem perfeitos mas tem alguns horários
        # Pega horários com poucos problemas (até 2 pontos)
        matrizes_boas = [m for m in matrizes_processadas if m[6] <= 2]
        if matrizes_boas:  # Se tem horários bons
            print(f"⚠ Nenhum horário perfeito. Salvando {len(matrizes_boas)} horários com poucos problemas")  # Mensagem
            matrizes_para_exportar = matrizes_boas  # Salva os bons
        else:  # Se não tem horários bons
            print(f"⚠ Salvando os {len(matrizes_processadas)} melhores horários encontrados")  # Mensagem
            matrizes_para_exportar = matrizes_processadas  # Salva todos
        print(f"📤 Salvando em: {nome_arquivo}")  # Mensagem
    else:  # Se não tem nenhum horário
        print("❌ NENHUM horário foi gerado. Verifique os dados de entrada.")  # Erro
        return  # Termina

    # Prepara os dados para salvar
    matrizes_exportacao = [(curso, serie, turma, matriz, professores, df)
                           for curso, serie, turma, matriz, professores, df, pontuacao in matrizes_para_exportar]

    print(f"\n{'=' * 60}")  # Linha de separação
    print("SALVANDO RESULTADOS FINAIS...")  # Título
    print(f"{'=' * 60}")  # Linha de separação

    # Salva os horários no arquivo
    df_export = exportar_matrizes_para_csv(matrizes_exportacao, nome_arquivo)

    # Mostra relatório final
    print(f"\n📊 RELATÓRIO FINAL DETALHADO:")  # Título
    print(f"{'-' * 50}")  # Linha

    total_turmas = len(todas_matrizes)  # Total de turmas processadas
    turmas_perfeitas = len(matrizes_perfeitas)  # Turmas com horários perfeitos
    turmas_exportadas = len(matrizes_para_exportar)  # Turmas que serão salvas

    # Calcula estatísticas
    pontuacao_total = sum(pontuacao for _, _, _, _, _, _, pontuacao in matrizes_processadas)  # Soma todas as pontuações
    pontuacao_media = pontuacao_total / total_turmas if total_turmas > 0 else 0  # Calcula média

    print(f"   • Total de turmas processadas: {total_turmas}")  # Mostra total
    print(f"   • Turmas com horários perfeitos: {turmas_perfeitas}")  # Mostra perfeitas
    print(f"   • Turmas salvas: {turmas_exportadas}")  # Mostra salvas
    print(f"   • Taxa de sucesso perfeito: {(turmas_perfeitas / total_turmas) * 100:.1f}%")  # Mostra percentual
    print(f"   • Pontuação média por turma: {pontuacao_media:.2f}")  # Mostra pontuação média
    print(f"   • Taxa de salvamento: {(turmas_exportadas / total_turmas) * 100:.1f}%")  # Mostra percentual salvamento

    # Se há turmas com problemas que não foram salvas
    if matrizes_com_violacoes and matrizes_para_exportar == matrizes_perfeitas:
        print(f"\n⚠ TURMAS COM PROBLEMAS (não salvas):")  # Título
        for curso, serie, turma, pontuacao_inicial, pontuacao_final, status in estatisticas:  # Para cada estatística
            if pontuacao_final > 0:  # Se tem problemas
                print(f"   • {curso} - {serie} - Turma {turma}: {status}")  # Mostra a turma

    print(f"\n✅ ARQUIVO GERADO: {nome_arquivo}")  # Mensagem final
    print(f"\n=== PROCESSO CONCLUÍDO ===")  # Fim


if __name__ == "__main__":  # Se este arquivo for executado diretamente
    main()  # Roda a função principal