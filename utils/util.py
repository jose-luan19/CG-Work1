import json
import math
import numpy as np

def get_resolutions():
  return [(100, 100), (300, 300), (800, 600), (1920, 1080)]

def generate_matrix(fill_value, width, height):
    return np.full((height, width), fill_value, dtype=np.uint8)

def add_point(x, y, points):
  points.append((round(x), round(y)))

def denormalization(X, Y, width, height):
  rmin = -1
  rmax = 1

  ys = (Y - rmin) / (rmax - rmin)
  xs = (X - rmin) / (rmax - rmin)

  xs *= width - 0
  ys *= height - 0

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
  x , y = point
  width, height = window
  
# '|=' OR bit a bit atribuído
  if x < 0:
    code |= LEFT
  elif x > width:
    code |= RIGHT

  if y < 0:
    code |= BOTTOM
  elif y > height:
    code |= TOP

  return code

# Dependendo do código da região, aqui calcula o ponto de interseção da linha com a borda
def findIntersection(code_point_out, start_point, end_point, window):
  start_x, start_y = start_point
  end_x, end_y = end_point
  width, height = window
  dx = end_x - start_x
  dy = end_y - start_y

  if code_point_out & TOP:
    # (height - start_y) calcula a distância vertical entre o ponto inicial da linha e o topo da janela.
    # (dx) * (height - start_y) / (dy) Mudança correspondente em x para que a linha alcance a borda superior.
    x_new = start_x + (dx) * (height - start_y) / (dy)
    y_new = height
  elif code_point_out & BOTTOM:
    # (0 - start_y) calcula a distância vertical entre o ponto inicial da linha e o fundo da janela.
    # (dx) * (0 - start_y) / (dy) Mudança correspondente em x para que a linha alcance a borda inferior.
    x_new = start_x + (dx) * (0 - start_y) / (dy)
    y_new = 0
  elif code_point_out & RIGHT:
    # (width - start_x) calcula a distância horizontal entre o ponto inicial da linha e a borda da direita da janela.
    # (dx) * (height - start_y) / (dy) Mudança correspondente em y para que a linha alcance a borda da direita.
    y_new = start_y + (dy) * (width - start_x) / (dx)
    x_new = width
  elif code_point_out & LEFT:
    # (0 - start_x) calcula a distância horizontal entre o ponto inicial da linha e a borda da esquerda da janela.
    # (dx) * (height - start_y) / (dy) Mudança correspondente em y para que a linha alcance a borda da esquerda.
    y_new = start_y + (dy) * (0 - start_x) / (dx)
    x_new = 0

  return (x_new, y_new)

# Função de recorte de linha utilizando o algoritmo de Cohen-Sutherland
def cohenSutherland_line(start_point, end_point, window):
  start_x, start_y = start_point
  end_x, end_y = end_point

  code_start_point = computeCode(start_point, window)

  code_end_point = computeCode(end_point, window)
  accept = False

  while True:
    if code_start_point == 0 and code_end_point == 0:  # Ambos os pontos estão dentro da janela
      accept = True
      break
    elif code_start_point & code_end_point != 0:  # Os pontos estão ambos em uma região fora da janela
      break
    else:
      x_new = 0
      y_new = 0
      # Verifica qual ponto está fora da janela e põe na variavel code_point_out
      if code_start_point != 0:
        code_point_out = code_start_point
      else:
        code_point_out = code_end_point

      #Encontra a interscção do ponto nessa interação ponde ser para o start ou end point,
      # depende da verificação anterior qual atribuiu seu valor ao code_point_out
      x_new, y_new = findIntersection(code_point_out, start_point, end_point, window)

      # Verifica se o ponto que está fora da janela é o start ou end
      if code_point_out == code_start_point:
        start_x, start_y = x_new, y_new # Atualiza o ponto fora da janela
        code_start_point = computeCode((x_new, y_new), window) # calcula novamente para verificar se ponto entrou na janela
      else:
        end_x, end_y = x_new, y_new # Atualiza o ponto fora da janela
        code_end_point = computeCode((x_new, y_new), window) # calcula novamente para verificar se ponto entrou na janela

  if accept:
      return [(start_x, start_y), (end_x, end_y)]
  else:
      return []

def clipPolygonEdge(polygon, edge_code, window):
  new_polygon = []
  for i in range(len(polygon)):
    start_point = polygon[i]
    end_point = polygon[(i + 1) % len(polygon)]

    code_start = computeCode(start_point, window)
    code_end = computeCode(end_point, window)

    # Ambos os pontos dentro da janela
    if code_start & edge_code == 0 and code_end & edge_code == 0:
      new_polygon.append(end_point)
    # O ponto inicial está fora e o final está dentro
    elif code_start & edge_code != 0 and code_end & edge_code == 0:
      intersection = findIntersection(code_start, start_point, end_point, window)
      new_polygon.append(intersection)
      new_polygon.append(end_point)
    # O ponto inicial está dentro e o final está fora
    elif code_start & edge_code == 0 and code_end & edge_code != 0:
      intersection = findIntersection(code_end, start_point, end_point, window)
      new_polygon.append(intersection)

  return new_polygon

# Método novo: Recorta o polígono utilizando as quatro bordas da janela
def clipPolygon(polygon, window=(100, 100)):
  # Recorte nas quatro bordas (esquerda, direita, baixo, cima)
  polygon = clipPolygonEdge(polygon, LEFT, window)   # Borda esquerda
  polygon = clipPolygonEdge(polygon, RIGHT, window)  # Borda direita
  polygon = clipPolygonEdge(polygon, BOTTOM, window) # Borda inferior
  polygon = clipPolygonEdge(polygon, TOP, window)    # Borda superior
  
  return polygon

# Função que realiza o recorte em linhas
def clip_line(object, window=(100,100)):
  return cohenSutherland_line(object[0], object[1], window)

def readFile():
  with open("data.json", "r") as f:
    return json.load(f)

# Converte a lista de pontos de linhas para uma lista de tuplas de tuplas
def convert_lines(points):
  # Cada elemento de 'points' é uma linha com duas tuplas de pontos
  return [((tuple(line[0]), tuple(line[1]))) for line in points]


def convert_curves(points):
  p0_list, p1_list, m0_list, m1_list = [], [], [], []

  for curve in points:
    p0 = np.append(np.array(normalization(curve[0])), [0.0])
    p1 = np.append(np.array(normalization(curve[1])), [0.0])
    m0 = np.append(np.array(normalization(curve[2])), [0.0])
    m1 = np.append(np.array(normalization(curve[3])), [0.0])

    p0_list.append(p0)
    p1_list.append(p1)  
    m0_list.append(m0)
    m1_list.append(m1)

  return p0_list, p1_list, m0_list, m1_list

# Converte a lista de pontos de polígonos para uma lista de tuplas de tuplas
def convert_polygon(points):
  shapes = []
  
  for polygon_type in ["Triangle", "Square", "Hexagon"]:
    for polygon in points[polygon_type]:
      if polygon:  # Se o polígono não estiver vazio
        shapes.append([tuple(point) for point in polygon])
  
  return shapes

# Converte os dados para tuplas de acordo com o tipo de figura
def convert_to_tuples(data):
  points = data["points"]
  
  if data["figura"] == "Line":
    return convert_lines(points)
  elif data["figura"] == "Polygon":
    return convert_polygon(points)
  elif data["figura"] == "Curve":
    return convert_curves(points)
  else:
    raise ValueError("Tipo de figura desconhecido.")

#Examples json
  
# {"figura": "Line", "points": [[[1, 1], [1, 1]], [[2, 2], [2, 2]], [[3, 3], [3, 3]], [[4, 4], [4, 4]]]}
# {"figura": "Curve", "points": [[[1, 1], [1, 1], [1, 1], [1, 1]], [[2, 2], [2, 2], [2, 2], [2, 2]], [[3, 3], [3, 3], [3, 3], [3, 3]], [[4, 4], [4, 4], [4, 4], [4, 4]]]}
# {"figura": "Polygon", "points": {"Triangle": [[10, 10], [20, 20], [30, 10]], "Square": [[70,60],[70,75],[85,75],[85,60]], "Hexagon": [[15, 55], [30, 70], [50, 70], [65, 55], [50, 40], [30, 40]]}}