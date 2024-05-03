import math
import random
import numpy as np

def get_resolutions():
  return [(100, 100), (300, 300), (800, 600), (1920, 1080)]

def generate_matrix(fill_value, height, width):
    return np.full((height, width), fill_value, dtype=np.uint8)

def add_point(x_new, y_new, points):
  points.append((round(x_new), round(y_new)))

def plot_raster(points, height, width):
  matrix = generate_matrix(0, height, width)
  for x_new, y_new in points:
    if 0 <= y_new < height and 0 <= x_new < width:
      matrix[math.floor(y_new)][math.floor(x_new)] = 1

  return matrix

def gen_point():
  x_new = random.uniform(-1, 1)
  y_new = random.uniform(-1, 1)

  return (x_new, y_new)

def denormalization(X, Y, width, height):
  rmin = -1
  rmax = 1

  ys = (Y - rmin) / (rmax - rmin)
  xs = (X - rmin) / (rmax - rmin)

  xs *= height - 0
  ys *= width - 0

  xs += 0
  ys += 0

  return (round(xs), round(ys))

def normalization(ponto):
  x, y = ponto
  x_normalizado = (x / 100) * 2 - 1
  y_normalizado = (y / 100) * 2 - 1
  return (x_normalizado, y_normalizado)

INSIDE = 0    # 0000 
LEFT = 1    # 0001
RIGHT = 2   # 0010
BOTTOM = 4  # 0100
TOP = 8     # 1000

def computeCode(point, window):
  code = INSIDE
  x_new , y_new = point
  width, height = window

  if x_new < 0:
    code |= LEFT
  elif x_new > width:
    code |= RIGHT

  if y_new < 0:
    code |= BOTTOM
  elif y_new > height:
    code |= TOP

  return code

  # Encontra a interseção
def findIntersection(code_point_out, start_point, end_point, window):
  start_x, start_y = start_point
  end_x, end_y = end_point
  width, height = window

  if code_point_out & TOP:
    x_new = start_x + (end_x - start_x) * (height - start_y) / (end_y - start_y)
    y_new = height
  elif code_point_out & BOTTOM:
    x_new = start_x + (end_x - start_x) * (0 - start_y) / (end_y - start_y)
    y_new = 0
  elif code_point_out & RIGHT:
    y_new = start_y + (end_y - start_y) * (width - start_x) / (end_x - start_x)
    x_new = width
  elif code_point_out & LEFT:
    y_new = start_y + (end_y - start_y) * (0 - start_x) / (end_x - start_x)
    x_new = 0

  return (x_new, y_new)

# Função de recorte de linha utilizando o algoritmo de Cohen-Sutherland
def cohenSutherland(start_point, end_point, window):
  start_x, start_y = start_point
  end_x, end_y = end_point

  code_start_point = computeCode(start_point, window)
  code_end_point = computeCode(end_point, window)
  accept = False

  while True:
    if code_start_point == 0 and code_end_point == 0:  # Ambos os pontos estão dentro da janela
      accept = True
      break
    elif code_start_point & code_end_point != 0:  # Os pontos estão ambos em uma região da janela
      break
    else:
      # Escolhe um ponto fora da janela
      x_new = 0
      y_new = 0
      if code_start_point != 0:
        code_point_out = code_start_point
      else:
        code_point_out = code_end_point

      x_new, y_new = findIntersection(code_point_out, start_point, end_point, window)

      # Atualiza o ponto fora da janela
      if code_point_out == code_start_point:
        start_x, start_y = x_new, y_new
        code_start_point = computeCode((x_new, y_new), window)
      else:
        end_x, end_y = x_new, y_new
        code_end_point = computeCode((x_new, y_new), window)

  if accept:
      return [(start_x, start_y), (end_x, end_y)]
  else:
      return []

# Função de recorte de polígono utilizando o algoritmo de Cohen-Sutherland
def clipPolygon(polygon, window):
  clipped_polygon = []

  # Adiciona o primeiro ponto do polígono ao final para fechar o loop
  polygon = polygon + (polygon[0],)

  lenght_polygon = len(polygon)
  # Recorte de cada lado do polígono
  for i in range(lenght_polygon - 1):
    start_point = polygon[i]
    end_point = polygon[i + 1]
    
    if i+1 == lenght_polygon-1:
      clipped_segment = [start_point, clipped_polygon[0]]
      clipped_polygon.extend(clipped_segment)
      continue
    else:
      clipped_segment = cohenSutherland(start_point, end_point, window) 

    if clipped_segment:
      clipped_polygon.extend(clipped_segment)

  return clipped_polygon


# Função para determinar se um objeto é uma linha ou um polígono
def isLine(object):
    return len(object) == 2 and all(isinstance(coord, tuple) for coord in object)

# Função principal que realiza o recorte em linhas e polígonos
def clip(object, window):
    if isLine(object):
      return cohenSutherland(object[0], object[1], window)
    return clipPolygon(object, window)