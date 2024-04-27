
# Analizator Zmian Obrazu

## Opis projektu

Projekt `Analizator Zmian Obrazu` to narzędzie do analizy i identyfikacji różnic między dwoma obrazami, które są wizualnie podobne, ale mogą różnić się szczegółami takimi jak rozmiar, położenie czy orientacja obiektów. Projekt wykorzystuje Pythona oraz biblioteki OpenCV i matplotlib do przetwarzania obrazów i wizualizacji wyników.

## Funkcjonalności

- Wczytywanie dwóch obrazów (oryginału i zmodyfikowanej wersji).
- Rozdzielenie obrazów na kanały kolorów.
- Detekcja i wizualizacja zmian na obrazach.
- Zaznaczanie obszarów, które różnią się między obrazami.
- Eksport wyników analizy do pliku PNG z przezroczystością tych miejsc, które uległy zmianie.

## Wymagania

- Python 3.6+
- OpenCV
- NumPy
- Matplotlib

## Instalacja bibliotek

Biblioteki można zainstalować za pomocą poniższego polecenia:

```bash
pip install numpy opencv-python matplotlib
```

## Struktura projektu

```plaintext
Analizator_Zmian_Obrazu/
|- dublin.jpg           # Oryginalny obraz
|- dublin_edited.jpg    # Edytowany obraz
|- analizator.py        # Skrypt główny
|- README.md            # Ten plik
```

## Uruchomienie projektu

Aby uruchomić projekt, wykonaj skrypt `kevin.py` w terminalu lub środowisku programistycznym:

```bash
python kevin.py
```

## Przykładowe wyniki

Wyniki działania programu zostaną zapisane w pliku `kevin.png`, który zawiera wykryte różnice z zaznaczeniem na przezroczystym tle.

## Autor

Przemysław Piątkiewiczc

## Licencja

Ten projekt jest udostępniany na licencji MIT. Szczegóły znajdziesz w pliku `LICENSE`.
