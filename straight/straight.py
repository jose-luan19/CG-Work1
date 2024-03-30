import os
import matplotlib.pyplot as plt
import numpy as np
import math


def rasterizacao_retas (X_start, Y_start, X_end, Y_end ): # RECEBE O PONTO INICIAL E O PONTO FINAL

  x = X_start  # Declara o ponto inicial no eixo x de onde a reta será incrementada ou decrementada
  y = Y_start  # Declara o ponto inicial no eixo y de onde a reta será incrementada ou decrementada
  matriz_pixels = [(round(x),round(y))]
  
  dx = abs(X_end - X_start)  # VARIÁVEL QUE RECEBE O MÓDULO DA DIFERENÇA ENTRE X2 E X1
  dy = abs(Y_end - Y_start)  # VARIÁVEL QUE RECEBE O MÓDULO DA DIFERENÇA ENTRE Y_end E Y_start

  # FUNÇÃO SEMI-RETA: y = m * x + b
  m = 0 if dx == 0 else dy / dx

  b =  y - m * x

  if math.fabs(dx) >= math.fabs(dy):
    step_x = 1 if X_start < X_end else -1
    while x != X_end:
      x += step_x
      y = m * x + b
      add_point(x, y, matriz_pixels)
  else:
    step_y = 1 if Y_start < Y_end else -1
    while y != Y_end:
      y += step_y
      if m != 0:
        x = (y - b) / m
      add_point(x, y, matriz_pixels)

  return matriz_pixels

def add_point(x, y, points):
  points.append((round(x), round(y)))


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

resolutions = [(100, 100), (300, 300), (800, 600), (1920, 1080)]


X_start,Y_start,X_end,Y_end,width,height = 0,0,100,100

# PLOT DE GRÁFICO RASTERIZADO
for width, height in resolutions:
    plt.figure(2, figsize=[4,4])
    matriz_pixels = rasterizacao_retas(X_start, Y_start, X_end, Y_end) # Chamada ao algoritmo rasterizacao_retas

    plt.imshow(matriz_pixels, cmap='Blues', origin='lower')
    plt.title('Rasterização de Reta usando rasterizacao_retas')
    plt.xlabel('Coordenada X')
    plt.ylabel('Coordenada Y')
    plt.grid()

    file_name = f'image/straight_{width}x{height}.png'
    plt.savefig(file_name)
    plt.show()

    if os.path.exists(file_name):
      print(f"Saved image with success {file_name}")
    else:
      print(f"Fail to save image {file_name}")