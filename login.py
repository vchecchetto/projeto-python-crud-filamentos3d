import tkinter as tk
import sqlite3
import cadastro as ca
import menu as m
from tkinter import messagebox, Menu, Frame, Label, Entry, Button, RAISED, RIDGE, NW


def bt_cadastrar():
    ca.janela_cadastro()


def limpar_campos():
    entry_usuario.delete(0, 'end')
    entry_senha.delete(0, 'end')


def bt_acessar(cpf_email, senha):
    cpf_email = entry_usuario.get()
    senha = entry_senha.get()

    try:
        conn = sqlite3.connect("banco.db")
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM usuario WHERE cpf=? OR email=?", (cpf_email, cpf_email))
        result = cursor.fetchone()

        if result is not None:
            db_cpf, _, _, _, _, db_senha = result

            if senha == db_senha:
                janela.destroy()
                messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
                m.janela_menu()
            else:
                messagebox.showerror("Erro", "Senha incorreta.")
        else:
            messagebox.showerror("Erro", "Usuário não encontrado.")

        conn.close()
    except Exception as e:
        print("Erro na consulta do banco: ", e)
        messagebox.showerror("Erro", "Erro na consulta do banco de dados.")


# >>> Interface Grafica <<<
def janela_login():
    global janela
    global entry_senha
    global entry_usuario
    # Cores
    cor00 = "#FFFAFA"     # Branco Neve
    cor01 = "#DCDCDC"     # Cinza Claro
    cor02 = "#4F4F4F"     # Cinza Escuro
    cor03 = "#1C1C1C"     # Preto

    # Janela
    janela = tk.Tk()
    janela.title("")
    width = 500
    height = 350
    screen_width = janela.winfo_screenwidth()
    screen_height = janela.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    janela.geometry(f"{width}x{height}+{x}+{y}")
    janela.configure(bg=cor00)
    janela.resizable(width=False, height=False)

    # Menu superior
    def sobre():
        messagebox.showinfo("Sobre", "Software desenvolvido com finalidade \nde cadastramento de filamentos 3D."
                                     "\n\nDesenvolvido por Vinicius Checchetto.")

    menubar = Menu(janela)
    janela.config(menu=menubar)

    mainmenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Opções", menu=mainmenu)

    mainmenu.add_command(label="Acessar", command=lambda: bt_acessar(entry_usuario.get(), entry_senha.get()))
    mainmenu.add_command(label="Cadastrar", command=bt_cadastrar)
    mainmenu.add_separator()
    mainmenu.add_command(label="Sair", command=janela.destroy)

    menubar.add_command(label="Sobre", command=sobre)

    # Frames
    frame_top = Frame(janela, width=500, height=80, bg=cor00, relief="flat")
    frame_top.grid(row=0, column=0, pady=1, padx=0)

    frame_down = Frame(janela, width=500, height=270, bg=cor01, relief="flat")
    frame_down.grid(row=1, column=0, pady=1, padx=0)

    # Frame Top
    label_titulo = Label(frame_top, text="LOGIN", font="Bahnschrift 26", anchor=NW, fg=cor03, bg=cor00)
    label_titulo.place(x=10, y=10)

    label_linha = Label(frame_top, text="", font="Bahnschrift 1", width=460, anchor=NW, bg=cor02)
    label_linha.place(x=10, y=65)

    # Frame Down
    label_usuario = Label(frame_down, text="Usuário:", font="Calibri 14 bold", anchor=NW, fg=cor03, bg=cor01)
    label_usuario.place(x=10, y=25)
    entry_usuario = Entry(frame_down, width=20, justify="left", font="Calibri 14", highlightthickness=1, relief="solid")
    entry_usuario.place(x=100, y=25)

    label_senha = Label(frame_down, text="Senha:", font="Calibri 14 bold", anchor=NW, fg=cor03, bg=cor01)
    label_senha.place(x=10, y=80)
    entry_senha = Entry(frame_down, show="•", width=20, justify="left", font="Calibri 14", highlightthickness=1,
                        relief="solid")
    entry_senha.place(x=100, y=80)

    botao_ok = Button(frame_down, text="Acessar", font="Calibri 14 bold", width=10, height=1, fg=cor00, bg=cor02,
                      relief=RAISED, overrelief=RIDGE,
                      command=lambda: bt_acessar(entry_usuario.get(), entry_senha.get()))
    botao_ok.place(x=350, y=45)

    botao_limpar = Button(frame_down, text="Limpar", font="Calibri 12 bold", width=10, height=1, fg=cor00, bg=cor02,
                          relief=RAISED, overrelief=RIDGE, command=limpar_campos)
    botao_limpar.place(x=80, y=180)

    botao_cadastrar = Button(frame_down, text="Cadastrar", font="Calibri 12 bold", width=10, height=1, fg=cor00,
                             bg=cor02,
                             relief=RAISED, overrelief=RIDGE, command=bt_cadastrar)
    botao_cadastrar.place(x=215, y=180)

    botao_sair = Button(frame_down, text="Sair", font="Calibri 12 bold", width=10, height=1, fg=cor00, bg=cor02,
                        relief=RAISED, overrelief=RIDGE, command=lambda: janela.destroy())
    botao_sair.place(x=350, y=180)

    janela.mainloop()
