import sys
import os

files_dir = os.path.join(os.path.dirname(__file__), "System")
sys.path.append(files_dir)

from app_ui import Ui_MainWindow
from app_func import AppBD
from app_img import img

from PyQt5.QtWidgets import QMainWindow, QDialog, QMessageBox, QApplication, QFileDialog, QAbstractItemView, QTableView, QButtonGroup, QVBoxLayout, QCalendarWidget, QDateTimeEdit, QPushButton
from PyQt5.QtCore import Qt, QAbstractTableModel, QDateTime
import getpass

import pandas as pd
import datetime
from unidecode import unidecode


class App1(QMainWindow, QDialog):
    def __init__(self):
        super(App1, self).__init__()
        self.gui = Ui_MainWindow()
        self.img = img()
        self.bd = AppBD()
        self.gui.setupUi(self)

        #Classe
        self.data_atual = datetime.datetime.now().date()
        self.data_futura = self.data_atual + datetime.timedelta(days=7)

        #OCULTAR
        self.gui.gridGroupBox_amostra.setVisible(False)
        self.gui.gridGroupBox_limpeza.setVisible(False)
        self.gui.gridGroupBox_injecoes.setVisible(False)
        self.gui.formGroupBox_testes.setVisible(False)
        self.gui.gridGroupBox_injecoes_2.setVisible(False)
        self.gui.gridGroupBox_linearidade.setVisible(False)

        #Agrupar botoes cadastro
        self.button_group = QButtonGroup()
        self.button_group.addButton(self.gui.radiodesenv, 1)
        self.button_group.addButton(self.gui.radiovalidacao, 2)
        self.button_group.addButton(self.gui.radioestab, 3)
        self.button_group.addButton(self.gui.radioinvestig, 4)
        self.button_group.buttonClicked[int].connect(self.on_radio_button_clicked) 
        self.gui.checkBox_setup.stateChanged.connect(self.on_checkbox_state_changed)
        self.gui.checkBox_linearidade.stateChanged.connect(self.on_checkbox_linearidade_changed)
        self.gui.checkBox_estab_sol.stateChanged.connect(self.on_checkbox_state_changed_estab)

        #iniciar
        self.comboBOX()
        self.calendarios()
        self.check_users()
        self.seticons()
        self.check_funcionamento()
        self.tabOrder()

        #calendario
        self.gui.calendarWidget.selectionChanged.connect(self.calendarDateChanged)
        self.calendarDateChanged()
        self.gui.tableView_agenda.setSelectionMode(QAbstractItemView.SingleSelection)

        # BOTOES
        self.gui.btn_agendar.clicked.connect(self.fAgendarBD)
        self.gui.btn_limpar.clicked.connect(self.limpar_variaveis)
        self.gui.btn_deletar_1.clicked.connect(self.fRemoverProjetoBD)        
        self.gui.btn_buscar1.clicked.connect(self.fSelecionarBDAgenda)
        self.gui.btn_iniciar_1.clicked.connect(self.fIniciarProjetoBD)
        self.gui.btn_buscar_exec.clicked.connect(self.fSelecionarBDEXEC)
        self.gui.btn_finalizar.clicked.connect(self.fFinalizarBD)
        self.gui.btn_buscar_manut.clicked.connect(self.fConsultaManutencao)
        self.gui.btn_manut.clicked.connect(self.fIniciarManutencao)
        self.gui.btn_parada.clicked.connect(self.fFinalizarManutencao)
        self.gui.btn_buscar_registro.clicked.connect(self.fConsultaRegistro)
        self.gui.btn_atualizar.clicked.connect(self.check_funcionamento)
                
    def tabOrder(self):
        #PAG1 - CADASTRAR 
        self.setTabOrder(self.gui.ln_id, self.gui.ln_produto)
        self.setTabOrder(self.gui.ln_produto, self.gui.ln_ativos)
        self.setTabOrder(self.gui.ln_ativos, self.gui.ln_lote)
        self.setTabOrder(self.gui.ln_lote, self.gui.ln_metodo)
        self.setTabOrder(self.gui.ln_metodo, self.gui.ln_coluna)
        self.setTabOrder(self.gui.ln_coluna, self.gui.comboBox_equip)
        self.setTabOrder(self.gui.comboBox_equip, self.gui.btn_limpar)
        self.setTabOrder(self.gui.btn_limpar, self.gui.ln_tempocorrida)
        self.setTabOrder(self.gui.ln_tempocorrida, self.gui.radiodesenv)
        self.setTabOrder(self.gui.radiodesenv, self.gui.btn_agendar)

        #PAG2 - AGENDA
        self.setTabOrder(self.gui.dateEdit_inicio, self.gui.dateEdit_fim)
        self.setTabOrder(self.gui.dateEdit_fim, self.gui.comboBox_equip_3)
        self.setTabOrder(self.gui.comboBox_equip_3, self.gui.btn_buscar1)
        self.setTabOrder(self.gui.btn_buscar1, self.gui.calendarWidget)
        self.setTabOrder(self.gui.calendarWidget, self.gui.btn_iniciar_1)
        self.setTabOrder(self.gui.btn_iniciar_1, self.gui.btn_limpar)
        
        #PAG3 - EXECUCAO
        self.setTabOrder(self.gui.dateEdit_inicio_exec, self.gui.dateEdit_fim_exec)
        self.setTabOrder(self.gui.dateEdit_fim_exec, self.gui.comboBox_equip_7)
        self.setTabOrder(self.gui.comboBox_equip_7, self.gui.btn_buscar_exec)
        self.setTabOrder(self.gui.btn_buscar_exec, self.gui.comboBox_equip_2)
        self.setTabOrder(self.gui.comboBox_equip_2, self.gui.ln_intervencao)
        self.setTabOrder(self.gui.ln_intervencao, self.gui.btn_finalizar)
        
        #PAG4 - MANUTENÇÃO
        self.setTabOrder(self.gui.comboBox_equip_4, self.gui.btn_manut)
        self.setTabOrder(self.gui.btn_manut, self.gui.btn_parada)
        self.setTabOrder(self.gui.btn_parada, self.gui.dateEdit_manut_ini)
        self.setTabOrder(self.gui.dateEdit_manut_ini, self.gui.dateEdit_manut_fim)
        self.setTabOrder(self.gui.dateEdit_manut_fim, self.gui.comboBox_equip_5)
        self.setTabOrder(self.gui.comboBox_equip_5, self.gui.btn_buscar_manut)

        #PAG5 -  REGISTRO
        self.setTabOrder(self.gui.dateEdit_registro_ini, self.gui.dateEdit_registro_fim)
        self.setTabOrder(self.gui.dateEdit_registro_fim, self.gui.ln_usuario)
        self.setTabOrder(self.gui.ln_usuario, self.gui.comboBox_equip_6)
        self.setTabOrder(self.gui.comboBox_equip_6, self.gui.btn_buscar_registro)

    def on_radio_button_clicked(self, button_id):
        if button_id == 1:
            self.gui.gridGroupBox_amostra.setVisible(False)
            self.gui.gridGroupBox_injecoes.setVisible(False)
            self.gui.gridGroupBox_limpeza.setVisible(True)
            self.gui.formGroupBox_testes.setVisible(True)

            self.gui.checkBox_setup.setChecked(False)
            self.gui.checkBox_seletividade.setChecked(False)
            self.gui.checkBox_exatidao.setChecked(False)
            self.gui.checkBox_precisao.setChecked(False)
            self.gui.checkBox_prec_int.setChecked(False)
            self.gui.checkBox_linearidade.setChecked(False)
            self.gui.checkBox_robustez.setChecked(False)
            self.gui.checkBox_estab_sol.setChecked(False)   

        elif button_id == 2:
            self.gui.gridGroupBox_amostra.setVisible(False)
            self.gui.gridGroupBox_injecoes.setVisible(False)
            self.gui.gridGroupBox_limpeza.setVisible(True)
            self.gui.formGroupBox_testes.setVisible(True)

            self.gui.checkBox_setup.setChecked(False)
            self.gui.checkBox_seletividade.setChecked(False)
            self.gui.checkBox_exatidao.setChecked(False)
            self.gui.checkBox_precisao.setChecked(False)
            self.gui.checkBox_prec_int.setChecked(False)
            self.gui.checkBox_linearidade.setChecked(False)
            self.gui.checkBox_robustez.setChecked(False)
            self.gui.checkBox_estab_sol.setChecked(False)   

        elif button_id == 3:
            self.gui.gridGroupBox_amostra.setVisible(True)
            self.gui.gridGroupBox_injecoes.setVisible(True)
            self.gui.gridGroupBox_limpeza.setVisible(True)
            self.gui.formGroupBox_testes.setVisible(False)

            self.gui.checkBox_setup.setChecked(False)
            self.gui.checkBox_seletividade.setChecked(False)
            self.gui.checkBox_exatidao.setChecked(False)
            self.gui.checkBox_precisao.setChecked(False)
            self.gui.checkBox_prec_int.setChecked(False)
            self.gui.checkBox_linearidade.setChecked(False)
            self.gui.checkBox_robustez.setChecked(False)
            self.gui.checkBox_estab_sol.setChecked(False)   

        elif button_id == 4:
            self.gui.gridGroupBox_amostra.setVisible(True)
            self.gui.gridGroupBox_injecoes.setVisible(True)
            self.gui.gridGroupBox_limpeza.setVisible(True)
            self.gui.formGroupBox_testes.setVisible(False)

            self.gui.checkBox_setup.setChecked(False)
            self.gui.checkBox_seletividade.setChecked(False)
            self.gui.checkBox_exatidao.setChecked(False)
            self.gui.checkBox_precisao.setChecked(False)
            self.gui.checkBox_prec_int.setChecked(False)
            self.gui.checkBox_linearidade.setChecked(False)
            self.gui.checkBox_robustez.setChecked(False)
            self.gui.checkBox_estab_sol.setChecked(False)   
        else:
            self.gui.gridGroupBox_amostra.setVisible(False)
            self.gui.gridGroupBox_injecoes.setVisible(False)
            self.gui.gridGroupBox_limpeza.setVisible(False)
            self.gui.formGroupBox_testes.setVisible(False)

            self.gui.checkBox_setup.setChecked(False)
            self.gui.checkBox_seletividade.setChecked(False)
            self.gui.checkBox_exatidao.setChecked(False)
            self.gui.checkBox_precisao.setChecked(False)
            self.gui.checkBox_prec_int.setChecked(False)
            self.gui.checkBox_linearidade.setChecked(False)
            self.gui.checkBox_robustez.setChecked(False)
            self.gui.checkBox_estab_sol.setChecked(False)   
   
    def on_checkbox_state_changed(self, state):
        if state == Qt.Checked:
            self.gui.gridGroupBox_injecoes.setVisible(True)
        else:
            self.gui.gridGroupBox_injecoes.setVisible(False)

    def on_checkbox_linearidade_changed(self, state):
        if state == Qt.Checked:
            self.gui.gridGroupBox_linearidade.setVisible(True)
        else:
            self.gui.gridGroupBox_linearidade.setVisible(False)

    def on_checkbox_state_changed_estab(self, state):
        if state == Qt.Checked:
            self.gui.gridGroupBox_injecoes_2.setVisible(True)
        else:
            self.gui.gridGroupBox_injecoes_2.setVisible(False)
        
    def comboBOX(self):
        #variaveis
        self.maquina = ""
        self.maquina_list = ["", "HPLC-0122", "HPLC-0123", "HPLC-0124", "HPLC-0125"]
        for maquina in self.maquina_list:
            self.gui.comboBox_equip.addItem(maquina)
            self.gui.comboBox_equip_2.addItem(maquina)
            self.gui.comboBox_equip_3.addItem(maquina)
            self.gui.comboBox_equip_4.addItem(maquina)
            self.gui.comboBox_equip_5.addItem(maquina)
            self.gui.comboBox_equip_6.addItem(maquina)
            self.gui.comboBox_equip_7.addItem(maquina)

    def calendarios(self):
        #DATAS cadastras
        self.gui.dateEdit_inicio.setDate(self.data_atual)
        self.gui.dateEdit_inicio.setCalendarPopup(True)
        self.gui.dateEdit_fim.setDate(self.data_futura)
        self.gui.dateEdit_fim.setCalendarPopup(True)
        #manutencao
        self.gui.dateEdit_manut_ini.setDate(self.data_atual)
        self.gui.dateEdit_manut_ini.setCalendarPopup(True)
        self.gui.dateEdit_manut_fim.setDate(self.data_futura)
        self.gui.dateEdit_manut_fim.setCalendarPopup(True)
        #registros
        self.gui.dateEdit_registro_ini.setDate(self.data_atual)
        self.gui.dateEdit_registro_ini.setCalendarPopup(True)
        self.gui.dateEdit_registro_fim.setDate(self.data_futura)
        self.gui.dateEdit_registro_fim.setCalendarPopup(True)
        #execução
        self.gui.dateEdit_inicio_exec.setDate(self.data_atual)
        self.gui.dateEdit_inicio_exec.setCalendarPopup(True)
        self.gui.dateEdit_fim_exec.setDate(self.data_futura)
        self.gui.dateEdit_fim_exec.setCalendarPopup(True)
        
    def check_users(self):
        self.usuario = getpass.getuser()
        usuarios_autorizados = ['diullio.santos', 'gabriela.teotonio', 'ds']
        # Verifique se o nome de usuário atual está na lista de usuários autorizados
        if self.usuario in usuarios_autorizados:
            self.gui.btn_deletar_1.setVisible(True)
            self.gui.tabWidget.setTabEnabled(5, True)
        else:
            self.gui.btn_deletar_1.setVisible(False)
            self.gui.tabWidget.setTabEnabled(5, False)

    def seticons(self):
        try:
            #logo      
            logo_brain = self.img.logo_brainfarma()
            logo_brain = self.img.pixmap_img(logo_brain)
            logo_brain = logo_brain.scaled(200, 60)
            self.gui.logo1.setPixmap(logo_brain)

            #imagens
            hplc = self.img.maquina1()
            hplc = self.img.pixmap_img(hplc)
            hplc = hplc.scaled(250, 250)
            self.gui.img_hplc.setPixmap(hplc)

            cg = self.img.maquina2()
            cg = self.img.pixmap_img(cg)
            cg = cg.scaled(250, 250)
            self.gui.img_cg.setPixmap(cg)

        except Exception as e:
            print(f"Ocorreu uma exceção: {e}")

    def agendar(self):
        dialog = DateTimeDialog()
        result = dialog.exec_()

        if result == QDialog.Accepted:
            selected_datetime = dialog.getSelectedDateTime()
            return selected_datetime

#--- FINALIZADO ---

# CADASTRAR PRODUTO
    def fLerCamposSearch(self):   
        try:
            ln_id = self.gui.ln_id.text()
            ln_produto = self.gui.ln_produto.text()
            ln_produto = self.remover_acentos(ln_produto)
            ln_ativos = self.gui.ln_ativos.text()
            if ln_ativos:
                ln_ativos = int(ln_ativos)
            ln_lote = self.gui.ln_lote.text()
            ln_lote = ln_lote.upper()
            ln_metodo = self.gui.ln_metodo.text()
            ln_coluna = self.gui.ln_coluna.text()
            ln_maquina = self.gui.comboBox_equip.currentText()

            ln_tempocorrida = self.gui.ln_tempocorrida.text()
            if ln_tempocorrida:
                ln_tempocorrida = int(ln_tempocorrida)

            id_radio = self.button_group.checkedId()
            if id_radio == 1:
                self.radio = "Desenvolvimento"
            elif id_radio == 2:
                self.radio = "Validação"
            elif id_radio == 3:
                self.radio = "Estabilidade"
            elif id_radio == 4:
                self.radio = "Investigação"
            else:
                self.radio = None

            ln_num_amostras = self.gui.ln_num_amostras.text()
            if ln_num_amostras:
                ln_num_amostras = int(ln_num_amostras)
            ln_injecoes = self.gui.ln_injecoes.text()
            if ln_injecoes:
                ln_injecoes = int(ln_injecoes)
            ln_injecoes_2 = self.gui.ln_injecoes_2.text()
            if ln_injecoes_2:
                ln_injecoes_2 = int(ln_injecoes_2)
            ln_tempo_limpeza = self.gui.ln_tempo_limpeza.text()
            if ln_tempo_limpeza:
                ln_tempo_limpeza = int(ln_tempo_limpeza)
            ln_linearidade_pontos = self.gui.ln_linearidade_pontos.text()
            if ln_linearidade_pontos:
                ln_linearidade_pontos = int(ln_linearidade_pontos)
            

            checkBox_setup = lambda x: True if x == 2 else False
            checkBox_setup = checkBox_setup(self.gui.checkBox_setup.checkState())
            checkBox_seletividade = lambda x: True if x == 2 else False
            checkBox_seletividade = checkBox_seletividade(self.gui.checkBox_seletividade.checkState())
            checkBox_exatidao = lambda x: True if x == 2 else False
            checkBox_exatidao = checkBox_exatidao(self.gui.checkBox_exatidao.checkState())
            checkBox_precisao = lambda x: True if x == 2 else False
            checkBox_precisao = checkBox_precisao(self.gui.checkBox_precisao.checkState())
            checkBox_prec_int = lambda x: True if x == 2 else False
            checkBox_prec_int = checkBox_prec_int(self.gui.checkBox_prec_int.checkState())
            checkBox_linearidade = lambda x: True if x == 2 else False
            checkBox_linearidade = checkBox_linearidade(self.gui.checkBox_linearidade.checkState())
            checkBox_robustez = lambda x: True if x == 2 else False
            checkBox_robustez = checkBox_robustez(self.gui.checkBox_robustez.checkState())
            checkBox_estab_sol = lambda x: True if x == 2 else False
            checkBox_estab_sol = checkBox_estab_sol(self.gui.checkBox_estab_sol.checkState())

            return ln_id, ln_produto, ln_ativos, ln_lote, ln_metodo, ln_coluna, ln_maquina, ln_tempocorrida, id_radio, ln_num_amostras, ln_injecoes, ln_injecoes_2, ln_tempo_limpeza, checkBox_setup, checkBox_seletividade, checkBox_exatidao, checkBox_precisao, checkBox_prec_int, checkBox_linearidade, checkBox_robustez, checkBox_estab_sol, ln_linearidade_pontos

        except Exception as e:
            print(f"Ocorreu uma exceção fLerCamposSearch: {e}") 

    def limpar_variaveis(self):
        try:
            self.gui.ln_id.setText('')
            self.gui.ln_produto.setText('')
            self.gui.ln_ativos.setText('')
            self.gui.ln_lote.setText('')
            self.gui.ln_metodo.setText('')
            self.gui.ln_coluna.setText('')
            self.gui.comboBox_equip.setCurrentIndex(0)
            self.gui.ln_tempocorrida.setText('')

            self.button_group.setExclusive(False)
            self.button_group.button(1).setChecked(False)
            self.button_group.button(2).setChecked(False)
            self.button_group.button(3).setChecked(False)
            self.button_group.button(4).setChecked(False)
            self.button_group.setExclusive(True)
            self.on_radio_button_clicked(0)

            self.gui.ln_num_amostras.setText('')
            self.gui.ln_injecoes.setText('')
            self.gui.ln_injecoes_2.setText('')
            self.gui.ln_tempo_limpeza.setText('')
            self.gui.ln_linearidade_pontos.setText('')

            self.gui.checkBox_setup.setChecked(False)
            self.gui.checkBox_seletividade.setChecked(False)
            self.gui.checkBox_exatidao.setChecked(False)
            self.gui.checkBox_precisao.setChecked(False)
            self.gui.checkBox_prec_int.setChecked(False)
            self.gui.checkBox_linearidade.setChecked(False)
            self.gui.checkBox_robustez.setChecked(False)
            self.gui.checkBox_estab_sol.setChecked(False)        

        except Exception as e:
            print(f"Ocorreu uma exceção: {e}") 

    def tratar_Dados(self):
        try:
            ln_id, ln_produto, ln_ativos, ln_lote, ln_metodo, ln_coluna, ln_maquina, ln_tempocorrida, id_radio, ln_num_amostras, ln_injecoes, ln_injecoes_2, ln_tempo_limpeza, checkBox_setup, checkBox_seletividade, checkBox_exatidao, checkBox_precisao, checkBox_prec_int, checkBox_linearidade, checkBox_robustez, checkBox_estab_sol, ln_linearidade_pontos = self.fLerCamposSearch()

            variaveis = [ln_id, ln_produto, ln_ativos, ln_lote, ln_metodo, ln_coluna, ln_maquina, ln_tempocorrida, id_radio, ln_tempo_limpeza, checkBox_setup, checkBox_seletividade, checkBox_exatidao, checkBox_precisao, checkBox_prec_int, checkBox_linearidade, checkBox_robustez, checkBox_estab_sol]

            todas_existem = all(var is not None and var != '' for var in variaveis)

            if todas_existem:

                testes = []
                self.injecoes = 0

                if id_radio == 1 or id_radio == 2:
                    if checkBox_setup and ln_injecoes:
                        self.injecoes += int(ln_injecoes)
                        testes.append("Setup")
                    if checkBox_seletividade and ln_ativos:
                        self.injecoes += 2
                        self.injecoes += int(ln_ativos)
                        testes.append("Seletividade")
                    if checkBox_exatidao:
                        self.injecoes += 9
                        testes.append("Exatidão")
                    if checkBox_precisao:
                        self.injecoes += 6
                        testes.append("Precisão")
                    if checkBox_prec_int:
                        self.injecoes += 6
                        testes.append("Precisão Intermediária")
                    if checkBox_linearidade and ln_linearidade_pontos:
                        self.injecoes += (3* int(ln_linearidade_pontos))
                        testes.append("Linearidade")
                    if checkBox_robustez:
                        self.injecoes += 30
                        testes.append("Robustez")
                    if checkBox_estab_sol and ln_injecoes_2:
                        self.injecoes += int(ln_injecoes_2)
                        testes.append("Estabilidade Solução")
                elif id_radio == 3:
                    if ln_num_amostras and ln_injecoes:
                        inj_estab = ln_num_amostras * ln_injecoes
                        self.injecoes += inj_estab
                        testes.append("Estabilidade")    
                elif id_radio == 4:
                    if ln_num_amostras and ln_injecoes:
                        inj_estab = int(ln_num_amostras) * int(ln_injecoes)
                        self.injecoes += inj_estab
                        testes.append("Investigação")
                else:
                    print("Sem radio selecionado")

                if ln_tempocorrida and self.injecoes and ln_tempo_limpeza: 
                    tempo_total = (int(ln_tempocorrida) * int(self.injecoes)) + int(ln_tempo_limpeza)
                    tempo_total = int(tempo_total)
                else:
                    print("Falha ao calcular tempo total")
                tipo = str(self.radio)
                teste = ', '.join(testes)

                return ln_id, ln_produto, ln_ativos, ln_lote, ln_metodo, ln_coluna, ln_maquina, ln_tempocorrida, ln_tempo_limpeza, tempo_total, tipo, teste, ln_num_amostras, self.injecoes
            
            else:
                QMessageBox.information(None, "Alerta", "Dados ausentes! Conferir as informações acima", QMessageBox.Ok)
                pass
            
        except Exception as e:
            print(f"Ocorreu uma exceção no tratar_Dados: {e}") 

    def fAgendarBD(self):
        try:
            retorno_tratar_dados = self.tratar_Dados()

            if retorno_tratar_dados is not None:

                ln_id, ln_produto, ln_ativos, ln_lote, ln_metodo, ln_coluna, ln_maquina, ln_tempocorrida, ln_tempo_limpeza, tempo_total, tipo, teste, numero_amostras, numero_injecoes = self.tratar_Dados()
        
                variaveis = [ln_id, ln_produto, ln_ativos, ln_lote, ln_metodo, ln_coluna, ln_maquina, ln_tempocorrida, ln_tempo_limpeza]

                todas_existem = all(var is not None and var != '' for var in variaveis)

                if todas_existem:
                    data_inicio = self.agendar()

                    self.bd.fAgendarDados(ln_id, data_inicio, ln_produto, ln_ativos, ln_lote, ln_metodo, ln_coluna, ln_maquina, ln_tempocorrida, ln_tempo_limpeza, tempo_total, tipo, teste, numero_amostras, numero_injecoes)

                    self.limpar_variaveis()

                    self.calendarDateChanged()
            else:
                pass
        except Exception as e:
            print(f"Ocorreu uma exceção fAgendarBD: {e}") 

## AGENDA
    def calendarDateChanged(self):
        try:
            dateSelected = self.gui.calendarWidget.selectedDate().toPyDate()
            self.updateTaskList(dateSelected)
        except Exception as e:
            print(f"Ocorreu uma exceção calendarDateChanged: {e}") 

    def updateTaskList(self, dateSelected):
        try:
            df = self.bd.fSelecionarDadosCurrent(dateSelected)
            df= df.drop(['Id'], axis=1)
            model = PandasModel(df)
            self.gui.tableView_agenda.setModel(model)
            self.gui.tableView_agenda.resizeColumnsToContents()
        except Exception as e:
            print(f"Ocorreu uma exceção updateTaskList: {e}") 

    def fSelecionarBDAgenda(self):
        try:
            data_inicio = self.gui.dateEdit_inicio.date().toString("yyyy-MM-dd")
            data_fim = self.gui.dateEdit_fim.date().toString("yyyy-MM-dd")
            maquina = self.gui.comboBox_equip_3.currentText()

            df = self.bd.fSelecionarDados(data_inicio, data_fim, maquina)

            df['Data Início'] = pd.to_datetime(df['Data Início'], format='%Y-%m-%d %H:%M:%S')
            df['Data Início'] = df['Data Início'].dt.strftime('%d/%m/%Y %H:%M')
            df['Data Prevista'] = pd.to_datetime(df['Data Prevista'], format='%Y-%m-%d %H:%M:%S')
            df['Data Prevista'] = df['Data Prevista'].dt.strftime('%d/%m/%Y %H:%M')

            df = df.drop('Id', axis=1)

            model = PandasModel(df)
            self.gui.tableView_agenda.setModel(model)
            self.gui.tableView_agenda.resizeColumnsToContents()
        except Exception as e:
            print(f"Ocorreu uma exceção fSelecionarBDAgenda: {e}") 

    def fIniciarProjetoBD(self):
        try:
            selected_indexes = self.gui.tableView_agenda.selectionModel().selectedIndexes()
            if selected_indexes:
                self.bd.fIniciarProjeto(selected_indexes)
                self.check_funcionamento()
            else:
                message = f"Selecione um projeto"
                QMessageBox.information(None, "Alerta", message, QMessageBox.Ok)
        
        except Exception as e:
            print(f"Ocorreu uma exceção fIniciarProjetoBD: {e}") 

    def fRemoverProjetoBD(self):
        try:
            selected_indexes = self.gui.tableView_agenda.selectionModel().selectedIndexes()

            if selected_indexes:
                # Crie um QMessageBox de confirmação
                confirm_dialog = QMessageBox()
                confirm_dialog.setIcon(QMessageBox.Question)
                confirm_dialog.setWindowTitle("Confirmação")
                confirm_dialog.setText(f"Você tem certeza de que deseja remover o agendamento?")
                confirm_dialog.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

                response = confirm_dialog.exec_()

                if response == QMessageBox.Yes:
                    produto = self.bd.fRemoverProjeto(selected_indexes)
                    if produto:
                        message = f"Produto {produto} removido com sucesso"
                        QMessageBox.information(None, "Confirmação", message, QMessageBox.Ok)
                        self.calendarDateChanged()
                else:
                    pass
            else:
                message = f"Selecione um projeto"
                QMessageBox.information(None, "Alerta", message, QMessageBox.Ok)

        except Exception as e:
            print(f"Ocorreu uma exceção fRemoverProjetoBD: {e}") 

## EXECUTAR
    def fSelecionarBDEXEC(self):
        try:
            data_inicio = self.gui.dateEdit_inicio_exec.date().toString("yyyy-MM-dd")
            data_fim = self.gui.dateEdit_fim_exec.date().toString("yyyy-MM-dd")
            maquina = self.gui.comboBox_equip_7.currentText()

            df = self.bd.fSelecionarDadosExec(data_inicio, data_fim, maquina)

            df['Data Início'] = pd.to_datetime(df['Data Início'], format='%Y-%m-%d %H:%M')
            df['Data Início'] = df['Data Início'].dt.strftime('%d/%m/%Y %H:%M')
            df['Data Prevista'] = pd.to_datetime(df['Data Prevista'], format='%Y-%m-%d %H:%M')
            df['Data Prevista'] = df['Data Prevista'].dt.strftime('%d/%m/%Y %H:%M')

            mask = df['Data Fim'].notnull()
            if mask.any():
                df['Data Fim'] = pd.to_datetime(df['Data Fim'], format='%Y-%m-%d %H:%M:%S')
                df['Data Fim'] = df['Data Fim'].dt.strftime('%d/%m/%Y %H:%M')

            df = df.drop(['Id'], axis=1)

            model = PandasModel(df)
            self.gui.tableView_execucao.setModel(model)
            self.gui.tableView_execucao.resizeColumnsToContents()
        except Exception as e:
            print(f"Ocorreu uma exceção fSelecionarBDEXEC: {e}")

    def fLerFinalizado(self):
        try:
            maquina = self.gui.comboBox_equip_2.currentText()
            intervencao = self.gui.ln_intervencao.text()
            intervencao = self.remover_acentos(intervencao)

            return maquina, intervencao
        except Exception as e:
            print(f"Ocorreu uma exceção: {e}") 

    def fLimparFinalizado(self):
        try:
            self.gui.comboBox_equip_2.setCurrentIndex(0)
            self.gui.ln_intervencao.clear()
        except Exception as e:
            print(f"Ocorreu uma exceção: {e}") 

    def fFinalizarBD(self):
        try:
            maquina, intervencao = self.fLerFinalizado()
            if maquina:
                self.bd.fFinalizarDados(maquina,intervencao)
                self.fLimparFinalizado()
                self.check_funcionamento()
                self.fSelecionarBDEXEC()
            else:
                QMessageBox.information(None, "Alerta", "Selecione um equipamento a ser finalizado!", QMessageBox.Ok)
        except Exception as e:
            print(f"Ocorreu uma exceção: {e}") 

## FUNCIONAMENTO

    def check_funcionamento(self):
        try:
            verde = "background-color: rgb(0, 255, 0);"
            vermelho = "background-color: rgb(255, 0, 0);"
            amarelo = "background-color: rgb(255, 255, 0);"
            maquina = ['HPLC-0122', 'HPLC-0123', 'HPLC-0124', 'HPLC-0125']
                 
            for item in maquina:
                produto = self.bd.fCheckFuncionamento(item)
                id = self.bd.fCheckManutencao(item)
                if item == "HPLC-0122":
                    if id is not None:
                        exec(f"self.gui.txt_hplc0122.setText('Manutenção')")
                        exec(f"self.gui.hplc0122.setStyleSheet('{amarelo}')")
                    elif produto is not None:
                        exec(f"self.gui.txt_hplc0122.setText('{produto}')")
                        exec(f"self.gui.hplc0122.setStyleSheet('{verde}')")
                    else:
                        exec(f"self.gui.txt_hplc0122.setText('')")
                        exec(f"self.gui.hplc0122.setStyleSheet('{vermelho}')")

                if item == "HPLC-0123":
                    if id is not None:
                        exec(f"self.gui.txt_hplc0123.setText('Manutenção')")
                        exec(f"self.gui.hplc0123.setStyleSheet('{amarelo}')")
                    elif produto is not None:
                        exec(f"self.gui.txt_hplc0123.setText('{produto}')")
                        exec(f"self.gui.hplc0123.setStyleSheet('{verde}')")
                    else:
                        exec(f"self.gui.txt_hplc0123.setText('')")
                        exec(f"self.gui.hplc0123.setStyleSheet('{vermelho}')")

                if item == "HPLC-0124":
                    if id is not None:
                        exec(f"self.gui.txt_hplc0124.setText('Manutenção')")
                        exec(f"self.gui.hplc0124.setStyleSheet('{amarelo}')")
                    elif produto is not None:
                        exec(f"self.gui.txt_hplc0124.setText('{produto}')")
                        exec(f"self.gui.hplc0124.setStyleSheet('{verde}')")
                    else:
                        exec(f"self.gui.txt_hplc0124.setText('')")
                        exec(f"self.gui.hplc0124.setStyleSheet('{vermelho}')")
                    
                if item == "HPLC-0125":
                    if id is not None:
                        exec(f"self.gui.txt_hplc0125.setText('Manutenção')")
                        exec(f"self.gui.hplc0125.setStyleSheet('{amarelo}')")
                    elif produto is not None:
                        exec(f"self.gui.txt_hplc0125.setText('{produto}')")
                        exec(f"self.gui.hplc0125.setStyleSheet('{verde}')")
                    else:
                        exec(f"self.gui.txt_hplc0125.setText('')")
                        exec(f"self.gui.hplc0125.setStyleSheet('{vermelho}')")

        except Exception as e:
            print(f"Ocorreu uma exceção: {e}") 

## MANUTENÇÃO

    def fIniciarManutencao(self):
        try:
            maquina = self.gui.comboBox_equip_4.currentText()
            if maquina:
                self.bd.StartManutencao(maquina)
                self.fConsultaManutencao()
                self.check_funcionamento()
            else:
                QMessageBox.information(None, "Alerta", "Selecione um equipamento!", QMessageBox.Ok)
            
        except Exception as e:
            print(f"Ocorreu uma exceção fIniciarManutencao: {e}") 

    def fFinalizarManutencao(self):
        try:
            maquina = self.gui.comboBox_equip_4.currentText()
            if maquina:
                self.bd.FinalizarManutencao(maquina)
                self.fConsultaManutencao()
                self.check_funcionamento()
            else:
                QMessageBox.information(None, "Alerta", "Selecione um equipamento!", QMessageBox.Ok)
        except Exception as e:
            print(f"Ocorreu uma exceção fFinalizarManutencao: {e}") 

    def fConsultaManutencao(self):
        try:
            data_inicio = self.gui.dateEdit_manut_ini.date().toString("yyyy-MM-dd")
            data_fim = self.gui.dateEdit_manut_fim.date().toString("yyyy-MM-dd")
            maquina = self.gui.comboBox_equip_5.currentText()

            df = self.bd.fSelecionarDadosManutencao(data_inicio, data_fim, maquina)

            df['Data Início'] = pd.to_datetime(df['Data Início'], format='%Y-%m-%d %H:%M:%S')
            df['Data Início'] = df['Data Início'].dt.strftime('%d/%m/%Y %H:%M')
            mask = df['Data Fim'].notnull()
            if mask.any():
                df['Data Fim'] = pd.to_datetime(df['Data Fim'], format='%Y-%m-%d %H:%M:%S')
                df['Data Fim'] = df['Data Fim'].dt.strftime('%d/%m/%Y %H:%M')

            df = df.drop(['Id'], axis=1)
            model = PandasModel(df)
            self.gui.tableView_parada.setModel(model)
            self.gui.tableView_parada.resizeColumnsToContents()
        except Exception as e:
            print(f"Ocorreu uma exceção fSelecionarManutencao: {e}")

## REGISTRO

    def fConsultaRegistro(self):
        try:
            data_inicio = self.gui.dateEdit_registro_ini.date().toString("yyyy-MM-dd")
            data_fim = self.gui.dateEdit_registro_fim.date().toString("yyyy-MM-dd")
            usuario = self.gui.ln_usuario.text()
            maquina = self.gui.comboBox_equip_6.currentText()    

            df = self.bd.fConsultarRegistro(data_inicio, data_fim, usuario, maquina)

            df['Data'] = pd.to_datetime(df['Data'], format='%Y-%m-%d %H:%M')
            df['Data'] = df['Data'].dt.strftime('%d/%m/%Y %H:%M')

            model = PandasModel(df)
            self.gui.tableView_registros.setModel(model)
            self.gui.tableView_registros.resizeColumnsToContents()

        except Exception as e:
            print(f"Ocorreu uma exceção fConsultaRegistro: {e}")

#MENSAGENS
    def fMessageSucess(self):
        # Criar a mensagem de sucesso
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("Ação realizada com sucesso!")
        msg.setWindowTitle("Confirmação")
        msg.setStandardButtons(QMessageBox.Ok)
        # Exibir a mensagem de sucesso
        msg.exec_()

    def remover_acentos(self, texto):
        texto_sem_acentos = unidecode(texto)
        texto_sem_acentos = texto_sem_acentos.lower()
        texto_sem_acentos = texto_sem_acentos.capitalize()
        return texto_sem_acentos

## FECHAR PROGRAMA
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Fechar programa', 'Você realmente deseja fechar essa aplicação?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            event.accept()        
        else:
            event.ignore()

class PandasModel(QAbstractTableModel):
    """
    Class to populate a table view with a pandas dataframe
    """
    def __init__(self, data, parent=None):
        QAbstractTableModel.__init__(self, parent)
        self._data = data

    def rowCount(self, parent=None):
        return self._data.shape[0]

    def columnCount(self, parent=None):
        return self._data.shape[1]

    def data(self, index, role=Qt.DisplayRole):
        if index.isValid():
            if role == Qt.DisplayRole:
                return str(self._data.iloc[index.row(), index.column()])
        return None

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._data.columns[col]
        return None

class DateTimeDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        # Crie um QCalendarWidget para a data
        self.calendar = QCalendarWidget(self)
        layout.addWidget(self.calendar)

        # Crie um QDateTimeEdit para a hora
        self.time_edit = QDateTimeEdit(self)
        self.time_edit.setDisplayFormat("HH:mm")
        layout.addWidget(self.time_edit)

        # Crie um botão "Agendar"
        agendar_button = QPushButton("Agendar", self)
        layout.addWidget(agendar_button)

        # Conecte o botão "Agendar" a uma função que fecha o diálogo
        agendar_button.clicked.connect(self.accept)

        self.setLayout(layout)
        self.setWindowTitle("Selecionar Data e Hora")

    def getSelectedDateTime(self):
        date = self.calendar.selectedDate()
        time = self.time_edit.time()
        qdate_time = QDateTime(date, time)
        formatted_date_time = qdate_time.toString("dd/MM/yyyy HH:mm")
        return formatted_date_time
    
if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    
    gui = App1()
    gui.show()
    sys.exit(app.exec())
        