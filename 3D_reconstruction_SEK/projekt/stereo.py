import cv2
import numpy as np
import glob
import os
import json

# Ustawienia dla szachownicy
CHECKERBOARD = (6,9)  # Rozmiar wewnętrznych narożników szachownicy
square_size = 6.5  # Rozmiar jednego pola szachownicy w cm

# Ścieżki do folderów z obrazami i do zapisywania wyników
image_folder_1 = "ZDJ/lewa_3"  # Ścieżka do folderu z obrazami z lewej kamery
image_folder_2 = "ZDJ/prawa_3"  # Ścieżka do folderu z obrazami z prawej kamery
output_folder = "ZDJ/narozniki"  # Ścieżka do folderu na obrazy z wykrytymi rogami
json_folder = "JSON"  # Ścieżka do folderu na plik JSON
output_stereo_json_filename = os.path.join(json_folder, "LewaPrawaSTEREO.json")

# Wczytywanie parametrów z plików JSON
def load_intrinsics(json_filename):
    with open(json_filename, 'r') as f:
        data = json.load(f)
    return data

# Ścieżki do plików JSON z parametrami kamer
intrinsics1 = load_intrinsics("JSON/lewa_K.json")
intrinsics2 = load_intrinsics("JSON/prawa_K.json")

# Tworzenie folderów, jeśli nie istnieją
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
objpoints, imgpoints1, imgpoints2 = [], [], []

# Licznik zdjęć z wykrytymi rogami
found_corners_count = 0

# Ładowanie obrazów
images1 = sorted(glob.glob(os.path.join(image_folder_1, '*.png')))
images2 = sorted(glob.glob(os.path.join(image_folder_2, '*.png')))

# Sprawdzenie, czy liczba obrazów jest zgodna
if len(images1) != len(images2):
    print("Liczba obrazów nie jest zgodna w obu folderach.")
else:
    print(f"Liczba wczytanych zdjęć z obu kamer: {len(images1)}")

# Przetwarzanie par obrazów z obu kamer
for i, (fname1, fname2) in enumerate(zip(images1, images2)):
    print(f"Przetwarzam parę zdjęć {i + 1}/{len(images1)}: {fname1} i {fname2}")
    img1 = cv2.imread(fname1)
    img2 = cv2.imread(fname2)

    # Skalowanie obrazów
    img1 = cv2.resize(img1, (1024, 768))
    img2 = cv2.resize(img2, (1024, 768))
    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    # Wykrywanie rogów szachownicy
    ret1, corners1 = cv2.findChessboardCorners(gray1, CHECKERBOARD, None)
    ret2, corners2 = cv2.findChessboardCorners(gray2, CHECKERBOARD, None)
    print(f"Rogi znalezione w obrazie lewej kamery: {ret1}, w obrazie prawej kamery: {ret2}")

    if ret1 and ret2:
        found_corners_count += 1
        objpoints.append(objp)

        # Dokładniejsza detekcja narożników
        corners1 = cv2.cornerSubPix(gray1, corners1, (11, 11), (-1, -1), criteria)
        corners2 = cv2.cornerSubPix(gray2, corners2, (11, 11), (-1, -1), criteria)
        imgpoints1.append(corners1)
        imgpoints2.append(corners2)

        # Rysowanie rogów na obrazach
        img_with_corners1 = cv2.drawChessboardCorners(img1.copy(), CHECKERBOARD, corners1, ret1)
        img_with_corners2 = cv2.drawChessboardCorners(img2.copy(), CHECKERBOARD, corners2, ret2)

        # Zapis obrazów z rogami
        output_path1 = os.path.join(output_folder, f"narozniki_lewa_{i + 1}.jpg")
        output_path2 = os.path.join(output_folder, f"narozniki_prawa_{i + 1}.jpg")
        cv2.imwrite(output_path1, img_with_corners1)
        cv2.imwrite(output_path2, img_with_corners2)
        print(f"Zapisano obrazy z narożnikami: {output_path1} oraz {output_path2}")

        # Wyświetlanie obrazów z rogami
        cv2.imshow('Szachownica - Lewa Kamera', img_with_corners1)
        cv2.imshow('Szachownica - Prawa Kamera', img_with_corners2)
        cv2.waitKey(2000)  # Krótkie opóźnienie na podgląd rogów

cv2.destroyAllWindows()

# Wyświetlanie liczby par zdjęć z wykrytymi rogami
print(f"Liczba par zdjęć z wykrytymi rogami: {found_corners_count}/{len(images1)}")

# Wczytanie parametrów wewnętrznych kamer
mtx1 = np.array(intrinsics1['camera_matrix'])
dist1 = np.array(intrinsics1['distortion_coefficients'][0])
mtx2 = np.array(intrinsics2['camera_matrix'])
dist2 = np.array(intrinsics2['distortion_coefficients'][0])

# Stereo kalibracja
if len(objpoints) > 0:
    ret, mtx1, dist1, mtx2, dist2, R, T, E, F = cv2.stereoCalibrate(
        objpoints, imgpoints1, imgpoints2, mtx1, dist1, mtx2, dist2, gray1.shape[::-1],
        flags=cv2.CALIB_FIX_INTRINSIC, criteria=criteria)

    print(f"Błąd RMS kalibracji stereo: {ret}")

    # Zapis wyników kalibracji stereo do pliku JSON
    stereo_calibration_data = {
        "RMS_error": ret,
        "R": R.tolist(),
        "T": T.tolist(),
        "Essential_matrix": E.tolist(),
        "Fundamental_matrix": F.tolist()
    }
    with open(output_stereo_json_filename, 'w') as json_file:
        json.dump(stereo_calibration_data, json_file, indent=4)

    print("Kalibracja stereo zakończona.")
    print("R:", R)
    print("T:", T)
else:
    print("Nie znaleziono wystarczającej liczby par obrazów z wykrytymi narożnikami do przeprowadzenia kalibracji stereo.")
