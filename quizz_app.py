import tkinter as tk
from tkinter import messagebox

class QuizApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quiz Python")
        self.root.geometry("400x400")

        # Dados da pergunta (Poderia vir de um arquivo JSON)
        self.pergunta_dados = {
            "pergunta": "Qual é a capital da França?",
            "opcoes": ["Londres", "Berlim", "Paris", "Madri"],
            "correta": 2  # Índice da opção 'Paris'
        }

        self.botoes = []
        self.criar_widgets()

    def criar_widgets(self):
        # Texto da Pergunta
        self.label_pergunta = tk.Label(self.root, text=self.pergunta_dados["pergunta"], 
                                      font=("Arial", 14), pady=20, wraplength=350)
        self.label_pergunta.pack()

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