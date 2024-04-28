# Algorytm Sobel

## Opis
Projekt implementuje algorytm Sobel, który służy do wykrywania krawędzi w obrazach za pomocą operatora Sobela. Algorytm czyta obrazy w formacie BMP, stosuje różne maski Sobela do analizy gradientów jasności pikseli, a następnie generuje nowy obraz wynikowy z zaznaczonymi krawędziami.

## Funkcjonalności
- Wczytywanie obrazów BMP.
- Możliwość użycia różnych masek filtrujących.
- Wsparcie dla niestandardowych masek definiowanych przez użytkownika.
- Możliwość pracy w trybie wczytania całego pliku lub podzielonego na części.

## Wymagania
- Kompilator C++ obsługujący standard C++11 lub nowszy.
- Obrazy wejściowe muszą być w formacie BMP.

## Sposób użycia
1. Skompiluj plik źródłowy projektu.
2. Uruchom program i podaj ścieżkę do pliku BMP.
3. Wybierz tryb pracy programu:
   - Wczytaj cały plik.
   - Wczytaj plik podzielony na części.
4. Podaj nazwę pliku wynikowego, w którym zostaną zapisane wyniki.

## Przykład kompilacji i uruchomienia
```bash
g++ -o sobel SobelAlgorithm.cpp
./sobel
```
## Autor 
Przemysław Piątkiewicz

## Licencja
Ten projekt jest udostępniany na licencji MIT. Szczegóły znajdziesz w pliku `LICENSE`.
