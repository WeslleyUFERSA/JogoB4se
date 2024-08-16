import tkinter as tk
from tkinter import messagebox, simpledialog
import random

#Base operadores logicos (and, or, not)
perguntas_logica = [
    {"pergunta": "Se P → Q é verdadeiro e Q é falso, então P também é falso?", "resposta": "sim"}, #resultado = not P or Q  P → Q
    {"pergunta": "Se P ∨ Q é verdadeiro e P é verdadeiro, então Q deve ser verdadeiro?", "resposta": "nao"}, #resultado = P or Q  P ∨ Q
    {"pergunta": "Se ¬P ∧ Q é verdadeiro, então P é falso?", "resposta": "sim"}, #resultado = not P and Q  ¬P ∧ Q
    {"pergunta": "Se P ∧ Q é falso, então ambos P e Q são falsos?", "resposta": "nao"}, #resultado = P and Q  P ∧ Q
    {"pergunta": "Se P ↔ Q é falso, então P e Q têm valores lógicos diferentes?", "resposta": "sim"}, #resultado = (P and not Q) or (not P and Q) P ↔ Q
    {"pergunta": "Se P → Q é verdadeiro e P é falso, então Q deve ser falso?", "resposta": "nao"}, #resultado = not P or Q  # P → Q
    {"pergunta": "Se ¬(P ∨ Q) é verdadeiro, então P e Q são falsos?", "resposta": "sim"}, #resultado = not (P or Q)  # ¬(P ∨ Q)
    {"pergunta": "Se P → ¬Q é verdadeiro e P é verdadeiro, então Q é verdadeiro?", "resposta": "nao"}, #resultado = not P or not Q  # P → ¬Q
]

#funcao verificar vitoria e empate
def verificar_vitoria():
    combinacoes_vencedoras = [
        [tabuleiro[0][0], tabuleiro[0][1], tabuleiro[0][2]],
        [tabuleiro[1][0], tabuleiro[1][1], tabuleiro[1][2]],
        [tabuleiro[2][0], tabuleiro[2][1], tabuleiro[2][2]],
        [tabuleiro[0][0], tabuleiro[1][0], tabuleiro[2][0]],
        [tabuleiro[0][1], tabuleiro[1][1], tabuleiro[2][1]],
        [tabuleiro[0][2], tabuleiro[1][2], tabuleiro[2][2]],
        [tabuleiro[0][0], tabuleiro[1][1], tabuleiro[2][2]],
        [tabuleiro[0][2], tabuleiro[1][1], tabuleiro[2][0]]
    ]
    for linha in combinacoes_vencedoras:
        if linha[0] == linha[1] == linha[2] != "":
            return True
    return False

def verificar_empate():
    for linha in tabuleiro:
        if "" in linha:
            return False
    return True

#funcao jogadas da ia de acordo com o nivel de dificuldade
def jogada_aleatoria():
    vazias = [(i, j) for i in range(3) for j in range(3) if tabuleiro[i][j] == ""]
    if vazias:
        i, j = random.choice(vazias)
        tabuleiro[i][j] = "O"
        botoes[i][j].config(text="O")

def jogada_ia():
    global jogador_atual, jogo_terminado

    if dificuldade == "Fácil":
        jogada_aleatoria()
    elif dificuldade == "Médio":
        #Bloquear a vitoria de Goku
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] == "":
                    tabuleiro[i][j] = "X"
                    if verificar_vitoria():
                        tabuleiro[i][j] = "O"
                        botoes[i][j].config(text="O")
                        return
                    tabuleiro[i][j] = ""
        jogada_aleatoria()
    elif dificuldade == "Difícil":
        #Ganhar se possivel
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] == "":
                    tabuleiro[i][j] = "O"
                    if verificar_vitoria():
                        botoes[i][j].config(text="O")
                        return
                    tabuleiro[i][j] = ""
        #Bloquear a vitoria de Goku
        for i in range(3):
            for j in range(3):
                if tabuleiro[i][j] == "":
                    tabuleiro[i][j] = "X"
                    if verificar_vitoria():
                        tabuleiro[i][j] = "O"
                        botoes[i][j].config(text="O")
                        return
                    tabuleiro[i][j] = ""
        jogada_aleatoria()

#Funcao para fazer perguntas de logica proposicional;
def verificar_resposta():
    pergunta_aleatoria = random.choice(perguntas_logica)
    resposta = simpledialog.askstring("Desafio de Lógica", pergunta_aleatoria["pergunta"])
    if resposta and resposta.lower() == pergunta_aleatoria["resposta"]:
        messagebox.showinfo("Resposta Correta", "Você acertou! Faça sua jogada.")
        return True
    else:
        messagebox.showwarning("Resposta Incorreta", "Resposta errada! Vegeta vai jogar.")
        return False

#Funcao para fornecer dicas especificas relacionadas a logica proposicional
def verificar_dica():
    if dificuldade == "Fácil":
        return "Dica: Controle o centro do tabuleiro para aumentar suas chances de vencer. (Lógica: P → Q)"
    elif dificuldade == "Médio":
        return "Dica: Se o Vegeta tem duas marcas em linha, bloqueie a terceira posição. (Lógica: ¬P → ¬Q)"
    elif dificuldade == "Difícil":
        return "Dica: Crie duas linhas possíveis ao mesmo tempo para forçar o Vegeta a errar. (Lógica: (P ∧ Q) → R)"

#Funcao de clique dos botoes
def clique_botao(linha, coluna):
    global jogador_atual, jogo_terminado
    if tabuleiro[linha][coluna] == "" and not jogo_terminado:
        if desafio_ativo and jogador_atual == "X":
            if not verificar_resposta():
                jogada_ia()
                return
        
        tabuleiro[linha][coluna] = jogador_atual
        botoes[linha][coluna].config(text=jogador_atual)
        
        if verificar_vitoria():
            if jogador_atual == "X":
                messagebox.showinfo("Fim de Jogo", "Goku venceu.")
            else:
                messagebox.showinfo("Fim de Jogo", "Vegeta venceu.")
            jogo_terminado = True
        elif verificar_empate():
            messagebox.showinfo("Fim de Jogo", "Empate.")
            jogo_terminado = True
        else:
            jogador_atual = "O" if jogador_atual == "X" else "X"
            if jogador_atual == "O":
                jogada_ia()
                if verificar_vitoria():
                    messagebox.showinfo("Fim de Jogo", "Vegeta venceu.")
                    jogo_terminado = True
                elif verificar_empate():
                    messagebox.showinfo("Fim de Jogo", "Empate.")
                    jogo_terminado = True
                jogador_atual = "X"

#Funcao para reiniciar o jogo
def reiniciar_jogo():
    global tabuleiro, jogador_atual, jogo_terminado
    jogador_atual = "X"
    jogo_terminado = False
    tabuleiro = [[""] * 3 for _ in range(3)]
    for i in range(3):
        for j in range(3):
            botoes[i][j].config(text="", state=tk.NORMAL)

#Funcao para definir a dificuldade
def definir_dificuldade(dif):
    global dificuldade
    dificuldade = dif
    reiniciar_jogo()

#Funcao para definir se o jogador deseja jogar com o desafio ou nao
def definir_desafio(escolha):
    global desafio_ativo
    desafio_ativo = escolha
    reiniciar_jogo()

#Configuracao inicial
janela = tk.Tk()
janela.title("Trabalho matemática discreta")
janela.configure(bg='black')

jogador_atual = "X"
jogo_terminado = False
tabuleiro = [[""] * 3 for _ in range(3)]
botoes = [[None for _ in range(3)] for _ in range(3)]
dificuldade = "Médio"  # Define a dificuldade padrao
desafio_ativo = False  # Define se o desafio de equivalencias esta ativo

# Criar os botoes do tabuleiro
for i in range(3):
    for j in range(3):
        botoes[i][j] = tk.Button(janela, text="", font=('Arial', 40), width=5, height=2,
                                 bg='lightblue', fg='darkblue', bd=0,
                                 command=lambda i=i, j=j: clique_botao(i, j))
        botoes[i][j].grid(row=i, column=j, padx=5, pady=5)

#Criar uma frame para os botoes de reiniciar, dica e selecao de dificuldade
frame_botoes = tk.Frame(janela, bg='black')
frame_botoes.grid(row=4, column=0, columnspan=3)

#Botao de reiniciar
botao_reiniciar = tk.Button(frame_botoes, text="Reiniciar", font=('Arial', 20), command=reiniciar_jogo, bg='orange', fg='black', bd=0)
botao_reiniciar.grid(row=0, column=0, padx=10, pady=10)

#Botao de dica
botao_dica = tk.Button(frame_botoes, text="Dica", font=('Arial', 20), command=lambda: messagebox.showinfo("Dica", verificar_dica()), bg='green', fg='black', bd=0)
botao_dica.grid(row=0, column=1, padx=10, pady=10)

#Botoes de dificuldade
botao_facil = tk.Button(frame_botoes, text="Fácil", font=('Arial', 20), command=lambda: definir_dificuldade("Fácil"), bg='lightgray', fg='black', bd=0)
botao_facil.grid(row=0, column=2, padx=10, pady=10)

botao_medio = tk.Button(frame_botoes, text="Médio", font=('Arial', 20), command=lambda: definir_dificuldade("Médio"), bg='lightgray', fg='black', bd=0)
botao_medio.grid(row=0, column=3, padx=10, pady=10)

botao_dificil = tk.Button(frame_botoes, text="Difícil", font=('Arial', 20), command=lambda: definir_dificuldade("Difícil"), bg='lightgray', fg='black', bd=0)
botao_dificil.grid(row=0, column=4, padx=10, pady=10)

#Botoes para ativar ou desativar o desafio
botao_desafio_on = tk.Button(frame_botoes, text="Desafio: ON", font=('Arial', 20), command=lambda: definir_desafio(True), bg='blue', fg='white', bd=0)
botao_desafio_on.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

botao_desafio_off = tk.Button(frame_botoes, text="Desafio: OFF", font=('Arial', 20), command=lambda: definir_desafio(False), bg='red', fg='white', bd=0)
botao_desafio_off.grid(row=1, column=2, columnspan=2, padx=10, pady=10)

#Executar a janela principal
janela.mainloop()
