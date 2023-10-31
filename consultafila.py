import tkinter as tk
import sqlite3
import sys
from tkinter import ttk, messagebox, Menu, Frame, Label, Entry, Button, Toplevel, RAISED, RIDGE, E, NW


# >>> Interface Grafica <<<
def janela_consulta():
    global escolha_tipo, escolha_cor, escolha_fabri, escolha_peso, entry_preco, janela_cons

    # Cores
    cor00 = "#FFFAFA"  # Branco Neve
    cor01 = "#DCDCDC"  # Cinza Claro
    cor02 = "#4F4F4F"  # Cinza Escuro
    cor03 = "#1C1C1C"  # Preto

    # Janela
    janela_cons = tk.Tk()
    janela_cons.title("")
    width = 500
    height = 500
    screen_width = janela_cons.winfo_screenwidth()
    screen_height = janela_cons.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    janela_cons.geometry(f"{width}x{height}+{x}+{y}")
    janela_cons.configure(bg=cor00)
    janela_cons.resizable(width=False, height=False)

    # Menu superior
    def sobre():
        messagebox.showinfo("Sobre", "Janela de Consulta de filamentos:\n"
                                     "Consulte informações essenciais sobre filamentos"
                                     "\n3D de forma rápida e intuitiva."
                                     "\n\nDesenvolvido por Vinicius Checchetto.")
        janela_cons.lift()

    menubar = Menu(janela_cons)
    janela_cons.config(menu=menubar)

    mainmenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Opções", menu=mainmenu)

    mainmenu.add_command(label="Editar", command=lambda: editar_filamento(tree))
    mainmenu.add_command(label="Excluir", command=lambda: excluir_filamento(tree))
    mainmenu.add_separator()
    mainmenu.add_command(label="Sair", command=janela_cons.destroy)

    menubar.add_command(label="Sobre", command=sobre)

    # Frames
    frame_top = Frame(janela_cons, width=500, height=80, bg=cor00, relief="flat")
    frame_top.grid(row=0, column=0, pady=1, padx=0)

    frame_down = Frame(janela_cons, width=500, height=420, bg=cor01, relief="flat")
    frame_down.grid(row=1, column=0, pady=1, padx=0)

    # Frame Top
    label_titulo = Label(frame_top, text="CONSULTAR FILAMENTOS", font="Bahnschrift 26", anchor=NW, fg=cor03, bg=cor00)
    label_titulo.place(x=10, y=10)

    label_linha = Label(frame_top, text="", font="Bahnschrift 1", width=460, anchor=NW, bg=cor02)
    label_linha.place(x=10, y=65)

    # Frame Down
    tree = ttk.Treeview(frame_down)
    tree["columns"] = ("Tipo", "Cor", "Fabricante", "Peso", "Preço")

    tree.column("#0", width=0, stretch=tk.NO)
    tree.column("Tipo", width=115)
    tree.column("Cor", width=115)
    tree.column("Fabricante", width=80)
    tree.column("Peso", width=50)
    tree.column("Preço", width=70)

    tree.heading("#0", text="", anchor=NW)
    tree.heading("Tipo", text="Tipo", anchor=NW)
    tree.heading("Cor", text="Cor", anchor=NW)
    tree.heading("Fabricante", text="Fabricante", anchor=NW)
    tree.heading("Peso", text="Peso", anchor=NW)
    tree.heading("Preço", text="Preço", anchor=NW)

    resultados = consultar_filamento()

    for resultado in resultados:
        id_filamento = resultado[0]
        valores = (resultado[1], resultado[2], resultado[3], resultado[4], resultado[5])
        tree.insert("", tk.END, text=id_filamento, values=valores)

    tree.place(x=30, y=30)
    tree["height"] = 11

    botao_voltar = Button(frame_down, text="Voltar", font="Calibri 12 bold", width=10, height=1, fg=cor00, bg=cor02,
                          relief=RAISED, overrelief=RIDGE, command=janela_cons.destroy)
    botao_voltar.place(x=70, y=315)

    botao_excluir = Button(frame_down, text="Excluir", font="Calibri 12 bold", width=10, height=1, fg=cor00,
                           bg=cor02, relief=RAISED, overrelief=RIDGE, command=lambda: excluir_filamento(tree))
    botao_excluir.place(x=190, y=315)

    botao_editar = Button(frame_down, text="Editar", font="Calibri 12 bold", width=10, height=1, fg=cor00,
                          bg=cor02, relief=RAISED, overrelief=RIDGE, command=lambda: editar_filamento(tree))
    botao_editar.place(x=310, y=315)

    janela_cons.mainloop()


def excluir_filamento(tree):
    item_selecionado = tree.focus()
    if item_selecionado:
        resposta = messagebox.askquestion("Confirmação", "Tem certeza que deseja excluir?",
                                          icon='warning')
        if resposta == 'yes':
            conn = sqlite3.connect("bancofila.db")
            cursor = conn.cursor()
            id_filamento = tree.item(item_selecionado)["text"]
            cursor.execute("DELETE FROM filamentos WHERE rowid=?", (id_filamento,))
            conn.commit()
            conn.close()
            messagebox.showinfo("Sucesso", "Excluído com sucesso!")
            tree.delete(item_selecionado)
        else:
            janela_cons.lift()
    else:
        messagebox.showwarning("Aviso", "Nenhum item selecionado.")
        janela_cons.lift()


def consultar_filamento():
    try:
        conn = sqlite3.connect("bancofila.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM filamentos")
        resultados = cursor.fetchall()
        conn.close()
        return resultados
    except Exception as e:
        print("Erro na consulta de filamentos: ", e)


def editar_filamento(tree):
    item_selecionado = tree.focus()
    if item_selecionado:
        id_filamento = tree.item(item_selecionado)["text"]
        janela_edicao(id_filamento)
    else:
        messagebox.showwarning("Aviso", "Nenhum item selecionado.")
        janela_cons.lift()


def janela_edicao(id_filamento):
    global escolha_tipo, escolha_cor, escolha_fabri, escolha_peso, entry_preco, janela_ed

    def voltar_janela_cons():
        global janela_cons, janela_ed
        janela_ed.destroy()
        janela_cons.deiconify()

    # Cores
    cor00 = "#FFFAFA"  # Branco Neve
    cor01 = "#DCDCDC"  # Cinza Claro
    cor02 = "#4F4F4F"  # Cinza Escuro
    cor03 = "#1C1C1C"  # Preto

    # Janela
    janela_ed = Toplevel()
    janela_ed.title("")
    width = 500
    height = 500
    screen_width = janela_ed.winfo_screenwidth()
    screen_height = janela_ed.winfo_screenheight()
    x = int((screen_width / 2) - (width / 2))
    y = int((screen_height / 2) - (height / 2))
    janela_ed.geometry(f"{width}x{height}+{x}+{y}")
    janela_ed.configure(bg=cor02)
    janela_ed.resizable(width=False, height=False)

    # Menu superior
    def sobre():
        messagebox.showinfo("Sobre", "Janela de edição:\n"
                                     "Edite as informações dos filamentos 3D \njá cadastrados."
                                     "\n\nDesenvolvido por Vinicius Checchetto.")
        janela_ed.lift()

    menubar = Menu(janela_ed)
    janela_ed.config(menu=menubar)

    mainmenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Opções", menu=mainmenu)

    mainmenu.add_command(label="Salvar", command=lambda: salvar_edicao(id_filamento))
    mainmenu.add_separator()
    mainmenu.add_command(label="Sair", command=janela_ed.destroy)

    menubar.add_command(label="Sobre", command=sobre)

    # Frames
    frame_top = Frame(janela_ed, width=500, height=80, bg=cor00, relief="flat")
    frame_top.grid(row=0, column=0, pady=1, padx=0)

    frame_down = Frame(janela_ed, width=500, height=420, bg=cor01, relief="flat")
    frame_down.grid(row=1, column=0, pady=1, padx=0)

    # Frame Top
    label_titulo = Label(frame_top, text="EDITAR DADOS", font="Bahnschrift 26", anchor=NW, fg=cor03, bg=cor00)
    label_titulo.place(x=10, y=10)

    label_linha = Label(frame_top, text="", font="Bahnschrift 1", width=460, anchor=NW, bg=cor02)
    label_linha.place(x=10, y=65)

    filamento = obter_filamento_por_id(id_filamento)

    if filamento is not None:
        tipo_filamento = filamento[1]
        cor_filamento = filamento[2]
        fabricante_filamento = filamento[3]
        peso_filamento = filamento[4]
        preco_filamento = filamento[5]

        label_tipo = Label(frame_down, text="Tipo:", font="Calibri 12 bold", width=14, anchor=E, fg=cor03, bg=cor01)
        label_tipo.place(x=0, y=50)

        valores_tipo = ("ABS", "ABS Premium", "Eco (Low Cost)", "PETG", "PLA", "PLA Easyfill", "PLA Premium", "Tritan",
                        "Nylon", "Fibra de Carbono", "Wood", "HIPS", "Condutivo", "ABS Antichamas")
        valores_ordenados = sorted(valores_tipo)
        t = tk.StringVar(value=tipo_filamento)  # Tipo de Filamento
        escolha_tipo = ttk.Combobox(frame_down, width=20, font="Calibri 12", textvariable=t)
        escolha_tipo["values"] = valores_ordenados
        escolha_tipo.place(x=170, y=50)

        label_cor = Label(frame_down, text="Cor:", font="Calibri 12 bold", width=14, anchor=E, fg=cor03, bg=cor01)
        label_cor.place(x=0, y=95)

        opcoes_cor = ("Preto", "Azul", "Azul Metal", "Branco", "Branco Gesso", "Branco Neve", "Cinza", "Cinza Escuro",
                      "Fosforescente", "Laranja", "Marfim", "Mármore", "Natural", "Rosa", "Verde", "Verde Limão",
                      "Verde Metal", "Vermelho", "Vermelho Metal", "Transparente", "Verde Água", "Cobre", "Prata",
                      "Marrom",
                      "Pink", "Pérola", "Areia", "Madeira Escura", "Madeira Clara", "Ouro", "Azul Sky", "Azul Bebê",
                      "Azul Claro", "Verde Escuro", "Verde Musgo", "Verde Abacate", "Vermelho Ferrari",
                      "Vermelho Cereja",
                      "Bicolor", "Eco (Low Cost)")
        cores_ordenadas = sorted(opcoes_cor)
        c = tk.StringVar(value=cor_filamento)  # Cor do Filamento
        escolha_cor = ttk.Combobox(frame_down, width=20, font="Calibri 12", textvariable=c)
        escolha_cor["values"] = cores_ordenadas
        escolha_cor.place(x=170, y=95)

        label_fabri = Label(frame_down, text="Fabricante:", font="Calibri 12 bold", width=14, anchor=E, fg=cor03,
                            bg=cor01)
        label_fabri.place(x=0, y=140)

        valores_fabricantes = ("Creality", "3D Fila", "3D Lab", "Voolt 3D", "3D Prime", "Up 3D", "F3D Brasil", "Esun")
        fabricantes_ordenados = sorted(valores_fabricantes)

        f = tk.StringVar(value=fabricante_filamento)  # Fabricante
        escolha_fabri = ttk.Combobox(frame_down, width=20, font="Calibri 12", textvariable=f)
        escolha_fabri["values"] = fabricantes_ordenados
        escolha_fabri.place(x=170, y=140)

        label_peso = Label(frame_down, text="Peso:", font="Calibri 12 bold", width=14, anchor=E, fg=cor03, bg=cor01)
        label_peso.place(x=0, y=185)

        p = tk.StringVar(value=peso_filamento)  # Peso
        escolha_peso = ttk.Combobox(frame_down, width=20, font="Calibri 12", textvariable=p, state="readonly")
        escolha_peso["values"] = ("75g", "250g", "500g", "1kg")
        escolha_peso.place(x=170, y=185)

        label_preco = Label(frame_down, text="Preço:", font="Calibri 12 bold", width=14, anchor=E, fg=cor03, bg=cor01)
        label_preco.place(x=0, y=230)

        entry_preco = Entry(frame_down, width=22, justify="left", font="Calibri 12", highlightthickness=1,
                            relief="solid")
        entry_preco.place(x=170, y=230)
        entry_preco.insert(0, preco_filamento)

        botao_salvar = Button(frame_down, text="Salvar", font="Calibri 12 bold", width=10, height=1, fg=cor00, bg=cor02,
                              relief=RAISED, overrelief=RIDGE, command=lambda: salvar_edicao(id_filamento))
        botao_salvar.place(x=260, y=315)

        botao_cancel = Button(frame_down, text="Cancelar", font="Calibri 12 bold", width=10, height=1, fg=cor00,
                              bg=cor02, relief=RAISED, overrelief=RIDGE, command=voltar_janela_cons)
        botao_cancel.place(x=130, y=315)

    janela_ed.mainloop()


def obter_filamento_por_id(id_filamento):
    try:
        conn = sqlite3.connect("bancofila.db")
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM filamentos WHERE rowid=?", (id_filamento,))
        resultado = cursor.fetchone()
        conn.close()
        return resultado
    except Exception as e:
        print("Erro ao obter filamento por ID:", e)


def salvar_edicao(id_filamento):
    global escolha_tipo, escolha_cor, escolha_fabri, escolha_peso, entry_preco
    conn = sqlite3.connect('bancofila.db')
    cursor = conn.cursor()

    try:
        tipo = escolha_tipo.get()
        cor = escolha_cor.get()
        fabricante = escolha_fabri.get()
        peso = escolha_peso.get()
        preco = entry_preco.get()

        if tipo and cor and fabricante and peso and preco:
            if preco and not preco.startswith("R$"):
                preco = "R$" + preco

            mensagem = f"Tipo: {tipo}\nCor: {cor}\nFabricante: {fabricante}" \
                       f"\nPeso: {peso}\nPreço: {preco}\n\nDeseja salvar as alterações?"
            resposta = messagebox.askquestion("Confirmação", mensagem)

            if resposta == "yes":
                cursor.execute("""
                        UPDATE filamentos
                        SET tipo = ?,
                            cor = ?,
                            fabricante = ?,
                            peso = ?,
                            preco = ?
                        WHERE id_filamento = ?
                    """, (tipo, cor, fabricante, peso, preco, id_filamento))
                conn.commit()
                messagebox.showinfo("Sucesso", "Os dados foram atualizados com sucesso.")
                janela_ed.destroy()
                janela_cons.destroy()
                sys.modules[__name__].janela_consulta()
            else:
                messagebox.showinfo("Aviso", "Alterações descartadas.")
                janela_ed.destroy()
                janela_cons.lift()
        else:
            messagebox.showwarning("Aviso", "Por favor, preencha todos os campos.")
            janela_ed.lift()
    except Exception as e:
        conn.rollback()
        messagebox.showerror("Erro", f"Ocorreu um erro ao atualizar os dados no banco de dados: {str(e)}")
    finally:
        conn.close()
