
### Instrukcja do Gry Pentago

**Pentago** to strategiczna gra planszowa dla dwóch graczy, której celem jest ułożenie pięciu swoich znaków w rzędzie. Gra wykorzystuje obrotowe sektory planszy, co dodaje dodatkową warstwę taktycznego planowania.

#### Wymagania Systemowe
- System operacyjny: Windows, Linux lub MacOS
- Kompilator: Zgodny z C++, np. GCC, Clang, MSVC

#### Kompilacja i Uruchomienie
Aby skompilować grę, potrzebny jest kompilator obsługujący standard C++11 lub nowszy. Przykładowe polecenie kompilacji dla GCC:
```
g++ -std=c++11 -o pentago main.cpp
```
Aby uruchomić grę, wystarczy wykonać skompilowany plik:
```
./pentago
```

#### Zasady Gry
1. Plansza składa się z czterech kwadrantów, każdy zawiera 3x3 pola.
2. Gracze na przemian umieszczają swoje znaki ('o' lub 'x') na dowolnym wolnym polu.
3. Po wykonaniu ruchu (dodaniu znaku), gracz musi wybrać jeden z kwadrantów i obrócić go o 90 stopni w lewo lub w prawo.
4. Wygrywa gracz, który jako pierwszy ułoży pięć swoich znaków w rzędzie (pionowo, poziomo lub na skos) na całej planszy.

#### Opcje Dodatkowe
- **Zmiana znaku**: Gracze mogą zmieniać znak, którym grają w trakcie gry.
- **Cofanie ruchu (Undo)**: Możliwość cofnięcia ruchu do poprzedniego stanu.
- **Pauza**: Gracze mogą zatrzymać grę na czas nieokreślony.
- **Predefiniowana plansza**: Możliwość wczytania predefiniowanej konfiguracji planszy.

#### Interakcja z Graczem
Gra komunikuje się z użytkownikiem poprzez konsolę, gdzie gracze wprowadzają swoje ruchy oraz wybierają opcje. Tekst jest jasny i prosty, co ułatwia zrozumienie bieżącego stanu gry.
#### Autor

Przemysław Piątkiewicz

#### Licencja

Ten projekt jest udostępniany na licencji MIT. Szczegóły znajdziesz w pliku `LICENSE`.
