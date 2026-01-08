import sys
import tkinter as tk
from tkinter import messagebox
import json
from PIL import Image, ImageTk
import os

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quizz") # Titulo da janela
        self.root.geometry("400x500") # Proporcao padrao do frame
        self.container = tk.Frame(self.root) # O "container" onde as telas serão montadas
        self.container.pack(expand=True, fill="both")

        self.i_question = 0 # Indice da pergunta atual

        self.theme_questions = [] # lista das perguntas de cada tema
        self.botoes = [] # Lista com os botoes criados
        
        self.continue_button = tk.Button()
        self.label_question = tk.Label(text="")
        self.label_feedback = tk.Label(text="")
        
        self.acertos = 0
        self.erros = 0

        self.foto = "assets/images/foto.jpg"
        self.theme_menu() # chama o menu de temas

    # Remove todos os widgets que estão dentro do container
    def clean_screens(self):
        for widget in self.container.winfo_children():
            widget.destroy()
        self.botoes = []

    # funcao de escolha do tema das perguntas
    def theme_menu(self):
        self.acertos = 0
        self.erros = 0
        self.i_question = 0
        self.clean_screens()

        tk.Label(self.container, text="Escolha um tema", font=("Arial", 18, "bold")).pack(pady=20)
        
        temas = ["Geografia", "Programacao", "Video-Games"]

        for theme in temas:
            btn = tk.Button(self.container, text=theme, width=20, height=2, bg="white", fg="black", 
                            command=lambda t=theme: self.game_begin(t))
            btn.pack(pady=10)
        
        leave_btn = tk.Button(self.container, text="Sair", width=20, height=2, bg="white", fg="black", 
                            command=self.leave_game)
        leave_btn.pack(pady=10)

    # Funcao que inicializa o frame de respostas e onde o jogo ocorre
    def game_begin(self, theme):
        self.clean_screens()

        # Carregando perguntas
        self.theme_questions = self.load_questions(theme)

        if not self.theme_questions:
            print(f"Erro: Nenhuma pergunta encontrada para o tema '{theme}'")
            messagebox.showerror("Erro", "Não foi possível carregar as perguntas deste tema.")
            return # Interrompe o código antes de dar o erro de index

        print(f"Perguntas carregadas: {self.theme_questions}")
        print(f"Total de perguntas: {len(self.theme_questions)}")

        # Texto da pergunta
        current_question = self.theme_questions[self.i_question]["pergunta"]
        self.label_question = tk.Label(self.container, text=current_question, 
                font=("Arial", 14), pady=20, wraplength=350)
        self.label_question.pack()

        # Botões de Resposta
        for i, opcao in enumerate(self.theme_questions[self.i_question]["opcoes"]):
            btn = tk.Button(self.container, text=opcao, width=30, height=2,
                            command=lambda i=i: self.answer_verification(i))
            btn.pack(pady=5)
            self.botoes.append(btn)

        self.label_feedback = tk.Label(self.container, text="", font=("Arial", 12, "bold"), state="disabled")
        self.label_feedback.pack(pady=10)
        
        self.continue_button = tk.Button(self.container, text="Continuar →", 
                               command=self.next_question, 
                               state="disabled", bg="blue", fg="white")
        self.continue_button.pack(pady=20)

    def end_game(self, foto):
        # 1. Limpa tudo o que está no container atual
        self.clean_screens()

        # 2. Cria a mensagem de vitória
        tk.Label(self.container, text="🎉 PARABÉNS! 🎉", 
             font=("Arial", 24, "bold"), fg="gold").pack(pady=30)
    
        tk.Label(self.container, text=f"Acertos: {self.acertos}", 
                 font=("Arial", 16, "bold"), fg="green").pack(pady=10)
        
        tk.Label(self.container, text=f"Erros: {self.erros}", 
                 font=("Arial", 16, "bold"), fg="red").pack(pady=10)

        tk.Label(self.container, text="Gostou? Vamos tentar de novo?", 
             font=("Arial", 14)).pack(pady=10)
        
        self.show_image(foto)

        # 3. Botão para voltar ao início e jogar outro tema
        btn_voltar = tk.Button(self.container, text="Voltar ao Menu", width=20, height=2,
                           command=self.theme_menu, bg="green", fg="white")
        btn_voltar.pack(pady=30)   

    def leave_game(self):
        # Exibe uma caixa de mensagem pop-up
        messagebox.showinfo("Fim de Jogo! Obrigado por jogar!")
    
        # "Mata" o script e fecha a janela
        self.root.destroy()

    def answer_verification(self, submit_answer):

        correct_answer = self.theme_questions[self.i_question]["correta"]

        if submit_answer == correct_answer:
            self.botoes[submit_answer].config(bg="green", fg="white")
            self.label_feedback.config(text="Você está certo!", fg="green")
            self.acertos += 1
        else:
            self.botoes[submit_answer].config(bg="red", fg="white")
            self.botoes[correct_answer].config(bg="green", fg="white") # Mostra a certa
            self.label_feedback.config(text="Resposta errada!", fg="red")
            self.erros += 1

        # Desativar botões após a resposta para evitar múltiplos cliques
        for btn in self.botoes:
            btn.config(state="disabled")
        
        # Ativa o botao de continue apos uma pergunta respondida
        self.continue_button.config(state="normal") 

    # Funcao que executa a logica de troca de perguntas 
    def next_question(self):
        self.i_question += 1
        
        if len(self.theme_questions) > self.i_question:
            current_question = self.theme_questions[self.i_question]

            self.label_question.config(text=current_question["pergunta"])

            for i, btn in enumerate(self.botoes):
                btn.config(
                    text=current_question["opcoes"][i],
                    bg="white",   # Reseta o botao para a cor inicial
                    fg="black",   # Reseta o texto do botao para a cor inicial  
                    state="normal" # Reativa o botao
                )
            
            self.label_feedback.config(text="disable")
            self.continue_button.config(state="disable")

        else:
            self.end_game(self.foto) # Tela de parabenizacao antes de voltar pro theme_menu
    
    # Funcao que carrega o Json das perguntas com o tema escolhido
    def load_questions(self, theme):
        # ANTES era: resource_path('perguntas.json')
        # AGORA com a pasta data:
        caminho_arquivo = self.resource_path('assets/data/perguntas.json') 
    
        try:
            with open(caminho_arquivo, 'r', encoding='utf-8') as f:
                todos_os_dados = json.load(f)
            return todos_os_dados.get(theme, [])
        except FileNotFoundError:
            print(f"Erro: O arquivo não foi encontrado em {caminho_arquivo}")
            return []
        
    def resource_path(self, relative_path):
        # Retorna o caminho absoluto para o recurso, seja no modo script ou no .exe """
        try:
            # O PyInstaller cria uma variável temporária chamada _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            # Se não estiver no modo .exe, usa o caminho normal da pasta atual
            base_path = os.path.abspath(".")

        return os.path.join(base_path, relative_path)
    
    def show_image(self, nome_arquivo):
        # 1. Abre a imagem
        img = Image.open(nome_arquivo)
    
        # 2. Redimensiona (opcional, mas recomendado para não quebrar o layout)
        img =  img.resize((200, 150))
    
        # 3. Converte para o Tkinter
        self.foto = ImageTk.PhotoImage(img)
    
        # 4. Exibe em um Label
        self.label_foto = tk.Label(self.container, image=self.foto)
        self.label_foto.pack(pady=10)
