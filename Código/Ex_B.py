# IMPORTAÇÕES para o programa
from pymprog import*
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import time
# ------------------------------------------------------------------------------
# INICIO DO TEMPO
# ------------------------------------------------------------------------------
tempo_inicial = time.time() # em segundos
# ------------------------------------------------------------------------------
# FUNÇÃO para realizar a importação dos dados
# ------------------------------------------------------------------------------
def importar(file, L, Q, D):
    n = 0
    m = 0
    lista = list()
    arquivo = open(file, 'r')
    arquivo2 = []

    try:
      # passando todos os dados do arquivo para arquivo2
      for i in arquivo:
          arquivo2.append(i)

      # pegando todos os dados e passando para as devidas variaveis
      for i,j in enumerate(arquivo2):
          if i == 0:
              n = int(str(j))
          elif i == 1:
              m = int(str(j))
          else:
              v1 = int(str(f"{j[0]}{j[1]}{j[2]}"))
              v2 = int(str(f"{j[4]}{j[5]}{j[6]}"))
              lista.append(v1)
              lista.append(v2)
              L.append(lista.copy())
              lista.clear()

              v3 = int(str(f"{j[9]}{j[10]}"))
              Q.append(v3)

              v4 = int(str(f"{j[14]}"))
              D.append(v4)
      return n,m
    except:
      print("ERRO, VERIFIQUE!")
# ------------------------------------------------------------------------------
# FUNÇÃO para exportar as informações finais, para um arquivo .txt
# ------------------------------------------------------------------------------
def exportar(texto):
    with open('ResultadoB.txt', 'w') as f:
        f.write(texto)
# ------------------------------------------------------------------------------
# CRIAÇÃO de variaveis
#-------------------------------------------------------------------------------
L = []
Q = []
D = []
C = []
DAB = []
lista = list()
text = f"Exercício do Centro de Distribuição Parte A \n\n"
#-------------------------------------------------------------------------------
# CÓDIGO para abrir uma janela, para selecionar o arquivo desejado
# ------------------------------------------------------------------------------
Tk().withdraw() # Isto torna oculto a janela principal
filename = askopenfilename() # Isto te permite selecionar um arquivo
n,m = importar(filename, L, Q, D)
#-------------------------------------------------------------------------------
# DEFININDO um índice para as localidades
# ------------------------------------------------------------------------------
text = text + f"\n Definindo um indice para cada localidade"
cont = 0
for i,j in L:
  text = text + f'\nL{cont}: [{i},{j}]'
  cont = cont + 1
text = text + '\n\n'
#-------------------------------------------------------------------------------
# DEFININDO o grupo C
#-------------------------------------------------------------------------------
for i in range(n):
  if(D[i] == 1):
    C.append(i)
text = text + f"\n Grupo de possíveis centros: {C}"
text = text + '\n\n'
#-------------------------------------------------------------------------------
# DEFININDO a distancia de C - L (Teorema de Pitágoras)
# ------------------------------------------------------------------------------
text = text + f"\n Definindo a distancia entre C - L"
for i in C:
  for j in range(n):
    Pitagoras = round(pow((((L[i][0]) - (L[j][0]))**2) +
                          (((L[i][1]) - (L[j][1]))**2), 0.5), 2)
    lista.append(Pitagoras)
  DAB.append(lista.copy())
  lista.clear()
cont = 0
j = 0
for i in DAB:
  text = text + f'\nC{C[j]}: {i}'
  j = j + 1
text = text + '\n\n'
#-------------------------------------------------------------------------------
# DEFININDO AS VARIAVEIS
# ------------------------------------------------------------------------------
begin("Exercicio Avaliativo - Centros de Distribução - Parte B") # inicia um modelo
#verbose("true")
# variáveis de decisão
A = iprod(range(len(C)), range(n)) # cria os índices da variável x
x = var("x", A, bool) # cria variável binária x
y = var("y",C, bool) # criando a variável binária y
z = var("z")
#-------------------------------------------------------------------------------
# FUNÇÃO OBJETIVO
# ------------------------------------------------------------------------------
minimize(z)
#-------------------------------------------------------------------------------
# RESTRIÇÕES
# ------------------------------------------------------------------------------
for i in range(len(C)):
  sum(DAB[i][j] * x[i,j] * Q[j] for j in range(n)) <= z

for j in range(n):
  sum(x[i,j] for i in range(len(C))) == 1 # colocando somente um tipo de localidades em um centro

sum(y[i] for i in C) == m # definindo o máximo de centros

for i,k in enumerate(C):
  sum((x[i,j] for j in range(n))) <= n * y[k] # realizando a distribuição balanceada
#-------------------------------------------------------------------------------
# RESOLVENDO
# ------------------------------------------------------------------------------
solver(int, tm_lim = 3600 * 1000)
solve()
#-------------------------------------------------------------------------------
# MOSTRANDO VALORES FINAIS
# ------------------------------------------------------------------------------
acumulador = []
text = text + "Centros e as suas localidades"
for i,k in enumerate(C):
  if y[k].primal == 1:
    print(f"CD{C[i]} - ({L[k][0]:.2f},{L[k][1]:.2f}): ", end=" ")
    text = text + f"\nCD{C[i]} - ({L[k][0]:.2f},{L[k][1]:.2f}): "
    acm = 0
    for j in range(n):
      if x[i,j].primal == 1:
        print(f"{j}({L[j][0]:.2f},{L[j][1]:.2f}) [{(DAB[i][j] * Q[j]):.2f}]", end="   ")
        text = text + f"{j}({L[j][0]:.2f},{L[j][1]:.2f}) [{(DAB[i][j] * Q[j]):.2f}]  "
        acm = (DAB[i][j] * Q[j]) + acm
    print(f" Soma CD{C[i]} = ({acm:.2f})")
    text = text + f" Soma CD{C[i]} = ({acm:.2f})"
    acumulador.append(acm)
    print()
tempo_final = time.time() # em segundos

print(f"\nValor ótimo = {vobj():.2f}")
print(f"\nValor máximo = {max(acumulador, default=0.00):.2f}")
print(f"\nValor mínimo = {min(acumulador, default=0.00):.2f}")
print(f"\nSoma de todos os centos = {sum(acumulador):.2f}")
print()
text = text + f'''
\n* * * Dados de saida * * * 
\nValor otimo = {vobj():.2f}
\nValor maximo = {max(acumulador, default=0.00):.2f}
\nValor minimo = {min(acumulador, default=0.00):.2f}
\nSoma de todos os centos = {sum(acumulador):.2f}
\nTempo de execução = {((tempo_final - tempo_inicial) / 60):.2f} minuto
'''
#-------------------------------------------------------------------------------
# EXPORTANDO DADOS PARA ARQUIVO .TXT
# ------------------------------------------------------------------------------
exportar(text)
#-------------------------------------------------------------------------------
# FIM DO PROGRAMA
# ------------------------------------------------------------------------------
end()