import customtkinter as ctk
from tkinter import messagebox


class Livro:
    def __init__(self, titulo, autor, genero):
        self.titulo = titulo
        self.autor = autor
        self.genero = genero

class Usuario:
    def __init__(self, nome):
        self.nome = nome
        self.seguidores = []
        self.seguindo = []
        self.estante = {}

    def seguir(self, outro_usuario):
        self.seguindo.append(outro_usuario)
        outro_usuario.seguidores.append(self)

    def adicionar_livro_estante(self, livro, status):
        self.estante[livro] = status


usuarios = {}
livros = {}


def criar_usuario():
    nome = entry_usuario.get().strip()
    if not nome:
        messagebox.showwarning("Aviso", "Digite um nome!")
        return
    if nome in usuarios:
        messagebox.showerror("Erro", "Usuário já existe!")
    else:
        usuarios[nome] = Usuario(nome)
        messagebox.showinfo("Sucesso", f"Usuário '{nome}' criado!")
    entry_usuario.delete(0, "end")

def criar_livro():
    titulo = entry_titulo.get().strip()
    autor = entry_autor.get().strip()
    genero = entry_genero.get().strip()
    if not titulo or not autor or not genero:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")
        return
    if titulo in livros:
        messagebox.showerror("Erro", "Livro já cadastrado!")
    else:
        livros[titulo] = Livro(titulo, autor, genero)
        messagebox.showinfo("Sucesso", f"Livro '{titulo}' criado!")
    entry_titulo.delete(0, "end")
    entry_autor.delete(0, "end")
    entry_genero.delete(0, "end")

def adicionar_livro_estante():
    usuario_nome = entry_usuario_estante.get().strip()
    livro_titulo = entry_livro_estante.get().strip()
    status = combo_status.get()

    if usuario_nome not in usuarios:
        messagebox.showerror("Erro", "Usuário não encontrado!")
        return
    if livro_titulo not in livros:
        messagebox.showerror("Erro", "Livro não encontrado!")
        return

    usuarios[usuario_nome].adicionar_livro_estante(livros[livro_titulo], status)
    messagebox.showinfo("Sucesso", f"Livro '{livro_titulo}' adicionado à estante de {usuario_nome}!")

def seguir_usuario():
    seguidor = entry_seguidor.get().strip()
    seguido = entry_seguido.get().strip()
    if seguidor not in usuarios or seguido not in usuarios:
        messagebox.showerror("Erro", "Usuário(s) não encontrado(s)!")
        return
    usuarios[seguidor].seguir(usuarios[seguido])
    messagebox.showinfo("Sucesso", f"{seguidor} agora segue {seguido}!")

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Sistema de Livros")
app.geometry("600x700")

# Criar usuário
ctk.CTkLabel(app, text="Criar Usuário").pack(pady=5)
entry_usuario = ctk.CTkEntry(app, placeholder_text="Nome do usuário")
entry_usuario.pack()
ctk.CTkButton(app, text="Criar", command=criar_usuario).pack(pady=5)

# Criar livro
ctk.CTkLabel(app, text="Criar Livro").pack(pady=5)
entry_titulo = ctk.CTkEntry(app, placeholder_text="Título")
entry_titulo.pack()
entry_autor = ctk.CTkEntry(app, placeholder_text="Autor")
entry_autor.pack()
entry_genero = ctk.CTkEntry(app, placeholder_text="Gênero")
entry_genero.pack()
ctk.CTkButton(app, text="Adicionar Livro", command=criar_livro).pack(pady=5)

# Adicionar livro à estante
ctk.CTkLabel(app, text="Adicionar Livro à Estante").pack(pady=5)
entry_usuario_estante = ctk.CTkEntry(app, placeholder_text="Nome do usuário")
entry_usuario_estante.pack()
entry_livro_estante = ctk.CTkEntry(app, placeholder_text="Título do livro")
entry_livro_estante.pack()
combo_status = ctk.CTkComboBox(app, values=["lido", "lendo", "abandonado"])
combo_status.pack()
ctk.CTkButton(app, text="Adicionar", command=adicionar_livro_estante).pack(pady=5)

# Seguir usuário
ctk.CTkLabel(app, text="Seguir Usuário").pack(pady=5)
entry_seguidor = ctk.CTkEntry(app, placeholder_text="Seu nome")
entry_seguidor.pack()
entry_seguido = ctk.CTkEntry(app, placeholder_text="Nome da pessoa a seguir")
entry_seguido.pack()
ctk.CTkButton(app, text="Seguir", command=seguir_usuario).pack(pady=5)

app.mainloop()


