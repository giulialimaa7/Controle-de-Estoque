from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox, QTableWidgetItem, QToolButton, QMainWindow, QLabel
from reportlab.pdfgen import canvas
from reportlab.platypus import Paragraph
from pdf2image import convert_from_path
import sys
import base
import base2
import pandas as pd
import pymysql
import funcoes as f
import os
import cv2
     
class Janela2(QtWidgets.QMainWindow, base2.Ui_SegundaJanela):
    def __init__(self, parent=None):
        super(Janela2, self).__init__(parent)
        self.setupUi(self)
        
        #BOTÕES
        self.btn_buscar_nome.clicked.connect(self.buscar_nome)
        self.btn_limpar_nome.clicked.connect(self.limpar_nome)

    def buscar_nome(self): 
        filtro = self.txt_nome_buscar.text()
        
        try:
            if ( filtro == '' or filtro == None ):
                msg = QMessageBox()
                msg.setWindowTitle("AVISO")
                msg.setText("Campo vazio!")
                msg.setInformativeText("Por favor, preencha o campo de busca")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()  
                
            else:
                conn = pymysql.connect(host='nome-do-banco',port=0000, user='usuario'  ,password='00000000', db='nomde-da-tabela')
        
                query = f"""select t2.name, t1.patrimonio, t1.tipo_item, t1.posto_trabalho, t1.descricao, t1.uf, t1.modelo, t1.marca, t1.n_modelo, t1.processador, t1.n_serie, 
                t1.email, t1.memoria, t1.status, t1.condicoes, t1.ssd_hdd
                from nome-do-banco.nome-da-tabela as t1 left join nome-do-banco.nome-da-tabela as t2 on t1.id_usuario = t2.id where name like '%{ filtro }%' """
                  
                tabela = pd.read_sql(query, conn)
                
                if ( tabela.empty == True):
                    msg = QMessageBox()
                    msg.setWindowTitle('AVISO')
                    msg.setText("Usuário não encontrado!")
                    msg.setIcon(QMessageBox.Critical)
                    msg.exec_()
                    
                else:
                    linha = 0
                    for linha_indice in ( tabela.index ):
                        coluna = 0
                        
                        for item in tabela:  
                            self.x = tabela.iloc[ linha,coluna ] 
                            self.tabela_pc.setItem( linha, coluna, QTableWidgetItem( str( self.x ) ) )
                            coluna = coluna +1
                            
                        linha = linha + 1
                 
        except Exception as erro:
            print(erro)
            
    def limpar_nome(self):
        self.txt_nome_buscar.clear()

class Janela(QtWidgets.QMainWindow, base.Ui_PrimeiraJanela):
    def __init__(self, parent=None):
        super(Janela, self).__init__(parent)
        self.setupUi(self)
        
        self.janela2 = Janela2()
        
        #BOTÕES
        self.btn_buscar_detalhes.clicked.connect(self.detalhes_pc)
        self.btn_cadastrar.clicked.connect(self.cadastrar_pc)
        self.btn_alterar.clicked.connect(self.alterar_pc)
        self.btn_apagar.clicked.connect(self.deletar_pc)
        self.btn_limpar_detalhes.clicked.connect(self.limpar_pc)
        
        self.btn_preview .clicked.connect(self.gerar_pdf)
        
        self.btn_buscar_detalhes_2.clicked.connect(self.detalhes_equipamentos)
        self.btn_cadastrar_2.clicked.connect(self.cadastrar_equipamentos)
        self.btn_alterar_2.clicked.connect(self.alterar_equipamentos)
        self.btn_apagar_2.clicked.connect(self.deletar_equipamentos)
        self.btn_limpar_detalhes_2.clicked.connect(self.limpar_equipamentos)
        self.btn_carregar.clicked.connect(self.mostrar_equipamentos)
        
        self.btn_buscar_por_nome.clicked.connect(self.abrir_janela_buscar_nome)
        
        self.btn_buscar_detalhes_3.clicked.connect(self.detalhes_estoque)
        self.btn_cadastrar_3.clicked.connect(self.cadastrar_estoque)
        self.btn_alterar_3.clicked.connect(self.alterar_estoque)
        self.btn_apagar_3.clicked.connect(self.deletar_estoque)
        self.btn_limpar_detalhes_3.clicked.connect(self.limpar_estoque)
        self.btn_carregar_3.clicked.connect(self.mostrar_estoque)
        
        
#PAGE PC    
    def detalhes_pc(self): 
        conn = pymysql.connect(host='nome-do-banco',port=0000, user='usuario'  ,password='00000000', db='nomde-da-tabela')
        cur = conn.cursor()
    
        try:
            patrimonio_ver = self.txt_patrimonio.text()
            
            if patrimonio_ver == '' or patrimonio_ver == None:
                
                msg = QMessageBox()
                msg.setWindowTitle('AVISO')
                msg.setText('Campo vazio!')
                msg.setInformativeText('Por favor, preencha o campo de busca')
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
                
            else:
                filtro = int( self.txt_patrimonio.text() )
                
                query = f"select * from nome-da-tabela where patrimonio = { filtro }"
                tabela = pd.read_sql(query, conn)
            
                if tabela.empty == False:
            
                    tipo_item = list( tabela[ 'tipo_item' ] )[0]
                    posto_trabalho = list( tabela[ 'posto_trabalho' ] )[0]
                    descricao = list( tabela[ 'descricao' ] )[0]
                    
                    uf = list( tabela[ 'uf' ] )[0]
                    if list( tabela[ 'uf' ] )[0] == 'RJ':
                        indexUf = 0
                    if list( tabela[ 'uf' ] )[0] == 'RJ - NITEROI':
                        indexUf = 1
                    if list( tabela[ 'uf' ] )[0] == 'SP':
                        indexUf = 2    
                    if list( tabela[ 'uf' ] )[0] == 'GO':
                        indexUf = 3
                    if list( tabela[ 'uf' ] )[0] == 'AC':
                        indexUf = 4
                    if list( tabela[ 'uf' ] )[0] == 'RO':
                        indexUf = 5
                    if list( tabela[ 'uf' ] )[0] == 'MG':
                        indexUf = 6
                    if list( tabela[ 'uf' ] )[0] == 'CE':
                        indexUf = 7
                    if list( tabela[ 'uf' ] )[0] == 'PE':
                        indexUf = 8
                           
                    id_usuario = list( tabela[ 'id_usuario' ] )[0]
                
                    setor = list( tabela['setor'] )[0]
                    if list( tabela[ 'setor' ] )[0] == 'Analise de Projetos':
                        indexSetor =  0 
                    if list( tabela[ 'setor' ] )[0] == 'Projetos AT':
                        indexSetor =  1 
                    if list( tabela[ 'setor' ] )[0] == 'Projetos MT - BT':
                        indexSetor =  2 
                    if list( tabela[ 'setor' ] )[0] == 'Fiscalização':
                        indexSetor =  3 
                    if list( tabela[ 'setor' ] )[0] == 'Financeiro':
                        indexSetor =  4 
                    if list( tabela[ 'setor' ] )[0] == 'Recursos Humanos':
                        indexSetor =  5 
                    if list( tabela[ 'setor' ] )[0] == 'COM':
                        indexSetor =  6 
                    if list( tabela[ 'setor' ] )[0] == 'Segurança do Trabalho':
                        indexSetor =  7 
                    if list( tabela[ 'setor' ] )[0] == 'Administrativo':
                        indexSetor =  8 
                    if list( tabela[ 'setor' ] )[0] == 'T.I':
                        indexSetor =  9 
                    
                    modelo = list( tabela [ 'modelo' ] )[0]
                    marca = list( tabela [ 'marca' ] )[0]
                    n_modelo = list( tabela [ 'n_modelo' ] )[0]
                    processador = list( tabela [ 'processador' ] )[0]
                    n_serie = list( tabela [ 'n_serie' ] )[0]
                    email = list( tabela [ 'email' ] )[0]
                    memoria = list( tabela [ 'memoria' ] )[0]
                    
                    status = list( tabela [ 'status' ] )[0]
                    if list( tabela [ 'status' ] )[0] == 'Ativo':
                        indexStatus = 0
                    if list( tabela [ 'status' ] )[0] == 'Inativo':
                        indexStatus = 1
                        
                    condicoes = list( tabela [ 'condicoes' ] )[0]
                    
                    alugado = list( tabela [ 'alugado' ] )[0]
                    if list( tabela [ 'alugado' ] )[0] == 'Sim':
                        indexAlugado = 0
                    if list( tabela [ 'alugado' ] )[0] == 'Não':
                        indexAlugado = 1
                        
                    ssd_hdd = list( tabela[ 'ssd_hdd' ] )[0]
                    if list( tabela[ 'ssd_hdd' ] )[0] == 'SSD':
                        indexSSD = 0
                    if list( tabela[ 'ssd_hdd' ] )[0] == 'HDD':
                        indexSSD = 1
                    if list( tabela[ 'ssd_hdd' ] )[0] == 'Ambos':
                        indexSSD = 2
                    
                    windows = list( tabela[ 'windows' ] )[0]
                    anydesk = list( tabela[ 'anydesk' ] )[0]
                    
                    officie = list( tabela[ 'officie' ] )[0]
                    if list( tabela[ 'officie' ] )[0] == 'Sim':
                        indexOfficie = 0
                    if list( tabela[ 'officie' ] )[0] == 'Não':
                        indexOfficie = 1
                        
                    tipo_officie = list( tabela[ 'tipo_officie' ] )[0]
                    if list( tabela[ 'tipo_officie' ] )[0] == '365':
                        indexTipoOfficie = 0
                    if list( tabela[ 'tipo_officie' ] )[0] == 'Home & Business':
                        indexTipoOfficie = 1
                    if list( tabela[ 'tipo_officie' ] )[0] == 'Standard':
                        indexTipoOfficie = 2
                    
                    conta = list( tabela[ 'conta' ] )[0]        
                    chave = list( tabela[ 'chave' ] )[0]
                    licenca = list( tabela[ 'licenca' ] )[0] 
                    
                    self.txt_tipo_item.setText( tipo_item )
                    self.txt_posto_trabalho.setText( posto_trabalho )
                    self.txt_descricao.setText( descricao )
                    self.ddl_uf.setCurrentIndex( indexUf )
                    self.txt_id_usuario.setText( id_usuario )
                    self.ddl_setor.setCurrentIndex( indexSetor )
                    self.txt_modelo.setText( modelo )
                    self.txt_marca.setText( marca )
                    self.txt_n_modelo.setText( n_modelo )
                    self.txt_processador.setText( processador )
                    self.txt_n_serie.setText( n_serie )
                    self.txt_email.setText( email )
                    self.txt_memoria.setText( memoria )
                    self.ddl_status.setCurrentIndex( indexStatus )                  
                    self.txt_condicoes.setText( condicoes )
                    self.ddl_alugado.setCurrentIndex( indexAlugado )
                    self.ddl_ssd_hdd.setCurrentIndex( indexSSD )
                    self.txt_windows.setText( windows )
                    self.txt_anydesk.setText( anydesk )
                    self.ddl_officie.setCurrentIndex( indexOfficie )
                    self.ddl_tipo_officie.setCurrentIndex( indexTipoOfficie )
                    self.txt_conta.setText( conta )
                    self.txt_chave.setText( chave )
                    self.txt_licenca.setText( licenca )
                    
                else:
                    msg = QMessageBox()
                    msg.setWindowTitle("AVISO")
                    msg.setText("Patrimonio não encontrado!")
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()
                
        except Exception as error:
            print(error)
       
    def cadastrar_pc(self):        
        campos = { 'patrimonio': self.txt_patrimonio.text(), 'tipo_item':self.txt_tipo_item.text(), 'posto_trabalho':self.txt_posto_trabalho.text(), 'descricao':self.txt_descricao.text(), 
                 'uf':self.ddl_uf.currentText(),'id_usuario':self.txt_id_usuario.text(), 'setor':self.ddl_setor.currentText(), 'modelo':self.txt_modelo.text(), 'marca':self.txt_marca.text(), 
                 'n_modelo':self.txt_n_modelo.text(), 'processador':self.txt_processador.text(), 'n_serie':self.txt_n_serie.text(), 'email':self.txt_email.text(), 
                 'memoria':self.txt_memoria.text(), 'status':self.ddl_status.currentText(), 'condicoes':self.txt_condicoes.text(), 'alugado':self.ddl_alugado.currentText(), 
                 'ssd_hdd':self.ddl_ssd_hdd.currentText(), 'windows':self.txt_windows.text(), 'anydesk':self.txt_anydesk.text(), 'officie':self.ddl_officie.currentText(),
                 'tipo_officie':self.ddl_tipo_officie.currentText(), 'conta':self.txt_conta.text(), 'chave':self.txt_chave.text(), 'licenca':self.txt_licenca.text() }

        conn = pymysql.connect(host='nome-do-banco',port=0000, user='usuario'  ,password='00000000', db='nomde-da-tabela')
        cur = conn.cursor()
        
        if f.caracter_9( campos['anydesk'] ) == True: #refatorar
            
            if f.se_vazio( campos ) == False : 
                try:
                    query_insert = f"""INSERT INTO nome-do-banco.nome-da-tabela( patrimonio, tipo_item, posto_trabalho, descricao, uf, id_usuario, setor, modelo, marca, n_modelo, 
                                    processador, n_serie, email, memoria, status, condicoes, alugado, ssd_hdd, windows, anydesk, officie, tipo_officie, conta, chave, licenca ) 
                                    VALUES ( { campos['patrimonio'] }, '{ campos['tipo_item'] }', '{ campos['posto_trabalho']}', '{ campos['descricao'] }', '{ campos['uf'] }', '{ campos['id_usuario'] }', 
                                    '{ campos[ 'setor' ] }', '{ campos['modelo'] }', '{ campos['marca'] }', '{ campos['n_modelo'] }', '{ campos['processador'] }', '{ campos['n_serie'] }', 
                                    '{ campos['email'] }', '{ campos['memoria'] }', '{ campos['status'] }', '{ campos['condicoes'] }', '{ campos['alugado'] }', '{ campos['ssd_hdd'] }', 
                                    '{ campos['windows'] }', '{ campos['anydesk'] }','{ campos['officie'] }', '{ campos['tipo_officie'] }', '{ campos['conta'] }', '{ campos['chave'] }', 
                                    '{ campos['licenca'] }' ) """
                                    
                    
                    cur.execute(query_insert) #executa (raiozinho)
                    conn.commit() #salvar
                    conn.close()
                    
                    msg = QMessageBox()   
                    msg.setWindowTitle("AVISO")
                    msg.setText("Usuário cadastrado com sucesso!")
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()
                    
                except Exception as erro:
                    print(erro)
                    
            else:
                msg = QMessageBox()
                msg.setWindowTitle("FALHA")
                msg.setText("Usuário não cadastrado!")
                msg.setInformativeText("Nenhum campo pode estar vazio")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
        
        else:
            msg = QMessageBox()
            msg.setWindowTitle("FALHA")
            msg.setText("Usuário não cadastrado!")
            msg.setInformativeText("Verificar campo anydesk")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()

    def alterar_pc(self):
        campos = { 'patrimonio':self.txt_patrimonio.text(), 'tipo_item':self.txt_tipo_item.text(), 'posto_trabalho':self.txt_posto_trabalho.text(), 'descricao':self.txt_descricao.text(), 
                  'uf':self.ddl_uf.currentText(), 'id_usuario':self.txt_id_usuario.text(), 'setor':self.ddl_setor.currentText(), 'modelo':self.txt_modelo.text(), 'marca':self.txt_marca.text(), 
                  'n_modelo':self.txt_n_modelo.text(), 'processador':self.txt_processador.text(), 'n_serie':self.txt_n_serie.text(), 'email':self.txt_email.text(), 
                  'memoria':self.txt_memoria.text(), 'status':self.ddl_status.currentText(), 'condicoes':self.txt_condicoes.text(), 'alugado':self.ddl_alugado.currentText(), 
                  'ssd_hdd':self.ddl_ssd_hdd.currentText(), 'windows':self.txt_windows.text(), 'anydesk':self.txt_anydesk.text(), 'officie':self.ddl_officie.currentText(),
                  'tipo_officie':self.ddl_tipo_officie.currentText(), 'conta':self.txt_conta.text(), 'chave':self.txt_chave.text(), 'licenca':self.txt_licenca.text() }
        
        conn = pymysql.connect(host='nome-do-banco',port=0000, user='usuario'  ,password='00000000', db='nomde-da-tabela')
        cur = conn.cursor()
        
        msg = QMessageBox()
        msg.setWindowTitle("AVISO")
        msg.setText("DESEJA SALVAR AS ALTERAÇÕES?")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        executar = msg.exec_()
        
        
        if f.caracter_9( campos['anydesk'] ) == True: #refatorar
            if f.se_vazio( campos ) == False:
                try:
                    if executar == msg.Yes:
                        query_update = f"""UPDATE nome-do-banco.nome-da-tabela SET tipo_item = '{ campos['tipo_item'] }', posto_trabalho = '{ campos['posto_trabalho'] }', 
                                        descricao = '{ campos['descricao'] }', uf = '{ campos['uf'] }', id_usuario = '{ campos['id_usuario'] }', setor = '{campos['setor']}', 
                                        modelo = '{ campos['modelo'] }', marca = '{ campos['marca'] }', n_modelo = '{ campos['n_modelo'] }', processador = '{ campos['processador'] }', 
                                        n_serie = '{ campos['n_serie'] }', email = '{ campos['email'] }', memoria = '{ campos['memoria'] }', status = '{ campos['status'] }', 
                                        condicoes = '{ campos['condicoes'] }', alugado = '{ campos['alugado'] }', ssd_hdd = '{ campos['ssd_hdd'] }', windows = '{ campos['windows'] }',
                                        anydesk = '{ campos['anydesk'] }', officie = '{ campos['officie'] }', tipo_officie = '{ campos['tipo_officie'] }', conta = '{ campos['conta'] }',
                                        chave = '{ campos['chave'] }', licenca = '{ campos['licenca'] }' WHERE patrimonio = { campos['patrimonio'] } """
                    
                        cur.execute(query_update) #executa (raiozinho)
                        conn.commit() #salvar
                        conn.close()
                        
                        msg = QMessageBox()
                        msg.setWindowTitle("AVISO")
                        msg.setText("Alterações feitas com sucesso!")
                        msg.setIcon(QMessageBox.Information)
                        msg.exec_()
                    
                except Exception as erro:
                    print(erro) 
                    
            else:
                msg = QMessageBox()
                msg.setWindowTitle("FALHA")
                msg.setText("Não foi possivel fazer as alterações!")
                msg.setInformativeText("Nenhum campo pode estar vazio")
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
        
        else:
            msg = QMessageBox()
            msg.setWindowTitle("FALHA")
            msg.setText("Usuário não cadastrado!")
            msg.setInformativeText("Verificar campo anydesk")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
         
    def deletar_pc(self):
        campos = { 'patrimonio':self.txt_patrimonio.text(),'tipo_item':self.txt_tipo_item.text(), 'posto_trabalho':self.txt_posto_trabalho.text(), 'descricao':self.txt_descricao.text(),
                  'uf':self.ddl_uf.currentText(), 'id_usuario':self.txt_id_usuario.text(), 'setor':self.ddl_setor.currentText(), 'modelo':self.txt_modelo.text(), 'marca':self.txt_marca.text(), 
                  'n_modelo':self.txt_n_modelo.text(), 'processador':self.txt_processador.text(), 'n_serie':self.txt_n_serie.text(), 'email':self.txt_email.text(), 'memoria':self.txt_memoria.text(), 
                  'status':self.ddl_status.currentText(), 'condicoes':self.txt_condicoes.text(), 'alugado':self.ddl_alugado.currentText(), 'ssd_hdd':self.ddl_ssd_hdd.currentText(),
                  'windows':self.txt_windows.text(), 'anydesk':self.txt_anydesk.text(), 'officie':self.ddl_officie.currentText(),'tipo_officie':self.ddl_tipo_officie.currentText(), 
                  'conta':self.txt_conta.text(), 'chave':self.txt_chave.text(), 'licenca':self.txt_licenca.text() }
        
        conn = pymysql.connect(host='nome-do-banco',port=0000, user='usuario'  ,password='00000000', db='nomde-da-tabela')
        cur = conn.cursor()
      
        query_delete = f"""DELETE FROM nome-do-banco.nome-da-tabela WHERE patrimonio = { campos['patrimonio'] } """
                          
        msg = QMessageBox()
        msg.setWindowTitle("AVISO")
        msg.setText("ESTÁ AÇÃO É DEFINITIVA")
        msg.setInformativeText("Deseja continuar?")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        executar = msg.exec_()
                
        if f.se_vazio( campos ) == False:
            try:   
                if executar == msg.Yes:
                    cur.execute(query_delete) #executa (raiozinho)
                    conn.commit() #salvar
                    conn.close()
                    
                    msg = QMessageBox()
                    msg.setWindowTitle("AVISO")
                    msg.setText("Dados apagados com sucesso")
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()
                
            except Exception as erro:
                print(erro)
                
        else:
            msg = QMessageBox()
            msg.setWindowTitle("FALHA")
            msg.setText("Impossivel apagar os dados")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
            
    def limpar_pc(self): 
        campos = [ self.txt_patrimonio, self.txt_tipo_item, self.txt_posto_trabalho ,self.txt_descricao, self.txt_id_usuario ,self.txt_modelo, self.txt_marca, self.txt_n_modelo, 
                  self.txt_processador, self.txt_n_serie, self.txt_email, self.txt_memoria, self.txt_condicoes, self.txt_windows, self.txt_anydesk, self.txt_conta, self.txt_chave, 
                  self.txt_licenca, self.txt_windows, self.txt_anydesk, self.txt_conta, self.txt_chave, self.txt_licenca ]
        
        for item in campos:
            item.clear()
            
    def gerar_pdf(self):
        campos = { 'patrimonio':self.txt_patrimonio.text(), 'descricao':self.txt_descricao.text(), 'processador':self.txt_processador.text(), 'memoria': self.txt_memoria.text() }
        
        try:
            if f.se_vazio( campos ) == False: 
                conn = pymysql.connect(host='nome-do-banco',port=0000, user='usuario'  ,password='00000000', db='nomde-da-tabela')         
                cur = conn.cursor()
                
                filtro = int( self.txt_patrimonio.text() )
                
                query = f"""SELECT  t2.name, t1.setor, t1.patrimonio, t1.modelo, t1.descricao, t1.processador, t1.memoria, t1.n_modelo, t1.n_serie, t1.ssd_hdd, t1.marca 
                FROM nome-do-banco.nome-da-tabela AS t1 LEFT JOIN nome-do-banco.nome-da-tabela as t2 ON t1.id_usuario  = t2.id WHERE patrimonio = { filtro }"""
                
                tabela = pd.read_sql(query, conn)
                print(tabela)
                
                name = list( tabela[ 'name' ] )[0]
                setor = list( tabela[ 'setor' ] )[0]
                
                patrimonio = list( tabela[ 'patrimonio' ] )[0]
                
                marca = list( tabela[ 'marca' ] )[0]
                descricao = list( tabela[ 'descricao' ] )[0]
                memoria = list( tabela[ 'memoria' ] )[0]
                ssd_hdd = list( tabela[ 'ssd_hdd' ] )[0]
                
                quantidade = '1'
                
                modelo = list( tabela[ 'modelo' ] )[0]
                processador = list( tabela[ 'processador' ] )[0]
                n_modelo = list( tabela[ 'n_modelo' ] )[0]
                n_serie = list( tabela[ 'n_serie' ] )[0]
                
                pdf = canvas.Canvas(f"termos/{ patrimonio }_Termo_Responsabilidade.pdf")
                
                pdf.setTitle(f"patrimonio { str( patrimonio ) }")
                pdf.drawInlineImage('', 230, 740, 120, 120, preserveAspectRatio= True)
                pdf.setFont('Helvetica-Bold', 15)
                pdf.drawCentredString(290, 750, "Termo de Responsabilidade de Uso")
                pdf.setFont('Helvetica-Bold', 13)
                pdf.drawCentredString(290, 730, "SAT-RG-39")

                id = Paragraph('IDENTIFICAÇÃO DO COLABORADOR')
                id.wrapOn(pdf, 400, 100)
                id.drawOn(pdf, 100, 695)
                nome = Paragraph('Nome: ' + name)
                nome.wrapOn(pdf, 400, 100)
                nome.drawOn(pdf, 100, 670)
                setor = Paragraph('Setor: ' + setor)
                setor.wrapOn(pdf, 400, 100)
                setor.drawOn(pdf, 100, 655)
                n_id = Paragraph('N° de Identidade: ')
                n_id.wrapOn(pdf, 400, 100)
                n_id.drawOn(pdf, 100, 640)

                pdf.drawInlineImage('imagens/tabela patrimonio.png', 90, 380, 400, 400, preserveAspectRatio= True)

                p = Paragraph( str( patrimonio ) )
                p.wrapOn(pdf, 400, 100)
                p.drawOn(pdf, 117, 591)
                d = Paragraph( marca + ' / ' + descricao +  ' / ' + memoria + ' / ' +  ssd_hdd ) 
                d.wrapOn(pdf, 400, 100)
                d.drawOn(pdf, 165, 591)
                d2 = Paragraph( modelo + ' / ' + processador + ' / ' +  n_serie + ' / ' +  n_modelo ) 
                d2.wrapOn(pdf, 400, 100)
                d2.drawOn(pdf, 165, 575)
                q = Paragraph(quantidade)
                q.wrapOn(pdf, 400, 100)
                q.drawOn(pdf, 467, 591)

                pdf.line(80, 520, 500, 520)
                
                #RETIRAR CREDENCIAIS OU QUALQUER DADO LIGADO A EMPRESA
                p0 = Paragraph(f"""Recebi da empresa NOME DA EMPRESA DO BRASIL LTDA, CNPJ Nº 00.000.000/0000-00, a título de empréstimo, para uso exclusivo, 
                conforme determinado em lei, os equipamentos especificados neste termo de responsabilidade. Comprometendo-me a mantê-los em perfeito estado de conservação, 
                ficando ciente de que: """)
                p0.wrapOn(pdf, 400, 100)
                p0.drawOn(pdf, 95, 445)
                p1 = Paragraph(f"""1- Se o equipamento for danificado ou inutilizado por emprego inadequado, mau uso, negligência ou extravio, a empresa me fornecerá novo equipamento e cobrará o valor 
                de um equipamento da mesma marca ou equivalente ao da praça;""")
                p1.wrapOn(pdf, 400, 100)
                p1.drawOn(pdf, 95, 400)
                p2 = Paragraph("2- Em caso de perda, dano, furto, inutilização ou extravio do equipamento, deverei comunicar imediatamente ao setor competente;")
                p2.wrapOn(pdf, 400, 100)
                p2.drawOn(pdf, 95, 370)
                p3 = Paragraph(f"""3- Terminando os serviços ou em caso de rescisão do contrato de trabalho, devolverei o equipamento completo e em perfeito estado de conservação, considerando-se o tempo 
                do uso do mesmo (tempo de vida útil), ao setor competente;""")
                p3.wrapOn(pdf, 400, 100)
                p3.drawOn(pdf, 95, 330)
                p4 = Paragraph('4- Estando os equipamentos em minha posse, estarei sujeito a inspeções sem prévio aviso.')
                p4.wrapOn(pdf, 400, 100)
                p4.drawOn(pdf, 95, 300)
                p5 = Paragraph('Rio de Janeiro, ____ de ___________ de 20____.')
                p5.wrapOn(pdf, 400, 100)
                p5.drawOn(pdf, 100, 272)
                p6 = Paragraph('Assinatura:____________________________________________________')
                p6.wrapOn(pdf, 400, 100)
                p6.drawOn(pdf, 100, 250)

                pdf.line(80, 230, 500, 230)

                p7 = Paragraph('Data devolução: ____/____/____')
                p7.wrapOn(pdf, 400, 100)
                p7.drawOn(pdf, 100, 202)
                p8 = Paragraph('Assinatura:____________________________________________________')
                p8.wrapOn(pdf, 400, 100)
                p8.drawOn(pdf, 100, 180)

                pdf.drawInlineImage('imagens/check box.png', 85, 97, 50, 60, preserveAspectRatio= True)

                p9 = Paragraph('Em perfeito estado')
                p9.wrapOn(pdf, 400, 100)
                p9.drawOn(pdf, 125, 145)
                p10 = Paragraph('Apresentando defeito')
                p10.wrapOn(pdf, 400, 100)
                p10.drawOn(pdf, 125, 122)
                p11 = Paragraph('Faltando peças ou acessórios')
                p11.wrapOn(pdf, 400, 100)
                p11.drawOn(pdf, 125, 98)
                
                p12 = Paragraph('Responsável pelo recebimento')
                p12.wrapOn(pdf, 400, 100)
                p12.drawOn(pdf, 100, 62)
                p13 = Paragraph('Nome:_______________________________________________________')
                p13.wrapOn(pdf, 400, 100)
                p13.drawOn(pdf, 100, 38)
                p14 = Paragraph('Assinatura:____________________________________________________')
                p14.wrapOn(pdf, 400, 100)
                p14.drawOn(pdf, 100, 15)
                
                pdf.save()
                
                msg = QMessageBox()
                msg.setWindowTitle("AVISO")
                msg.setText('Deseja visualizar o pdf?')
                msg.setIcon(QMessageBox.Information)
                msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel | QMessageBox.Save)
                msg.setDefaultButton(QMessageBox.Cancel)
                executar = msg.exec_()

                if executar == msg.Yes:
                    patrimonio_yes = self.txt_patrimonio.text()
                    
                    if patrimonio_yes != '' or patrimonio_yes != None:
                
                        poppler_path = "OLHAR-NA-DOCUMENTAÇÃO-BIBLIOTECA"
                    
                        pdf_path = os.getcwd() + f"\\termos\\{ patrimonio_yes }_Termo_Responsabilidade.pdf"

                        paginas = convert_from_path(pdf_path=pdf_path, poppler_path=poppler_path)
                        
                        pasta_salvamento = os.getcwd() + '\preview'
                        
                        c=1
                        for pagina in paginas:
                            nome_imagem = f"{ patrimonio_yes }_Termo_Responsabilidade.png"
                            
                            pagina.save( os.path.join( pasta_salvamento, nome_imagem ), "PNG" )
                            c+=1
                        
                        imagem = cv2.imread(f"preview/{ patrimonio_yes }_Termo_Responsabilidade.png")
                        
                        down_width = 300
                        down_height = 360
                        down_points = (down_width, down_height)
                        resized_down = cv2.resize(imagem, down_points, interpolation= cv2.INTER_LINEAR)
                    
                        up_width = 600
                        up_height = 720
                        up_points = (up_width, up_height)
                        resized_up = cv2.resize(imagem, up_points, interpolation= cv2.INTER_LINEAR)
                        
                        cv2.imshow('Preview', resized_down)
                        cv2.imshow('Preview', resized_up)
                        
                        arquivo_png = f"preview/{ patrimonio_yes }_Termo_Responsabilidade.png"
                        
                        os.remove(arquivo_png)
                        
                        msg = QMessageBox()
                        msg.setWindowTitle("AVISO")
                        msg.setText("Deseja salvar o arquivo?")
                        msg.setIcon(QMessageBox.Information)
                        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
                        msg.setDefaultButton(QMessageBox.Yes)
                        executar = msg.exec_()
                        
                        if executar == msg.Cancel:
                            patrimonio_cancel = self.txt_patrimonio.text()
                            
                            os.remove(f"termos/{patrimonio_cancel}_Termo_Responsabilidade.pdf")
                            
                            msg = QMessageBox()
                            msg.setWindowTitle('WARNING')
                            msg.setText('Operação cancelada')
                            msg.setIcon(QMessageBox.Critical)  
                            msg.exec_()
                            
                        if executar == msg.Yes:
                            
                            msg = QMessageBox()
                            msg.setWindowTitle('AVISO')
                            msg.setText('Arquivo salvo com sucesso!')
                            msg.setIcon(QMessageBox.Information)  
                            msg.exec_()
                        
                if executar == msg.Cancel:
                    patrimonio_cancel_preview = self.txt_patrimonio.text()
                    
                    arquivo_pdf = f"termos/{ patrimonio_cancel_preview }_Termo_Responsabilidade.pdf"
                    arquivo_png = f"preview/{ patrimonio_cancel_preview }_Termo_Responsabilidade.png"
                    
                    os.remove( arquivo_pdf )
                    os.remove( arquivo_png )
                    
                if executar == msg.Save:
                    patrimonio_save = self.txt_patrimonio.text()
                    
                    arquivo_png = f"preview/{ patrimonio_save }_Termo_Responsabilidade.png"
                    
                    os.remove( arquivo_png )
                    
                    msg = QMessageBox()
                    msg.setWindowTitle('AVISO')
                    msg.setText('Arquivo salvo com sucesso!')
                    msg.setIcon(QMessageBox.Information)  
                    msg.exec_()
                                
            else:
                msg = QMessageBox()
                msg.setWindowTitle("FALHA")
                msg.setText('Impossivel gerar documento!')
                msg.setInformativeText('O campo do patrimonio não pode estar vazio')
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                
        except Exception as erro:
            print(erro)
            
    def abrir_janela_buscar_nome(self):
        self.janela2.show()
           

#PAGE EQUIPAMENTOS
    def detalhes_equipamentos(self):
        conn = pymysql.connect(host='nome-do-banco',port=0000, user='usuario'  ,password='00000000', db='nomde-da-tabela')
        cur = conn.cursor()
    
        try:
            patrimonio_ver = self.txt_patrimonio_e.text()
            
            if patrimonio_ver == '' or patrimonio_ver == None:
                msg = QMessageBox()
                msg.setWindowTitle('AVISO')
                msg.setText('Campo vazio!')
                msg.setInformativeText('Por favor, preencha o campo de busca')
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
                
            else:
                filtro = int( self.txt_patrimonio_e.text() )
                
                query = f"select * from nome-da-tabela where patrimonio = { filtro }"
                tabela = pd.read_sql(query, conn)
            
                if tabela.empty == False:
                    
                    if list( tabela[ 'uf' ] )[0] == 'RJ':
                        indexUf = 0
                    if list( tabela[ 'uf' ] )[0] == 'RJ - NITEROI':
                        indexUf = 1
                    if list( tabela[ 'uf' ] )[0] == 'SP':
                        indexUf = 2    
                    if list( tabela[ 'uf' ] )[0] == 'GO':
                        indexUf = 3
                    if list( tabela[ 'uf' ] )[0] == 'AC':
                        indexUf = 4
                    if list( tabela[ 'uf' ] )[0] == 'RO':
                        indexUf = 5
                    if list( tabela[ 'uf' ] )[0] == 'MG':
                        indexUf = 6
                    if list( tabela[ 'uf' ] )[0] == 'CE':
                        indexUf = 7
                    if list( tabela[ 'uf' ] )[0] == 'PE':
                        indexUf = 8
                        
                    descricao = list( tabela[ 'descricao' ] )[0]
                    posto_trabalho = list( tabela[ 'posto_trabalho' ] )[0]
                    modelo = list( tabela[ 'modelo' ] )[0]
                    marca = list( tabela[ 'marca' ] )[0]
                    n_modelo = list( tabela[ 'n_modelo' ] )[0]
                    n_serie = list( tabela[ 'n_serie' ] )[0]
                    
                    if list( tabela[ 'status' ] )[0] == 'Ativo':
                        indexStatus = 0
                    if list( tabela[ 'status' ] )[0] == 'Inativo':
                        indexStatus = 1
                    
                    self.ddl_uf_e.setCurrentIndex( indexUf )
                    self.txt_tipo.setText( descricao )
                    self.txt_posto_trabalho_e.setText( posto_trabalho )
                    self.txt_modelo_e.setText( modelo )
                    self.txt_marca_e.setText( marca )
                    self.txt_n_modelo_e.setText( n_modelo )
                    self.txt_n_serie_e.setText( n_serie )
                    self.ddl_status_e.setCurrentIndex( indexStatus )
                
                else:
                    msg = QMessageBox()
                    msg.setWindowTitle("AVISO")
                    msg.setText("Patrimonio não encontrado!")
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()
                    
        except Exception as error:
            print(error)
            
    def cadastrar_equipamentos (self):
        campos = { 'patrimonio':self.txt_patrimonio_e.text(),'uf':self.ddl_uf_e.currentText(), 'descricao':self.txt_tipo.text(), 'posto_trabalho':self.txt_posto_trabalho_e.text(), 
                  'modelo':self.txt_modelo_e.text(), 'marca':self.txt_marca_e.text(), 'n_modelo':self.txt_n_modelo_e.text(), 'n_serie':self.txt_n_serie_e.text(), 
                  'status':self.ddl_status_e.currentText() }
        
        conn = pymysql.connect(host='nome-do-banco',port=0000, user='usuario'  ,password='00000000', db='nomde-da-tabela')
        cur = conn.cursor()
        
        if f.se_vazio( campos ) == False:
            try:
                query_insert = f""" INSERT INTO nome-do-banco.nome-da-tabela (patrimonio, uf, descricao, posto_trabalho, modelo, marca, n_modelo, n_serie, status) VALUES 
                              ( { campos[ 'patrimonio' ] }, '{ campos[ 'uf' ] }', '{ campos[ 'descricao' ] }', '{ campos[ 'posto_trabalho' ] }', '{ campos[ 'modelo' ] }', 
                              '{ campos[ 'marca' ] }', '{ campos[ 'n_modelo' ] }', '{ campos[ 'n_serie'] }', '{ campos[ 'status' ] }' )"""      
                
                cur.execute(query_insert)
                conn.commit()
                conn.close()
                
                msg = QMessageBox()
                msg.setWindowTitle("AVISO")
                msg.setText("Equipamento cadastrado com sucesso!")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
                
            except Exception as erro:
                print(erro)
                
        else:
            msg = QMessageBox()
            msg.setWindowTitle("FALHA")
            msg.setText("Equipamento não cadastrado!")
            msg.setInformativeText("Nenhum campo pode estar vazio")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
            
    def alterar_equipamentos (self):
        campos = { 'patrimonio':self.txt_patrimonio_e.text(), 'uf':self.ddl_uf_e.currentText(), 'descricao':self.txt_tipo.text(), 'posto_trabalho':self.txt_posto_trabalho_e.text(), 
                    'modelo':self.txt_modelo_e.text(), 'marca':self.txt_marca_e.text(), 'n_modelo':self.txt_n_modelo_e.text(), 'n_serie':self.txt_n_serie_e.text(),
                    'status':self.ddl_status_e.currentText() }
        
        conn = pymysql.connect(host='nome-do-banco',port=0000, user='usuario'  ,password='00000000', db='nomde-da-tabela')
        cur = conn.cursor()
        
        msg = QMessageBox()
        msg.setWindowTitle("WARNING")
        msg.setText("DESEJA SALVAR AS ALTERAÇÕES?")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        executar = msg.exec_()
        
        if f.se_vazio( campos ) == False:
            try:
                if executar == msg.Yes:
                    query_update = f""" UPDATE nome-do-banco.nome-da-tabela SET uf = '{ campos[ 'uf' ] }', descricao = '{ campos[ 'descricao' ] }', 
                    posto_trabalho = '{ campos[ 'posto_trabalho' ] }', modelo = '{ campos[ 'modelo' ] }', marca = '{ campos[ 'marca' ] }', n_modelo = '{ campos[ 'n_modelo' ] }', 
                    n_serie = '{ campos[ 'n_serie'] }', status = '{ campos[ 'status' ] }' WHERE patrimonio = { campos['patrimonio'] }"""
                    
                    cur.execute( query_update )
                    conn.commit()
                    conn.close()
                    
                    msg = QMessageBox()
                    msg.setWindowTitle("AVISO")
                    msg.setText("Alterações feitas com sucesso!")
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()
                
            except Exception as erro:
                print(erro)
        
        else:
            msg = QMessageBox()
            msg.setWindowTitle("FALHA")
            msg.setText("Não foi possivel fazer as alterações!")
            msg.setInformativeText("Nenhum campo pode estar vazio")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
            
    def deletar_equipamentos (self):
        campos = { 'patrimonio':self.txt_patrimonio_e.text(),'uf':self.ddl_uf_e.currentText(), 'descricao':self.txt_tipo.text(), 'posto_trabalho':self.txt_posto_trabalho_e.text(), 
            'modelo':self.txt_modelo_e.text(), 'marca':self.txt_marca_e.text(), 'n_modelo':self.txt_n_modelo_e.text(), 'n_serie':self.txt_n_serie_e.text(), 
            'status':self.ddl_status_e.currentText() }
        
        conn = pymysql.connect(host='nome-do-banco',port=0000, user='usuario'  ,password='00000000', db='nomde-da-tabela')
        cur = conn.cursor()
        
        query_delete = f"""DELETE FROM nome-do-banco.nome-da-tabela WHERE patrimonio = { campos['patrimonio'] }"""
        
        msg = QMessageBox()
        msg.setWindowTitle("WARNING")
        msg.setText("ESTÁ AÇÃO É DEFINITIVA")
        msg.setInformativeText("Deseja continuar?")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        executar = msg.exec_()
        
        if f.se_vazio( campos ) == False:
            try:
                if executar == msg.Yes:
                    cur.execute( query_delete )
                    conn.commit()
                    conn.close()

                    msg = QMessageBox()
                    msg.setWindowTitle("AVISO")
                    msg.setText("Dados apagados com sucesso!")
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()
                
            except Exception as erro:
                print(erro)
        
        else:
            msg = QMessageBox()
            msg.setWindowTitle("FALHA")
            msg.setText("Impossivel apagar os dados!")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
        
    def limpar_equipamentos (self):
        campos = [ self.txt_patrimonio_e, self.txt_tipo, self.txt_posto_trabalho_e, self.txt_modelo_e, self.txt_marca_e, self.txt_n_modelo_e, self.txt_n_serie_e ]
        
        for item in campos:
            item.clear()

    def mostrar_equipamentos(self):
        try:
            conn = pymysql.connect(host='nome-do-banco',port=0000, user='usuario'  ,password='00000000', db='nomde-da-tabela')
            
            query = f"""SELECT patrimonio, uf, descricao, posto_trabalho, modelo, marca, n_modelo, n_serie, status FROM nome-do-banco.nome-da-tabela"""
            tabela = pd.read_sql(query, conn)
            
            if (tabela.empty == True):
                
                msg = QMessageBox()
                msg.setWindowTitle('AVISO')
                msg.setText('Impossivel carregar dados!')
                msg.setInformativeText('Não há dados registrados')
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
                
            else:
                linha = 0
                
                for linha_indice in ( tabela.index ):
                    coluna = 0
                    
                    for item in tabela:  
                        self.x = tabela.iloc[ linha,coluna ] 
                        self.tabela_equipamentos.setItem( linha, coluna, QTableWidgetItem( str( self.x ) ) )
                        coluna = coluna +1
                        
                    linha = linha + 1
            
        except Exception as erro:
            print(erro)


#PAGE ESTOQUE
    def detalhes_estoque(self):
        conn = pymysql.connect(host='nome-do-banco',port=0000, user='usuario'  ,password='00000000', db='nomde-da-tabela')
        cur = conn.cursor()
        
        try:
            patrimonio_ver = self.txt_patrimonio_3.text()
        
            if patrimonio_ver == '' or patrimonio_ver == None:
                msg = QMessageBox()
                msg.setWindowTitle('AVISO')
                msg.setText('Campo vazio!')
                msg.setInformativeText('Por favor, preencha o campo de busca')
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
            
            else:
                filtro = int( self.txt_patrimonio_3.text() )
                
                query = f"SELECT * FROM nome-do-banco.nome-da-tabela WHERE patrimonio = { filtro }"
                tabela = pd.read_sql(query, conn)
                
                if tabela.empty == False:
                    if list( tabela[ 'uf' ] )[0] == 'RJ':
                        indexUf = 0
                    if list( tabela[ 'uf' ] )[0] == 'RJ - NITEROI':
                        indexUf = 1
                    if list( tabela[ 'uf' ] )[0] == 'SP':
                        indexUf = 2    
                    if list( tabela[ 'uf' ] )[0] == 'GO':
                        indexUf = 3
                    if list( tabela[ 'uf' ] )[0] == 'AC':
                        indexUf = 4
                    if list( tabela[ 'uf' ] )[0] == 'RO':
                        indexUf = 5
                    if list( tabela[ 'uf' ] )[0] == 'MG':
                        indexUf = 6
                    if list( tabela[ 'uf' ] )[0] == 'CE':
                        indexUf = 7
                    if list( tabela[ 'uf' ] )[0] == 'PE':
                        indexUf = 8
                        
                    tipo = list( tabela[ 'tipo' ] ) [0]
                    quantidade = list( tabela[ 'quantidade' ] )[0]
                    modelo = list( tabela[ 'modelo' ] )[0]
                    marca = list( tabela[ 'marca' ] )[0]
                    descricao = list( tabela[ 'descricao' ] )[0]
                    destino = list( tabela[ 'destino' ] )[0]
                    
                    self.ddl_uf_3.setCurrentIndex( indexUf )
                    self.txt_tipo_3.setText( tipo )
                    self.txt_quantidade.setText( quantidade )
                    self.txt_modelo_3.setText( modelo )
                    self.txt_marca_3.setText( marca )
                    self.txt_descricao_3.setText( descricao )
                    self.txt_destino.setText( destino )
                
                else:
                    msg = QMessageBox()
                    msg.setWindowTitle("AVISO")
                    msg.setText("Patrimonio não encontrado!")
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()
        
        except Exception as error:
            print(error)
                
    def cadastrar_estoque(self):
        campos = { 'patrimonio':self.txt_patrimonio_3.text(),'uf':self.ddl_uf_3.currentText(),'tipo':self.txt_tipo_3.text(), 'quantidade':self.txt_quantidade.text(), 
                  'modelo':self.txt_modelo_3.text(), 'marca':self.txt_marca_3.text(), 'descricao':self.txt_descricao_3.text(), 'destino':self.txt_destino.text() }
        
        conn = pymysql.connect(host='nome-do-banco',port=0000, user='usuario'  ,password='00000000', db='nomde-da-tabela')
        cur = conn.cursor()
        
        if f.se_vazio( campos ) == False:
            try:
                query_insert = f""" INSERT INTO nome-do-banco.nome-da-tabela (patrimonio, uf, tipo, quantidade, modelo, marca, descricao, destino) VALUES 
                                ( { campos[ 'patrimonio' ] },  '{ campos[ 'uf' ] }', '{ campos[ 'tipo' ] }', '{ campos[ 'quantidade' ] }', '{ campos[ 'modelo' ] }', '{ campos[ 'marca' ] }',
                                '{ campos[ 'descricao' ] }', '{ campos[ 'destino' ] }' ) """  
                
                cur.execute(query_insert)
                conn.commit()
                conn.close()
                
                msg = QMessageBox()
                msg.setWindowTitle("AVISO")
                msg.setText("Adicionado ao estoque com sucesso!")
                msg.setIcon(QMessageBox.Information)
                msg.exec_()
                
            except Exception as erro:
                print(erro)
                
        else:
            msg = QMessageBox()
            msg.setWindowTitle("FALHA")
            msg.setText("Não foi possivel adicionar ao estoque!")
            msg.setInformativeText("Nenhum campo pode estar vazio")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
            
    def alterar_estoque(self):
        campos = { 'patrimonio':self.txt_patrimonio_3.text(),'uf':self.ddl_uf_3.currentText(),'tipo':self.txt_tipo_3.text(), 'quantidade':self.txt_quantidade.text(), 
        'modelo':self.txt_modelo_3.text(), 'marca':self.txt_marca_3.text(), 'descricao':self.txt_descricao_3.text(), 'destino':self.txt_destino.text() }
        
        conn = pymysql.connect(host='nome-do-banco',port=0000, user='usuario'  ,password='00000000', db='nomde-da-tabela')
        cur = conn.cursor()
        
        msg = QMessageBox()
        msg.setWindowTitle("WARNING")
        msg.setText("DESEJA SALVAR AS ALTERAÇÕES?")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        executar = msg.exec_()
        
        if f.se_vazio( campos ) == False:
            try:
                if executar == msg.Yes:
                    query_update = f""" UPDATE nome-do-banco.nome-da-tabela SET uf = '{ campos[ 'uf' ] }', tipo = '{ campos [ 'tipo' ] }', quantidade = '{ campos [ 'quantidade' ] }', 
                    modelo = '{ campos[ 'modelo' ] }', marca = '{ campos[ 'marca' ] }', descricao = '{ campos[ 'descricao' ] }', destino = '{ campos[ 'destino' ] }' 
                    WHERE patrimonio = { campos['patrimonio'] }"""

                    cur.execute( query_update )
                    conn.commit()
                    conn.close()
                    
                    msg = QMessageBox()
                    msg.setWindowTitle("AVISO")
                    msg.setText("Alterações feitas com sucesso!")
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()
                    
            except Exception as erro:
                print(erro)
        
        else:
            msg = QMessageBox()
            msg.setWindowTitle("FALHA")
            msg.setText("Não foi possivel fazer as alterações!")
            msg.setInformativeText("Nenhum campo pode estar vazio")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_()
     
    def deletar_estoque(self):
        campos = { 'patrimonio':self.txt_patrimonio_3.text(),'uf':self.ddl_uf_3.currentText(),'tipo':self.txt_tipo_3.text(), 'quantidade':self.txt_quantidade.text(), 
        'modelo':self.txt_modelo_3.text(), 'marca':self.txt_marca_3.text(), 'descricao':self.txt_descricao_3.text(), 'destino':self.txt_destino.text() }
        
        conn = pymysql.connect(host='nome-do-banco',port=0000, user='usuario'  ,password='00000000', db='nomde-da-tabela')
        cur = conn.cursor()
        
        query_delete = f"""DELETE FROM nome-do-banco.nome-da-tabela WHERE patrimonio = { campos[ 'patrimonio' ] }"""
        
        msg = QMessageBox()
        msg.setWindowTitle("WARNING")
        msg.setText("ESTÁ AÇÃO É DEFINITIVA")
        msg.setInformativeText("Deseja continuar?")
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        executar = msg.exec_()
        
        if f.se_vazio( campos ) == False:
            try:
                if executar == msg.Yes:
                    cur.execute( query_delete )
                    conn.commit()
                    conn.close()

                    msg = QMessageBox()
                    msg.setWindowTitle("AVISO")
                    msg.setText("Dados apagados com sucesso!")
                    msg.setIcon(QMessageBox.Information)
                    msg.exec_()
                
            except Exception as erro:
                print(erro)
        
        else:
            msg = QMessageBox()
            msg.setWindowTitle("FALHA")
            msg.setText("Impossivel apagar os dados!")
            msg.setIcon(QMessageBox.Critical)
            msg.exec_() 
            
    def limpar_estoque(self):
        campos = [ self.txt_patrimonio_3, self.txt_tipo_3, self.txt_quantidade, self.txt_modelo_3, self.txt_marca_3, self.txt_descricao_3, self.txt_destino ]
        
        for item in campos:
            item.clear()   
    
    def mostrar_estoque(self):
        try:
            conn = pymysql.connect(host='nome-do-banco',port=0000, user='usuario'  ,password='00000000', db='nomde-da-tabela')
            
            query = f"""SELECT patrimonio, uf, tipo, quantidade, modelo, marca, descricao, destino FROM nome-do-banco.nome-da-tabela"""
            tabela = pd.read_sql(query, conn)
            
            if (tabela.empty == True):
                msg = QMessageBox()
                msg.setWindowTitle('AVISO')
                msg.setText('Impossivel carregar dados!')
                msg.setInformativeText('Não há dados registrados')
                msg.setIcon(QMessageBox.Critical)
                msg.exec_()
            
            else:
                linha = 0
                
                for linha_indice in ( tabela.index ):
                    coluna = 0
                    
                    for item in tabela:  
                        self.x = tabela.iloc[ linha,coluna ] 
                        self.tabela_estoque.setItem( linha, coluna, QTableWidgetItem( str( self.x ) ) )
                        coluna = coluna +1
                        
                    linha = linha + 1
        
        except Exception as erro:
            print(erro)

            
def main():
    app = QApplication(sys.argv)
    form = Janela()
    form.show()
    app.exec_()

if __name__ == '__main__':
    main()