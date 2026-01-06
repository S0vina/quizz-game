import tkinter as tk
from tkinter import messagebox

class QuizApp:
    def __init__(self, questions, root):
        self.root = root
        self.root.title("Quiz")
        self.root.geometry("400x400")
        self.i_question = 0 # Indice da pergunta atual

        # Dados da pergunta (Poderia vir de um arquivo JSON)
        self.questions_data = questions

        self.botoes = []
        self.criar_widgets()

    def criar_widgets(self):
        # Texto da Pergunta
        current_question = self.questions_data[self.i_question]["pergunta"]
        self.label_question = tk.Label(self.root, text=current_question, 
                                      font=("Arial", 14), pady=20, wraplength=350)
        self.label_question.pack()

        # Botões de Resposta
        for i, opcao in enumerate(self.pergunta_dados["opcoes"]):
            btn = tk.Button(self.root, text=opcao, width=30, height=2,
                            command=lambda i=i: self.verificar_resposta(i))
            btn.pack(pady=5)
            self.botoes.append(btn)

        # Mensagem de Feedback
        self.label_feedback = tk.Label(self.root, text="", font=("Arial", 12, "bold"))
        self.label_feedback.pack(pady=20)

    def verificar_resposta(self, indice_escolhido):
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