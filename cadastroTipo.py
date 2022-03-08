from multiprocessing.sharedctypes import Value
import tkinter as tk
from tkinter import Button, ttk
from tkinter import Entry, Frame, Label, Tk, ttk
from tkinter import messagebox
from tkinter.ttk import Combobox, Notebook
from tkcalendar import DateEntry
import sqlite3
from tkinter.messagebox import showinfo



class FUNCOES():
    def conectarBD(self):
        self.conn = sqlite3.connect("financeiro.db3")
        self.cursor = self.conn.cursor()
    def desconectar_bd(self):
        self.conn.close()        
    def criarTabelas(self):
        self.conectarBD(); print("Conectando ao Banco de Dados!!!")
        ### Criar tabela
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tbl_categoria (
                                id_cat           INTEGER      PRIMARY KEY AUTOINCREMENT NOT NULL,
                                tipo_cat         VARCHAR (7)  NOT NULL,
                                descri_cat       VARCHAR (50) NOT NULL,
                                datacadastro_cat DATE         DEFAULT (CURRENT_DATE) 
                                    );
                        """)
        self.conn.commit();print("Banco de dados criado!!!")
        self.desconectar_bd();print("Banco de Dados desconectado")
    def criar_tbl_movimentacao(self):
        self.conectarBD()
        ## Criar a tabela
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS tbl_movimentacao (
                                id_mov          INTEGER      PRIMARY KEY AUTOINCREMENT
                                                            NOT NULL,
                                fk_categoria_id              REFERENCES tbl_categoria (id_cat) ON DELETE RESTRICT
                                                            NOT NULL,
                                mov_descricao   VARCHAR (40),
                                mov_data        DATE,
                                mov_valor       DECIMAL
                                    );
                        """)
        self.conn.commit();print("tabela Movimentacao Criada com Sucesso")
        self.desconectar_bd();print("Banco de Dados desconectado")

class APP(FUNCOES):
    def __init__(self):
        self.tela()
        self.conectarBD()
        self.criarTabelas()
        self.criar_tbl_movimentacao()
        self.componentes()
        self.carregarCOMBO()
        self.janela.mainloop()
    def tela(self):
        self.janela = Tk()
        self.largura = 500
        self.altura = 200
        self.largura_screen = self.janela.winfo_screenwidth()
        self.altura_screen = self.janela.winfo_screenheight()
        self.posX = self.largura_screen/2 - self.largura/2
        self.posY = self.altura_screen/2 - self.altura/2
        self.janela.geometry("%dx%d+%d+%d" % (self.largura, self.altura, self.posX, self.posY))
        self.janela.title("Controle Financeiro")
        self.janela.configure(bg='#B0E0E6')
    def componentes(self):
        ## Entrada
        self.ENTRADA_descricao_MOV =Entry(self.janela, width=40)
        self.ENTRADA_descricao_MOV.place(x=135, y=90)
        ## ROTULOS
        self.ROTULO_titulo_CAT = Label(self.janela, text='Cadastro de Categoria', bg='#B0E0E6', font=('Ivy', 18, 'bold', 'italic', 'underline'))
        self.ROTULO_titulo_CAT.place(x=1,y=1, width=self.largura)
        self.ROTULO_tipo_cat = Label(self.janela, text="Tipo: ", bg='#B0E0E6', font=('Ivy', 10, 'bold', 'italic'))
        self.ROTULO_tipo_cat.place(x=1,y=50)
        self.ROTULO_descricao_MOV = Label(self.janela, text='Descrição Tipo Mov: ', bg='#B0E0E6', font=('Ivy', 8, 'bold', 'italic'))
        self.ROTULO_descricao_MOV.place(x=1, y=93)
        ## Botão
        self.BOTAO_cadastrar_MOV = Button(self.janela, text='Cadastrar', activebackground='red', activeforeground='white',command=self.cadastro)
        self.BOTAO_cadastrar_MOV.place(x=200, y=130)
        ###COMBO
        self.COMBO_tipo_MOV = Combobox(self.janela, values=['','RENDA','DESPESA'])
        self.COMBO_tipo_MOV.place(x=44,y=50)
    def cadastro(self):
        if (self.COMBO_tipo_MOV.get() == '') or (self.ENTRADA_descricao_MOV.get() == ''):
            showinfo(
                'Campos Obrigatórios',
                'Todos os campos são obrigatórios'
            )
        else:
            self.conectarBD()
            self.cursor.execute(""" INSERT INTO tbl_categoria (
                                    tipo_cat,
                                    descri_cat
                                    )
                                    VALUES (?,?)""",(self.COMBO_tipo_cat.get(), self.ENTRADA_descricao_MOV.get()))
            self.conn.commit()
            self.desconectar_bd()