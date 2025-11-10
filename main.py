from csvpandas import horariosTURMAS  # Pega os dados das turmas que já foram preparados no outro arquivo
from matrizGeradora import gerar_matrizes_por_turma, dias, horarios  # Pega as funções para criar horários e as listas de dias e horários
from restricoes import (validar_restricoes, autoajustar_matriz_com_pontuacao,  # Pega funções para verificar e melhorar os horários
                        inicializar_validador, validar_restricoes_com_pontuacao)
import pandas as pd  # Importa biblioteca para trabalhar com planilhas e salvar arquivos


def exportar_matrizes_para_csv(todas_matrizes, arquivo_saida="horariosAjustados.csv"):  # Função para salvar os horários em um arquivo
    dados_exportacao = []  # Lista vazia onde vamos guardar todos os dados que serão salvos

    for curso, serie, turma, matriz, professores, df in todas_matrizes:  # Para cada turma que tem horário gerado
        dados_exportacao.append({  # Adiciona uma linha com o nome da turma
            "Turma": f"{curso} - {serie} - Turma {turma}",  # Escreve o nome completo da turma
            **{horario: "" for horario in horarios}  # Cria colunas vazias para cada horário
        })

        for dia_idx, dia in enumerate(dias):  # Para cada dia da semana (Segunda, Terça, etc.)
            linha = {"Turma": dia}  # Cria uma nova linha com o nome do dia

            for horario_idx, horario in enumerate(horarios):  # Para cada horário do dia
                cod_disc = matriz[dia_idx, horario_idx]  # Pega qual matéria está neste horário

                if cod_disc == 0 or cod_disc == '0':  # Se não tem aula neste horário
                    linha[horario] = ""  # Deixa a célula vazia
                else:  # Se tem aula neste horário
                    disciplina_info = df[df["Código da Disciplina"] == cod_disc]  # Busca informações sobre esta matéria
                    if not disciplina_info.empty:  # Se encontrou a matéria
                        disciplina = disciplina_info["Disciplina"].iloc[0]  # Pega o nome da matéria
                        professor = professores.get(cod_disc, "Desconhecido")  # Pega o nome do professor

                        if len(disciplina) > 20:  # Se o nome da matéria é muito longo
                            disciplina_abreviada = disciplina[:20] + "..."  # Encurta o nome
                        else:  # Se o nome é de tamanho normal
                            disciplina_abreviada = disciplina  # Usa o nome completo

                        if len(professor) > 15:  # Se o nome do professor é muito longo
                            professor_abreviado = professor[:15] + "..."  # Encurta o nome
                        else:  # Se o nome é de tamanho normal
                            professor_abreviado = professor  # Usa o nome completo

                        # Coloca no formato: "Nome da Matéria (Nome do Professor)"
                        linha[horario] = f"{disciplina_abreviada} ({professor_abreviado})"
                    else:  # Se não encontrou informações da matéria
                        linha[horario] = f"ERRO: {cod_disc}"  # Mostra mensagem de erro

            dados_exportacao.append(linha)  # Adiciona a linha do dia à lista

        # Adiciona uma linha em branco entre turmas para separar
        dados_exportacao.append({"Turma": "", **{horario: "" for horario in horarios}})

    # Cria uma planilha com todos os dados coletados
    df_export = pd.DataFrame(dados_exportacao)
    # Salva a planilha em um arquivo CSV
    df_export.to_csv(arquivo_saida, index=False, encoding="utf-8-sig", sep=";")
    print(f"✓ Horários salvos em: {arquivo_saida}")  # Mostra mensagem de confirmação
    return df_export  # Retorna a planilha criada


def main():  # Função principal que coordena todo o processo
    print("=== SISTEMA DE GERAÇÃO DE HORÁRIOS ===")  # Título do sistema
    print("REGRAS APLICADAS:")  # Lista das regras que o sistema segue
    print("✓ Prioridade de colocar aulas na manhã")  # Regra 1: tentar colocar o máximo possível na manhã
    print("✓ Professor não pode estar em duas turmas ao mesmo tempo")  # Regra 2: evitar conflitos de professores
    print("✓ Dois professores não podem estar na mesma turma ao mesmo tempo")  # Regra 3: evitar sobreposição
    print("✓ Respeito ao horário de funcionamento dos cursos")  # Regra 4: seguir os horários definidos
    print("✓ Máximo 2 dias com aulas no período da tarde")  # Regra 5: limitar uso da tarde
    print("Gerando horários...")  # Mensagem de que o processo começou

    # Gera os horários iniciais para todas as turmas
    todas_matrizes = gerar_matrizes_por_turma(horariosTURMAS)
    # Prepara o sistema de verificação com todos os horários gerados
    inicializar_validador(todas_matrizes)

    print(f"\nTotal de horários gerados inicialmente: {len(todas_matrizes)}")  # Mostra quantos horários foram criados

    matrizes_processadas = []  # Lista para guardar os horários depois de verificados e ajustados
    estatisticas = []  # Lista para guardar informações sobre cada turma

    print(f"\n{'=' * 60}")  # Linha de separação visual
    print("VERIFICANDO E CLASSIFICANDO HORÁRIOS...")  # Título da seção
    print(f"{'=' * 60}")  # Linha de separação visual

    for i, (curso, serie, turma, matriz, professores, df) in enumerate(todas_matrizes):  # Para cada turma
        print(f"\n▶ PROCESSANDO: {curso} | {serie} | Turma {turma}")  # Mostra qual turma está sendo processada

        # Verifica se o horário desta turma está bom e dá uma pontuação
        erros_iniciais, pontuacao_inicial = validar_restricoes_com_pontuacao(matriz, df, curso, serie, turma)

        if pontuacao_inicial == 0:  # Se o horário já está perfeito (pontuação 0)
            print(f"   ✅ Horário inicial PERFEITO (pontuação: 0)")  # Mensagem de sucesso
            # Guarda este horário como bom
            matrizes_processadas.append((curso, serie, turma, matriz, professores, df, 0))
            estatisticas.append((curso, serie, turma, 0, 0, "Perfeita"))  # Guarda estatística

            # Conta quantas aulas ficaram na manhã e na tarde
            aulas_manha = sum(1 for dia in range(len(dias)) for hora in [0, 1, 2, 3, 4, 5] if matriz[dia, hora] != 0)
            aulas_tarde = sum(1 for dia in range(len(dias)) for hora in [6, 7, 8, 9] if matriz[dia, hora] != 0)
            print(f"   📊 Estatísticas: {aulas_manha} aulas manhã, {aulas_tarde} aulas tarde")  # Mostra as contagens
        else:  # Se o horário tem problemas
            print(f"   ⚠ Horário inicial com {len(erros_iniciais)} problemas (pontuação: {pontuacao_inicial})")  # Avisa

            # Mostra os primeiros 3 problemas encontrados
            for erro in erros_iniciais[:3]:  # Pega apenas os 3 primeiros erros
                print(f"      • {erro}")  # Mostra cada problema
            if len(erros_iniciais) > 3:  # Se tem mais de 3 problemas
                print(f"      ... e mais {len(erros_iniciais) - 3} problemas")  # Mostra quantos problemas a mais tem

            print(f"   🔄 Tentando ajustar automaticamente...")  # Mensagem de que vai tentar melhorar
            # Tenta melhorar o horário automaticamente
            matriz_ajustada, sucesso, pontuacao_final = autoajustar_matriz_com_pontuacao(
                matriz, df, curso, serie, turma, max_tentativas=50  # Tenta até 50 vezes melhorar
            )

            # Verifica o horário depois do ajuste
            erros_finais, _ = validar_restricoes_com_pontuacao(matriz_ajustada, df, curso, serie, turma)

            if sucesso:  # Se conseguiu deixar o horário perfeito
                status = "Perfeita"  # Marca como perfeito
                print(f"   ✅ Horário ajustado para PERFEITO (pontuação: 0)")  # Mensagem de sucesso

                # Conta aulas na manhã e tarde do horário ajustado
                aulas_manha = sum(
                    1 for dia in range(len(dias)) for hora in [0, 1, 2, 3, 4, 5] if matriz_ajustada[dia, hora] != 0)
                aulas_tarde = sum(
                    1 for dia in range(len(dias)) for hora in [6, 7, 8, 9] if matriz_ajustada[dia, hora] != 0)
                print(f"   📊 Estatísticas: {aulas_manha} aulas manhã, {aulas_tarde} aulas tarde")  # Mostra
            else:  # Se não conseguiu deixar perfeito
                status = f"Melhor possível (pontuação: {pontuacao_final})"  # Marca como o melhor que conseguiu
                print(f"   ⚠ Melhor horário encontrado com {len(erros_finais)} problemas (pontuação: {pontuacao_final})")  # Mensagem

                # Mostra os principais problemas que ainda existem
                for erro in erros_finais[:2]:  # Pega os 2 primeiros problemas
                    print(f"      • {erro}")  # Mostra cada problema

            # Guarda o horário ajustado na lista
            matrizes_processadas.append((curso, serie, turma, matriz_ajustada, professores, df, pontuacao_final))
            estatisticas.append((curso, serie, turma, pontuacao_inicial, pontuacao_final, status))  # Guarda estatística

    # Ordena os horários do melhor para o pior (menor pontuação primeiro)
    matrizes_processadas.sort(key=lambda x: x[6])

    # Separa os horários perfeitos dos que têm problemas
    matrizes_perfeitas = [m for m in matrizes_processadas if m[6] == 0]  # Só os com pontuação 0
    matrizes_com_violacoes = [m for m in matrizes_processadas if m[6] > 0]  # Os com pontuação maior que 0

    print(f"\n{'=' * 60}")  # Linha de separação visual
    print("ANALISANDO RESULTADOS FINAIS...")  # Título da seção
    print(f"{'=' * 60}")  # Linha de separação visual

    # NOTA: A verificação de problemas entre turmas foi removida nesta versão

    nome_arquivo = "horariosAjustados.csv"  # Nome do arquivo onde será salvo

    # Decide quais horários salvar no arquivo final
    if matrizes_perfeitas:  # Se tem horários perfeitos
        print(f"✅ Encontrados {len(matrizes_perfeitas)} horários PERFEITOS")  # Mostra quantos
        matrizes_para_exportar = matrizes_perfeitas  # Vai salvar só os perfeitos
        print(f"📤 Salvando horários perfeitos em: {nome_arquivo}")  # Mensagem
    elif matrizes_processadas:  # Se não tem perfeitos mas tem alguns horários
        print(f"⚠ Nenhum horário perfeito encontrado. Salvando os {len(matrizes_processadas)} melhores horários")  # Mensagem
        matrizes_para_exportar = matrizes_processadas  # Salva todos os horários disponíveis
        print(f"📤 Salvando melhores horários encontrados em: {nome_arquivo}")  # Mensagem
    else:  # Se não tem nenhum horário
        print("❌ NENHUM horário foi gerado. Verifique os dados de entrada.")  # Mensagem de erro
        return  # Termina o programa

    # Prepara os dados para salvar (remove a pontuação da lista)
    matrizes_exportacao = [(curso, serie, turma, matriz, professores, df)
                           for curso, serie, turma, matriz, professores, df, pontuacao in matrizes_para_exportar]

    print(f"\n{'=' * 60}")  # Linha de separação visual
    print("SALVANDO RESULTADOS FINAIS...")  # Título da seção
    print(f"{'=' * 60}")  # Linha de separação visual

    # Salva os horários no arquivo
    df_export = exportar_matrizes_para_csv(matrizes_exportacao, nome_arquivo)

    # Mostra um relatório final com estatísticas
    print(f"\n📊 RELATÓRIO FINAL DETALHADO:")  # Título do relatório
    print(f"{'-' * 50}")  # Linha de separação

    total_turmas = len(todas_matrizes)  # Total de turmas que foram processadas
    turmas_perfeitas = len(matrizes_perfeitas)  # Quantas turmas têm horários perfeitos
    turmas_exportadas = len(matrizes_para_exportar)  # Quantas turmas serão salvas

    # Calcula estatísticas de pontuação
    pontuacao_total = sum(pontuacao for _, _, _, _, _, _, pontuacao in matrizes_processadas)  # Soma todas as pontuações
    pontuacao_media = pontuacao_total / total_turmas if total_turmas > 0 else 0  # Calcula a pontuação média

    print(f"   • Total de turmas processadas: {total_turmas}")  # Mostra total
    print(f"   • Turmas com horários perfeitos: {turmas_perfeitas}")  # Mostra perfeitas
    print(f"   • Turmas salvas: {turmas_exportadas}")  # Mostra salvas
    print(f"   • Taxa de sucesso perfeito: {(turmas_perfeitas / total_turmas) * 100:.1f}%")  # Calcula e mostra percentual
    print(f"   • Pontuação média por turma: {pontuacao_media:.2f}")  # Mostra pontuação média
    print(f"   • Taxa de salvamento: {(turmas_exportadas / total_turmas) * 100:.1f}%")  # Calcula e mostra percentual

    # Se há turmas com problemas que não foram salvas (quando só salvamos as perfeitas)
    if matrizes_com_violacoes and matrizes_para_exportar == matrizes_perfeitas:
        print(f"\n⚠ TURMAS COM PROBLEMAS (não salvas):")  # Título
        for curso, serie, turma, pontuacao_inicial, pontuacao_final, status in estatisticas:  # Para cada estatística
            if pontuacao_final > 0:  # Se a turma tem problemas
                print(f"   • {curso} - {serie} - Turma {turma}: {status}")  # Mostra a turma e seu status

    print(f"\n✅ ARQUIVO GERADO: {nome_arquivo}")  # Mensagem final com nome do arquivo
    print(f"\n=== PROCESSO CONCLUÍDO ===")  # Mensagem de fim do processo


if __name__ == "__main__":  # Se este arquivo for executado diretamente (não importado)
    main()  # Roda a função principal