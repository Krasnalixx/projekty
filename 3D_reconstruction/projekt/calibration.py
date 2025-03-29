import cv2
import numpy as np
import glob
import os
import json

# Ustawienia dla szachownicy
CHECKERBOARD = (6,9)  # Rozmiar wewnętrznych narożników szachownicy
square_size = 6.5  # Rozmiar jednego pola szachownicy w cm

img_folder = "prawa_K"
# Folder z obrazami i folder do zapisywania wyników
image_folder = "ZDJ/" + img_folder  # Ścieżka do folderu z obrazami
output_folder = "ZDJ/narozniki"  # Ścieżka do folderu na obrazy z wykrytymi rogami
json_folder = "JSON"  # Folder do zapisu pliku JSON
json_filename = img_folder + ".json"  # Nazwa pliku JSON

# Tworzenie folderów „narozniki” i „JSON” jeśli nie istnieją
if not os.path.exists(output_folder):
    os.makedirs(output_folder)
if not os.path.exists(json_folder):
    os.makedirs(json_folder)

# Kryteria dla funkcji cornerSubPix
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 0.01)

# Współrzędne punktów szachownicy w przestrzeni 3D
objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2) * square_size

# Listy na punkty 3D (świat) i punkty 2D (obraz)
objpoints = []
imgpoints = []

# Licznik zdjęć z wykrytymi rogami
found_corners_count = 0

# Ładowanie obrazów
images = glob.glob(os.path.join(image_folder, '*.png'))

if len(images) == 0:
    print("Brak zdjęć w folderze 'zdjecia'. Upewnij się, że folder zawiera pliki .jpg.")
else:
    print(f"Liczba wczytanych zdjęć: {len(images)}")

for i, fname in enumerate(images):
    print(f"Przetwarzam zdjęcie {i + 1}/{len(images)}: {fname}")
    img = cv2.imread(fname)

    # Skalowanie obrazu
    img = cv2.resize(img, (1024, 768))
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Wykrywanie rogów szachownicy
    ret, corners = cv2.findChessboardCorners(gray, CHECKERBOARD, None)
    print(f"Rogi znalezione: {ret}")

    if ret:
        found_corners_count += 1
        objpoints.append(objp)

        # Dokładniejsza detekcja narożników
        corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
        imgpoints.append(corners2)

        # Rysowanie rogów na obrazie
        img_with_corners = cv2.drawChessboardCorners(img.copy(), CHECKERBOARD, corners2, ret)

        # Zapis obrazu z rogami
        output_path = os.path.join(output_folder, f"narozniki_{i + 1}.jpg")
        cv2.imwrite(output_path, img_with_corners)
        print(f"Zapisano obraz z narożnikami: {output_path}")

        # Wyświetlanie obrazu z rogami
        cv2.imshow('Szachownica', img_with_corners)
        cv2.waitKey(500)  # Krótkie opóźnienie na podgląd rogów

cv2.destroyAllWindows()

# Wyświetlanie liczby zdjęć z wykrytymi rogami
print(f"Liczba zdjęć z wykrytymi rogami: {found_corners_count}/{len(images)}")

# Kalibracja kamery
ret, camera_matrix, distortion_coefficients, rotation_vectors, translation_vectors = cv2.calibrateCamera(
    objpoints, imgpoints, gray.shape[::-1], None, None
)

# Przygotowanie danych do zapisu w JSON zgodnie z Twoim formatem
calibration_data = {
    "camera_matrix": camera_matrix.tolist(),
    "distortion_coefficients": distortion_coefficients.tolist(),
    "rotation_vectors": [rvec.tolist() for rvec in rotation_vectors],
    "translation_vectors": [tvec.tolist() for tvec in translation_vectors]
}

# Ścieżka do pliku JSON
json_path = os.path.join(json_folder, json_filename)

# Zapis danych do pliku JSON
with open(json_path, 'w') as json_file:
    json.dump(calibration_data, json_file, indent=4)

print(f"Dane kalibracyjne zapisano do pliku JSON: {json_path}")
