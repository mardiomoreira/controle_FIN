from tkinter import Button, Entry, Frame, Label, Tk, ttk
from tkinter import messagebox
from tkinter.ttk import Notebook, Combobox
from tkcalendar import DateEntry
import sqlite3


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
    def carregarCOMBO(self):
        self.dicionarioCOMBO = {}
        self.conectarBD()
        self.consultaSQL = self.cursor.execute(""" SELECT id_cat, descri_cat FROM tbl_categoria ORDER BY descri_cat ASC; """)
        ##Criando o dicionario com os dados da pesquisa
        for i in self.consultaSQL:
            self.dicionarioCOMBO[i[1]]= i[0]
        self.desconectar_bd()
        self.listaCOMBO =[]
        for self.valor in self.dicionarioCOMBO.keys():
            self.listaCOMBO.append(self.valor)
            print(self.valor)

    

class APP(FUNCOES):
    def __init__(self):
        self.tela()
        self.carregarCOMBO()
        self.componentes()
        self.conectarBD()
        self.criarTabelas()
        self.criar_tbl_movimentacao()
        self.janela.mainloop()
    def tela(self):
        self.janela = Tk()
        self.largura = 700
        self.altura = 400
        self.largura_screen = self.janela.winfo_screenwidth()
        self.altura_screen = self.janela.winfo_screenheight()
        self.posX = self.largura_screen/2 - self.largura/2
        self.posY = self.altura_screen/2 - self.altura/2
        self.janela.geometry("%dx%d+%d+%d" % (self.largura, self.altura, self.posX, self.posY))
        self.janela.title("Controle Financeiro")
        self.janela.configure(bg='#B0E0E6')

    def componentes(self):
        #### FRAMES/ABAS ##
        self.frame_cima = Frame(self.janela, bg='#D3D3D3')
        self.frame_cima.place(relx=0, rely=0,relheight=0.99, relwidth=0.99)
        self.abas = Notebook(self.frame_cima)
        self.aba1 = Frame(self.abas)
        self.aba2 = Frame(self.abas)
        self.aba1.configure(background='#DCDCDC')
        self.aba2.configure(background="#DCDCDC")
        self.abas.add(self.aba1,text="Cadastro")
        self.abas.add(self.aba2,text="Movimentações")
        self.abas.place(relx=0,rely=0, relwidth=0.99,relheight=0.99)
        #### ENTRADAS ##
        self.ENTRADA_descricao_MOV = Entry(self.aba1, width=30)
        self.ENTRADA_descricao_MOV.place(x=400,y=50, width=200)
        self.ENTRADA_valor_MOV = Entry(self.aba1, width=10)
        self.ENTRADA_valor_MOV.place(x=335,y=80)
        # Entrada Data
        self.ENTRADA_data_MOV = DateEntry(self.aba1,width=10,bg="darkblue",fg="white",locale='pt_br')
        self.ENTRADA_data_MOV.place(x=60,y=50)

        #### Rótulo ##
        self.ROTULO_titulo_ABA = Label(self.aba1, text="Cadastro de Movimentacao", font=('arial', 20, 'bold', 'italic', 'underline'), fg='#DC143C')
        self.ROTULO_titulo_ABA.place(x=1, y=1, width=self.largura)
        self.ROTULO_descricao_MOV = Label(self.aba1, text="Descricao Movimentacao:", font=('arial', 10, 'bold', 'italic'))
        self.ROTULO_descricao_MOV.place(x=225,y=52)
        self.ROTULO_data_MOV = Label(self.aba1, text="Data:", font=('arial', 10, 'bold', 'italic'))
        self.ROTULO_data_MOV.place(x=15, y=50)
        self.ROTULO_categoris_MOV = Label(self.aba1, text="Categoria:", font=('arial', 10, 'bold', 'italic'))
        self.ROTULO_categoris_MOV.place(x=15, y=80)
        self.ROTULO_valor_MOV = Label(self.aba1, text="Valor:", font=('arial', 10, 'bold', 'italic'))
        self.ROTULO_valor_MOV.place(x=290,y=80)
        ### ComboBox ##
        self.COMBO_tipo_MOV = Combobox(self.janela, values=self.listaCOMBO)
        self.COMBO_tipo_MOV.place(x=85,y=105)
        ### Botão ##
        self.BOTAO_cadastrar_MOV = Button(self.aba1, text='Cadastrar',bg='#00FA9A', activebackground='#00FF00', activeforeground='red',command=self.cadastro_MOV)
        self.BOTAO_cadastrar_MOV.place(x=455,y=75)
    def cadastro_MOV(self):
        self.data_MOV = self.ENTRADA_data_MOV.get()
        self.descricao_MOV = self.ENTRADA_descricao_MOV.get()
        self.chave_CAT = self.COMBO_tipo_MOV.get()
        self.ID_categoria_MOV = self.dicionarioCOMBO[self.chave_CAT]
        self.valor_MOV = self.ENTRADA_valor_MOV.get()
        if (self.data_MOV == '') or (self.descricao_MOV == '') or (self.chave_CAT == '') or (self.valor_MOV == ''):
          messagebox.showinfo('Campos em Branco', 'Todos os campos são obrigatórios')
        else:
            print("Campos OK!!!")
            self.conectarBD()
            self.cursor.execute(""" INSERT INTO tbl_movimentacao (
                                    fk_categoria_id, 
                                    mov_descricao, 
                                    mov_data, 
                                    mov_valor)  
                                    VALUES (?,?,?,?)""",(self.ID_categoria_MOV, self.descricao_MOV, self.data_MOV, self.ENTRADA_valor_MOV.get()))
            self.conn.commit()
            self.desconectar_bd()

          
    

APP()
