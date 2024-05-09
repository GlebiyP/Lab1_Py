import matplotlib.pyplot as plt
import numpy as np

def generate_points(num_points, xlim=(-10, 10), ylim=(-10, 10)):
    np.random.seed()  # Задаємо seed випадковим числом
    return np.random.uniform(xlim[0], xlim[1], num_points), np.random.uniform(ylim[0], ylim[1], num_points)

def plot_points(points, hull, furthest_points=None):
    plt.scatter(points[:,0], points[:,1], c='b', label='Points', s = 5)
    for i in range(len(hull)):
        plt.plot([points[hull[i]][0], points[hull[(i+1)%len(hull)]][0]], [points[hull[i]][1], points[hull[(i+1)%len(hull)]][1]], 'g-')
    if furthest_points:
        plt.scatter(points[furthest_points, 0], points[furthest_points, 1], c='r', label='Furthest Points')
        plt.plot([points[furthest_points[0]][0], points[furthest_points[1]][0]], [points[furthest_points[0]][1], points[furthest_points[1]][1]], 'r--')
    plt.scatter(points[hull, 0], points[hull, 1], c='g', label='Convex Hull Points')
    plt.text(points[hull[0]][0], points[hull[0]][1], '  Start', verticalalignment='bottom')
    plt.text(points[hull[-1]][0], points[hull[-1]][1], '  End', verticalalignment='bottom')
    plt.legend()
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.title('Convex Hull with Furthest Points')
    plt.grid(True)
    plt.show()

def orientation(p, q, r):
    val = (q[1] - p[1]) * (r[0] - q[0]) - (q[0] - p[0]) * (r[1] - q[1])
    if val == 0:
        return 0
    return 1 if val > 0 else 2

def convex_hull(points):
    n = len(points)
    if n < 3:
        return None

    # Знаходимо точку з найменшою y-координатою (якщо їх декілька, то точку з найменшою x-координатою)
    min_idx = 0
    for i in range(1, n):
        if points[i][1] < points[min_idx][1] or (points[i][1] == points[min_idx][1] and points[i][0] < points[min_idx][0]):
            min_idx = i

    hull = []
    p = min_idx
    q = None

    while True:
        hull.append(p)

        q = (p + 1) % n
        for i in range(n):
            if orientation(points[p], points[i], points[q]) == 2:
                q = i

        p = q

        if p == min_idx:
            break

    return hull

def find_furthest_points(points, hull):
    max_dist = 0
    furthest_points = None
    for i in range(len(hull)):
        for j in range(i+1, len(hull)):
            dist = np.linalg.norm(points[hull[i]] - points[hull[j]])
            if dist > max_dist:
                max_dist = dist
                furthest_points = (hull[i], hull[j])
    return furthest_points

# Кількість точок, що генеруються
num_points = 10000

# Генеруємо точки
points_x, points_y = generate_points(num_points)
points = np.array(list(zip(points_x, points_y)))

# Будуємо опуклу оболонку
hull = convex_hull(points)

# Знаходимо найбільш віддалені точки
furthest_points = find_furthest_points(points, hull)

# Малюємо графік
plot_points(points, hull, furthest_points)
