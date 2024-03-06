import matplotlib.pyplot as plt
import numpy as np


def DDA (x1,y1,x2,y2,width, height): # RECEBE AS COORDENADAS E OS TAMANHOS DA MATRIZ A SER PLOTADA

  dx = abs(x2 - x1)  # VARIÁVEL QUE RECEBE O MÓDULO DA DIFERENÇA ENTRE X2 E X1
  dy = abs(y2 - y1)  # VARIÁVEL QUE RECEBE O MÓDULO DA DIFERENÇA ENTRE Y2 E Y1

  if dx >= dy:
        passos = abs(dx)
        if x1 > x2:
            x1, x2 = x2, x1 
            y1, y2 = y2, y1
  else:                       # Casos em que dy é mais ou igual a dx
        passos = abs(dy)
        if y1 > y2:
            x1, x2 = x2, x1
            y1, y2 = y2, y1

  xInc = (x2 - x1) / passos    # Aqui ele declara como vai se dar o incremento no eixo x, não é dx porque a diferença pode ser negativa
  yInc = (y2 - y1) / passos    # Aqui ele declara como vai se dar o incremento no eixo y, não é dy porque a diferença pode ser negativa

  x = x1  # Declara o ponto inicial no eixo x de onde a reta será incrementada ou decrementada
  y = y1  # Declara o ponto inicial no eixo y de onde a reta será incrementada ou decrementada

  matriz_pixels = np.zeros((height, width), dtype=int)

  for i in range(int(passos) + 1):

        x_round = round(x)
        # Arredonda a coordenada atual x para o valor mais próximo, a fim de determinar a posição em que a linha deve ser traçada na matriz de pixels
        # Isso é feito porque as coordenadas no espaço contínuo não se encaixam perfeitamente nas coordenadas discretas da matriz de pixels. 
        # Portanto, arredondamos as coordenadas para obter as posições exatas na matriz de pixels onde a linha deve ser desenhada.
        y_round = round(y)

        # Certifique-se de que os índices estejam dentro dos limites da matriz
        if 0 <= y_round < matriz_pixels.shape[0] and 0 <= x_round < matriz_pixels.shape[1]:   # matriz_pixels.shape[0] = numero de linhas da matriz e matriz_pixels.shape[1] = numero de colunas da matriz
            matriz_pixels[y_round, x_round] = 1         # itera ao longo da reta calculada e preenche os pixels 
                                                        # correspondentes na matriz matriz_pixels com o valor 1, de modo a representar a reta na 
                                                        # forma rasterizada.

        x += xInc # Aqui eu vou incrementar cada ponto da matriz no eixo x, mesmo se xInc for negativo ou 0, formando no final a reta
        y += yInc # Aqui eu vou incrementar cada ponto da matriz no eixo y, mesmo se yInc for negativo ou 0, formando no final a reta

  return matriz_pixels

def normalization(x1, y1, x2, y2, width, height):
    rmin = -1
    rmax = 1

    xs1 = (x1 - rmin) / (rmax - rmin)
    ys1 = (y1 - rmin) / (rmax - rmin)

    xs2 = (x2 - rmin) / (rmax - rmin)
    ys2 = (y2 - rmin) / (rmax - rmin)

    xs1 *= height - 0
    ys1 *= width - 0
    
    xs2 *= height - 0
    ys2 *= width - 0

    xs1 += 0
    ys1 += 0

    xs2 += 0
    ys2 += 0

    return round(xs1), round(ys1), round(xs2), round(ys2)

""" def main():
      x1 = float(input("Digite um valor para x1: "))
      y1 = float(input("Digite um valor para y1: "))
      x2 = float(input("Digite um valor para x2: "))
      y2 = float(input("Digite um valor para y2: "))

      # x1, x2, y1, y2 = 50, 100, 100, 50 # <- AQUI VOCE DETERMINA AS COORDENADAS DOS PONTOS
      width, height = 200, 200 # <- AQUI VOCE REDIMENSIONA A MATRIZ DE PIXELS
      return x1,y1,x2,y2,width,height

x1,y1,x2,y2,width,height = main()
# PLOT DE GRÁFICO SEM SER RASTERIZADO
plt.figure(1, figsize=[2,2])
px, py = [x1, x2], [y1, y2]

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
matriz_pixels = DDA(x1, y1, x2, y2, width, height) # Chamada ao algoritmo DDA

plt.imshow(matriz_pixels, cmap='Blues', origin='lower')
plt.title('Rasterização de Reta usando DDA')
plt.xlabel('Coordenada X')
plt.ylabel('Coordenada Y')
plt.grid()


# Mostrar as figuras separadamente
plt.show() """