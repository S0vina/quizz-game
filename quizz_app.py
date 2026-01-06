import tkinter as tk
from tkinter import messagebox
import json
import time

class QuizApp:
    def __init__(self, jsons, root):
        self.root = root
        self.root.title("Quizz")
        self.root.geometry("400x500")
        # O "container" onde as telas serão montadas
        self.container = tk.Frame(self.root)
        self.container.pack(expand=True, fill="both")

        self.i_question = 0 # Indice da pergunta atual

        # JSON das perguntas 
        self.questions_data = jsons

        self.temas_menu()

    def clean_screens(self):
    # Remove todos os widgets que estão dentro do container
        for widget in self.container.winfo_children():
            widget.destroy()

    def temas_menu(self):
        self.clean_screens()

        tk.Label(self.container, text="Escolha um tema", font=("Arial", 18, "bold")).pack(pady=20)
        
        temas = ["Historia", "Geografia", "Programacao", "Princesas"]

        for theme in temas:
            btn = tk.Button(self.container, text=theme, width=20, height=2, bg="white", fg="black", 
                            command=lambda t=theme: self.game_begin(t))
            btn.pack(pady=10)
        
        leave_btn = tk.Button(self.container, text="Sair", width=20, height=2, bg="white", fg="black", 
                            command=lambda : self.leave_game())
        leave_btn.pack(pady=10)

    def game_begin(self, theme):
        self.clean_screens()

        # Tela pre-jogo
        tk.Label(self.container, text=f"Tema escolhido {theme}! Comecando o quizz...", font=("arial", 20, "bold")).pack(pady=20)

        # Definindo quais perguntas do json serao usadas
        theme_questions = self.questions_data[theme]

        time.sleep(3)

        self.clean_screens()

        # Texto da pergunta
        current_question = theme_questions[self.i_question]["pergunta"]
        question = tk.Label(self.container, text=current_question, 
                font=("Arial", 14), pady=20, wraplength=350)
        question.pack()

        # Botões de Resposta
        botoes = []
        for i, opcao in enumerate(theme_questions[self.i_question]["opcoes"]):
            btn = tk.Button(self.container, text=opcao, width=30, height=2,
                            command=lambda i=i: self.verificar_resposta(i, botoes))
            btn.pack(pady=5)
            botoes.append(btn)
        
    def leave_game(self, theme):
        pass

    def criar_widgets(self):     

        # Mensagem de Feedback
        self.label_feedback = tk.Label(self.root, text="", font=("Arial", 12, "bold"))
        self.label_feedback.pack(pady=20)

    def verificar_resposta(self, indice_escolhido, b_list):
        indice_correto = self.pergunta_dados["correta"]

        if indice_escolhido == indice_correto:
            self.botoes[indice_escolhido].config(bg="green", fg="white")
            self.label_feedback.config(text="Você está certo!", fg="green")
        else:
            self.botoes[indice_escolhido].config(bg="red", fg="white")
            self.botoes[indice_correto].config(bg="green", fg="white") # Mostra a certa
            self.label_feedback.config(text="Resposta errada!", fg="red")

        # Desativar botões após a resposta para evitar múltiplos cliques
        for btn in self.botoes:
            btn.config(state="disabled")

    def next_question(self):
        self.i_question += 1
        
        if len(self.questions_data) > self.i_question:
            current_question = self.questions_data[self.i_question]["pergunta"]

            self.label_question.config(text=current_question["pergunta"])

            for i, btn in enumerate(self.botoes):
                btn.config(
                    text=current_question["opcoes"][i],
                    bg="white",   # Reseta o botao para a cor inicial
                    fg="black",   # Reseta o texto do botao para a cor inicial  
                    state="normal" # Reativa o botao
                )
            
            self.label_feedback.config(text="")

        else:
            self.end_game()

    def end_game(self):
        self.label_question.config(text="Parabéns! Você concluiu o Quizz.")
        for btn in self.botoes:
            btn.pack_forget()
        self.label_feedback.config("Voce concluiu o tema!")