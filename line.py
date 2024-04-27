import matplotlib.pyplot as plt
import math
import utils.util as util

def raster_points (X_start, Y_start, X_end, Y_end ): # RECEBE O PONTO INICIAL E O PONTO FINAL

  x = X_start  # DECLARA O PONTO INICIAL NO EIXO X DE ONDE A RETA SERÁ INCREMENTADA OU DECREMENTADA
  y = Y_start  # DECLARA O PONTO INICIAL NO EIXO Y DE ONDE A RETA SERÁ INCREMENTADA OU DECREMENTADA
  points = [(round(x),round(y))]
  
  dx = abs(X_end - X_start)  # VARIÁVEL QUE RECEBE O MÓDULO DA DIFERENÇA ENTRE X2 E X1
  dy = abs(Y_end - Y_start)  # VARIÁVEL QUE RECEBE O MÓDULO DA DIFERENÇA ENTRE Y_end E Y_start

  # FUNÇÃO SEMI-RETA: y = m * x + b
  m = 0 if dx == 0 else dy / dx

  b =  y - m * x

  # ITERAR NO EIXO X
  if math.fabs(dx) >= math.fabs(dy):
    step_x = 1 if X_start < X_end else -1 # VERIFICA SE IRÁ INCREMENTAR OU DECREMENTAR
    while x != X_end:
      x += step_x
      y = m * x + b # ACHA O PONTO Y A PARTIR DA FUNÇÃO DE SEMI-RETA
      util.add_point(x, y, points)

  # ITERAR NO EIXO Y
  else:
    step_y = 1 if Y_start < Y_end else -1  # VERIFICA SE IRÁ INCREMENTAR OU DECREMENTAR
    while y != Y_end:
      y += step_y
      if m != 0:
        x = (y - b) / m # ACHA O PONTO X A PARTIR DA FUNÇÃO DE SEMI-RETA
      util.add_point(x, y, points)

  return points


# PONTOS
line = ((10,10),(85,50))

# NORMALIZAR OS PONTOS QUE DESEJA USAR PARA RASTERIZAR A LINHA, USA-SE COMO BASE A RESOLUÇÃO 100X100
start_point_norm = util.normalization(line[0])
end_point_norm = util.normalization(line[1])

# PLOT DE GRÁFICO RASTERIZADO
for width, height in util.get_resolutions():
  # DENORMALIZANDO OS PONTOS PARA 
  start_point = util.denormalization(*start_point_norm, width, height)
  end_point = util.denormalization(*end_point_norm, width, height)
  points = raster_points(*start_point, *end_point) # ACHAR PONTOS COM O ALGORITMO DE RASTERIZÇÃO
  matrix = util.plot_raster(points, width, height) # INCLUIR OS PONTOS NA MATRIZ 
  

  plt.imshow(matrix, cmap='Blues', extent=(0, width, 0, height), origin='lower')
  plt.title('Rasterização de Reta usando rasterizacao_retas')
  plt.xlabel('Coordenada X')
  plt.ylabel('Coordenada Y')
  plt.grid()

  file_name = f'line-image/line{width}x{height}.png'
  plt.savefig(file_name)
  plt.show()