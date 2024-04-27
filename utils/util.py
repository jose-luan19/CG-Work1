import math
import random
import numpy as np

def get_resolutions():
  return [(100, 100), (300, 300), (800, 600), (1920, 1080)]

def generate_matrix(fill_value, height, width):
    return np.full((height, width), fill_value, dtype=np.uint8)

def add_point(x, y, points):
  points.append((round(x), round(y)))

def plot_raster(points, height, width):
  matrix = generate_matrix(0, height, width)
  for x, y in points:
    if 0 <= y < height and 0 <= x < width:
      matrix[math.floor(y)][math.floor(x)] = 1

  return matrix

def gen_point():
    x = random.uniform(-1, 1)
    y = random.uniform(-1, 1)

    return (x, y)

def normalization(X, Y, width, height):
  rmin = -1
  rmax = 1

  ys = (Y - rmin) / (rmax - rmin)
  xs = (X - rmin) / (rmax - rmin)

  xs *= height - 0
  ys *= width - 0

  xs += 0
  ys += 0

  return (round(xs), round(ys))