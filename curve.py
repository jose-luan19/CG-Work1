import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw
import utils.util as util


# A curva é calculada a partir da função parametrica cubica: P(t_x) = TC ; onde C = MG

# Quantidade de amostras
N = 200

# Defina a matriz de transformação de Hermite
M = np.array([[2, -2, 1, 1],
              [-3, 3, -2, -1],
              [0, 0, 1, 0],
              [1, 0, 0, 0]
            ])


def find_point(t_x, p0, p1, m0, m1):
    # Matriz T
    T = np.array([t_x ** 3, t_x ** 2, t_x, 1])
    # Matriz G que é composta pelo ponto inicial, final, vetor tangente no inicio e vetor tangente no final
    G = np.vstack((p0, p1, m0, m1))
    # Encontrar o ponto com o parametro t_x 
    point = np.dot(np.dot(T, M), G)
    return point


def rasterize_hermite_curve(p0, p1, m0, m1):
    # 1000 amostras para usar como parametro de t_x, no intervalo de 0 a 1
    t_values = np.linspace(0, 1, N)
    x_values = []
    y_values = []

    # Encontra os pontos para rasterizar pequenos segmentos de retas
    for t_x in t_values:
        point = find_point(t_x, p0, p1, m0, m1)
        x_values.append(point[0])
        y_values.append(point[1])

    return x_values, y_values

# Defina as resoluções desejadas
resolutions = [(100, 100), (300, 300), (800, 600), (1920, 1080)]

# Defina as listas de pontos de controle p0, p1, m0 e m1 para as 5 curvas
p0_list = [np.array([0.0, 0.0, 0.0]), 
           np.array([-0.6, 0.0, 0.0]), 
           np.array([-0.7, 0.7, 0.0]), 
           np.array([0.8, 0.0, 0.0]), 
           np.array([-1.0, -1.0, 0.0])
           ]

p1_list = [np.array([0.0, 0.0, 0.0]), 
           np.array([0.6, 0.0, 0.0]), 
           np.array([0.4, 0.7, 0.0]), 
           np.array([0.9, 0.9, 0.0]), 
           np.array([-0.3, 0.3, 0.0])
           ]

m0_list = [np.array([2.0, 0.0, 0.0]), 
           np.array([0.5, 3.0, 0.0]), 
           np.array([0.9, 2.8, 0.0]), 
           np.array([0.5, -0.5, 0.0]), 
           np.array([0.5, -0.6, 0.0])
           ]

m1_list = [np.array([0.0, 2.0, 0.0]), 
           np.array([0.0, 0.0, 0.0]), 
           np.array([0.2, 2.4, 0.0]), 
           np.array([0.5, 0.5, 0.0]), 
           np.array([-0.7, 5.0, 0.0])
           ]


data = util.readFile()
p0_list, p1_list, m0_list, m1_list = util.convert_to_tuples(data)

for resolution_x, resolution_y in resolutions:
    # Crie uma nova imagem PIL, ou seja uma imagem de fundo branco
    image = Image.new('RGB', (resolution_x, resolution_y), color=(255, 255, 255))
    # Cria objeto que será usado para desenhar na imagem que está associada
    draw = ImageDraw.Draw(image)

    for i in range(len(p0_list)):
        p0 = p0_list[i]
        p1 = p1_list[i]
        m0 = m0_list[i]
        m1 = m1_list[i]

        x_curve, y_curve = rasterize_hermite_curve(p0, p1, m0, m1)

        # Redução da escala do plano para diminuir processamento
        x_scale = resolution_x / 2
        y_scale = resolution_y / 2

        # Faz a Rasterização da curva na Imagem PIL usando o draw com uma linha preta
        for j in range(1, N):
            x0 = int(round(x_curve[j - 1] * x_scale + resolution_x / 2))
            y0 = int(round(y_curve[j - 1] * y_scale + resolution_y / 2))
            x1 = int(round(x_curve[j] * x_scale + resolution_x / 2))
            y1 = int(round(y_curve[j] * y_scale + resolution_y / 2))
            draw.line((x0, y0, x1, y1), fill=(0, 0, 0), width=1)

    plt.figure(figsize=(6, 6))
    plt.imshow(image, extent=(0, resolution_x, 0, resolution_y),origin='lower')

    plt.xlabel('Eixo X')
    plt.ylabel('Eixo Y')
    plt.title(f'Cuve - Resolution: {resolution_x}x{resolution_y}')
    plt.grid(True)
    file_name = f'curves-image/curve_{resolution_x}x{resolution_y}.png'
    plt.savefig(file_name)
    plt.show()