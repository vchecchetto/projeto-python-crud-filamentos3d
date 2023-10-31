import tkinter as tk
import sqlite3
from tkinter import ttk, messagebox, Menu, Frame, Label, Entry, Button, Toplevel, RAISED, RIDGE, E, NW


def criar_bancofila():
    try:
        db = "bancofila.db"
        conn = sqlite3.connect(db)
        cursor = conn.cursor()
        cursor.execute("""
                   CREATE TABLE IF NOT EXISTS filamentos (
                       id_filamento INTEGER PRIMARY KEY AUTOINCREMENT,
                       tipo TEXT NOT NULL,
                       cor TEXT NOT NULL,
                       fabricante TEXT NOT NULL,
                       peso TEXT NOT NULL,
                       preco REAL NOT NULL
                   ); """)
        conn.commit()
    except Exception as e:
        print("Erro na criação do banco: ", e)


# >>> Interface Grafica <<<
def janela_cadastrofila():
    global escolha_tipo, escolha_cor, escolha_fabri, escolha_peso, entry_preco, janela_cad

    # Cores
    cor00 = "#FFFAFA"  # Branco Neve
    cor01 = "#DCDCDC"  # Cinza Claro
    cor02 = "#4F4F4F"  # Cinza Escuro
    cor03 = "#1C1C1C"  # Preto

    # Janela
    janela_cad = Toplevel()
    janela_cad.title("")
    width = 500
    height = 500
    screen_width = janela_cad.winfo_screenwidth()
    screen_height = janela_cad.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    janela_cad.geometry(f"{width}x{height}+{x}+{y}")
    janela_cad.configure(bg=cor00)
    janela_cad.resizable(width=False, height=False)

    # Menu superior
    def sobre():
        messagebox.showinfo("Sobre", "Janela de cadastro de filamentos:\n"
                                     "Gerencie e registre informações essenciais sobre"
                                     "\nfilamentos 3D de forma rápida e intuitiva."
                                     "\n\nDesenvolvido por Vinicius Checchetto.")
        janela_cad.lift()

    menubar = Menu(janela_cad)
    janela_cad.config(menu=menubar)

    mainmenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Opções", menu=mainmenu)

    mainmenu.add_command(label="Salvar", command=inserir_filamento)
    mainmenu.add_separator()
    mainmenu.add_command(label="Sair", command=janela_cad.destroy)

    menubar.add_command(label="Sobre", command=sobre)

    # Frames
    frame_top = Frame(janela_cad, width=500, height=80, bg=cor00, relief="flat")
    frame_top.grid(row=0, column=0, pady=1, padx=0)

    frame_down = Frame(janela_cad, width=500, height=420, bg=cor01, relief="flat")
    frame_down.grid(row=1, column=0, pady=1, padx=0)

    # Frame Top
    label_titulo = Label(frame_top, text="CADASTRAR FILAMENTO", font="Bahnschrift 26", anchor=NW, fg=cor03, bg=cor00)
    label_titulo.place(x=10, y=10)

    label_linha = Label(frame_top, text="", font="Bahnschrift 1", width=460, anchor=NW, bg=cor02)
    label_linha.place(x=10, y=65)

    # Frame Down
    label_tipo = Label(frame_down, text="Tipo:", font="Calibri 12 bold", width=14, anchor=E, fg=cor03,
                       bg=cor01)
    label_tipo.place(x=0, y=50)

    valores_tipo = ("ABS", "ABS Premium", "Eco (Low Cost)", "PETG", "PLA", "PLA Easyfill", "PLA Premium", "Tritan",
                    "Nylon", "Fibra de Carbono", "Wood", "HIPS", "Condutivo", "ABS Antichamas")
    valores_ordenados = sorted(valores_tipo)
    t = tk.StringVar()  # Tipo de Filamento
    escolha_tipo = ttk.Combobox(frame_down, width=20, font="Calibri 12", textvariable=t)
    escolha_tipo["values"] = valores_ordenados
    escolha_tipo.place(x=170, y=50)
    escolha_tipo.current()

    label_cor = Label(frame_down, text="Cor:", font="Calibri 12 bold", width=14, anchor=E, fg=cor03,
                      bg=cor01)
    label_cor.place(x=0, y=95)

    opcoes_cor = ("Preto", "Azul", "Azul Metal", "Branco", "Branco Gesso", "Branco Neve", "Cinza", "Cinza Escuro",
                  "Fosforescente", "Laranja", "Marfim", "Mármore", "Natural", "Rosa", "Verde", "Verde Limão",
                  "Verde Metal", "Vermelho", "Vermelho Metal", "Transparente", "Verde Água", "Cobre", "Prata", "Marrom",
                  "Pink", "Pérola", "Areia", "Madeira Escura", "Madeira Clara", "Ouro", "Azul Sky", "Azul Bebê",
                  "Azul Claro", "Verde Escuro", "Verde Musgo", "Verde Abacate", "Vermelho Ferrari", "Vermelho Cereja",
                  "Bicolor", "Eco (Low Cost)")
    cores_ordenadas = sorted(opcoes_cor)
    c = tk.StringVar()  # Cor do Filamento
    escolha_cor = ttk.Combobox(frame_down, width=20, font="Calibri 12", textvariable=c)
    escolha_cor["values"] = cores_ordenadas
    escolha_cor.place(x=170, y=95)
    escolha_cor.current()

    label_fabri = Label(frame_down, text="Fabricante:", font="Calibri 12 bold", width=14, anchor=E, fg=cor03, bg=cor01)
    label_fabri.place(x=0, y=140)

    valores_fabricantes = ("Creality", "3D Fila", "3D Lab", "Voolt 3D", "3D Prime", "Up 3D", "F3D Brasil", "Esun")
    fabricantes_ordenados = sorted(valores_fabricantes)

    f = tk.StringVar()  # Fabricante
    escolha_fabri = ttk.Combobox(frame_down, width=20, font="Calibri 12", textvariable=f)
    escolha_fabri["values"] = fabricantes_ordenados
    escolha_fabri.place(x=170, y=140)
    escolha_fabri.current()

    label_peso = Label(frame_down, text="Peso:", font="Calibri 12 bold", width=14, anchor=E, fg=cor03, bg=cor01)
    label_peso.place(x=0, y=185)

    p = tk.StringVar()  # Peso
    escolha_peso = ttk.Combobox(frame_down, width=20, font="Calibri 12", textvariable=p, state="readonly")
    escolha_peso["values"] = ("75g", "250g", "500g", "1kg")
    escolha_peso.place(x=170, y=185)
    escolha_peso.current()

    label_preco = Label(frame_down, text="Preço:", font="Calibri 12 bold", width=14, anchor=E, fg=cor03,
                        bg=cor01)
    label_preco.place(x=0, y=230)

    entry_preco = Entry(frame_down, width=22, justify="left", font="Calibri 12", highlightthickness=1, relief="solid")
    entry_preco.place(x=170, y=230)

    botao_cadastrar = Button(frame_down, text="Cadastrar", font="Calibri 12 bold", width=10, height=1, fg=cor00,
                             bg=cor02, relief=RAISED, overrelief=RIDGE, command=inserir_filamento)
    botao_cadastrar.place(x=260, y=315)

    botao_voltar = Button(frame_down, text="Voltar", font="Calibri 12 bold", width=10, height=1, fg=cor00, bg=cor02,
                          relief=RAISED, overrelief=RIDGE, command=janela_cad.destroy)
    botao_voltar.place(x=130, y=315)

    janela_cad.mainloop()


def inserir_filamento():
    global escolha_tipo, escolha_cor, escolha_fabri, escolha_peso, entry_preco, janela_cad
    tipo = escolha_tipo.get()
    cor = escolha_cor.get()
    fabricante = escolha_fabri.get()
    peso = escolha_peso.get()
    preco = entry_preco.get()

    if tipo and cor and fabricante and peso and preco:
        if preco and not preco.startswith("R$"):
            preco = "R$" + preco

        try:
            conn = sqlite3.connect("bancofila.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO filamentos (tipo, cor, fabricante, peso, preco) VALUES (?, ?, ?, ?, ?)",
                           (tipo, cor, fabricante, peso, preco))
            conn.commit()
            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!")
            conn.close()

            escolha_tipo.delete(0, 'end')
            escolha_cor.delete(0, 'end')
            escolha_fabri.delete(0, 'end')
            escolha_peso.delete(0, 'end')
            entry_preco.delete(0, 'end')

            resposta = messagebox.askquestion("Opções", "Deseja adicionar outro filamento?",
                                              icon='question')
            if resposta == 'yes':
                janela_cad.lift()
            else:
                janela_cad.destroy()

        except Exception as e:
            messagebox.showerror("Erro", "Erro ao cadastrar filamento: " + str(e))
    else:
        messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
        janela_cad.lift()


criar_bancofila()
