import tkinter as tk
import sqlite3
import re
from tkinter import messagebox, Menu, Frame, Label, Entry, Button, RAISED, RIDGE, E, NW


def criar_banco():
    try:
        db = "banco.db"
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuario (
                cpf TEXT PRIMARY KEY NOT NULL,
                nome TEXT NOT NULL,
                sobrenome TEXT NOT NULL,
                email TEXT NOT NULL,
                telefone TEXT NOT NULL,
                senha TEXT NOT NULL
            ); """)
        conn.commit()
    except Exception as e:
        print("Erro na criação do banco: ", e)


# >>> Interface Grafica <<<
def janela_cadastro():
    global janela_ca
    # >>> Interface Grafica <<<
    # Cores
    cor00 = "#FFFAFA"  # Branco Neve
    cor01 = "#DCDCDC"  # Cinza Claro
    cor02 = "#4F4F4F"  # Cinza Escuro
    cor03 = "#1C1C1C"  # Preto

    # Janela
    janela_ca = tk.Toplevel()
    janela_ca.title("")
    width = 500
    height = 500
    screen_width = janela_ca.winfo_screenwidth()
    screen_height = janela_ca.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    janela_ca.geometry(f"{width}x{height}+{x}+{y}")
    janela_ca.configure(bg=cor00)
    janela_ca.resizable(width=False, height=False)


    def limpar_campos():
        entry_cpf.delete(0, 'end')
        entry_nome.delete(0, 'end')
        entry_sobrenome.delete(0, 'end')
        entry_email.delete(0, 'end')
        entry_telefone.delete(0, 'end')
        entry_senha.delete(0, 'end')
        entry_con_senha.delete(0, 'end')

    # Menu superior
    def sobre():
        messagebox.showinfo("Sobre", "Janela de Cadastro de Usuário:\n"
                                     "Cadastro de usuários com intuito de logar"
                                     "\nno sistema de cadastramentos de filamentos 3D."
                                     "\n\nDesenvolvido por Vinicius Checchetto.")
        janela_ca.lift()

    menubar = Menu(janela_ca)
    janela_ca.config(menu=menubar)

    mainmenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Opções", menu=mainmenu)

    mainmenu.add_command(label="Salvar", command=lambda: inserir_dados(entry_cpf.get(), entry_nome.get(), entry_sobrenome.get(),
                                                           entry_email.get(), entry_telefone.get(), entry_senha.get(),
                                                           entry_con_senha.get(), janela_ca))
    mainmenu.add_command(label="Limpar", command=limpar_campos)
    mainmenu.add_separator()
    mainmenu.add_command(label="Sair", command=janela_ca.destroy)

    menubar.add_command(label="Sobre", command=sobre)

    # Frames
    frame_top = Frame(janela_ca, width=500, height=80, bg=cor00, relief="flat")
    frame_top.grid(row=0, column=0, pady=1, padx=0)

    frame_down = Frame(janela_ca, width=500, height=420, bg=cor01, relief="flat")
    frame_down.grid(row=1, column=0, pady=1, padx=0)

    # Frame Top
    label_titulo = Label(frame_top, text="CADASTRO", font="Bahnschrift 26", anchor=NW, fg=cor03, bg=cor00)
    label_titulo.place(x=10, y=10)

    label_linha = Label(frame_top, text="", font="Bahnschrift 1", width=460, anchor=NW, bg=cor02)
    label_linha.place(x=10, y=65)

    # Frame Down
    label_nome = Label(frame_down, text="Nome:", font="Calibri 12 bold", width=14, anchor=E, fg=cor03, bg=cor01)
    label_nome.place(x=10, y=25)
    entry_nome = Entry(frame_down, width=20, justify="left", font="Calibri 12", highlightthickness=1, relief="solid")
    entry_nome.place(x=180, y=25)

    label_sobrenome = Label(frame_down, text="Sobrenome:", font="Calibri 12 bold", width=14, anchor=E, fg=cor03,
                            bg=cor01)
    label_sobrenome.place(x=10, y=70)
    entry_sobrenome = Entry(frame_down, width=20, justify="left", font="Calibri 12", highlightthickness=1,
                            relief="solid")
    entry_sobrenome.place(x=180, y=70)

    label_cpf = Label(frame_down, text="CPF:", font="Calibri 12 bold", width=14, anchor=E, fg=cor03, bg=cor01)
    label_cpf.place(x=10, y=115)
    entry_cpf = Entry(frame_down, width=20, justify="left", font="Calibri 12", highlightthickness=1,
                      relief="solid")
    entry_cpf.place(x=180, y=115)

    label_telefone = Label(frame_down, text="Telefone:", font="Calibri 12 bold", width=14, anchor=E, fg=cor03, bg=cor01)
    label_telefone.place(x=10, y=160)
    entry_telefone = Entry(frame_down, width=20, justify="left", font="Calibri 12", highlightthickness=1,
                           relief="solid")
    entry_telefone.place(x=180, y=160)

    label_email = Label(frame_down, text="E-mail:", font="Calibri 12 bold", width=14, anchor=E, fg=cor03, bg=cor01)
    label_email.place(x=10, y=205)
    entry_email = Entry(frame_down, width=30, justify="left", font="Calibri 12", highlightthickness=1,
                        relief="solid")
    entry_email.place(x=180, y=205)

    label_senha = Label(frame_down, text="Senha:", font="Calibri 12 bold", width=14, anchor=E, fg=cor03, bg=cor01)
    label_senha.place(x=10, y=250)
    entry_senha = Entry(frame_down, show="•", width=20, justify="left", font="Calibri 12", highlightthickness=1,
                        relief="solid")
    entry_senha.place(x=180, y=250)

    label_con_senha = Label(frame_down, text="Confirmar Senha:", font="Calibri 12 bold", width=14, anchor=E, fg=cor03,
                            bg=cor01)
    label_con_senha.place(x=10, y=295)
    entry_con_senha = Entry(frame_down, show="•", width=20, justify="left", font="Calibri 12", highlightthickness=1,
                            relief="solid")
    entry_con_senha.place(x=180, y=295)

    botao_cadastrar = Button(frame_down, text="Confirmar", font="Calibri 12 bold", width=10, height=1, fg=cor00,
                             bg=cor02, relief=RAISED, overrelief=RIDGE,
                             command=lambda: inserir_dados(entry_cpf.get(), entry_nome.get(), entry_sobrenome.get(),
                                                           entry_email.get(), entry_telefone.get(), entry_senha.get(),
                                                           entry_con_senha.get(), janela_ca))
    botao_cadastrar.place(x=260, y=345)

    botao_voltar = Button(frame_down, text="Voltar", font="Calibri 12 bold", width=10, height=1, fg=cor00, bg=cor02,
                          relief=RAISED, overrelief=RIDGE, command=janela_ca.destroy)
    botao_voltar.place(x=130, y=345)

    janela_ca.mainloop()


def validar_email(email):
    email_valido = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+([.]\w+)+$"
    return re.match(email_valido, email)


def validar_nome(nome):
    nome_valido = r'^[a-zA-Z ]+$'
    return re.match(nome_valido, nome)


def validar_telefone(telefone):
    telefone_valido = r'^\d+$'
    return re.match(telefone_valido, telefone)


def inserir_dados(cpf, nome, sobrenome, email, telefone, senha, con_senha, janela):
    if senha == con_senha:
        if cpf and nome and sobrenome and email and telefone and senha and con_senha:
            if validar_email(email):
                if validar_nome(nome) and validar_nome(sobrenome):
                    if validar_telefone(telefone):
                        try:
                            db = "banco.db"
                            conn = sqlite3.connect(db)
                            cursor = conn.cursor()

                            cursor.execute("""
                                INSERT INTO usuario (cpf, nome, sobrenome, email, telefone, senha)
                                VALUES (?, ?, ?, ?, ?, ?)
                            """, (cpf, nome, sobrenome, email, telefone, senha))

                            conn.commit()
                            conn.close()

                            messagebox.showinfo("Confirmação.", "Cadastro realizado com sucesso.")
                            janela.destroy()
                        except Exception as e:
                            print("Erro na inserção de dados: ", e)
                            messagebox.showerror("Erro", "Erro ao cadastrar: " + str(e))
                    else:
                        messagebox.showwarning("Atenção!", "Informe um número de telefone válido (apenas números).")
                        janela_ca.lift()
                else:
                    messagebox.showwarning("Atenção!", "Informe um nome e sobrenome válidos.")
                    janela_ca.lift()
            else:
                messagebox.showwarning("Atenção!", "Informe um endereço de e-mail válido.")
                janela_ca.lift()
        else:
            messagebox.showwarning("Atenção!", "Preencha todos os campos.")
            janela_ca.lift()
    else:
        messagebox.showwarning("Atenção!", "Senhas não conferem!")


criar_banco()
