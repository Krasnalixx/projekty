import cv2
import os

name = "lewa_sss"
close_value = True
n = 1

# Ścieżka, gdzie będą zapisywane obrazy
folder_path = "ZDJ/" + name

vidcap = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # Użycie DSHOW jako backendu

# Sprawdzenie, czy folder istnieje; jeśli nie, to zostaje utworzony
if not os.path.exists(folder_path):
    os.makedirs(folder_path)

# Znajdź ostatni numer obrazu w folderze, aby uniknąć nadpisywania
existing_images = [img for img in os.listdir(folder_path) if img.startswith('img') and img.endswith('.png')]
if existing_images:
    n = max([int(img[3:-4]) for img in existing_images]) + 1  # Rozpocznij od następnego numeru

# Inicjalizacja przechwytywania wideo
#vidcap = cv2.VideoCapture(1)  # indeks kamery, dostosuj w razie potrzeby

# Ustaw najwyższą możliwą rozdzielczość

vidcap.set(cv2.CAP_PROP_FRAME_WIDTH, 1920)  # Szerokość
vidcap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1080)  # Wysokość

# Sprawdzenie, czy ustawienie rozdzielczości się powiodło
actual_width = vidcap.get(cv2.CAP_PROP_FRAME_WIDTH)
actual_height = vidcap.get(cv2.CAP_PROP_FRAME_HEIGHT)
print(f"Ustawiona rozdzielczość: {int(actual_width)}x{int(actual_height)}")

# Współczynnik skalowania do wyświetlania pełnego obrazu w mniejszym oknie
display_scale = 0.4  # 50% oryginalnej wielkości, zmień, jeśli chcesz mniejsze/większe okno

while close_value:
    success, img = vidcap.read()
    if success:
        # Zmniejsz rozmiar obrazu do wyświetlania, aby lepiej mieścił się w oknie podglądu
        display_img = cv2.resize(img, (0, 0), fx=display_scale, fy=display_scale)
        cv2.imshow('Preview', display_img)

    k = cv2.waitKey(5)
    if k == 27:  # Klawisz ESC
        close_value = False
    elif k == ord('s'):  # Klawisz 's'
        file_path = os.path.join(folder_path, 'img' + str(n) + '.png')
        cv2.imwrite(file_path, img)
        print("Obraz nr " + str(n) + " zapisany")
        n += 1

# Zwolnienie zasobów
vidcap.release()
cv2.destroyAllWindows()
