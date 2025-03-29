import cv2
import os

# Nazwy folderów dla obu kamer
name1 = "Prawa"
name2 = "Lewa"
close_value = True
n1, n2 = 1, 1

# Ścieżki do zapisu obrazów
folder_path1 = "ZDJ/" + name1 + '_test1'
folder_path2 = "ZDJ/" + name2 + '_test1'

# Inicjalizacja przechwytywania wideo dla dwóch kamer
vidcap1 = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Indeks pierwszej kamery
vidcap2 = cv2.VideoCapture(2, cv2.CAP_DSHOW)  # Indeks drugiej kamery

# Sprawdzenie, czy foldery istnieją; jeśli nie, to zostają utworzone
if not os.path.exists(folder_path1):
    os.makedirs(folder_path1)
if not os.path.exists(folder_path2):
    os.makedirs(folder_path2)

# Znajdź ostatnie numery obrazów w folderach, aby uniknąć nadpisywania
existing_images1 = [img for img in os.listdir(folder_path1) if img.startswith('img') and img.endswith('.png')]
if existing_images1:
    n1 = max([int(img[3:-4]) for img in existing_images1]) + 1  # Rozpocznij od następnego numeru

existing_images2 = [img for img in os.listdir(folder_path2) if img.startswith('img') and img.endswith('.png')]
if existing_images2:
    n2 = max([int(img[3:-4]) for img in existing_images2]) + 1  # Rozpocznij od następnego numeru



# Ustawienie rozdzielczości dla obu kamer
vidcap1.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
vidcap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
vidcap2.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)
vidcap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)
vidcap1.set(cv2.CAP_PROP_FPS, 5)  # Ustawienie FPS na 5 klatek na sekundę dla kamery 1
vidcap2.set(cv2.CAP_PROP_FPS, 5)  # Ustawienie FPS na 5 klatek na sekundę dla kamery 2


# Sprawdzenie, czy ustawienia rozdzielczości się powiodły
actual_width1 = vidcap1.get(cv2.CAP_PROP_FRAME_WIDTH)
actual_height1 = vidcap1.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(f"Ustawiona rozdzielczość kamery 1: {int(actual_width1)}x{int(actual_height1)}")

actual_width2 = vidcap2.get(cv2.CAP_PROP_FRAME_WIDTH)
actual_height2 = vidcap2.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(f"Ustawiona rozdzielczość kamery 2: {int(actual_width2)}x{int(actual_height2)}")

# Współczynnik skalowania do wyświetlania pełnego obrazu w mniejszym oknie
display_scale = 0.4

while close_value:
    # Przechwycenie klatek z obu kamer
    success1, img1 = vidcap1.read()
    success2, img2 = vidcap2.read()

    if success1 and success2:
        # Zmniejszenie rozmiaru obrazów do wyświetlania
        display_img1 = cv2.resize(img1, (0, 0), fx=display_scale, fy=display_scale)
        display_img2 = cv2.resize(img2, (0, 0), fx=display_scale, fy=display_scale)

        # Wyświetlanie podglądu dla obu kamer
        cv2.imshow('Preview Camera 1', display_img1)
        cv2.imshow('Preview Camera 2', display_img2)

    k = cv2.waitKey(5)
    if k == 27:  # Klawisz ESC
        close_value = False
    elif k == ord('s'):  # Klawisz 's' dla zapisu zdjęć z obu kamer
        # Zapis zdjęcia z kamery 1
        file_path1 = os.path.join(folder_path1, f'img{n1}.png')
        cv2.imwrite(file_path1, img1)
        print(f"Obraz nr {n1} z kamery 1 zapisany")
        n1 += 1

        # Zapis zdjęcia z kamery 2
        file_path2 = os.path.join(folder_path2, f'img{n2}.png')
        cv2.imwrite(file_path2, img2)
        print(f"Obraz nr {n2} z kamery 2 zapisany")
        n2 += 1

# Zwolnienie zasobów
vidcap1.release()
vidcap2.release()
cv2.destroyAllWindows()
