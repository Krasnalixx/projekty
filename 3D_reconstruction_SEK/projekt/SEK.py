import sys
import os
import open3d as o3d
import numpy as np
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QFrame)
from PyQt5.QtCore import Qt
from helpers import (reset_display, display_left_right_images, display_disparity_map,
    display_depth_map, open_point_cloud_viewer)
from stereovision import run_stereo_vision
from figures import analyze_point_cloud, highlight_selected_shape



class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("SEK")

        # Główny widget i layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)  # Ustawienie centralnego widgetu
        main_layout = QVBoxLayout(main_widget)

        self.analyzed_folders = {}

        # Linia 1: Przyciski główne
        line1_layout = QHBoxLayout()
        self.file_combo = QComboBox()
        self.file_combo.setMinimumWidth(200)
        result_dir = "result"
        if os.path.exists(result_dir) and os.path.isdir(result_dir):
            items = os.listdir(result_dir)
            self.file_combo.addItems(items)
        else:
            self.file_combo.addItem("Brak danych w 'result'")

        self.view_image_button = QPushButton("Wyświetl obraz")
        self.stereo_button = QPushButton("Przeprowadź stereowizję")
        self.disparity_button = QPushButton("Wyświetl mapę dysparycji")
        self.depth_button = QPushButton("Wyświetl mapę głębi")

        line1_layout.addWidget(self.file_combo)
        line1_layout.addWidget(self.view_image_button)
        line1_layout.addWidget(self.stereo_button)
        line1_layout.addWidget(self.disparity_button)
        line1_layout.addWidget(self.depth_button)

        # Linia 2: Przyciski analizy i zaznaczania
        line2_layout = QHBoxLayout()
        self.cloud_button = QPushButton("Wyświetl chmurę punktów")
        self.analyze_button = QPushButton("Analizuj chmurę punktów")

        self.highlight_combo = QComboBox()
        self.highlight_combo.addItems(["stożek", "sfera", "walec", "prostopadłościan", "podłoże"])
        self.highlight_button = QPushButton("Zaznacz")
        self.highlight_button.setEnabled(False)

        line2_layout.addWidget(self.cloud_button)
        line2_layout.addWidget(self.analyze_button)
        line2_layout.addWidget(self.highlight_combo)
        line2_layout.addWidget(self.highlight_button)

        # Obszar wyświetlania
        self.display_frame = QFrame()
        self.display_frame.setFrameShape(QFrame.StyledPanel)
        self.display_frame.setMinimumSize(400, 300)
        display_layout = QVBoxLayout(self.display_frame)

        self.image_label = QLabel("Tu będzie wyświetlany obraz")
        self.image_label.setAlignment(Qt.AlignCenter)
        display_layout.addWidget(self.image_label)

        main_layout.addLayout(line1_layout)  # Dodanie pierwszej linii przycisków
        main_layout.addLayout(line2_layout)  # Dodanie drugiej linii przycisków
        main_layout.addWidget(self.display_frame, stretch=2)  # Dodanie obszaru wyświetlania

        # Sygnały dla przycisków
        self.file_combo.currentIndexChanged.connect(self.on_folder_changed)
        self.analyze_button.clicked.connect(self.on_analyze_clicked)
        self.view_image_button.clicked.connect(self.on_view_image_clicked)
        self.disparity_button.clicked.connect(self.on_disparity_clicked)
        self.depth_button.clicked.connect(self.on_depth_clicked)
        self.cloud_button.clicked.connect(self.on_cloud_clicked)
        self.highlight_button.clicked.connect(self.on_highlight_clicked)
        self.stereo_button.clicked.connect(self.on_stereo_clicked)

        # Inicjalizacja kontenera dla widoku chmury punktów
        self.point_cloud_viewer = None  # Widok chmury punktów będzie inicjalizowany dynamicznie

        self.on_folder_changed()

    def get_current_folder(self):
        return self.file_combo.currentText()

    def on_folder_changed(self):
        current_folder = self.get_current_folder()
        reset_display(self.image_label)
        analyzed = self.analyzed_folders.get(current_folder, False)
        self.highlight_button.setEnabled(analyzed)



    def on_view_image_clicked(self):
        current_folder = self.get_current_folder()
        reset_display(self.image_label)
        display_left_right_images(current_folder, self.image_label)

    def on_disparity_clicked(self):
        current_folder = self.get_current_folder()
        reset_display(self.image_label)
        display_disparity_map(current_folder, self.image_label)

    def on_depth_clicked(self):
        current_folder = self.get_current_folder()
        reset_display(self.image_label)
        display_depth_map(current_folder, self.image_label)

    def on_cloud_clicked(self):
        """
        Funkcja obsługująca kliknięcie przycisku "Wyświetl chmurę punktów".
        """
        current_folder = self.get_current_folder()
        reset_display(self.image_label)
        open_point_cloud_viewer(current_folder)

    def on_analyze_clicked(self):
        current_folder = self.get_current_folder()
        reset_display(self.image_label)

        try:
            # Wczytaj oryginalną chmurę punktów
            self.original_cloud = o3d.io.read_point_cloud(f"result/{current_folder}/point_cloud.ply")

            # Wywołanie analizy
            shape_times, shapes_dict, combined_cloud, filtered_points, filtered_labels, filtered_indices, outlier_indices = analyze_point_cloud(
                current_folder)

            if combined_cloud is None:
                self.image_label.setText("Nie udało się przeanalizować chmury punktów.")
                print(f"Nie udało się przeanalizować chmury punktów w folderze '{current_folder}'.")
                self.highlight_button.setEnabled(False)
                return

            # Zapisanie wyników analizy w atrybutach klasy
            self.shapes_dict = shapes_dict
            self.combined_cloud = combined_cloud
            self.filtered_points = filtered_points
            self.filtered_labels = filtered_labels
            self.filtered_indices = filtered_indices
            self.outlier_indices = outlier_indices
            self.current_folder = current_folder

            self.image_label.setText("Analiza zakończona.")
            print("Analiza zakończona, wyniki zapisane.")
            self.highlight_button.setEnabled(True)

        except FileNotFoundError:
            self.image_label.setText("Nie znaleziono pliku point_cloud.ply.")
            print(f"Nie znaleziono pliku: result/{current_folder}/point_cloud.ply")
        except Exception as e:
            self.image_label.setText("Błąd podczas analizy chmury punktów.")
            print(f"Błąd podczas analizy chmury punktów: {str(e)}")

    def on_highlight_clicked(self):
        if not hasattr(self, 'original_cloud') or self.original_cloud is None:
            self.image_label.setText("Załaduj chmurę punktów przed podświetleniem.")
            print("Załaduj chmurę punktów przed podświetleniem.")
            return

        try:
            figure_type = self.highlight_combo.currentText()

            if figure_type == "podłoże":
                # Znajdź podłoże
                plane_model, inliers = self.original_cloud.segment_plane(
                    distance_threshold=0.03,
                    ransac_n=3,
                    num_iterations=1000
                )
                ground_cloud = self.original_cloud.select_by_index(inliers)
                remaining_cloud = self.original_cloud.select_by_index(inliers, invert=True)

                # Podświetlenie podłoża
                ground_color = [1, 0, 0]
                original_colors = np.asarray(self.original_cloud.colors)
                if original_colors.size == 0:
                    original_colors = np.ones((len(np.asarray(self.original_cloud.points)), 3))

                highlighted_colors = original_colors.copy()
                for index in inliers:
                    highlighted_colors[index] = ground_color

                highlighted_cloud = o3d.geometry.PointCloud(self.original_cloud)
                highlighted_cloud.colors = o3d.utility.Vector3dVector(highlighted_colors)

                # Wyświetlenie chmury z podświetlonym podłożem
                o3d.visualization.draw_geometries([highlighted_cloud], window_name="Podłoże")
            else:
                # Obsługa standardowych figur
                shape_translation = {
                    "stożek": "cone",
                    "sfera": "sphere",
                    "walec": "cylinder",
                    "prostopadłościan": "cubic"
                }

                if figure_type not in shape_translation:
                    self.image_label.setText("Nieznany typ figury.")
                    print(f"Nieznany typ figury: {figure_type}")
                    return

                figure_type_translated = shape_translation[figure_type]
                print("Max filtered_indices:", max(self.filtered_indices))
                print("Length of outlier_indices:", len(self.outlier_indices))
                if len(self.filtered_indices) > 0 and max(self.filtered_indices) >= len(self.outlier_indices):
                    print("Błąd: Niespójne indeksy po filtracji.")
                print("Liczba punktów w original_cloud:", len(np.asarray(self.original_cloud.points)))
                print("Maksymalny indeks w outlier_indices:", np.max(self.outlier_indices))

                highlight_selected_shape(
                    pcd=self.original_cloud,  # Zamiast self.combined_cloud
                    filtered_points=self.filtered_points,
                    filtered_labels=self.filtered_labels,
                    filtered_indices=self.filtered_indices,
                    outlier_indices=self.outlier_indices,
                    shapes_dict=self.shapes_dict,
                    selected_shape=figure_type_translated,
                    highlight_color=[1, 0, 0]
                )


        except Exception as e:
            self.image_label.setText("Błąd podczas podświetlania figur.")
            print(f"Błąd podczas podświetlania figur: {str(e)}")

    def on_stereo_clicked(self):
        current_folder = self.get_current_folder()
        run_stereo_vision(current_folder)
        # Po wykonaniu stereowizji możesz np. wywołać reset_display czy coś innego.
        # Na razie tylko wykonuje stereowizję i zapisuje wyniki do plików w result/current_folder.


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
