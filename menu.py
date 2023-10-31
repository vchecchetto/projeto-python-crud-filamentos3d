import tkinter as tk
from tkinter import messagebox, Frame, Menu, Label, Button, RAISED, RIDGE, NW
from PIL import ImageTk, Image
import cadastrofila as caf
import consultafila as cof


# >>> Interface Grafica <<<
def janela_menu():
    # Cores
    cor00 = "#FFFAFA"  # Branco Neve
    cor01 = "#DCDCDC"  # Cinza Claro
    cor02 = "#4F4F4F"  # Cinza Escuro
    cor03 = "#1C1C1C"  # Preto

    # Janela
    janela_m = tk.Tk()
    janela_m.title("")
    width=500
    height=500
    screen_width=janela_m.winfo_screenwidth()
    screen_height=janela_m.winfo_screenheight()
    x=int((screen_width/2)-(width/2))
    y=int((screen_height/2)-(height/2))
    janela_m.geometry(f"{width}x{height}+{x}+{y}")
    janela_m.configure(bg=cor00)
    janela_m.resizable(width=False, height=False)

    # Menu superior
    def sobre():
        messagebox.showinfo("Sobre", "Software desenvolvido com fim de \ncadastramento de filamentos 3D."
                                     "\n\nDesenvolvido por Vinicius Checchetto.")
        janela_m.lift()

    menubar = Menu(janela_m)
    janela_m.config(menu=menubar)

    mainmenu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Opções", menu=mainmenu)

    mainmenu.add_command(label="Cadastrar", command=lambda: caf.janela_cadastrofila())
    mainmenu.add_command(label="Consultar", command=lambda: cof.janela_consulta())
    mainmenu.add_separator()
    mainmenu.add_command(label="Sair", command=janela_m.destroy)

    menubar.add_command(label="Sobre", command=sobre)

    # Frames
    frame_top = Frame(janela_m, width=500, height=80, bg=cor00, relief="flat")
    frame_top.grid(row=0, column=0, pady=1, padx=0)

    frame_down = Frame(janela_m, width=500, height=420, bg=cor01, relief="flat")
    frame_down.grid(row=1, column=0, pady=1, padx=0)

    # Frame Top
    label_titulo = Label(frame_top, text="FILAMENTOS 3D", font="Bahnschrift 26", anchor=NW, fg=cor03, bg=cor00)
    label_titulo.place(x=10, y=10)

    label_linha = Label(frame_top, text="", font="Bahnschrift 1", width=460, anchor=NW, bg=cor02)
    label_linha.place(x=10, y=65)

    # Frame Down
    botao_cad_fil = Button(frame_down, text="Cadastrar", font="Calibri 12 bold", width=20, height=1, fg=cor00, bg=cor02,
                           relief=RAISED, overrelief=RIDGE, command=lambda: caf.janela_cadastrofila())
    botao_cad_fil.place(x=65, y=30)

    botao_cons_fil = Button(frame_down, text="Consultar", font="Calibri 12 bold", width=20, height=1, fg=cor00,
                            bg=cor02, relief=RAISED, overrelief=RIDGE, command=lambda: cof.janela_consulta())
    botao_cons_fil.place(x=65, y=90)

    botao_sair = Button(frame_down, text="Sair", font="Calibri 12 bold", width=10, height=1, fg=cor00, bg=cor02,
                        relief=RAISED, overrelief=RIDGE, command=janela_m.destroy)
    botao_sair.place(x=350, y=345)

    imagem_3d = Image.open("imagens/3d.png")
    tamanho = 130
    imagem_3d.thumbnail((tamanho, tamanho))
    img3d = ImageTk.PhotoImage(imagem_3d)
    imagem3d = Label(frame_down, image=img3d, bg=cor01)
    imagem3d.place(x=340, y=10)

    imagem_cad = Image.open("imagens/cadastrar.png")
    tamanho = 30
    imagem_cad.thumbnail((tamanho, tamanho))
    imgcad = ImageTk.PhotoImage(imagem_cad)
    imagemcad = Label(frame_down, image=imgcad, bg=cor01)
    imagemcad.place(x=15, y=33)

    imagem_cons = Image.open("imagens/consulta.png")
    tamanho = 35
    imagem_cons.thumbnail((tamanho, tamanho))
    imgcons = ImageTk.PhotoImage(imagem_cons)
    imagemcons = Label(frame_down, image=imgcons, bg=cor01)
    imagemcons.place(x=15, y=90)

    janela_m.mainloop()
