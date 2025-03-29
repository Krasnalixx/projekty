import os
import open3d as o3d
from PIL import Image
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QLabel


def reset_display(image_label: QLabel):
    """
    Resetuje wyświetlany obraz do domyślnego napisu.
    Wywoływać przy zmianie folderu.
    """
    image_label.clear()
    image_label.setText("Tu będzie wyświetlany obraz")
    image_label.setAlignment(Qt.AlignCenter)

def scale_pixmap_to_label(pixmap: QPixmap, image_label: QLabel):
    """
    Skaluje pixmapę do rozmiaru image_label z zachowaniem proporcji.
    """
    if pixmap.isNull():
        return pixmap
    scaled = pixmap.scaled(image_label.width(), image_label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation)
    return scaled

def display_left_right_images(folder: str, image_label: QLabel):
    """
    Wyświetla img_left.png i img_right.png obok siebie i skaluje do labela.
    """
    left_path = os.path.join("result", folder, "img_left.png")
    right_path = os.path.join("result", folder, "img_right.png")

    if not (os.path.exists(left_path) and os.path.exists(right_path)):
        image_label.setText("Brak obrazów img_left.png i/lub img_right.png")
        return

    left_img = Image.open(left_path).convert("RGB")
    right_img = Image.open(right_path).convert("RGB")

    # Łączymy obrazy obok siebie
    w, h = left_img.size
    w2, h2 = right_img.size
    total_width = w + w2
    max_height = max(h, h2)

    new_img = Image.new('RGB', (total_width, max_height))
    new_img.paste(left_img, (0, 0))
    new_img.paste(right_img, (w, 0))

    qimage = QImage(new_img.tobytes(), new_img.size[0], new_img.size[1], QImage.Format_RGB888)
    pixmap = QPixmap.fromImage(qimage)

    scaled = scale_pixmap_to_label(pixmap, image_label)
    image_label.setPixmap(scaled)
    image_label.setAlignment(Qt.AlignCenter)


def display_disparity_map(folder: str, image_label: QLabel):
    """
    Wyświetla disparity_map.png i skaluje do labela.
    """
    disp_path = os.path.join("result", folder, "disparity_map.png")
    if not os.path.exists(disp_path):
        image_label.setText("Brak disparity_map.png")
        return

    pixmap = QPixmap(disp_path)
    scaled = scale_pixmap_to_label(pixmap, image_label)
    image_label.setPixmap(scaled)
    image_label.setAlignment(Qt.AlignCenter)


def display_depth_map(folder: str, image_label: QLabel):
    depth_path = os.path.join("result", folder, "depth_map.png")
    if not os.path.exists(depth_path):
        image_label.setText("Brak depth_map.png")
        return

    pixmap = QPixmap(depth_path)
    scaled = scale_pixmap_to_label(pixmap, image_label)
    image_label.setPixmap(scaled)
    image_label.setAlignment(Qt.AlignCenter)


def open_point_cloud_viewer(folder_path):
    point_cloud_path = os.path.join("result", folder_path, "point_cloud.ply")

    try:
        # Wczytaj chmurę punktów z pliku
        pcd = o3d.io.read_point_cloud(point_cloud_path)

        # Sprawdzenie liczby punktów
        if len(pcd.points) == 0:
            print("Chmura punktów jest pusta.")
            return

        # Wyświetlenie chmury punktów w nowym oknie
        o3d.visualization.draw_geometries([pcd], window_name="Chmura Punktów")
    except FileNotFoundError:
        print(f"Nie znaleziono pliku: {point_cloud_path}")
    except Exception as e:
        print(f"Błąd podczas wyświetlania chmury punktów: {str(e)}")


def find_and_display_ground(pcd, distance_threshold=0.01, ransac_n=3, num_iterations=1000):

    # Sprawdzamy, czy chmura punktów jest poprawna
    if pcd.is_empty():
        print("Chmura punktów jest pusta.")
        return None

    try:
        # Segmentacja płaszczyzny (podłoża)
        plane_model, inliers = pcd.segment_plane(
            distance_threshold=distance_threshold,
            ransac_n=ransac_n,
            num_iterations=num_iterations
        )

        # Wyciągnięcie podłoża i nadanie kolorów
        ground_cloud = pcd.select_by_index(inliers)

        print(f"Podłoże znalezione z parametrami: a={plane_model[0]:.2f}, b={plane_model[1]:.2f}, "
              f"c={plane_model[2]:.2f}, d={plane_model[3]:.2f}.")

        # Wyświetlenie chmury punktów dla podłoża
        o3d.visualization.draw_geometries([ground_cloud], window_name="Podłoże w oryginalnych kolorach")

        return ground_cloud

    except Exception as e:
        print(f"Błąd podczas znajdowania podłoża: {str(e)}")
        return None

