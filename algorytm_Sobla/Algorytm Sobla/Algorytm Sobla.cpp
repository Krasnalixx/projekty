#include <iostream>
#include <fstream>
#include <string>
using namespace std;
struct BMP_naglowek_pliku
{
    uint16_t file_type{ 0x4D42 };          // File type always BM which is 0x4D42
    uint32_t file_size{ 0 };               // Size of the file (in bytes)
    uint16_t reserved1{ 0 };               // Reserved, always 0
    uint16_t reserved2{ 0 };               // Reserved, always 0
    uint32_t offset_data{ 0 };             // Start position of pixel data (bytes from the beginning of the file)
};
struct BMP_naglowek_obrazu
{
    uint32_t rozmiar_naglowka{ 0 };
    uint32_t szerokosc{ 0 };
    uint32_t wysokosc{ 0 };
    uint16_t platy{ 0 };
    uint16_t bitnapiksel{ 0 };
    uint32_t biCompression{ 0 };
    uint32_t rozmiar_rysunku{ 0 };
    uint32_t rozdzielczoscpozioma{ 0 };
    uint32_t rozdzielczoscpionowa{ 0 };
    uint32_t biCrlUses{ 0 };
    uint32_t biCrlImportant{ 0 };
};
int odczytajBMP_pliku(ifstream& ifs, BMP_naglowek_pliku& bfh);
int odczytajBMP_obrazu(ifstream& ifs, BMP_naglowek_obrazu& bfh);
void wypiszBMP_pliku(BMP_naglowek_pliku& bfh);
void wypiszBMP_obrazu(BMP_naglowek_obrazu& bfh);
int odczytajkolory(ifstream& ifs, BMP_naglowek_pliku& plik_naglowek, BMP_naglowek_obrazu& obraz_naglowek, uint8_t** kolor);
void sobel(BMP_naglowek_obrazu& obraz_naglowek, uint8_t** kol, uint8_t** zmien);
void pobierzzplikow(int maska[], ifstream& plikpob);
void wspolnywypis(BMP_naglowek_pliku& plik_naglowek, BMP_naglowek_obrazu& obraz_naglowek, uint8_t** zmien, uint8_t** kolor);
int roznemaski(ifstream& ifs, BMP_naglowek_pliku& plik_naglowek, BMP_naglowek_obrazu& obraz_naglowek, uint8_t** kol, uint8_t** zmien);
int niestandardowamaska(ifstream& ifs, BMP_naglowek_pliku& plik_naglowek, BMP_naglowek_obrazu& obraz_naglowek, uint8_t** kol, uint8_t** zmien);
void czesciowewpisywanie(ifstream& ifs, BMP_naglowek_pliku& plik_naglowek, BMP_naglowek_obrazu& obraz_naglowek);
int main()
{
    BMP_naglowek_pliku struktura_BMP_pliku;
    BMP_naglowek_obrazu  struktura_BMP_obrazu;
    string nazwa_pliku;
    cout << "Podaj nazwe pliku wejsciowego: ";
    cin >> nazwa_pliku;
    ifstream plik_zdj;
    plik_zdj.open(nazwa_pliku, ios::in | ios::binary);
    if (!plik_zdj)
    {
        cout << "blad1\n";
    }
    odczytajBMP_pliku(plik_zdj, struktura_BMP_pliku);
    odczytajBMP_obrazu(plik_zdj, struktura_BMP_obrazu);
    wypiszBMP_pliku(struktura_BMP_pliku);
    wypiszBMP_obrazu(struktura_BMP_obrazu);
    plik_zdj.seekg(struktura_BMP_pliku.offset_data, ios::beg);
    cout << "\nW jakim trybie ma pracowac program?\n";
    cout << "1 - wczytac caly plik\n";
    cout << "2 - wczytac plik podzielony na czesc\n";
    char wybor;
    cin >> wybor;
    switch (wybor)
    {
    case '1':
    {
        uint8_t** kolory = new uint8_t * [struktura_BMP_obrazu.wysokosc];
        for (int i = 0; i < struktura_BMP_obrazu.wysokosc; i++)
            kolory[i] = new uint8_t[struktura_BMP_obrazu.szerokosc * 3 + (4 - (struktura_BMP_obrazu.szerokosc * 3) % 4) % 4];
        uint8_t** zmieniona = new uint8_t * [struktura_BMP_obrazu.wysokosc];
        for (int i = 0; i < struktura_BMP_obrazu.wysokosc; i++)
            zmieniona[i] = new uint8_t[struktura_BMP_obrazu.szerokosc * 3 + (4 - (struktura_BMP_obrazu.szerokosc * 3) % 4) % 4];
        for (int i = 0; i < struktura_BMP_obrazu.wysokosc; i++)
        {
            for (int j = 0; j < struktura_BMP_obrazu.szerokosc * 3 + (4 - (struktura_BMP_obrazu.szerokosc * 3) % 4) % 4; j++)
            {
                zmieniona[i][j] = 0;
            }
        }
        cout << "Jakich masek chcesz uzyc?\n";
        cout << "1 - tryb podstawowy; uzycie wszystkich 8 masek\n";
        cout << "2 - podanie ilosci masek do uzycia\n";
        cout << "3 - uzycie niestandardowej maski\n";
        char tryb;
        cin >> tryb;
        switch (tryb)
        {
        case'1':
        {
            odczytajkolory(plik_zdj, struktura_BMP_pliku, struktura_BMP_obrazu, kolory);
            sobel(struktura_BMP_obrazu, kolory, zmieniona);
            wspolnywypis(struktura_BMP_pliku, struktura_BMP_obrazu, zmieniona, kolory);
            break;
        }
        case'2':
        {
            roznemaski(plik_zdj, struktura_BMP_pliku, struktura_BMP_obrazu, kolory, zmieniona);
            break;
        }
        case'3':
        {
            niestandardowamaska(plik_zdj, struktura_BMP_pliku, struktura_BMP_obrazu, kolory, zmieniona);
            break;
        }
        default:
        {
            cout << "podano bledne dane!\n";
            system("pause");
            return 0;
        }
        }
        for (int i = 0; i < struktura_BMP_obrazu.wysokosc; i++)
        {
            delete[] kolory[i];
            delete[] zmieniona[i];
        }
        delete[] kolory;
        delete[] zmieniona;
        break;
    }
    case'2':
    {
        czesciowewpisywanie(plik_zdj, struktura_BMP_pliku, struktura_BMP_obrazu);
        break;
    }
    default:
    {
        cout << "podano bledne dane!\n";
        system("pause");
        return 0;
    }
    }



    plik_zdj.close();
    return 0;
}
int odczytajBMP_pliku(ifstream& ifs, BMP_naglowek_pliku& bfh)
{
    ifs.read(reinterpret_cast<char*>(&bfh.file_type), 2);
    ifs.read(reinterpret_cast<char*>(&bfh.file_size), 4);
    ifs.read(reinterpret_cast<char*>(&bfh.reserved1), 2);
    ifs.read(reinterpret_cast<char*>(&bfh.reserved2), 2);
    ifs.read(reinterpret_cast<char*>(&bfh.offset_data), 4);
    return ifs.tellg();
}

int odczytajBMP_obrazu(ifstream& ifs, BMP_naglowek_obrazu& bfh)
{
    ifs.read(reinterpret_cast<char*>(&bfh.rozmiar_naglowka), 4);
    ifs.read(reinterpret_cast<char*>(&bfh.szerokosc), 4);
    ifs.read(reinterpret_cast<char*>(&bfh.wysokosc), 4);
    ifs.read(reinterpret_cast<char*>(&bfh.platy), 2);
    ifs.read(reinterpret_cast<char*>(&bfh.bitnapiksel), 2);
    ifs.read(reinterpret_cast<char*>(&bfh.biCompression), 4);
    ifs.read(reinterpret_cast<char*>(&bfh.rozmiar_rysunku), 4);
    ifs.read(reinterpret_cast<char*>(&bfh.rozdzielczoscpozioma), 4);
    ifs.read(reinterpret_cast<char*>(&bfh.rozdzielczoscpionowa), 4);
    ifs.read(reinterpret_cast<char*>(&bfh.biCrlUses), 4);
    ifs.read(reinterpret_cast<char*>(&bfh.biCrlImportant), 4);
    return ifs.tellg();
}
void wypiszBMP_pliku(BMP_naglowek_pliku& bfh)
{
    cout << "\nDane naglowka pliku:" << endl;
    cout << "Sygnatura pliku: " << bfh.file_type << endl;
    cout << "Dlugosc calego pliku: " << bfh.file_size << endl;
    cout << "Pole zarezerwowane: " << bfh.reserved1 << endl;
    cout << "Pole zarezerwowane: " << bfh.reserved2 << endl;
    cout << "Pozycja danych obrazowych w pliku: " << bfh.offset_data << endl;
}
void wypiszBMP_obrazu(BMP_naglowek_obrazu& bfh)
{
    cout << "\nDane naglowka obrazu:" << endl;
    cout << "Rozmiar naglowka informacyjnego: " << bfh.rozmiar_naglowka << endl;
    cout << "Szerokosc obrazu w pikselach: " << bfh.szerokosc << endl;
    cout << "Wysokosc obrazu w pikselach: " << bfh.wysokosc << endl;
    cout << "Liczba platow: " << bfh.platy << endl;
    cout << "Liczba bitow na piksel: " << bfh.bitnapiksel << endl;
    cout << "Algorytm kompresji: " << bfh.biCompression << endl;
    cout << "Rozmiar rysunku: " << bfh.rozmiar_rysunku << endl;
    cout << "Rozdzielczosc pozioma: " << bfh.rozdzielczoscpozioma << endl;
    cout << "Rozdzielczosc pionowa: " << bfh.rozdzielczoscpionowa << endl;
    cout << "Liczba kolorow w palecie: " << bfh.biCrlUses << endl;
    cout << "Liczba waznych kolorow w palecie: " << bfh.biCrlImportant << endl;
}
int odczytajkolory(ifstream& ifs, BMP_naglowek_pliku& plik_naglowek, BMP_naglowek_obrazu& obraz_naglowek, uint8_t** kolor)
{
    for (int i = 0; i < obraz_naglowek.wysokosc; i++)
    {
        for (int j = 0; j < obraz_naglowek.szerokosc * 3 + (4 - (obraz_naglowek.szerokosc * 3) % 4) % 4; j++)
        {
            ifs.read(reinterpret_cast<char*>(&kolor[i][j]), 1);
        }
    }
    return ifs.tellg();
}
void sobel(BMP_naglowek_obrazu& obraz_naglowek, uint8_t** kol, uint8_t** zmien)
{
    ifstream plikpob;
    plikpob.open("maska.txt");
    if (!plikpob) cout << "blad2\n";
    int  m0[9];
    int  m1[9];
    int  m2[9];
    int  m3[9];
    int  m4[9];
    int  m5[9];
    int  m6[9];
    int  m7[9];
    pobierzzplikow(m0, plikpob);
    pobierzzplikow(m1, plikpob);
    pobierzzplikow(m2, plikpob);
    pobierzzplikow(m3, plikpob);
    pobierzzplikow(m4, plikpob);
    pobierzzplikow(m5, plikpob);
    pobierzzplikow(m6, plikpob);
    pobierzzplikow(m7, plikpob);
    for (int i = 1; i < obraz_naglowek.wysokosc - 1; i++)
    {
        for (int j = 3; j < obraz_naglowek.szerokosc * 3 - 3; j++)
        {
            int s[8];
            s[0] = kol[i - 1][j - 3] * m0[0] + kol[i - 1][j] * m0[1] + kol[i - 1][j + 3] * m0[2] + kol[i][j - 3] * m0[3] + kol[i][j] * m0[4] + kol[i][j + 3] * m0[5] + kol[i + 1][j - 3] * m0[6] + kol[i + 1][j] * m0[7] + kol[i + 1][j + 3] * m0[8];
            s[1] = kol[i - 1][j - 3] * m1[0] + kol[i - 1][j] * m1[1] + kol[i - 1][j + 3] * m1[2] + kol[i][j - 3] * m1[3] + kol[i][j] * m1[4] + kol[i][j + 3] * m1[5] + kol[i + 1][j - 3] * m1[6] + kol[i + 1][j] * m1[7] + kol[i + 1][j + 3] * m1[8];
            s[2] = kol[i - 1][j - 3] * m2[0] + kol[i - 1][j] * m2[1] + kol[i - 1][j + 3] * m2[2] + kol[i][j - 3] * m2[3] + kol[i][j] * m2[4] + kol[i][j + 3] * m2[5] + kol[i + 1][j - 3] * m2[6] + kol[i + 1][j] * m2[7] + kol[i + 1][j + 3] * m2[8];
            s[3] = kol[i - 1][j - 3] * m3[0] + kol[i - 1][j] * m3[1] + kol[i - 1][j + 3] * m3[2] + kol[i][j - 3] * m3[3] + kol[i][j] * m3[4] + kol[i][j + 3] * m3[5] + kol[i + 1][j - 3] * m3[6] + kol[i + 1][j] * m3[7] + kol[i + 1][j + 3] * m3[8];
            s[4] = kol[i - 1][j - 3] * m4[0] + kol[i - 1][j] * m4[1] + kol[i - 1][j + 3] * m4[2] + kol[i][j - 3] * m4[3] + kol[i][j] * m4[4] + kol[i][j + 3] * m4[5] + kol[i + 1][j - 3] * m4[6] + kol[i + 1][j] * m4[7] + kol[i + 1][j + 3] * m4[8];
            s[5] = kol[i - 1][j - 3] * m5[0] + kol[i - 1][j] * m5[1] + kol[i - 1][j + 3] * m5[2] + kol[i][j - 3] * m5[3] + kol[i][j] * m5[4] + kol[i][j + 3] * m5[5] + kol[i + 1][j - 3] * m5[6] + kol[i + 1][j] * m5[7] + kol[i + 1][j + 3] * m5[8];
            s[6] = kol[i - 1][j - 3] * m6[0] + kol[i - 1][j] * m6[1] + kol[i - 1][j + 3] * m6[2] + kol[i][j - 3] * m6[3] + kol[i][j] * m6[4] + kol[i][j + 3] * m6[5] + kol[i + 1][j - 3] * m6[6] + kol[i + 1][j] * m6[7] + kol[i + 1][j + 3] * m6[8];
            s[7] = kol[i - 1][j - 3] * m7[0] + kol[i - 1][j] * m7[1] + kol[i - 1][j + 3] * m7[2] + kol[i][j - 3] * m7[3] + kol[i][j] * m7[4] + kol[i][j + 3] * m7[5] + kol[i + 1][j - 3] * m7[6] + kol[i + 1][j] * m7[7] + kol[i + 1][j + 3] * m7[8];
            for (int q = 0; q < 8; q++)
            {
                if (s[q] < 0) { s[q] = 0; }
                else  if (s[q] > 255) { s[q] = 255; }
            }
            zmien[i][j] = (s[0] + s[1] + s[2] + s[3] + s[4] + s[5] + s[6] + s[7]) / 8;
        }
    }
    plikpob.close();
}
void pobierzzplikow(int maska[], ifstream& plikpob)
{

    string s;
    int k = 0;
    while (getline(plikpob, s))
    {
        maska[k] = stoi(s);
        k++;
        if (k % 9 == 0) break;
    }
}
void wspolnywypis(BMP_naglowek_pliku& plik_naglowek, BMP_naglowek_obrazu& obraz_naglowek, uint8_t** zmien, uint8_t** kolor)
{
    string nazwa;
    cout << "Podaj nazwe pliku wyjsciowego: ";
    cin >> nazwa;
    ofstream plik_wypis;
    plik_wypis.open(nazwa, ios::out | ios::binary);
    if (!plik_wypis)
    {
        cout << "blad3\n";
    }
    plik_wypis.write((char*)&plik_naglowek.file_type, 2);
    plik_wypis.write((char*)&plik_naglowek.file_size, 4);
    plik_wypis.write((char*)&plik_naglowek.reserved1, 2);
    plik_wypis.write((char*)&plik_naglowek.reserved2, 2);
    plik_wypis.write((char*)&plik_naglowek.offset_data, 4);

    plik_wypis.write((char*)&obraz_naglowek.rozmiar_naglowka, 4);
    plik_wypis.write((char*)&obraz_naglowek.szerokosc, 4);
    plik_wypis.write((char*)&obraz_naglowek.wysokosc, 4);
    plik_wypis.write((char*)&obraz_naglowek.platy, 2);
    plik_wypis.write((char*)&obraz_naglowek.bitnapiksel, 2);
    plik_wypis.write((char*)&obraz_naglowek.biCompression, 4);
    plik_wypis.write((char*)&obraz_naglowek.rozmiar_rysunku, 4);
    plik_wypis.write((char*)&obraz_naglowek.rozdzielczoscpozioma, 4);
    plik_wypis.write((char*)&obraz_naglowek.rozdzielczoscpionowa, 4);
    plik_wypis.write((char*)&obraz_naglowek.biCrlUses, 4);
    plik_wypis.write((char*)&obraz_naglowek.biCrlImportant, 4);

    for (int i = 0; i < obraz_naglowek.wysokosc; i++)
    {
        for (int j = 0; j < obraz_naglowek.szerokosc * 3 + (4 - (obraz_naglowek.szerokosc * 3) % 4) % 4; j++)
        {
            plik_wypis.write((char*)&zmien[i][j], 1);
        }
    }
    plik_wypis.close();
}
int roznemaski(ifstream& ifs, BMP_naglowek_pliku& plik_naglowek, BMP_naglowek_obrazu& obraz_naglowek, uint8_t** kol, uint8_t** zmien)
{
    odczytajkolory(ifs, plik_naglowek, obraz_naglowek, kol);
    ifstream plikpob;
    plikpob.open("maska.txt");
    if (!plikpob) cout << "blad2\n";
    int  m0[9];
    int  m1[9];
    int  m2[9];
    int  m3[9];
    int  m4[9];
    int  m5[9];
    int  m6[9];
    int  m7[9];
    pobierzzplikow(m0, plikpob);
    pobierzzplikow(m1, plikpob);
    pobierzzplikow(m2, plikpob);
    pobierzzplikow(m3, plikpob);
    pobierzzplikow(m4, plikpob);
    pobierzzplikow(m5, plikpob);
    pobierzzplikow(m6, plikpob);
    pobierzzplikow(m7, plikpob);
    cout << "ile masek chcesz uzyc?\n";
    int ilosc;
    cin >> ilosc;
    int* s = new int[ilosc];
    for (int buf = 0; buf < ilosc; buf++)
    {
        cout << "jakiej maski uzyc?\n";
        cout << "1 - pionowa\n";
        cout << "2 - pozioma\n";
        cout << "3 - ukosna w prawy dol\n";
        cout << "4 - ukosna w lewy dol\n";
        char jaka;
        cin >> jaka;
        switch (jaka)
        {
        case'1':
        {
            for (int i = 1; i < obraz_naglowek.wysokosc - 1; i++)
            {
                for (int j = 3; j < obraz_naglowek.szerokosc * 3 - 3; j++)
                {
                    s[buf] = kol[i - 1][j - 3] * m0[0] + kol[i - 1][j] * m0[1] + kol[i - 1][j + 3] * m0[2] + kol[i][j - 3] * m0[3] + kol[i][j] * m0[4] + kol[i][j + 3] * m0[5] + kol[i + 1][j - 3] * m0[6] + kol[i + 1][j] * m0[7] + kol[i + 1][j + 3] * m0[8];
                    if (s[buf] < 0) { s[buf] = 0; }
                    else  if (s[buf] > 255) { s[buf] = 255; }
                    zmien[i][j] += s[buf];
                }
            }
            break;
        }
        case'2':
        {
            for (int i = 1; i < obraz_naglowek.wysokosc - 1; i++)
            {
                for (int j = 3; j < obraz_naglowek.szerokosc * 3 - 3; j++)
                {
                    s[buf] = kol[i - 1][j - 3] * m1[0] + kol[i - 1][j] * m1[1] + kol[i - 1][j + 3] * m1[2] + kol[i][j - 3] * m1[3] + kol[i][j] * m1[4] + kol[i][j + 3] * m1[5] + kol[i + 1][j - 3] * m1[6] + kol[i + 1][j] * m1[7] + kol[i + 1][j + 3] * m1[8];
                    if (s[buf] < 0) { s[buf] = 0; }
                    else  if (s[buf] > 255) { s[buf] = 255; }
                    zmien[i][j] += s[buf];
                }
            }
            break;
        }
        case'3':
        {
            for (int i = 1; i < obraz_naglowek.wysokosc - 1; i++)
            {
                for (int j = 3; j < obraz_naglowek.szerokosc * 3 - 3; j++)
                {
                    s[buf] = kol[i - 1][j - 3] * m2[0] + kol[i - 1][j] * m2[1] + kol[i - 1][j + 3] * m2[2] + kol[i][j - 3] * m2[3] + kol[i][j] * m2[4] + kol[i][j + 3] * m2[5] + kol[i + 1][j - 3] * m2[6] + kol[i + 1][j] * m2[7] + kol[i + 1][j + 3] * m2[8];
                    if (s[buf] < 0) { s[buf] = 0; }
                    else  if (s[buf] > 255) { s[buf] = 255; }
                    zmien[i][j] += s[buf];
                }
            }
            break;
        }
        case'4':
        {
            for (int i = 1; i < obraz_naglowek.wysokosc - 1; i++)
            {
                for (int j = 3; j < obraz_naglowek.szerokosc * 3 - 3; j++)
                {
                    s[buf] = kol[i - 1][j - 3] * m3[0] + kol[i - 1][j] * m3[1] + kol[i - 1][j + 3] * m3[2] + kol[i][j - 3] * m3[3] + kol[i][j] * m3[4] + kol[i][j + 3] * m3[5] + kol[i + 1][j - 3] * m3[6] + kol[i + 1][j] * m3[7] + kol[i + 1][j + 3] * m3[8];
                    if (s[buf] < 0) { s[buf] = 0; }
                    else  if (s[buf] > 255) { s[buf] = 255; }
                    zmien[i][j] += s[buf];
                }
            }
            break;
        }
        default:
        {
            cout << "podano bledne dane!\n";
            system("pause");
            return 1;
        }
        }
    }
    for (int i = 1; i < obraz_naglowek.wysokosc - 1; i++)
    {
        for (int j = 3; j < obraz_naglowek.szerokosc * 3 - 3; j++)
        {
            zmien[i][j] = zmien[i][j] / ilosc;
        }
    }
    wspolnywypis(plik_naglowek, obraz_naglowek, zmien, kol);
    delete[] s;
    plikpob.close();
}
int niestandardowamaska(ifstream& ifs, BMP_naglowek_pliku& plik_naglowek, BMP_naglowek_obrazu& obraz_naglowek, uint8_t** kol, uint8_t** zmien)
{
    cout << "podaj rozmiar maski (nieparzysta liczba): ";
    int wymiar;
    cin >> wymiar;
    if (!wymiar % 2)
    {
        cout << "podano bledne dane!\n";
        system("pause");
        return 1;
    }
    int** maska = new int* [wymiar];
    for (int i = 0; i < wymiar; i++)
        maska[i] = new int[wymiar];
    for (int i = 0; i <= wymiar / 2; i++)
    {
        for (int j = 0; j < wymiar / 2; j++)                            //lewa gorna czesc
        {
            maska[i][j] = i + j + 1;
        }
    }
    for (int i = wymiar / 2 + 1; i < wymiar; i++)
    {
        for (int j = 0; j < wymiar / 2; j++)
        {
            maska[i][j] = maska[wymiar - i - 1][j];                         //lewa dolna czesc
        }
    }
    for (int i = 0; i < wymiar; i++)
    {
        maska[i][wymiar / 2] = 0;                                               //srodkowa kolumna zer
    }
    for (int i = 0; i <= wymiar / 2; i++)
    {
        for (int j = wymiar / 2 + 1; j < wymiar; j++)
        {
            maska[i][j] = -maska[i][wymiar - j - 1];                                //prawa gorna czesc
        }
    }
    for (int i = wymiar / 2 + 1; i < wymiar; i++)
    {
        for (int j = wymiar / 2 + 1; j < wymiar; j++)                                   //prawa dolna czesc
        {
            maska[i][j] = maska[wymiar - i - 1][j];
        }
    }
    for (int i = 0; i < wymiar; i++)
    {
        for (int j = 0; j < wymiar; j++)
        {
            cout << maska[i][j] << " ";
        }
        cout << endl;
    }
    odczytajkolory(ifs, plik_naglowek, obraz_naglowek, kol);
    int suma = 0;
    for (int i = wymiar / 2; i < obraz_naglowek.wysokosc - wymiar / 2; i++)
    {
        for (int j = 3 * (wymiar / 2); j < obraz_naglowek.szerokosc * 3 - 3 * (wymiar / 2); j++)
        {
            for (int a = 0; a < wymiar; a++)
            {
                for (int b = 0; b < wymiar; b++)
                {
                    suma += maska[a][b] * kol[i - wymiar / 2 + a][j - (wymiar / 2 + b) * 3];
                    if (suma < 0) suma = 0;
                    if (suma > 255) suma = 255;
                }
            }
            zmien[i][j] = suma;
        }
    }
    wspolnywypis(plik_naglowek, obraz_naglowek, zmien, kol);
    for (int i = 0; i < wymiar; i++)
    {
        delete[] maska[i];
    }
    delete[] maska;
}

void czesciowewpisywanie(ifstream& ifs, BMP_naglowek_pliku& plik_naglowek, BMP_naglowek_obrazu& obraz_naglowek)
{
    static int dolna = 0;
    static int gorna = 100;
    static int licznik = 0;
    int ilosc = gorna - dolna;      //ile linijek pobiera
    ifstream plikpob;
    plikpob.open("maska.txt");
    if (!plikpob) cout << "blad2\n";
    int  m0[9];
    int  m1[9];
    int  m2[9];
    int  m3[9];                                         //maski
    int  m4[9];
    int  m5[9];
    int  m6[9];
    int  m7[9];
    pobierzzplikow(m0, plikpob);
    pobierzzplikow(m1, plikpob);
    pobierzzplikow(m2, plikpob);
    pobierzzplikow(m3, plikpob);
    pobierzzplikow(m4, plikpob);
    pobierzzplikow(m5, plikpob);
    pobierzzplikow(m6, plikpob);
    pobierzzplikow(m7, plikpob);
    string nazwa;
    cout << "Podaj nazwe pliku wyjsciowego: ";
    cin >> nazwa;
    ofstream plik_wypis;
    plik_wypis.open(nazwa, ios::out | ios::binary);
    if (!plik_wypis)
    {
        cout << "blad3\n";
    }
    plik_wypis.write((char*)&plik_naglowek.file_type, 2);
    plik_wypis.write((char*)&plik_naglowek.file_size, 4);
    plik_wypis.write((char*)&plik_naglowek.reserved1, 2);
    plik_wypis.write((char*)&plik_naglowek.reserved2, 2);
    plik_wypis.write((char*)&plik_naglowek.offset_data, 4);

    plik_wypis.write((char*)&obraz_naglowek.rozmiar_naglowka, 4);
    plik_wypis.write((char*)&obraz_naglowek.szerokosc, 4);
    plik_wypis.write((char*)&obraz_naglowek.wysokosc, 4);
    plik_wypis.write((char*)&obraz_naglowek.platy, 2);
    plik_wypis.write((char*)&obraz_naglowek.bitnapiksel, 2);                                    //wypisanie naglowka
    plik_wypis.write((char*)&obraz_naglowek.biCompression, 4);
    plik_wypis.write((char*)&obraz_naglowek.rozmiar_rysunku, 4);
    plik_wypis.write((char*)&obraz_naglowek.rozdzielczoscpozioma, 4);
    plik_wypis.write((char*)&obraz_naglowek.rozdzielczoscpionowa, 4);
    plik_wypis.write((char*)&obraz_naglowek.biCrlUses, 4);
    plik_wypis.write((char*)&obraz_naglowek.biCrlImportant, 4);
    while (gorna < obraz_naglowek.wysokosc)
    {
        uint8_t** kol = new uint8_t * [ilosc];
        uint8_t** zmien = new uint8_t * [ilosc];
        for (int i = 0; i < ilosc; i++)
        {
            kol[i] = new uint8_t[obraz_naglowek.szerokosc * 3 + (4 - (obraz_naglowek.szerokosc * 3) % 4) % 4];
            zmien[i] = new uint8_t[obraz_naglowek.szerokosc * 3 + (4 - (obraz_naglowek.szerokosc * 3) % 4) % 4];
        }
        for (int i = 0; i < ilosc; i++)
        {
            for (int j = 0; j < obraz_naglowek.szerokosc * 3 + (4 - (obraz_naglowek.szerokosc * 3) % 4) % 4; j++)
            {
                zmien[i][j] = 0;                                                                                                        //wczytanie czesci danych i wypelnienie drugiej tablicy "zerami"
                ifs.read(reinterpret_cast<char*>(&kol[i][j]), 1);
            }
        }
        for (int i = 1; i < ilosc - 1; i++)
        {
            for (int j = 3; j < obraz_naglowek.szerokosc * 3 - 3; j++)
            {
                int s[8];
                s[0] = kol[i - 1][j - 3] * m0[0] + kol[i - 1][j] * m0[1] + kol[i - 1][j + 3] * m0[2] + kol[i][j - 3] * m0[3] + kol[i][j] * m0[4] + kol[i][j + 3] * m0[5] + kol[i + 1][j - 3] * m0[6] + kol[i + 1][j] * m0[7] + kol[i + 1][j + 3] * m0[8];
                s[1] = kol[i - 1][j - 3] * m1[0] + kol[i - 1][j] * m1[1] + kol[i - 1][j + 3] * m1[2] + kol[i][j - 3] * m1[3] + kol[i][j] * m1[4] + kol[i][j + 3] * m1[5] + kol[i + 1][j - 3] * m1[6] + kol[i + 1][j] * m1[7] + kol[i + 1][j + 3] * m1[8];
                s[2] = kol[i - 1][j - 3] * m2[0] + kol[i - 1][j] * m2[1] + kol[i - 1][j + 3] * m2[2] + kol[i][j - 3] * m2[3] + kol[i][j] * m2[4] + kol[i][j + 3] * m2[5] + kol[i + 1][j - 3] * m2[6] + kol[i + 1][j] * m2[7] + kol[i + 1][j + 3] * m2[8];
                s[3] = kol[i - 1][j - 3] * m3[0] + kol[i - 1][j] * m3[1] + kol[i - 1][j + 3] * m3[2] + kol[i][j - 3] * m3[3] + kol[i][j] * m3[4] + kol[i][j + 3] * m3[5] + kol[i + 1][j - 3] * m3[6] + kol[i + 1][j] * m3[7] + kol[i + 1][j + 3] * m3[8];
                s[4] = kol[i - 1][j - 3] * m4[0] + kol[i - 1][j] * m4[1] + kol[i - 1][j + 3] * m4[2] + kol[i][j - 3] * m4[3] + kol[i][j] * m4[4] + kol[i][j + 3] * m4[5] + kol[i + 1][j - 3] * m4[6] + kol[i + 1][j] * m4[7] + kol[i + 1][j + 3] * m4[8];
                s[5] = kol[i - 1][j - 3] * m5[0] + kol[i - 1][j] * m5[1] + kol[i - 1][j + 3] * m5[2] + kol[i][j - 3] * m5[3] + kol[i][j] * m5[4] + kol[i][j + 3] * m5[5] + kol[i + 1][j - 3] * m5[6] + kol[i + 1][j] * m5[7] + kol[i + 1][j + 3] * m5[8];
                s[6] = kol[i - 1][j - 3] * m6[0] + kol[i - 1][j] * m6[1] + kol[i - 1][j + 3] * m6[2] + kol[i][j - 3] * m6[3] + kol[i][j] * m6[4] + kol[i][j + 3] * m6[5] + kol[i + 1][j - 3] * m6[6] + kol[i + 1][j] * m6[7] + kol[i + 1][j + 3] * m6[8];
                s[7] = kol[i - 1][j - 3] * m7[0] + kol[i - 1][j] * m7[1] + kol[i - 1][j + 3] * m7[2] + kol[i][j - 3] * m7[3] + kol[i][j] * m7[4] + kol[i][j + 3] * m7[5] + kol[i + 1][j - 3] * m7[6] + kol[i + 1][j] * m7[7] + kol[i + 1][j + 3] * m7[8];
                for (int q = 0; q < 8; q++)
                {
                    if (s[q] < 0) { s[q] = 0; }
                    else  if (s[q] > 255) { s[q] = 255; }
                }
                zmien[i][j] = (s[0] + s[1] + s[2] + s[3] + s[4] + s[5] + s[6] + s[7]) / 8;
            }
        }
        if (dolna == 0)
        {
            for (int j = 0; j < obraz_naglowek.szerokosc * 3 + (4 - (obraz_naglowek.szerokosc * 3) % 4) % 4; j++)
            {
                plik_wypis.write((char*)&zmien[0][j], 1);
            }
        }
        for (int i = 1; i < ilosc - 1; i++)
        {
            for (int j = 0; j < obraz_naglowek.szerokosc * 3 + (4 - (obraz_naglowek.szerokosc * 3) % 4) % 4; j++)
            {
                plik_wypis.write((char*)&zmien[i][j], 1);
            }
        }
        int poz = ifs.tellg();
        ifs.seekg(poz - 2 * (obraz_naglowek.szerokosc * 3 + (4 - (obraz_naglowek.szerokosc * 3) % 4) % 4), ios::beg);                //cofanie kursora o 2 linijki
        dolna += ilosc - 2;
        gorna += ilosc - 2;
        for (int i = 0; i < ilosc; i++)
        {
            delete[] kol[i];
            delete[] zmien[i];
        }                                                                                       //zwalnianie pamieci
        delete[] kol;
        delete[] zmien;
        plikpob.close();
        licznik++;
    }
    //------------------------------------------------------------------------------------------------reszta--------------------------------------------------------------------------------------------------
    uint8_t** kol2 = new uint8_t * [ilosc];
    for (int i = 0; i < obraz_naglowek.wysokosc - dolna; i++)
        kol2[i] = new uint8_t[obraz_naglowek.szerokosc * 3 + (4 - (obraz_naglowek.szerokosc * 3) % 4) % 4];
    uint8_t** zmien2 = new uint8_t * [obraz_naglowek.wysokosc - dolna];
    for (int i = 0; i < obraz_naglowek.wysokosc - dolna; i++)
        zmien2[i] = new uint8_t[obraz_naglowek.szerokosc * 3 + (4 - (obraz_naglowek.szerokosc * 3) % 4) % 4];

    for (int i = 0; i < obraz_naglowek.wysokosc - dolna; i++)
    {
        for (int j = 0; j < obraz_naglowek.szerokosc * 3 + (4 - (obraz_naglowek.szerokosc * 3) % 4) % 4; j++)
        {
            zmien2[i][j] = 0;
            ifs.read(reinterpret_cast<char*>(&kol2[i][j]), 1);
        }
    }
    for (int i = 1; i < obraz_naglowek.wysokosc - dolna - 1; i++)
    {
        for (int j = 3; j < obraz_naglowek.szerokosc * 3 - 3; j++)
        {
            int s[8];
            s[0] = kol2[i - 1][j - 3] * m0[0] + kol2[i - 1][j] * m0[1] + kol2[i - 1][j + 3] * m0[2] + kol2[i][j - 3] * m0[3] + kol2[i][j] * m0[4] + kol2[i][j + 3] * m0[5] + kol2[i + 1][j - 3] * m0[6] + kol2[i + 1][j] * m0[7] + kol2[i + 1][j + 3] * m0[8];
            s[1] = kol2[i - 1][j - 3] * m1[0] + kol2[i - 1][j] * m1[1] + kol2[i - 1][j + 3] * m1[2] + kol2[i][j - 3] * m1[3] + kol2[i][j] * m1[4] + kol2[i][j + 3] * m1[5] + kol2[i + 1][j - 3] * m1[6] + kol2[i + 1][j] * m1[7] + kol2[i + 1][j + 3] * m1[8];
            s[2] = kol2[i - 1][j - 3] * m2[0] + kol2[i - 1][j] * m2[1] + kol2[i - 1][j + 3] * m2[2] + kol2[i][j - 3] * m2[3] + kol2[i][j] * m2[4] + kol2[i][j + 3] * m2[5] + kol2[i + 1][j - 3] * m2[6] + kol2[i + 1][j] * m2[7] + kol2[i + 1][j + 3] * m2[8];
            s[3] = kol2[i - 1][j - 3] * m3[0] + kol2[i - 1][j] * m3[1] + kol2[i - 1][j + 3] * m3[2] + kol2[i][j - 3] * m3[3] + kol2[i][j] * m3[4] + kol2[i][j + 3] * m3[5] + kol2[i + 1][j - 3] * m3[6] + kol2[i + 1][j] * m3[7] + kol2[i + 1][j + 3] * m3[8];
            s[4] = kol2[i - 1][j - 3] * m4[0] + kol2[i - 1][j] * m4[1] + kol2[i - 1][j + 3] * m4[2] + kol2[i][j - 3] * m4[3] + kol2[i][j] * m4[4] + kol2[i][j + 3] * m4[5] + kol2[i + 1][j - 3] * m4[6] + kol2[i + 1][j] * m4[7] + kol2[i + 1][j + 3] * m4[8];
            s[5] = kol2[i - 1][j - 3] * m5[0] + kol2[i - 1][j] * m5[1] + kol2[i - 1][j + 3] * m5[2] + kol2[i][j - 3] * m5[3] + kol2[i][j] * m5[4] + kol2[i][j + 3] * m5[5] + kol2[i + 1][j - 3] * m5[6] + kol2[i + 1][j] * m5[7] + kol2[i + 1][j + 3] * m5[8];
            s[6] = kol2[i - 1][j - 3] * m6[0] + kol2[i - 1][j] * m6[1] + kol2[i - 1][j + 3] * m6[2] + kol2[i][j - 3] * m6[3] + kol2[i][j] * m6[4] + kol2[i][j + 3] * m6[5] + kol2[i + 1][j - 3] * m6[6] + kol2[i + 1][j] * m6[7] + kol2[i + 1][j + 3] * m6[8];
            s[7] = kol2[i - 1][j - 3] * m7[0] + kol2[i - 1][j] * m7[1] + kol2[i - 1][j + 3] * m7[2] + kol2[i][j - 3] * m7[3] + kol2[i][j] * m7[4] + kol2[i][j + 3] * m7[5] + kol2[i + 1][j - 3] * m7[6] + kol2[i + 1][j] * m7[7] + kol2[i + 1][j + 3] * m7[8];
            for (int q = 0; q < 8; q++)
            {
                if (s[q] < 0) { s[q] = 0; }
                else  if (s[q] > 255) { s[q] = 255; }
            }
            zmien2[i][j] = (s[0] + s[1] + s[2] + s[3] + s[4] + s[5] + s[6] + s[7]) / 8;
        }
    }
    for (int i = 1; i < obraz_naglowek.wysokosc - dolna; i++)
    {
        for (int j = 0; j < obraz_naglowek.szerokosc * 3 + (4 - (obraz_naglowek.szerokosc * 3) % 4) % 4; j++)
        {
            plik_wypis.write((char*)&zmien2[i][j], 1);
        }
    }
    for (int i = 0; i < obraz_naglowek.wysokosc - dolna - 2; i++)
    {
        delete[] kol2[i];
        delete[] zmien2[i];
    }
    delete[] kol2;
    delete[] zmien2;
}

