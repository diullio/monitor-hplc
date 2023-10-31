# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime, timedelta
from traceback import print_tb

import pandas as pd
from PyQt5.QtWidgets import QMessageBox
import getpass


class AppBD:
    def __init__(self):
        print('Bem vindo ao Monitor HPLC-CG')

        ## Trocar diretorio aqui: self.diretorio = 'LUGAR NOVO\\monitor_hplc.db'
        self.diretorio = 'C:\\Users\\diullio.santos\\Documents\\GiT\\dsdev\\1-hypera\\1-finished\\7-HPLC\\System\\monitor_hplc.db'


# TELA 1 e 2- CADASTRAR
## FAZER CONSULTA

    def fAgendarDados(self, ln_id, data_inicio, ln_produto, ln_ativos, ln_lote, ln_metodo, ln_coluna, ln_maquina, ln_tempocorrida, ln_tempo_limpeza, tempo_total, tipo, teste, numero_amostras, numero_injecoes):
        try:
            data_inicio = datetime.strptime(data_inicio, '%d/%m/%Y %H:%M')
            data_prevista = data_inicio + timedelta(minutes=tempo_total)
            conn = sqlite3.connect(self.diretorio)
            cursor = conn.cursor()

            cursor.execute("""
                INSERT INTO agenda (id_projeto, produto, ativos, lote, metodo, coluna, maquina, tempocorrida, tempolimpeza, data_inicio, data_prevista, tipo, testes, numero_amostras, numero_injecoes)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (ln_id, ln_produto, ln_ativos, ln_lote, ln_metodo, ln_coluna, ln_maquina, ln_tempocorrida, ln_tempo_limpeza, data_inicio, data_prevista, tipo, teste, numero_amostras, numero_injecoes))
            conn.commit()
            
            conn.close()
            message = f"Agendamento realizado com sucesso!"
            QMessageBox.information(None, "Confirmação", message, QMessageBox.Ok)
            self.fInserirRegistro(f'Projeto agendado: {ln_id}, {ln_produto}, {ln_lote}', ln_maquina)
        except Exception as e:
            print(f"Ocorreu uma exceção fAgendarDados: {e}")

    def fSelecionarDados(self, data_inicio, data_fim, maquina):
        try:
            conn = sqlite3.connect(self.diretorio)
            cursor = conn.cursor()
            if maquina:
                cursor.execute("""
                    SELECT id, id_projeto, produto, lote, maquina, data_inicio, data_prevista, testes FROM agenda
                    WHERE data_inicio BETWEEN ? AND ? AND maquina = ?
                """, (data_inicio, data_fim, maquina))
                resultados = cursor.fetchall()
            else:
                cursor.execute("""
                    SELECT id, id_projeto, produto, lote, maquina, data_inicio, data_prevista, testes FROM agenda
                    WHERE data_inicio BETWEEN ? AND ?
                """, (data_inicio, data_fim))
                resultados = cursor.fetchall()
            conn.close()
            self.dfagenda = pd.DataFrame(resultados, columns=['Id', 'Id Projeto', 'Produto', 'Lote', 'Maquina', 'Data Início', 'Data Prevista', 'Testes'])
            return self.dfagenda
        except Exception as e:
            print(f"Ocorreu uma exceção fSelecionarDados: {e}")

    def fSelecionarDadosCurrent(self, data):
        try:
            if isinstance(data, str):
                data = datetime.strptime(data, '%Y-%m-%d')
            
            data_2 = data + timedelta(days=1)

            conn = sqlite3.connect(self.diretorio)
            cursor = conn.cursor()
            cursor.execute("""
                SELECT id, id_projeto, produto, lote, maquina, data_inicio, data_prevista, testes FROM agenda
                WHERE data_inicio BETWEEN ? AND ?;
            """, (data, data_2))
            resultados = cursor.fetchall()
            conn.close()
            self.dfagenda = pd.DataFrame(resultados, columns=['Id', 'Id Projeto', 'Produto', 'Lote', 'Maquina', 'Data Início', 'Data Prevista', 'Testes'])
            return self.dfagenda
        except Exception as e:
            print(f"Ocorreu uma exceção: {e}")

    def fRemoverProjeto(self, selected_indexes):
    # Obtenha o índice da linha selecionada no QTableView
        try:
            if selected_indexes:
                row = selected_indexes[0].row()  # Supondo que apenas uma célula foi selecionada
                # Obtenha o valor da coluna "Id" na linha selecionada
                id = self.dfagenda.iloc[row]['Id']
                produto = self.dfagenda.iloc[row]['Produto']
                id_projeto = self.dfagenda.iloc[row]['Id Projeto']
                Lote = self.dfagenda.iloc[row]['Lote']
                Maquina = self.dfagenda.iloc[row]['Maquina']
                id = int(id)
                conn = sqlite3.connect(self.diretorio)
                cursor = conn.cursor()
                
                cursor.execute("SELECT id FROM agenda WHERE id = ?", (id,))
                resultado = cursor.fetchone()
                if resultado:
                        cursor.execute("DELETE FROM agenda WHERE id = ?", (id,))
                        conn.commit()   
                conn.close()
                self.fInserirRegistro(f'Projeto removido: {id_projeto}, {produto}, {Lote}', Maquina)
            return produto                
        except Exception as e:
            print(f"Ocorreu uma exceção: {e}")

    def fIniciarProjeto(self, selected_indexes):
        try:         
            if selected_indexes:
                row = selected_indexes[0].row()
                # Obtenha o valor da coluna "Id" na linha selecionada
                id = self.dfagenda.iloc[row]['Id']
                produto = self.dfagenda.iloc[row]['Produto']
                id_projeto = self.dfagenda.iloc[row]['Id Projeto']
                Lote = self.dfagenda.iloc[row]['Lote']
                Maquina = self.dfagenda.iloc[row]['Maquina']
                id = int(id)

                conn = sqlite3.connect(self.diretorio)
                cursor = conn.cursor()
                
                cursor.execute("""
                    SELECT id_projeto, produto, ativos, lote, metodo, coluna, maquina, tempocorrida, tempolimpeza, data_inicio, data_prevista, tipo, testes, numero_amostras, numero_injecoes FROM agenda
                    WHERE id = ?;              
                """, (id,))
                resultados = cursor.fetchall()

                if resultados:
                    id_projeto, produto, ativos, lote, metodo, coluna, maquina, tempocorrida, tempolimpeza, data_inicio, data_prevista, tipo, testes, numero_amostras, numero_injecoes = resultados[0]
                
                    data_inicio = datetime.strptime(data_inicio, "%Y-%m-%d %H:%M:%S")
                    data_prevista = datetime.strptime(data_prevista, "%Y-%m-%d %H:%M:%S")
                    tempo_total = (data_prevista - data_inicio).total_seconds() / 60
                    tempo_total = int(tempo_total)

                    self.fInserirDados(id_projeto, produto, ativos, lote, metodo, coluna, maquina, tempocorrida, tempolimpeza, tipo, testes, numero_amostras, numero_injecoes, tempo_total)
                    self.fInserirRegistro(f'Projeto iniciado: {id_projeto}, {produto}, {Lote}', Maquina)
                else:
                    print("Consulta não retornou resultados")
                conn.close()
        except Exception as e:
            print(f"Ocorreu uma exceção fIniciarProjeto: {e}")

 ## TELA 3 - EXECUCAO
    def fInserirDados(self, id_projeto, produto, ativos, lote, metodo, coluna, maquina, tempocorrida, tempolimpeza, tipo, testes, numero_amostras, numero_injecoes, tempo_total):
        try:            
            data_inicio = datetime.now()
            data_prevista = data_inicio + timedelta(minutes=tempo_total)

            data_inicio = data_inicio.strftime("%Y-%m-%d %H:%M")
            data_prevista = data_prevista.strftime("%Y-%m-%d %H:%M")

            conn = sqlite3.connect(self.diretorio)
            cursor = conn.cursor()

            # Verificar se a máquina já foi usada
            cursor.execute("SELECT id FROM controle WHERE maquina = ? AND data_fim IS NULL", (maquina,))
            registro_existente = cursor.fetchone()
       
            if registro_existente:
                message = f"O equipamento selecionado já está em uso."
                QMessageBox.information(None, "Alerta", message, QMessageBox.Ok)
           
            else:
                cursor.execute("""
                    INSERT INTO controle (id_projeto, produto, ativos, lote, metodo, coluna, maquina, tempocorrida, tempolimpeza, data_inicio, data_prevista, tipo, testes, numero_amostras, numero_injecoes)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (id_projeto, produto, ativos, lote, metodo, coluna, maquina, tempocorrida, tempolimpeza, data_inicio, data_prevista, tipo, testes, numero_amostras, numero_injecoes))            
                conn.commit()
                message = f"Produto {produto} iniciado com sucesso"
                QMessageBox.information(None, "Confirmação", message, QMessageBox.Ok)
            conn.close()
                    

        except Exception as e:
            print(f"Ocorreu uma exceção fInserirDados: {e}") 

    def fFinalizarDados(self, maquina, justificativa):
        try:
            data_fim = datetime.now()
            data_fim = data_fim.strftime("%Y-%m-%d %H:%M:%S")

            conn = sqlite3.connect(self.diretorio)
            cursor = conn.cursor()

            # Verificar se a máquina já foi usada
            cursor.execute("SELECT id, id_projeto, produto, lote FROM controle WHERE maquina = ? AND data_fim IS NULL", (maquina,))
            registro_existente = cursor.fetchone()

            if registro_existente:
                id, id_projeto, produto, lote = registro_existente
                id = int(id)
                cursor.execute("""
                    UPDATE controle
                    SET data_fim = ?, justificativa = ? 
                    WHERE id = ?
                """, (data_fim, justificativa, id))
                conn.commit()
                message = f"Teste finalizado com sucesso."
                QMessageBox.information(None, "Confirmação", message, QMessageBox.Ok)
                self.fInserirRegistro(f'Projeto finalizado: {id_projeto}, {produto}, {lote}', maquina)
            else:
                message = f"Não há testes pendentes para serem finalizados."
                QMessageBox.information(None, "Alerta", message, QMessageBox.Ok)
            conn.close()

        except Exception as e:
            print(f"Ocorreu uma exceção: {e}") 

    def fSelecionarDadosExec(self, data_inicio, data_fim, maquina):
        try:
            conn = sqlite3.connect(self.diretorio)
            cursor = conn.cursor()
            if maquina:
                cursor.execute("""
                    SELECT id, id_projeto, produto, lote, maquina, data_inicio, data_prevista, data_fim, testes, justificativa FROM controle
                    WHERE data_inicio BETWEEN ? AND ? AND maquina = ?
                """, (data_inicio, data_fim, maquina))
                resultados = cursor.fetchall()
            else:
                cursor.execute("""
                    SELECT id, id_projeto, produto, lote, maquina, data_inicio, data_prevista, data_fim, testes, justificativa FROM controle
                    WHERE data_inicio BETWEEN ? AND ?
                """, (data_inicio, data_fim))
                resultados = cursor.fetchall()
            conn.close()
            self.dfexecucao = pd.DataFrame(resultados, columns=['Id', 'Código', 'Produto', 'Lote', 'Máquina', 'Data Início', 'Data Prevista', 'Data Fim', 'Testes', 'Justificativa'])
            return self.dfexecucao
        except Exception as e:
            print(f"Ocorreu uma exceção: {e}")

## CHECAR FUNCIONAMENTO
    def fCheckFuncionamento(self, ln_maquina):
        try:
            conn = sqlite3.connect(self.diretorio)
            cursor = conn.cursor()
            if ln_maquina:
            # Verificar se a máquina já foi usada
                cursor.execute("SELECT produto FROM controle WHERE maquina = ? AND data_fim IS NULL", (ln_maquina,))
                registro_existente = cursor.fetchone()
                if registro_existente:
                    produto = registro_existente[0] 
                    return produto
            else:
                return None
        except Exception as e:
            print(f"Ocorreu uma exceção fCheckFuncionamento: {e}") 


## MANUTENÇÃO
    def StartManutencao(self, maquina):
        try:
            data_inicio = datetime.now()
            data_inicio = data_inicio.strftime("%Y-%m-%d %H:%M:%S")

            conn = sqlite3.connect(self.diretorio)
            cursor = conn.cursor()

            cursor.execute("SELECT id FROM manutencao WHERE maquina = ? AND data_fim IS NULL", (maquina,))
            registro_existente = cursor.fetchone()

            if registro_existente:
                message = f"Maquina já está em manutenção"
                QMessageBox.information(None, "Alerta", message, QMessageBox.Ok)
            
            else:
                cursor.execute("""
                    INSERT INTO manutencao (maquina, data_inicio)
                    VALUES (?, ?)
                """, (maquina, data_inicio))
                conn.commit()
                message = f"Manutenção iniciada no equipamento: {maquina}"
                QMessageBox.information(None, "Confirmação", message, QMessageBox.Ok)  
                self.fInserirRegistro(f'Manutenção iniciada', maquina)             
            conn.close()
        except Exception as e:
            print(f"Ocorreu uma exceção StartManutencao: {e}")

    def FinalizarManutencao(self, maquina):
        try:
            data_fim = datetime.now()
            data_fim = data_fim.strftime("%Y-%m-%d %H:%M:%S")

            conn = sqlite3.connect(self.diretorio)
            cursor = conn.cursor()

            # Verificar se a máquina já foi usada
            cursor.execute("SELECT id FROM manutencao WHERE maquina = ? AND data_fim IS NULL", (maquina,))
            registro_existente = cursor.fetchone()

            if registro_existente:
                id_registro = registro_existente[0]
                id_registro = int(id_registro)
                cursor.execute("""
                    UPDATE manutencao SET data_fim = ? WHERE id = ?
                """, (data_fim, id_registro))
                conn.commit()
                message = f"Manutenção finalizada no Equipamento: {maquina}."
                QMessageBox.information(None, "Confirmação", message, QMessageBox.Ok)
                self.fInserirRegistro(f'Manutenção finalizada', maquina)  
            else:
                message = f"Não há manutenção pendente para ser finalizada."
                QMessageBox.information(None, "Alerta", message, QMessageBox.Ok)
            conn.close()

        except Exception as e:
            print(f"Ocorreu uma exceção FinalizarManutencao: {e}") 

    def fSelecionarDadosManutencao(self, data_inicio, data_fim, maquina):
        try:
            conn = sqlite3.connect(self.diretorio)
            cursor = conn.cursor()
            if maquina:
                cursor.execute("""
                    SELECT id, maquina, data_inicio, data_fim FROM manutencao
                    WHERE data_inicio BETWEEN ? AND ? AND maquina = ?
                """, (data_inicio, data_fim, maquina))
                resultados = cursor.fetchall()
            else:
                cursor.execute("""
                    SELECT id, maquina, data_inicio, data_fim FROM manutencao
                    WHERE data_inicio BETWEEN ? AND ?
                """, (data_inicio, data_fim))
                resultados = cursor.fetchall()
            conn.close()
            self.dfmanutencao = pd.DataFrame(resultados, columns=['Id', 'Máquina', 'Data Início', 'Data Fim'])
            return self.dfmanutencao
        except Exception as e:
            print(f"Ocorreu uma exceção fSelecionarDadosManutencao: {e}")

    def fCheckManutencao(self, ln_maquina):
        try:
            conn = sqlite3.connect(self.diretorio)
            cursor = conn.cursor()
            if ln_maquina:
            # Verificar se a máquina já foi usada
                cursor.execute("SELECT id FROM manutencao WHERE maquina = ? AND data_fim IS NULL", (ln_maquina,))
                registro_existente = cursor.fetchone()
                if registro_existente:
                    id = registro_existente[0] 
                    return id
            else:
                return None
        except Exception as e:
            print(f"Ocorreu uma exceção fCheckManutencao: {e}")  

## REGISTRO

    def fInserirRegistro(self, acao, maquina):
        try:
            data = datetime.now()
            data = data.strftime("%Y-%m-%d %H:%M")

            usuario = getpass.getuser()

            conn = sqlite3.connect(self.diretorio)
            cursor = conn.cursor()

            cursor.execute("""
                    INSERT INTO registros (usuario, acao, data, maquina)
                    VALUES (?, ?, ?, ?)
                """, (usuario, acao, data, maquina))            
            conn.commit()

            conn.close()                    

        except Exception as e:
            print(f"Ocorreu uma exceção fInserirRegistro: {e}") 

    def fConsultarRegistro(self, data, data_fim, usuario, maquina):
        try:
            conn = sqlite3.connect(self.diretorio)
            cursor = conn.cursor()

            if maquina and usuario:
                cursor.execute("""
                    SELECT data, usuario, acao, maquina FROM registros
                    WHERE data BETWEEN ? AND ? AND maquina = ? AND usuario LIKE ?
                """, (data, data_fim, maquina, f"%{usuario}%"))
            elif usuario:
                 cursor.execute("""
                    SELECT data, usuario, acao, maquina FROM registros
                    WHERE data BETWEEN ? AND ? AND usuario LIKE ?
                """, (data, data_fim, f"%{usuario}%"))
            elif maquina:
                cursor.execute("""
                    SELECT data, usuario, acao, maquina FROM registros
                    WHERE data BETWEEN ? AND ? AND maquina = ?
                """, (data, data_fim, maquina))
            else:
                cursor.execute("""
                    SELECT data, usuario, acao, maquina FROM registros
                    WHERE data BETWEEN ? AND ?
                """, (data, data_fim))
            resultados = cursor.fetchall()
            conn.close()
            df_registro = pd.DataFrame(resultados, columns=['Data', 'Usuário', 'Ação', 'Maquina'])
            return df_registro
        except Exception as e:
            print(f"Ocorreu uma exceção fConsultarRegistro: {e}")



        pass
