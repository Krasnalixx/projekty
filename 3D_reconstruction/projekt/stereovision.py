import os
import json
import numpy as np
import cv2
from PIL import Image
import open3d as o3d


def run_stereo_vision(image_folder_name: str):
    folder_path = 'JSON'
    image_folder_path = f'result/{image_folder_name}'

    def load_json_file(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    # Wczytanie plików JSON
    lewa_K = load_json_file(os.path.join(folder_path, 'lewa_K.json'))
    prawa_K = load_json_file(os.path.join(folder_path, 'prawa_K.json'))
    lewa_prawa_stereo = load_json_file(os.path.join(folder_path, 'LewaPrawaSTEREO.json'))

    # Ścieżki do obrazów
    left_image_path = os.path.join(image_folder_path, 'img_left.png')
    right_image_path = os.path.join(image_folder_path, 'img_right.png')

    # Wczytanie obrazów przy użyciu PIL
    if not os.path.exists(left_image_path) or not os.path.exists(right_image_path):
        print("Brak obrazów img_left.png lub img_right.png w wybranym folderze.")
        return

    left_image = Image.open(left_image_path)
    right_image = Image.open(right_image_path)

    # Skala do przeskalowania obrazów (np. 0.5)
    scale_factor = 0.5
    new_size_left = (int(left_image.width * scale_factor), int(left_image.height * scale_factor))
    new_size_right = (int(right_image.width * scale_factor), int(right_image.height * scale_factor))

    left_image_resized = left_image.resize(new_size_left)
    right_image_resized = right_image.resize(new_size_right)

    left_image_cv = np.array(left_image_resized)
    right_image_cv = np.array(right_image_resized)

    # Konwersja z RGB do BGR dla OpenCV
    left_image_cv = cv2.cvtColor(left_image_cv, cv2.COLOR_RGB2BGR)
    right_image_cv = cv2.cvtColor(right_image_cv, cv2.COLOR_RGB2BGR)

    K_left = np.array(lewa_K['camera_matrix'])
    K_right = np.array(prawa_K['camera_matrix'])

    dist_left = np.array(lewa_K['distortion_coefficients'])
    dist_right = np.array(prawa_K['distortion_coefficients'])

    # Konwersja do skali szarości
    left_gray = cv2.cvtColor(left_image_cv, cv2.COLOR_BGR2GRAY)
    right_gray = cv2.cvtColor(right_image_cv, cv2.COLOR_BGR2GRAY)

    # Tworzenie obiektu StereoSGBM
    stereo = cv2.StereoSGBM_create(
        minDisparity=0,
        numDisparities=16,
        blockSize=5,
        P1=8 * 3 * 5 ** 2,
        P2=32 * 3 * 5 ** 2,
        disp12MaxDiff=1,
        uniquenessRatio=10,
        speckleWindowSize=100,
        speckleRange=32
    )

    # Obliczenie mapy dysparycji
    disparity = stereo.compute(left_gray, right_gray)
    disparity_normalized = cv2.normalize(disparity, None, 0, 255, cv2.NORM_MINMAX)
    disparity_normalized = np.uint8(disparity_normalized)

    # Wyświetlanie oryginalnych obrazów (opcjonalne)
    # Możesz usunąć jeśli nie chcesz mieć okien matplotlib
    # plt.figure(figsize=(10, 5))
    # plt.subplot(1, 2, 1)
    # plt.imshow(cv2.cvtColor(left_image_cv, cv2.COLOR_BGR2RGB))
    # plt.title("Lewa Kamera")
    # plt.axis('off')
    # plt.subplot(1, 2, 2)
    # plt.imshow(cv2.cvtColor(right_image_cv, cv2.COLOR_BGR2RGB))
    # plt.title("Prawa Kamera")
    # plt.axis('off')
    # plt.tight_layout()
    # plt.show()

    disparity_map_path = f'result/{image_folder_name}/disparity_map.png'
    if not os.path.exists(disparity_map_path):
        print(f"Błąd: Plik '{disparity_map_path}' nie istnieje.")
    else:
        disparity_image = cv2.imread(disparity_map_path, cv2.IMREAD_GRAYSCALE)
        if disparity_image is None:
            print(f"Błąd: Nie udało się wczytać pliku '{disparity_map_path}'.")
        else:
            # plt.figure(figsize=(8, 6))
            # plt.imshow(disparity_image, cmap='gray')
            # plt.title("Mapa Dysparycji")
            # plt.axis('off')
            # plt.show()
            pass

    T = np.array(lewa_prawa_stereo['T'])
    B = np.linalg.norm(T)
    f = K_left[0, 0]  # Ogniskowa

    depth_map = (f * B) / (disparity + 1e-5)
    depth_map_normalized = cv2.normalize(depth_map, None, 0, 255, cv2.NORM_MINMAX)
    depth_map_normalized = np.uint8(depth_map_normalized)

    depth_map_path = f'result/{image_folder_name}/depth_map.png'
    if not os.path.exists(depth_map_path):
        print(f"Błąd: Plik '{depth_map_path}' nie istnieje.")
    else:
        depth_image = cv2.imread(depth_map_path, cv2.IMREAD_GRAYSCALE)
        if depth_image is None:
            print(f"Błąd: Nie udało się wczytać pliku '{depth_map_path}'.")
        else:
            # plt.figure(figsize=(8, 6))
            # plt.imshow(depth_image, cmap='gray')
            # plt.title("Mapa Głębi")
            # plt.axis('off')
            # plt.show()
            pass

    height, width = depth_map.shape
    fx, fy = K_left[0, 0], K_left[1, 1]
    cx, cy = K_left[0, 2], K_left[1, 2]

    points = []
    colors = []
    ply_input_path = f'result/{image_folder_name}/point_cloud2.ply'

    for v in range(height):
        for u in range(width):
            Z_norm = depth_map[v, u] / 255.0 * 10
            X = (u - cx) * Z_norm / fx
            Y = (v - cy) * Z_norm / fy
            points.append([X, Y, Z_norm])
            B_val, G_val, R_val = left_image_cv[v, u]
            colors.append([R_val/255.0, G_val/255.0, B_val/255.0])

    point_cloud = o3d.geometry.PointCloud()
    point_cloud.points = o3d.utility.Vector3dVector(points)
    point_cloud.colors = o3d.utility.Vector3dVector(colors)

    # Zapisz chmurę punktów
    #o3d.io.write_point_cloud(ply_input_path, point_cloud)
