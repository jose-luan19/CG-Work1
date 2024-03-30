import matplotlib.pyplot as plt
import numpy as np


def rasterizacao_retas (X_start, Y_start, X_end, Y_end ): # RECEBE O PONTO INICIAL E O PONTO FINAL

  x = X_start  # Declara o ponto inicial no eixo x de onde a reta será incrementada ou decrementada
  y = Y_start  # Declara o ponto inicial no eixo y de onde a reta será incrementada ou decrementada
  points = [(x,y)]
  
  dx = abs(X_end - X_start)  # VARIÁVEL QUE RECEBE O MÓDULO DA DIFERENÇA ENTRE X2 E X1
  dy = abs(Y_end - Y_start)  # VARIÁVEL QUE RECEBE O MÓDULO DA DIFERENÇA ENTRE Y_end E Y_start

  # FUNÇÃO SEMI-RETA: y = m * x + b
  m = 0 if dx == 0 else dy / dx

  b =  y - m * x


#   if dx >= dy:
#         passos = abs(dx)
#         if X_start > X_end:
#             X_start, X_end = X_end, X_start 
#             Y_start, Y_end = Y_end, Y_start
#   else:                       # Casos em que dy é mais ou igual a dx
#         passos = abs(dy)
#         if Y_start > Y_end:
#             X_start, X_end = X_end, X_start
#             Y_start, Y_end = Y_end, Y_start

#   xInc = (X_end - X_start) / passos    # Aqui ele declara como vai se dar o incremento no eixo x, não é dx porque a diferença pode ser negativa
#   yInc = (Y_end - Y_start) / passos    # Aqui ele declara como vai se dar o incremento no eixo y, não é dy porque a diferença pode ser negativa


#   matriz_pixels = np.zeros((height, width), dtype=int)

#   for i in range(int(passos) + 1):

#         x_round = round(x)
#         # Arredonda a coordenada atual x para o valor mais próximo, a fim de determinar a posição em que a linha deve ser traçada na matriz de pixels
#         # Isso é feito porque as coordenadas no espaço contínuo não se encaixam perfeitamente nas coordenadas discretas da matriz de pixels. 
#         # Portanto, arredondamos as coordenadas para obter as posições exatas na matriz de pixels onde a linha deve ser desenhada.
#         y_round = round(y)

#         # Certifique-se de que os índices estejam dentro dos limites da matriz
#         if 0 <= y_round < matriz_pixels.shape[0] and 0 <= x_round < matriz_pixels.shape[1]:   # matriz_pixels.shape[0] = numero de linhas da matriz e matriz_pixels.shape[1] = numero de colunas da matriz
#             matriz_pixels[y_round, x_round] = 1         # itera ao longo da reta calculada e preenche os pixels 
#                                                         # correspondentes na matriz matriz_pixels com o valor 1, de modo a representar a reta na 
#                                                         # forma rasterizada.

#         x += xInc # Aqui eu vou incrementar cada ponto da matriz no eixo x, mesmo se xInc for negativo ou 0, formando no final a reta
#         y += yInc # Aqui eu vou incrementar cada ponto da matriz no eixo y, mesmo se yInc for negativo ou 0, formando no final a reta

#   return matriz_pixels

def normalization(X_start, Y_start, X_end, Y_end, width, height):
    rmin = -1
    rmax = 1

    xs1 = (X_start - rmin) / (rmax - rmin)
    ys1 = (Y_start - rmin) / (rmax - rmin)

    xs2 = (X_end - rmin) / (rmax - rmin)
    ys2 = (Y_end - rmin) / (rmax - rmin)

    xs1 *= height - 0
    ys1 *= width - 0
    
    xs2 *= height - 0
    ys2 *= width - 0

    xs1 += 0
    ys1 += 0

    xs2 += 0
    ys2 += 0

    return round(xs1), round(ys1), round(xs2), round(ys2)

def main():
      X_start = float(input("Digite um valor para X_start: "))
      Y_start = float(input("Digite um valor para Y_start: "))
      X_end = float(input("Digite um valor para X_end: "))
      Y_end = float(input("Digite um valor para Y_end: "))

      # X_start, X_end, Y_start, Y_end = 50, 100, 100, 50 # <- AQUI VOCE DETERMINA AS COORDENADAS DOS PONTOS
      width, height = 200, 200 # <- AQUI VOCE REDIMENSIONA A MATRIZ DE PIXELS
      return X_start,Y_start,X_end,Y_end,width,height

X_start,Y_start,X_end,Y_end,width,height = main()
# PLOT DE GRÁFICO SEM SER RASTERIZADO
plt.figure(1, figsize=[2,2])
px, py = [X_start, X_end], [Y_start, Y_end]

plt.plot(px, py, marker='o')
plt.title('Gráfico das Coordenadas')
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')
# Defina os limites nos eixos x e y do gráfico de coordenadas
plt.xlim(0, width)
plt.ylim(0, height)
plt.grid()

# PLOT DE GRÁFICO RASTERIZADO
plt.figure(2, figsize=[4,4])
matriz_pixels = rasterizacao_retas(X_start, Y_start, X_end, Y_end) # Chamada ao algoritmo rasterizacao_retas

plt.imshow(matriz_pixels, cmap='Blues', origin='lower')
plt.title('Rasterização de Reta usando rasterizacao_retas')
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')
plt.grid()


# Mostrar as figuras separadamente
plt.show()