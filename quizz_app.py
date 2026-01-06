import tkinter as tk
from tkinter import messagebox
import json
import time

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quizz")
        self.root.geometry("400x500")
        # O "container" onde as telas serão montadas
        self.container = tk.Frame(self.root)
        self.container.pack(expand=True, fill="both")

        self.i_question = 0 # Indice da pergunta atual

        self.theme_questions = []

        self.botoes = []
        
        self.continue_button = tk.Button()
        self.label_question = tk.Label(text="")
        self.label_feedback = tk.Label(text="")

        self.theme_menu()

    def clean_screens(self):
    # Remove todos os widgets que estão dentro do container
        for widget in self.container.winfo_children():
            widget.destroy()

    def theme_menu(self):
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

        # Definindo quais perguntas do json serao usadas
        self.theme_questions = self.load_questions(theme)

        # Texto da pergunta
        self.current_question = self.theme_questions[self.i_question]["pergunta"]
        question = tk.Label(self.container, text=self.current_question, 
                font=("Arial", 14), pady=20, wraplength=350)
        question.pack()

        # Botões de Resposta
        for i, opcao in enumerate(self.theme_questions[self.i_question]["opcoes"]):
            btn = tk.Button(self.container, text=opcao, width=30, height=2,
                            command=lambda i=i: self.verificar_resposta(i))
            btn.pack(pady=5)
            self.botoes.append(btn)
        
        self.continue_button = tk.Button(self.container, text="Continuar →", 
                               command=self.next_question(self.theme_questions), 
                               state="disabled", bg="blue", fg="white")
        self.continue_button.pack(pady=20)

    def leave_game(self, theme):
        pass     

    def verificar_resposta(self, indice_escolhido):

        indice_correto = self.theme_questions[self.i_question]["correta"]

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
        
        self.continue_button.config(state="normal")

    def next_question(self, current_question):
        self.i_question += 1
        
        if len(self.theme_questions) > self.i_question:
            current_question = self.theme_questions[self.i_question]

            self.label_question.config(text=current_question)

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
            self.theme_menu()

    def end_game(self):
        self.label_question.config(text="Parabéns! Você concluiu o Quizz.")
        for btn in self.botoes:
            btn.pack_forget()
        self.label_feedback.config("Voce concluiu o tema!")

    def load_questions(self, theme):
        with open('perguntas.json', 'r', encoding='utf-8') as f:
            todos_os_dados = json.load(f)
    
        # Retorna a lista de perguntas do tema ou uma lista vazia se não existir
        return todos_os_dados.get(theme, [])
