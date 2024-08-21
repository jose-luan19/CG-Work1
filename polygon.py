import numpy as np
import matplotlib.pyplot as plt
import utils.util as util


class ScanlinePolygonFiller:
    def __init__(self, vertices, color_value):
        if len(vertices) < 3:
            raise ValueError("Um polígono deve ter pelo menos 3 vértices.")
        self.vertices = vertices
        self.color_value = color_value
        self.edges = self._compute_edges()

    def _compute_edges(self):
        edges = []
        num_vertices = len(self.vertices)
        for i in range(num_vertices):
            x0, y0 = self.vertices[i]
            x1, y1 = self.vertices[(i + 1) % num_vertices]
            if y0 != y1:  # Ignora linhas horizontais
                edges.append((x0, y0, x1, y1))
        return edges

    def _fill_scanline(self, canvas, y):
        x_intersections = []
        for x0, y0, x1, y1 in self.edges:
            if y0 > y1:
                x0, x1 = x1, x0
                y0, y1 = y1, y0
            if y0 <= y < y1:
                if y1 != y0:
                    x = x0 + (y - y0) * (x1 - x0) / (y1 - y0)
                    x_intersections.append(x)
        x_intersections.sort()
        for i in range(0, len(x_intersections), 2):
            x_start = int(np.ceil(x_intersections[i]))
            x_end = int(np.floor(x_intersections[i + 1])) - 1
            if x_start <= x_end:
                canvas[y, x_start : x_end + 1] = self.color_value

    def fill_polygon(self, canvas):
        num_rows, num_cols, _ = canvas.shape
        for y in range(num_rows):
            self._fill_scanline(canvas, y)


def rasterize_polygon(vertices, width, height, color_value):
    canvas = np.zeros((height, width, 3), dtype=np.uint8)  # RGB canvas
    filler = ScanlinePolygonFiller(vertices, color_value)
    filler.fill_polygon(canvas)
    return canvas


def normalize_vertices(vertices):
    normalized = []
    for point in vertices:
        point_norm = util.normalization(point)
        normalized.append(point_norm)
    return normalized


def denormalize_vertices(vertices, width, height):
    denormalized = []
    for point in vertices:
        point_denor = util.denormalization(*point, width, height)
        denormalized.append(point_denor)
    return denormalized


# Definindo os vértices dos triângulos
triangle1 = [(10, 10), (20, 10), (20, 20)]  # Triângulo no canto superior esquerdo
triangle2 = [(70, 70), (80, 50), (130, 90)]  # Triângulo no canto inferior direito

square1 = [(20, 60), (20, 80), (40, 80), (40, 60)]  # Quadrado no canto superior direito
square2 = [(20, 40), (20, 60), (40, 60), (40, 40)]  # Quadrado no canto inferior direito

hexagon1 = [(25,35 ), (35, 35), (40, 30), (35, 25), (25, 25), (20, 30)]  # Hexágono no centro superior
hexagon2 = [(65, 75), (75, 75), (80, 70), (75, 65), (65, 65), (60, 70)]

figures = [triangle1, triangle2, square1, square2, hexagon1, hexagon2]
data = util.readFile()
if(data["figura"] == "Polygon" ):
    figures = util.convert_to_tuples(data)
    
polygon_clippeds = []
for fig in figures:
    polygon_clippeds.append(util.clipPolygon(fig))
    if len(polygon_clippeds) == 0:
        continue


# Cores distintas para cada triângulo (em formato RGB)
colors = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
]


polygons = []

for i, polygon in enumerate(polygon_clippeds):
    polygons.append((polygon, colors[i]))


for width, height in util.get_resolutions():
      canvas = np.zeros((height, width, 3), dtype=np.uint8)

      for vertices, color_value in polygons:
            # Normalizar as coordenadas dos polígonos para o intervalo [0, 1]
            normalized_vertices = normalize_vertices(vertices)
            # Rasterizar o polígono normalizado
            denormalized_vertices = denormalize_vertices(normalized_vertices, width, height)
            canvas = np.maximum(
                  canvas, rasterize_polygon(denormalized_vertices, width, height, color_value)
            )

      # Plotando o resultado
      plt.imshow(canvas, extent=(0, width, 0, height), origin="lower")
      plt.title(f'Polygon - Resolution: {width}x{height}')
      plt.xlabel('Eixo X')
      plt.ylabel('Eixo Y')
      plt.grid(True)
      file_name = f'polygons-image/polygons_{width}x{height}.png'
      plt.savefig(file_name)
      plt.show()

