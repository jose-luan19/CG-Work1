import matplotlib.pyplot as plt
import numpy as np
from PIL import Image, ImageDraw
import os

def hermite_curve(t, p0, p1, m0, m1, M):
    tt = np.array([t ** 3, t ** 2, t, 1])
    pt = np.dot(np.dot(tt, M), np.vstack((p0, p1, m0, m1)))
    return pt[0], pt[1]



def rasterize_hermite_curve(p0, p1, m0, m1, num_points=100, M=None):
    t_values = np.linspace(0, 1, num_points)
    x_values = []
    y_values = []

    for t in t_values:
        point = hermite_curve(t, p0, p1, m0, m1, M)
        x_values.append(point[0])
        y_values.append(point[1])

    return x_values, y_values

# Defina a matriz de transformação de Hermite
M = np.array([[2, -2, 1, 1],
              [-3, 3, -2, -1],
              [0, 0, 1, 0],
              [1, 0, 0, 0]])

# Defina as resoluções desejadas
resolutions = [(100, 100), (300, 300), (800, 600), (1920, 1080)]
#resolutions = [(100,100)]

# Lista de cores para as curvas
colors = ['red', 'green', 'blue', 'purple', 'orange']

# Defina as listas de pontos de controle p0, p1, m0 e m1 para as 5 curvas
p0_list = [np.array([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 0.0]), np.array([0.0, 0.0, 0.0])]
p1_list = [np.array([1.0, 1.0, 0.0]), np.array([-1.0, 1.0, 0.0]), np.array([-1.0, -1.0, 0.0]), np.array([1.0, -1.0, 0.0]), np.array([0.0, 0.0, 0.0])]
m0_list = [np.array([5.0, 0.0, 0.0]), np.array([-5.0, 0.0, 0.0]), np.array([0.0, -5.0, 0.0]), np.array([0.0, -5.0, 0.0]), np.array([0.0, 0.0, 0.0])]
m1_list = [np.array([5.0, 0.0, 0.0]), np.array([-5.0, 0.0, 0.0]), np.array([0.0, -5.0, 0.0]), np.array([0.0, -5.0, 0.0]), np.array([0.0, 0.0, 0.0])]


# Input para definir a quantidade de pontos na curva
num_points = int(1000)

for resolution_x, resolution_y in resolutions:
    # Crie uma nova imagem PIL
    image = Image.new('RGB', (resolution_x, resolution_y), color=(0, 0, 0))
    draw = ImageDraw.Draw(image)

    for i in range(1):
        p0 = p0_list[i]
        p1 = p1_list[i]
        m0 = m0_list[i]
        m1 = m1_list[i]

        x_curve, y_curve = rasterize_hermite_curve(p0, p1, m0, m1, num_points, M)

        x_scale = resolution_x / 2
        y_scale = resolution_y / 2

        for j in range(1, len(x_curve)):
            x0 = int(round(x_curve[j - 1] * x_scale + resolution_x / 2))
            y0 = int(round(y_curve[j - 1] * y_scale + resolution_y / 2))
            x1 = int(round(x_curve[j] * x_scale + resolution_x / 2))
            y1 = int(round(y_curve[j] * y_scale + resolution_y / 2))
            draw.line((x0, y0, x1, y1), fill=(255, 255, 255), width=1)

    plt.figure(figsize=(6, 6))
    plt.imshow(image, extent=(0, resolution_x, 0, resolution_y),origin='lower')

    plt.xlabel('Eixo X')
    plt.ylabel('Eixo Y')
    plt.title(f'Curvas de Hermite Rasterizadas ({resolution_x}x{resolution_y})')
    plt.grid(True)
    plt.show()

    file_name = f'image/curvas_hermite_{resolution_x}x{resolution_y}.png'
    image.save(file_name)

    if os.path.exists(file_name):
        print(f"Imagem salva com sucesso no arquivo {file_name}")
    else:
        print(f"A imagem não foi salva no arquivo {file_name}")
