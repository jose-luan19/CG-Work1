import matplotlib.pyplot as plt
import numpy as np

import utils.util as util


# Função para mapear as coordenadas de -1 a 1 para a resolução desejada
def map_coordinates(x, y, resolution_x, resolution_y):
    mapped_x = int((x + 1) * (resolution_x / 2))
    mapped_y = int((1 - y) * (resolution_y / 2))
    return mapped_x, mapped_y

# Função para desenhar uma linha entre dois pontos
def draw_line(x1, y1, x2, y2, image, color):
    steep = abs(y2 - y1) > abs(x2 - x1)
    if steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
    dx = x2 - x1
    dy = y2 - y1
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
    y = y1
    for x in range(x1, x2 + 1):
        if steep:
            if 0 <= x < image.shape[1] and 0 <= y < image.shape[0]:
                image[y, x, :] = color
        else:
            if 0 <= y < image.shape[0] and 0 <= x < image.shape[1]:
                image[y, x, :] = color
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

# Função para determinar o mínimo e o máximo de y para cada varredura
def scan_polygon(vertices):
    min_y = min(vertices, key=lambda v: v[1])[1]
    max_y = max(vertices, key=lambda v: v[1])[1]
    return min_y, max_y

# Função para rasterizar o polígono convexo com coordenadas mapeadas
def rasterize_polygon(vertices, image, color):
    min_y, max_y = scan_polygon(vertices)
    for y in range(min_y, max_y + 1):
        intersections = []
        for i in range(len(vertices)):
            x1, y1 = vertices[i]
            x2, y2 = vertices[(i + 1) % len(vertices)]
            if (y1 <= y and y2 > y) or (y2 <= y and y1 > y):
                if y1 == y2:
                    intersections.append(x1)
                else:
                    intersections.append(x1 + (y - y1) / (y2 - y1) * (x2 - x1))
        intersections.sort()
        for i in range(0, len(intersections), 2):
            x1 = int(intersections[i])
            x2 = int(intersections[i + 1])
            draw_line(x1, y, x2, y, image, color)

# Define as coordenadas dos vértices dos triângulos, quadrados e hexágonos no intervalo de -1 a 1
triangle1 = [(-1, -1),(-0.75, -0.50), 
             (-0.75, -0.50),(-0.50, -1), 
             (-0.50, -1), (-1, -1)
            ]
triangle2 = [(-0.25, -0.5),(0.25, -0.5), 
             (0.25, -0.5),(0, 0), 
             (0, 0),(-0.25, -0.5)
            ]

square1 = [(-1, 1),(-0.50, 1), 
           (-0.50, 1),(-0.50, 0.50), 
           (-1, 0.50),(-1, 0.50), 
           (-1, 0.50),(-1, 1)
           ]
square2 = [(0, -1),(0.25, -1), 
           (0.25, -1),(0.25, -0.75), 
           (0.25, -0.75),(0, -0.75), 
           (0, -0.75),(0, -1)
           ]

hexagon1 = [(-0.25, 0.5), (0, 0.25), 
            (0, 0.25), (0.25, 0.25), 
            (0.25, 0.25), (0.5, 0.5), 
            (0.5, 0.5), (0.25, 0.75), 
            (0.25, 0.75), (0, 0.75), 
            (0, 0.75), (-0.25, 0.5)
            ]
hexagon2 = [(0.95, 0.75), (0.85, 0.92),
            (0.85, 0.92), (0.65, 0.92),
            (0.65, 0.92), (0.55, 0.75),
            (0.55, 0.75), (0.65, 0.58),
            (0.65, 0.58), (0.85, 0.58),
            (0.85, 0.58), (0.95, 0.75)
            ]

square = [(-0.8, -0.8), (-0.8, -0.4), (-0.8, -0.4), (-0.4, -0.4), (-0.4, -0.4), (-0.4, -0.8), (-0.4, -0.8), (-0.8, -0.8)]

data = util.readFile()
lines = util.convert_to_tuples(data)

# triangle_clip = util.clip(((-2, -10), (75, 50), (50, 10)), (100,100)) # exemplo com recorte numa janela de 100x100
polygon = []
polygon_clipped = util.clip_polygon(lines, (100,100))
for point in polygon_clipped:
    polygon.append(util.normalization(point))

# Lista de resoluções
# resolutions = [(100, 100)]
resolutions = [(100, 100), (300, 300), (800, 600), (1920, 1080)]
# Cores para cada forma geométrica
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255)]

# Rasteriza as formas geométricas em cada resolução e exibe em janelas separadas
for resolution_x, resolution_y in resolutions:
    image = np.full((resolution_y, resolution_x, 3), 255, dtype=np.uint8)
    shapes = [triangle1, triangle2, square1, square2, hexagon1, hexagon2]
    # shapes = [square]
    for i, shape in enumerate(shapes):
        color = colors[i]
        adjusted_shape = [map_coordinates(x, y, resolution_x, resolution_y) for x, y in shape]
        rasterize_polygon(adjusted_shape, image, color)
    plt.imshow(image, extent=(0, resolution_x, 0, resolution_y), origin="upper")
    plt.title(f'Polygon - Resolution: {resolution_x}x{resolution_y}')
    plt.xlabel('Eixo X')
    plt.ylabel('Eixo Y')
    plt.grid(True)
    file_name = f'polygons-image/polygons_{resolution_x}x{resolution_y}.png'
    plt.savefig(file_name)
    plt.show()