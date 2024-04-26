#include <iostream>
#include <cstdlib>
#include <stdlib.h>
#include <time.h>
#include <string.h>
#include <string>
using namespace std;
const int rozmiar = 3;
const int dlugosc = 20;
void wpisztablice(char tab[rozmiar][rozmiar]);
void krawedzgorna();
void srodkowapusta(char tab[rozmiar][rozmiar]);
void srodkowapelna();
void krawedzdolna();
void wypiszwygrana(char Q[rozmiar][rozmiar], char W[rozmiar][rozmiar], char A[rozmiar][rozmiar], char S[rozmiar][rozmiar], char imiePIERWSZE[dlugosc], char imieDRUGIE[dlugosc], char pierwszygracz, char drugigracz);
void wypisz(char Q[rozmiar][rozmiar], char W[rozmiar][rozmiar], char A[rozmiar][rozmiar], char S[rozmiar][rozmiar], int czasPIERWSZY, int czasDRUGI, char imiePIERWSZE[dlugosc], char imieDRUGIE[dlugosc], char pierwszygracz, char drugigracz);
void wypiszhistoria(char Q[rozmiar][rozmiar], char W[rozmiar][rozmiar], char A[rozmiar][rozmiar], char S[rozmiar][rozmiar], char imiePIERWSZE[dlugosc], char imieDRUGIE[dlugosc], char pierwszygracz, char drugigracz);
int wyliczaniewypisan();
void dopisz(char tab[rozmiar][rozmiar], int pole, char pierwszygracz, char drugigracz, int zajete);
int sprawdzdopisanie(char tab[rozmiar][rozmiar], int znak);
int sprawdzzwyciestwo(char Q[rozmiar][rozmiar], char W[rozmiar][rozmiar], char A[rozmiar][rozmiar], char S[rozmiar][rozmiar], char pierwszygracz, char drugigracz, int czasPIERWSZY, int czasDRUGI, bool predefiniowana, int& zajete);
void obrocwlewo(char tab[rozmiar][rozmiar]);
void obrocwprawo(char tab[rozmiar][rozmiar]);
void wyborplanszyipola(char imiePIERWSZE[dlugosc], char imieDRUGIE[dlugosc], char& pierwszygracz, char& drugigracz, char Q[rozmiar][rozmiar], char W[rozmiar][rozmiar], char A[rozmiar][rozmiar], char S[rozmiar][rozmiar], int czasPIERWSZY, int czasDRUGI, int& pauzaczas, bool& predefiniowana, int& zajete, char planszaDOPISANIA[rozmiar * rozmiar * 4], int poleDOPISANIA[rozmiar * rozmiar * 4], bool kolkoikrzyzyk, char planszaOBROTU[rozmiar * rozmiar * 4], char stronaOBROTU[rozmiar * rozmiar * 4]);
void wyborplanszydoobrotu(char  Q[rozmiar][rozmiar], char W[rozmiar][rozmiar], char A[rozmiar][rozmiar], char S[rozmiar][rozmiar], char imiePIERWSZE[dlugosc], char imieDRUGIE[dlugosc], char pierwszygracz, char drugigracz, int czasPIERWSZY, int czasDRUGI, char planszaOBROTU[rozmiar * rozmiar * 4], char stronaOBROTU[rozmiar * rozmiar * 4], int zajete);
void opcje(char& aktualnyznak, char znakprzeciwnika, char Q[rozmiar][rozmiar], char W[rozmiar][rozmiar], char A[rozmiar][rozmiar], char S[rozmiar][rozmiar], int& pauzaczas, bool& predefiniowana, int& zajete, char planszaDOPISANIA[rozmiar * rozmiar * 4], int poleDOPISANIA[rozmiar * rozmiar * 4], char planszaOBROTU[rozmiar * rozmiar * 4], char stronaOBROTU[rozmiar * rozmiar * 4], bool kolkoikrzyzyk);
void zmienznak(char& staryznak, char znakprzeciwnika, char Q[rozmiar][rozmiar], char W[rozmiar][rozmiar], char A[rozmiar][rozmiar], char S[rozmiar][rozmiar]);
void opisprogramu();
void pauza(int& pauzaczas);
void wczytajplansze(char  Q[rozmiar][rozmiar], char W[rozmiar][rozmiar], char A[rozmiar][rozmiar], char S[rozmiar][rozmiar], char graczzaczynajacy, char graczdrugi, int& zajete);
void undo(int& zajete, char planszaDOPISANIA[rozmiar * rozmiar * 4], int poleDOPISANIA[rozmiar * rozmiar * 4], char  Q[rozmiar][rozmiar], char W[rozmiar][rozmiar], char A[rozmiar][rozmiar], char S[rozmiar][rozmiar], char planszaOBROTU[rozmiar * rozmiar * 4], char stronaOBROTU[rozmiar * rozmiar * 4], bool kolkoikrzyzyk);
void historia(int& zajete, char planszaDOPISANIA[rozmiar * rozmiar * 4], int poleDOPISANIA[rozmiar * rozmiar * 4], char  Q[rozmiar][rozmiar], char W[rozmiar][rozmiar], char A[rozmiar][rozmiar], char S[rozmiar][rozmiar], char planszaOBROTU[rozmiar * rozmiar * 4], char stronaOBROTU[rozmiar * rozmiar * 4], char imiePIERWSZE[dlugosc], char imieDRUGIE[dlugosc], char pierwszygracz, char drugigracz, bool kolkoikrzyzyk);
void ruchdoprzodu(int& zajete, char planszaDOPISANIA[rozmiar * rozmiar * 4], int poleDOPISANIA[rozmiar * rozmiar * 4], char  Q[rozmiar][rozmiar], char W[rozmiar][rozmiar], char A[rozmiar][rozmiar], char S[rozmiar][rozmiar], char planszaOBROTU[rozmiar * rozmiar * 4], char stronaOBROTU[rozmiar * rozmiar * 4], char pierwszygracz, char drugigracz, bool kolkoikrzyzyk);
int main()
{
	bool czykolkoikrzyzyk = false;
	bool czypredefiniowana = false;
	char planszaDOPISANIA[rozmiar * rozmiar * 4];			//tablice zapamietujace ruchy
	int poleDOPISANIA[rozmiar * rozmiar * 4];
	char planszaOBROTU[rozmiar * rozmiar * 4];
	char stronaOBROTU[rozmiar * rozmiar * 4];
	int ilezajetych = 0;
	char tabQ[rozmiar][rozmiar];
	char tabW[rozmiar][rozmiar];
	char tabA[rozmiar][rozmiar];
	char tabS[rozmiar][rozmiar];
	wpisztablice(tabQ);
	wpisztablice(tabW);
	wpisztablice(tabA);
	wpisztablice(tabS);
	char imieJEDEN[dlugosc], imieDWA[dlugosc];
	cout << " podaj imie pierwszego gracza:" << endl;
	cin >> imieJEDEN;
	cout << " podaj imie drugiego gracza:" << endl;
	cin >> imieDWA;
	system("cls");
	char graczJEDEN[dlugosc];
	char graczDWA[dlugosc];
	graczJEDEN[0] = 'o';
	graczDWA[0] = 'x';
	cout << " W jaka gre chcesz zagrac?" << endl;
	cout << " 1 - kolko i krzyzyk" << endl << " 2 - pentago" << endl;
	char  ktoragra[dlugosc];
	do
	{
		cin >> ktoragra;
		if ((ktoragra[0] == '1') and (strlen(ktoragra) == 1))
		{
			break;
		}
		if ((ktoragra[0] == '2') and (strlen(ktoragra) == 1))
		{
			break;
		}
		system("cls");
		cout << " Bledne dane!\n Podaj poprawne dane:" << endl;
		cout << " W jaka gre chcesz zagrac?" << endl;
		cout << " 1 - kolko i krzyzyk" << endl << " 2 - pentago" << endl;
	} while (true);
	switch (ktoragra[0])
	{
	case '1':																								//kolko i krzyzyk
	{
		czykolkoikrzyzyk = true;
		int czascalkowity;
		cout << " Podaj limit czasu w sekundach: ";
		while (!(cin >> czascalkowity) or (czascalkowity <= 0))
		{
			cout << " Bledne dane!\n Podaj poprawne dane:" << endl << " Podaj poprawna wartosc czasu: ";
			cin.clear();
			cin.ignore(cin.rdbuf()->in_avail());
		}
		int czasJEDEN = czascalkowity;
		int czasDWA = czascalkowity;
		int czasrundy;
		clock_t startczas, stopczas;
		while (sprawdzzwyciestwo(tabQ, tabW, tabA, tabS, graczJEDEN[0], graczDWA[0], czasJEDEN, czasDWA, czypredefiniowana, ilezajetych) == 0)
		{
			int czaspauzy = 0;
			startczas = clock();
			wyborplanszyipola(imieJEDEN, imieDWA, graczJEDEN[0], graczDWA[0], tabQ, tabW, tabA, tabS, czasJEDEN, czasDWA, czaspauzy, czypredefiniowana, ilezajetych, planszaDOPISANIA, poleDOPISANIA, czykolkoikrzyzyk, planszaOBROTU, stronaOBROTU);
			stopczas = clock();
			czasrundy = (stopczas - startczas) / CLOCKS_PER_SEC;
			wyliczaniewypisan();
			if (wyliczaniewypisan() == 1)
			{
				czasJEDEN = czasJEDEN - czasrundy + czaspauzy;
			}
			else {
				czasDWA = czasDWA - czasrundy + czaspauzy;
			}
			ilezajetych++;
		}
		wypiszwygrana(tabQ, tabW, tabA, tabS, imieJEDEN, imieDWA, graczJEDEN[0], graczDWA[0]);
		if (sprawdzzwyciestwo(tabQ, tabW, tabA, tabS, graczJEDEN[0], graczDWA[0], czasJEDEN, czasDWA, czypredefiniowana, ilezajetych) == 1)
		{
			cout << endl << " zwyciezyl " << imieJEDEN << " gratulacje!" << endl;
		}
		if (sprawdzzwyciestwo(tabQ, tabW, tabA, tabS, graczJEDEN[0], graczDWA[0], czasJEDEN, czasDWA, czypredefiniowana, ilezajetych) == 2)
		{
			cout << endl << " zwyciezyl " << imieDWA << " gratulacje!" << endl;
		}
		if (sprawdzzwyciestwo(tabQ, tabW, tabA, tabS, graczJEDEN[0], graczDWA[0], czasJEDEN, czasDWA, czypredefiniowana, ilezajetych) == 10)
		{
			cout << endl << imieDWA << " skonczyl sie czas!" << endl;
			cout << " zwyciezyl " << imieJEDEN << " gratulacje!" << endl;
		}
		if (sprawdzzwyciestwo(tabQ, tabW, tabA, tabS, graczJEDEN[0], graczDWA[0], czasJEDEN, czasDWA, czypredefiniowana, ilezajetych) == 20)
		{
			cout << endl << imieJEDEN << " skonczyl sie czas!" << endl;
			cout << " zwyciezyl " << imieDWA << " gratulacje!" << endl;
		}
		if (sprawdzzwyciestwo(tabQ, tabW, tabA, tabS, graczJEDEN[0], graczDWA[0], czasJEDEN, czasDWA, czypredefiniowana, ilezajetych) == 3)
		{
			cout << endl << " gra zakonczyla sie remisem!" << endl;
		}
		system("pause");
		historia(ilezajetych, planszaDOPISANIA, poleDOPISANIA, tabQ, tabW, tabA, tabS, planszaOBROTU, stronaOBROTU, imieJEDEN, imieDWA, graczJEDEN[0], graczDWA[0], czykolkoikrzyzyk);
		system("pause");
		return 0;
	}
	case '2':																		//pentago
	{
		do
		{
			cout << imieJEDEN << " podaj swoj zeton: " << endl;
			cin >> graczJEDEN;
			if (strlen(graczJEDEN) == 1)
			{
				break;
			}
			cout << " Bledne dane!\n Podaj poprawne dane:" << endl;
		} while (true);
		do
		{
			cout << imieDWA << " podaj swoj zeton: " << endl;
			cin >> graczDWA;
			if (graczJEDEN == graczDWA)
			{
				cout << " Znaki musza byc rozne!" << endl;
			}
			if (strlen(graczDWA) == 1)
			{
				break;
			}
			cout << " Bledne dane!\n Podaj poprawne dane:" << endl;
		} while (true);
		int czascalkowity;
		cout << " Podaj limit czasu w sekundach: ";
		while (!(cin >> czascalkowity) or (czascalkowity <= 0))
		{
			cout << " Bledne dane!\n Podaj poprawne dane:" << endl << " Podaj poprawna wartosc czasu: ";
			cin.clear();
			cin.ignore(cin.rdbuf()->in_avail());
		}
		int czasJEDEN = czascalkowity;
		int czasDWA = czascalkowity;
		int czasrundy;
		clock_t startczas, stopczas;
		while (sprawdzzwyciestwo(tabQ, tabW, tabA, tabS, graczJEDEN[0], graczDWA[0], czasJEDEN, czasDWA, czypredefiniowana, ilezajetych) == 0)
		{
			int czaspauzy = 0;
			startczas = clock();
			wyborplanszyipola(imieJEDEN, imieDWA, graczJEDEN[0], graczDWA[0], tabQ, tabW, tabA, tabS, czasJEDEN, czasDWA, czaspauzy, czypredefiniowana, ilezajetych, planszaDOPISANIA, poleDOPISANIA, czykolkoikrzyzyk, planszaOBROTU, stronaOBROTU);
			wyborplanszydoobrotu(tabQ, tabW, tabA, tabS, imieJEDEN, imieDWA, graczJEDEN[0], graczDWA[0], czasJEDEN, czasDWA, planszaOBROTU, stronaOBROTU, ilezajetych);
			stopczas = clock();
			czasrundy = (stopczas - startczas) / CLOCKS_PER_SEC;
			wyliczaniewypisan();
			if (wyliczaniewypisan() == 1)
			{
				czasJEDEN = czasJEDEN - czasrundy + czaspauzy;
			}
			else {
				czasDWA = czasDWA - czasrundy + czaspauzy;
			}
			ilezajetych++;
		}
		wypiszwygrana(tabQ, tabW, tabA, tabS, imieJEDEN, imieDWA, graczJEDEN[0], graczDWA[0]);
		if (sprawdzzwyciestwo(tabQ, tabW, tabA, tabS, graczJEDEN[0], graczDWA[0], czasJEDEN, czasDWA, czypredefiniowana, ilezajetych) == 1)
		{
			cout << endl << " zwyciezyl " << imieJEDEN << " gratulacje!" << endl;
		}
		if (sprawdzzwyciestwo(tabQ, tabW, tabA, tabS, graczJEDEN[0], graczDWA[0], czasJEDEN, czasDWA, czypredefiniowana, ilezajetych) == 2)
		{
			cout << endl << " zwyciezyl " << imieDWA << " gratulacje!" << endl;
		}
		if (sprawdzzwyciestwo(tabQ, tabW, tabA, tabS, graczJEDEN[0], graczDWA[0], czasJEDEN, czasDWA, czypredefiniowana, ilezajetych) == 10)
		{
			cout << endl << imieDWA << " skonczyl sie czas!" << endl;
			cout << " zwyciezyl " << imieJEDEN << " gratulacje!" << endl;
		}
		if (sprawdzzwyciestwo(tabQ, tabW, tabA, tabS, graczJEDEN[0], graczDWA[0], czasJEDEN, czasDWA, czypredefiniowana, ilezajetych) == 20)
		{
			cout << endl << imieJEDEN << " skonczyl sie czas!" << endl;
			cout << " zwyciezyl " << imieDWA << " gratulacje!" << endl;
		}
		if (sprawdzzwyciestwo(tabQ, tabW, tabA, tabS, graczJEDEN[0], graczDWA[0], czasJEDEN, czasDWA, czypredefiniowana, ilezajetych) == 3)
		{
			cout << endl << " gra zakonczyla sie remisem!" << endl;
		}
	}
	system("pause");
	historia(ilezajetych, planszaDOPISANIA, poleDOPISANIA, tabQ, tabW, tabA, tabS, planszaOBROTU, stronaOBROTU, imieJEDEN, imieDWA, graczJEDEN[0], graczDWA[0], czykolkoikrzyzyk);
	system("pause");
	return 0;
	}
}
//------------------------------------------------------------------------------------------------------------ wybieranie planszy i pola --------------------------------------------------------------------------------
void wyborplanszyipola(char imiePIERWSZE[dlugosc], char imieDRUGIE[dlugosc], char& pierwszygracz, char& drugigracz, char Q[rozmiar][rozmiar], char W[rozmiar][rozmiar], char A[rozmiar][rozmiar], char S[rozmiar][rozmiar], int czasPIERWSZY, int czasDRUGI, int& pauzaczas, bool& predefiniowana, int& zajete, char planszaDOPISANIA[rozmiar * rozmiar * 4], int poleDOPISANIA[rozmiar * rozmiar * 4], bool kolkoikrzyzyk, char planszaOBROTU[rozmiar * rozmiar * 4], char stronaOBROTU[rozmiar * rozmiar * 4])
{
	while (true)
	{
		system("cls");
		wyliczaniewypisan();
		wypisz(Q, W, A, S, czasPIERWSZY, czasDRUGI, imiePIERWSZE, imieDRUGIE, pierwszygracz, drugigracz);
		char znakplansza[dlugosc];
		int znakpole;
		int sprawdza = 0;
		cout << " jesli chcesz przejsc do opcji nacisnij: 'm'" << endl;
		cout << " wybierz plansze do wpisania (q, w, a, s): ";
		int dlugo;
		do
		{
			dlugo = 0;
			cin >> znakplansza;
			dlugo = strlen(znakplansza);
			if ((znakplansza[0] == 'q') and (dlugo == 1))
			{
				break;
			}
			if ((znakplansza[0] == 'w') and (dlugo == 1))
			{
				break;
			}
			if ((znakplansza[0] == 'a') and (dlugo == 1))
			{
				break;
			}
			if ((znakplansza[0] == 's') and (dlugo == 1))
			{
				break;
			}
			if ((znakplansza[0] == 'm') and (dlugo == 1))
			{
				wyliczaniewypisan();
				if (wyliczaniewypisan() == 1)
				{
					opcje(pierwszygracz, drugigracz, Q, W, A, S, pauzaczas, predefiniowana, zajete, planszaDOPISANIA, poleDOPISANIA, planszaOBROTU, stronaOBROTU, kolkoikrzyzyk);
				}
				else {
					opcje(drugigracz, pierwszygracz, Q, W, A, S, pauzaczas, predefiniowana, zajete, planszaDOPISANIA, poleDOPISANIA, planszaOBROTU, stronaOBROTU, kolkoikrzyzyk);
				}
				wypisz(Q, W, A, S, czasPIERWSZY, czasDRUGI, imiePIERWSZE, imieDRUGIE, pierwszygracz, drugigracz);
				cout << " jesli chcesz przejsc do opcji nacisnij: m" << endl;
				cout << " wybierz plansze do wpisania (q, w, a, s): ";
				continue;
			}
			wypisz(Q, W, A, S, czasPIERWSZY, czasDRUGI, imiePIERWSZE, imieDRUGIE, pierwszygracz, drugigracz);
			cout << " jesli chcesz przejsc do opcji nacisnij: m" << endl;
			cout << " Bledne dane!\n Podaj poprawne dane:" << endl << " wybierz plansze do wpisania (q, w, a, s): ";
		} while (true);
		cout << " wybierz pole: " << endl;
		while (!(cin >> znakpole) or (znakpole <= 0) or (znakpole > rozmiar * rozmiar))
		{
			wypisz(Q, W, A, S, czasPIERWSZY, czasDRUGI, imiePIERWSZE, imieDRUGIE, pierwszygracz, drugigracz);
			cout << " Bledne dane!\n Podaj poprawne dane:" << endl << " wybrana plansze do wpisania: " << znakplansza[0] << endl << " wybierz pole: " << endl;
			cin.clear();
			cin.ignore(cin.rdbuf()->in_avail());
		}
		switch (znakplansza[0])
		{
		case 'q':  sprawdza = sprawdzdopisanie(Q, znakpole);
			break;
		case 'w': sprawdza = sprawdzdopisanie(W, znakpole);
			break;
		case 'a': sprawdza = sprawdzdopisanie(A, znakpole);
			break;
		case 's': sprawdza = sprawdzdopisanie(S, znakpole);
			break;
		}
		if (sprawdza == 1)
		{
			wyliczaniewypisan();
			wypisz(Q, W, A, S, czasPIERWSZY, czasDRUGI, imiePIERWSZE, imieDRUGIE, pierwszygracz, drugigracz);
			cout << " Bledne dane!\n Podaj poprawne dane:" << endl;
			continue;
		}
		system("cls");
		switch (znakplansza[0])
		{
		case  'q': dopisz(Q, znakpole, pierwszygracz, drugigracz, zajete);
			break;
		case 'w': dopisz(W, znakpole, pierwszygracz, drugigracz, zajete);
			break;
		case 'a': dopisz(A, znakpole, pierwszygracz, drugigracz, zajete);
			break;
		case 's': dopisz(S, znakpole, pierwszygracz, drugigracz, zajete);
			break;
		}
		planszaDOPISANIA[zajete] = znakplansza[0];
		poleDOPISANIA[zajete] = znakpole;
		break;
	}
}
//------------------------------------------------------------------------------------------------------------ wybieranie planszy do obrotu --------------------------------------------------------------------------------
void wyborplanszydoobrotu(char  Q[rozmiar][rozmiar], char W[rozmiar][rozmiar], char A[rozmiar][rozmiar], char S[rozmiar][rozmiar], char imiePIERWSZE[dlugosc], char imieDRUGIE[dlugosc], char pierwszygracz, char drugigracz, int czasPIERWSZY, int czasDRUGI, char planszaOBROTU[rozmiar * rozmiar * 4], char stronaOBROTU[rozmiar * rozmiar * 4], int zajete)
{
	while (true)
	{
		wypisz(Q, W, A, S, czasPIERWSZY, czasDRUGI, imiePIERWSZE, imieDRUGIE, pierwszygracz, drugigracz);
		char znakplansza[dlugosc];
		cout << " wybierz plansze do obrotu (q, w, a, s): ";
		int dlugo;
		do
		{
			dlugo = 0;
			cin >> znakplansza;
			dlugo = strlen(znakplansza);
			if ((znakplansza[0] == 'q') and (dlugo == 1)) {
				break;
			}
			if ((znakplansza[0] == 'w') and (dlugo == 1)) {
				break;
			}
			if ((znakplansza[0] == 'a') and (dlugo == 1)) {
				break;
			}
			if ((znakplansza[0] == 's') and (dlugo == 1)) {
				break;
			}
			wypisz(Q, W, A, S, czasPIERWSZY, czasDRUGI, imiePIERWSZE, imieDRUGIE, pierwszygracz, drugigracz);
			cout << " Bledne dane!\n Podaj poprawne dane:" << endl << " wybierz plansze do obrotu (q, w, a, s): ";
		} while (true);

		cout << " wybierz strone obrotu (z, x): " << endl;
		char stronaobrotu[dlugosc];
		do
		{
			dlugo = 0;
			cin >> stronaobrotu;
			dlugo = strlen(stronaobrotu);
			if ((stronaobrotu[0] == 'x') and (dlugo == 1))
			{
				break;
			}
			if ((stronaobrotu[0] == 'z') and (dlugo == 1))
			{
				break;
			}
			wypisz(Q, W, A, S, czasPIERWSZY, czasDRUGI, imiePIERWSZE, imieDRUGIE, pierwszygracz, drugigracz);
			cout << " Bledne dane!\n Podaj poprawne dane:" << endl << " wybrana plansze do obrocenia: " << znakplansza[0] << endl << " wybierz strone obrotu (z, x): " << endl;
		} while (true);

		if ((znakplansza[0] == 'q') and (stronaobrotu[0] == 'z'))
		{
			obrocwprawo(Q);
		}
		else if ((znakplansza[0] == 'w') and (stronaobrotu[0] == 'z'))
		{
			obrocwprawo(W);
		}
		else if ((znakplansza[0] == 'a') and (stronaobrotu[0] == 'z'))
		{
			obrocwprawo(A);
		}
		else if ((znakplansza[0] == 's') and (stronaobrotu[0] == 'z'))
		{
			obrocwprawo(S);
		}


		else if ((znakplansza[0] == 'q') and (stronaobrotu[0] == 'x'))
		{
			obrocwlewo(Q);
		}
		else if ((znakplansza[0] == 'w') and (stronaobrotu[0] == 'x'))
		{
			obrocwlewo(W);
		}
		else if ((znakplansza[0] == 'a') and (stronaobrotu[0] == 'x'))
		{
			obrocwlewo(A);
		}
		else if ((znakplansza[0] == 's') and (stronaobrotu[0] == 'x'))
		{
			obrocwlewo(S);
		}

		planszaOBROTU[zajete] = znakplansza[0];								//zapamietuje ruch
		stronaOBROTU[zajete] = stronaobrotu[0];
		break;
	}
}

//------------------------------------------------------------------------------------------------------------ wpisywanie i wypisywanie tablicy --------------------------------------------------------------------------------
void wpisztablice(char tab[rozmiar][rozmiar])
{
	for (int i = 0; i < rozmiar; i++)
	{
		for (int j = 0; j < rozmiar; j++)
		{
			tab[i][j] = ' ';
		}
	}
}
void krawedzgorna()
{
	cout << (char)218;
	for (int i = 0; i < rozmiar - 1; i++)
	{
		cout << (char)196 << (char)196 << (char)196 << (char)194;
	}
	cout << (char)196 << (char)196 << (char)196 << (char)191 << " ";
}
void srodkowapusta(char tab[rozmiar][rozmiar])
{
	cout << (char)179;
	int i = 0;
	static int licz = 0;
	int j = (licz / 2) % rozmiar;
	for (i; i < rozmiar - 1; i++)
	{
		cout << " " << tab[j][i] << " " << (char)179;
	}
	cout << " " << tab[j][rozmiar - 1] << " " << (char)179 << " ";
	licz++;
}
void srodkowapelna()
{
	cout << (char)195;
	int i = 0;
	for (i; i < rozmiar - 1; i++)
	{
		cout << (char)196 << (char)196 << (char)196 << (char)197;
	}
	cout << (char)196 << (char)196 << (char)196 << (char)180 << " ";
}
void krawedzdolna()
{
	cout << (char)192;
	for (int i = 0; i < rozmiar - 1; i++)
	{
		cout << (char)196 << (char)196 << (char)196 << (char)193;
	}
	cout << (char)196 << (char)196 << (char)196 << (char)217 << " ";
}
void wypisz(char Q[rozmiar][rozmiar], char W[rozmiar][rozmiar], char A[rozmiar][rozmiar], char S[rozmiar][rozmiar], int czasPIERWSZY, int czasDRUGI, char imiePIERWSZE[dlugosc], char imieDRUGIE[dlugosc], char pierwszygracz, char drugigracz)
{
	system("cls");
	krawedzgorna();
	krawedzgorna();
	cout << endl;
	for (int m = 0; m < rozmiar - 1; m++)
	{
		srodkowapusta(Q);
		srodkowapusta(W);
		cout << endl;
		srodkowapelna();
		srodkowapelna();
		cout << endl;
	}
	srodkowapusta(Q);
	srodkowapusta(W);
	wyliczaniewypisan();
	if (wyliczaniewypisan() == 1)
	{
		cout << "\t" << imiePIERWSZE << " twoja tura (" << pierwszygracz << ")" << endl;
	}
	else {
		cout << "\t" << imieDRUGIE << " twoja tura (" << drugigracz << ")" << endl;
	}
	krawedzdolna();
	krawedzdolna();
	cout << endl;
	krawedzgorna();
	krawedzgorna();
	wyliczaniewypisan();
	if (wyliczaniewypisan() == 1)
	{
		cout << "\tpozostaly czas: " << czasPIERWSZY << " sekund" << endl;
	}
	else {
		cout << "\tpozostaly czas: " << czasDRUGI << " sekund" << endl;
	}
	for (int m = 0; m < rozmiar - 1; m++)
	{
		srodkowapusta(A);
		srodkowapusta(S);
		cout << endl;
		srodkowapelna();
		srodkowapelna();
		cout << endl;
	}
	srodkowapusta(A);
	srodkowapusta(S);
	cout << endl;
	krawedzdolna();
	krawedzdolna();
	cout << endl;
}
void wypiszwygrana(char Q[rozmiar][rozmiar], char W[rozmiar][rozmiar], char A[rozmiar][rozmiar], char S[rozmiar][rozmiar], char imiePIERWSZE[dlugosc], char imieDRUGIE[dlugosc], char pierwszygracz, char drugigracz)
{
	system("cls");
	krawedzgorna();
	krawedzgorna();
	cout << endl;
	for (int m = 0; m < rozmiar - 1; m++)
	{
		srodkowapusta(Q);
		srodkowapusta(W);
		cout << endl;
		srodkowapelna();
		srodkowapelna();
		cout << endl;
	}
	srodkowapusta(Q);
	srodkowapusta(W);
	cout << endl;
	krawedzdolna();
	krawedzdolna();
	cout << endl;
	krawedzgorna();
	krawedzgorna();
	cout << endl;
	for (int m = 0; m < rozmiar - 1; m++)
	{
		srodkowapusta(A);
		srodkowapusta(S);
		cout << endl;
		srodkowapelna();
		srodkowapelna();
		cout << endl;
	}
	srodkowapusta(A);
	srodkowapusta(S);
	cout << endl;
	krawedzdolna();
	krawedzdolna();
	cout << endl;
}
int wyliczaniewypisan()
{
	static int ilewypisan = 0;
	ilewypisan = ilewypisan + 1;
	return ilewypisan % 2;
}
//------------------------------------------------------------------------------------------------------------ dopisywanie znakow ---------------------------------------------------------------------------------------
void dopisz(char tab[rozmiar][rozmiar], int znak, char pierwszygracz, char drugigracz, int zajete)
{
	char wypisanyznak;
	if (zajete % 2 == 0)
	{
		wypisanyznak = pierwszygracz;
	}
	else
	{
		wypisanyznak = drugigracz;
	}
	for (int i = 1; i <= rozmiar; i++)
	{
		for (int j = 1; j <= rozmiar; j++)
		{
			if ((rozmiar - i) * rozmiar + j == znak)					//nadpisuje wybrane pole na zeton aktualnego gracza (po sprawdzeniu czy pole jest wolne)
			{
				tab[i - 1][j - 1] = wypisanyznak;
			}
		}
	}
}
int sprawdzdopisanie(char tab[rozmiar][rozmiar], int znak)						//zwraca 0 jesli podane pole jest wolne
{
	for (int j = 1; j <= rozmiar; j++)
	{
		for (int i = 1; i <= rozmiar; i++)
		{
			if ((rozmiar - j) * rozmiar + i == znak)
			{
				if (tab[j - 1][i - 1] == ' ')
				{
					return 0;
				}
				else
				{
					return 1;
				}
			}
		}
	}
}
//------------------------------------------------------------------------------------------------------------ sprawdzanie zwyciestwa ---------------------------------------------------------------------------------------
int sprawdzzwyciestwo(char Q[rozmiar][rozmiar], char W[rozmiar][rozmiar], char A[rozmiar][rozmiar], char S[rozmiar][rozmiar], char pierwszygracz, char drugigracz, int czasPIERWSZY, int czasDRUGI, bool predefiniowana, int& zajete)
{
	if (czasPIERWSZY <= 0) {
		return 20;
	}
	if (czasDRUGI <= 0) {
		return 10;
	}
	char duzatablica[rozmiar * 2][rozmiar * 2];					//tworzy 1 duza tablice z 4 malychtablic
	for (int i = 0; i < rozmiar; i++)
	{
		for (int j = 0; j < rozmiar; j++)
		{
			duzatablica[i][j] = Q[i][j];
			duzatablica[i][j + rozmiar] = W[i][j];
			duzatablica[i + rozmiar][j] = A[i][j];
			duzatablica[i + rozmiar][j + rozmiar] = S[i][j];
		}
	}
	char  zwyciezca;
	int licznik;
	for (int i = 0; i < rozmiar * 2; i++)
	{																								//sprawdzanie poziomu
		for (int j = 0; j < rozmiar * 2; j++)
		{
			if (duzatablica[i][j] == ' ')
			{
				continue;
			}
			zwyciezca = duzatablica[i][j];
			licznik = 0;
			for (int m = j; m < rozmiar * 2; m++)
			{
				if (zwyciezca == duzatablica[i][m])
				{
					licznik++;											//liczy ile jest tych samych zetonow obok siebie (w poziomie)
				}
				else
				{
					break;
				}
				if (licznik == 5)
				{
					if (pierwszygracz == zwyciezca)
					{
						return 1;
					}
					if (drugigracz == zwyciezca)
					{
						return 2;
					}
				}
			}
		}
	}
	for (int j = 0; j < rozmiar * 2; j++)
	{																											//sprawdzanie pionu
		for (int i = 0; i < rozmiar * 2; i++)
		{
			if (duzatablica[i][j] == ' ')
			{
				continue;
			}
			zwyciezca = duzatablica[i][j];
			licznik = 0;
			for (int m = i; m < rozmiar * 2; m++)
			{
				if (zwyciezca == duzatablica[m][j])
				{
					licznik++;															//liczy ile jest tych samych zetonow obok siebie (w pionie)
				}
				else
				{
					break;
				}
				if (licznik == 5)
				{
					if (pierwszygracz == zwyciezca)
					{
						return 1;
					}
					if (drugigracz == zwyciezca)
					{
						return 2;
					}
				}
			}
		}
	}
	for (int i = 0; i < rozmiar * 2 - 4; i++)
	{																								//sprawdzanie ukosow w prawydol
		for (int j = 0; j < rozmiar * 2 - 4; j++)
		{
			if (duzatablica[i][j] == ' ')
			{
				continue;
			}
			else
			{
				zwyciezca = duzatablica[i][j];
				licznik = 0;														//liczy ile jest tych samych zetonow obok siebie (ukosy z lewej gory do prawego dolu}
			}
			for (int m = j; m < rozmiar * 2; m++)
			{
				if ((j != 0) and licznik == 0)
				{
					licznik = licznik + 1;
				}
				if (duzatablica[i + m][j + m] == zwyciezca)
				{
					licznik = licznik + 1;
				}
				else
				{
					break;
				}
			}
			if (licznik == 5)
			{
				if (pierwszygracz == zwyciezca)
				{
					return 1;
				}
				if (drugigracz == zwyciezca)
				{
					return 2;
				}
			}
		}
	}
	for (int i = rozmiar * 2; i > 3; i--)
	{																						//sprawdzanie ukosow w prawagore
		for (int j = 0; j < rozmiar * 2 - 3; j++)
		{
			if (duzatablica[i][j] == ' ')
			{
				licznik = 0;
				continue;
			}
			else {
				zwyciezca = duzatablica[i][j];
				licznik = 0;													//liczy ile jest tych samych zetonow obok siebie (z lewego dolu do prawej gory)
			}
			for (int m = j; m < rozmiar * 2; m++)
			{
				if ((j != 0) and (licznik == 0))
				{
					licznik = licznik + 1;
				}
				if (duzatablica[i - m][j + m] == zwyciezca)
				{
					licznik = licznik + 1;
				}
				else
				{
					break;
				}
			}
			if (licznik == 5)
			{
				if (pierwszygracz == zwyciezca)
				{
					return 1;
				}
				if (drugigracz == zwyciezca)
				{
					return 2;
				}
			}
		}
	}
	if (predefiniowana == true)
	{
		if (zajete == 4 * rozmiar * rozmiar - 16)
		{
			return 3;
		}
	}																		//zwraca 0 jesli gra trwa dalej
	if (zajete == 4 * rozmiar * rozmiar)									//zwraca wartosc 3 jesli gra zakonczyla sie remisem
	{																		//zwraca wartosc 1 jesli wygrywa 1 gracz
		return 3;															//zwraca wartosc 2 jesli wygral 2 gracz
	}																		//zwraca wartosc 10 jesli 1 gracz wygral na czas
	return 0;																//zwraca wartosc 20 jesli 2 gracz wygral na czas
}
//------------------------------------------------------------------------------------------------------------ obroty ---------------------------------------------------------------------------------------
void obrocwlewo(char tab[rozmiar][rozmiar])
{
	int pion = rozmiar / 2;
	int poziom = rozmiar - 1;
	int buf;
	for (int i = 0; i < pion; i++)
	{
		for (int j = i; j < poziom - i; j++)
		{
			buf = tab[i][j];												//sekwencyjnie zamienia ze soba 4 wartosci
			tab[i][j] = tab[j][poziom - i];
			tab[j][poziom - i] = tab[poziom - i][poziom - j];
			tab[poziom - i][poziom - j] = tab[poziom - j][i];
			tab[poziom - j][i] = buf;
		}
	}
}
void obrocwprawo(char tab[rozmiar][rozmiar])
{
	int pion = rozmiar / 2;
	int poziom = rozmiar - 1;
	int buf;
	for (int i = 0; i < pion; i++)
	{
		for (int j = i; j < poziom - i; j++)
		{
			buf = tab[poziom - j][i];
			tab[poziom - j][i] = tab[poziom - i][poziom - j];
			tab[poziom - i][poziom - j] = tab[j][poziom - i];
			tab[j][poziom - i] = tab[i][j];
			tab[i][j] = buf;
		}
	}
}
//----------------------------------------------------------------------------------------------------------- opcje i podopcje----------------------------------------------------------------------------------------------
void opcje(char& aktualnyznak, char znakprzeciwnika, char Q[rozmiar][rozmiar], char W[rozmiar][rozmiar], char A[rozmiar][rozmiar], char S[rozmiar][rozmiar], int& pauzaczas, bool& predefiniowana, int& zajete, char planszaDOPISANIA[rozmiar * rozmiar * 4], int poleDOPISANIA[rozmiar * rozmiar * 4], char planszaOBROTU[rozmiar * rozmiar * 4], char stronaOBROTU[rozmiar * rozmiar * 4], bool kolkoikrzyzyk)
{
	cout << " y - zmien zeton aktualnego gracza" << endl;
	cout << " u - undo" << endl;
	cout << " p - pauza" << endl;
	cout << " o - wczytanie predefiniowanej planszy" << endl;
	cout << " h - wejscie do opisu programu" << endl;
	cout << " m - wyjdz z opcji" << endl;
	char opcja[dlugosc];
	do
	{
		cin >> opcja;
		if ((strlen(opcja) == 1) and (opcja[0] == 'y'))
		{
			break;
		}
		if ((strlen(opcja) == 1) and (opcja[0] == 'u'))
		{
			break;
		}
		if ((strlen(opcja) == 1) and (opcja[0] == 'p'))
		{
			break;
		}
		if ((strlen(opcja) == 1) and (opcja[0] == 'o'))
		{
			break;
		}
		if ((strlen(opcja) == 1) and (opcja[0] == 'h'))
		{
			break;
		}
		if ((strlen(opcja) == 1) and (opcja[0] == 'm'))
		{
			break;
		}
		cout << " Bledne dane!\nPodaj poprawne dane:" << endl;
	} while (true);
	switch (opcja[0])
	{
	case 'y': zmienznak(aktualnyznak, znakprzeciwnika, Q, W, A, S);
		break;
	case 'u':
		if (zajete == 0)
		{
			cout << " nie ma ruchow do cofniecia!" << endl;
			cout << " jesli chcesz powrocic do gry nacisnij 'u'" << endl;
			char wyjscie[dlugosc];
			do
			{
				cin >> wyjscie;
				if ((strlen(wyjscie) == 1) and (wyjscie[0] == 'u'))
				{
					break;
				}
				cout << " Bledne dane!\n Podaj poprawne dane:" << endl;
			} while (true);
			break;
		}
		undo(zajete, planszaDOPISANIA, poleDOPISANIA, Q, W, A, S, planszaOBROTU, stronaOBROTU, kolkoikrzyzyk);
		break;
	case 'p': pauza(pauzaczas);
		break;
	case 'o': wczytajplansze(Q, W, A, S, aktualnyznak, znakprzeciwnika, zajete);
		predefiniowana = true;
		break;
	case 'h': opisprogramu();
		break;
	case 'm':
		break;
	}
}
void zmienznak(char& staryznak, char znakprzeciwnika, char Q[rozmiar][rozmiar], char W[rozmiar][rozmiar], char A[rozmiar][rozmiar], char S[rozmiar][rozmiar])
{
	char nowyznak[dlugosc];
	cout << " Na jaki znak chcialbys zmienic swoj zeton?" << endl;
	do
	{
		cin >> nowyznak;
		if ((strlen(nowyznak) == 1) and (nowyznak[0] != znakprzeciwnika))
		{
			break;
		}
		cout << " Bledne dane!\n Podaj poprawne dane:" << endl;
	} while (true);
	for (int i = 0; i < rozmiar; i++)
	{
		for (int j = 0; j < rozmiar; j++)
		{
			if (Q[i][j] == staryznak) { Q[i][j] = nowyznak[0]; }
			if (W[i][j] == staryznak) { W[i][j] = nowyznak[0]; }
			if (A[i][j] == staryznak) { A[i][j] = nowyznak[0]; }
			if (S[i][j] == staryznak) { S[i][j] = nowyznak[0]; }
		}
	}
	staryznak = nowyznak[0];
}
void opisprogramu()
{
	system("cls");
	cout << " Pentago jest gra dwuosobowa na planszy. Plansza sklada sie z 4 ruchomych czesci, ktore mozna" << endl;
	cout << " obracac. Kazda czesc zawiera 9 miejsc na zetony." << endl;
	cout << " Gracze po kolei oddaja ruch skladajacy sie z 2 czesci:" << endl;
	cout << " - dolozenia swojego zetonu na niezajete pole planszy" << endl;
	cout << " - obrot jednej z czesci planszy o 90 stopni w dowolnym kierunku." << endl;
	cout << " Nie mozna zrezygnowac z zadnej czesci ruchu." << endl;
	cout << " Wygrywa osoba, ktorej 5 zetonow, po pelnym ruchu, sa ulozone w rzedzie / kolumnie / po skosach" << endl;
	cout << " (podobnie do gry kolko krzyzyk)" << endl << endl;
	cout << " q, w, a, s - wybor czesci planszy odpowiednio: lewej gornej, prawej gornej, lewej dolnej, prawej dolnej" << endl;
	cout << " 1..9 - wybor pola na czesci planszy jak na klawiaturze numerycznej tj. 1 to dolne lewe pole" << endl;
	cout << " z, x - obrot odpowiednio: zgodnie z ruchem wskazowek zegara, odwrotnie do ruchu wskazowek" << endl;
	cout << " p - pauza" << endl;
	cout << " u - undo" << endl;
	cout << " o - wczytanie predefiniowanej planszy" << endl;
	cout << " m - wejscie do opcji" << endl;
	cout << " h - wejscie do opisu programu" << endl;
	cout << " Ruch to najpierw wybor czesci planszy i pola(np.q5), a nastepnie wybor czesci planszy i obrotu (np.az)" << endl;
	cout << endl << " Nacisnij 'h', zeby wrocic do gry" << endl;
	char wyjscie[dlugosc];
	do
	{
		cin >> wyjscie;
		if ((strlen(wyjscie) == 1) and (wyjscie[0] == 'h'))
		{
			break;
		}
		cout << " Bledne dane!\n Podaj poprawne dane:" << endl;
	} while (true);
}
void pauza(int& pauzaczas)
{
	clock_t startczas, stopczas;
	startczas = clock();
	system("cls");
	cout << " 'PAUZA" << endl;
	cout << " jesli chcesz powrocic do gry nacisnij 'p'" << endl;
	char wyjscie[dlugosc];
	do
	{
		cin >> wyjscie;
		if ((strlen(wyjscie) == 1) and (wyjscie[0] == 'p'))
		{
			break;
		}
		cout << " Bledne dane!\n Podaj poprawne dane:" << endl;
	} while (true);
	stopczas = clock();
	pauzaczas = pauzaczas + (stopczas - startczas) / CLOCKS_PER_SEC;
}
void wczytajplansze(char  Q[rozmiar][rozmiar], char W[rozmiar][rozmiar], char A[rozmiar][rozmiar], char S[rozmiar][rozmiar], char graczzaczynajacy, char graczdrugi, int& zajete)
{
	zajete = 0;
	for (int i = 0; i < rozmiar; i++)							//czysci aktualna plansze
	{
		for (int j = 0; j < rozmiar; j++)
		{
			Q[i][j] = ' ';
			W[i][j] = ' ';
			A[i][j] = ' ';
			S[i][j] = ' ';
		}
	}
	Q[2][1] = graczzaczynajacy;								//wpisuje wartosci zgodne z predefiniowana plansza
	Q[1][1] = graczzaczynajacy;
	Q[1][0] = graczzaczynajacy;
	W[1][0] = graczzaczynajacy;
	W[0][1] = graczzaczynajacy;
	A[0][0] = graczzaczynajacy;
	A[0][1] = graczzaczynajacy;
	A[1][2] = graczzaczynajacy;
	Q[0][1] = graczdrugi;
	Q[1][2] = graczdrugi;
	W[1][1] = graczdrugi;
	A[2][1] = graczdrugi;
	A[1][0] = graczdrugi;
	S[1][1] = graczdrugi;
	S[2][1] = graczdrugi;
	S[2][2] = graczdrugi;
}
void undo(int& zajete, char planszaDOPISANIA[rozmiar * rozmiar * 4], int poleDOPISANIA[rozmiar * rozmiar * 4], char  Q[rozmiar][rozmiar], char W[rozmiar][rozmiar], char A[rozmiar][rozmiar], char S[rozmiar][rozmiar], char planszaOBROTU[rozmiar * rozmiar * 4], char stronaOBROTU[rozmiar * rozmiar * 4], bool kolkoikrzyzyk)
{
	zajete--;
	if (kolkoikrzyzyk == false)
	{
		switch (planszaOBROTU[zajete])
		{
		case 'q':	if (stronaOBROTU[zajete] == 'x') obrocwprawo(Q);
			if (stronaOBROTU[zajete] == 'z') obrocwlewo(Q);
			break;
		case 'w':	if (stronaOBROTU[zajete] == 'x') obrocwprawo(W);
			if (stronaOBROTU[zajete] == 'z') obrocwlewo(W);
			break;
		case 'a':	if (stronaOBROTU[zajete] == 'x') obrocwprawo(A);
			if (stronaOBROTU[zajete] == 'z') obrocwlewo(A);
			break;
		case 's':	if (stronaOBROTU[zajete] == 'x') obrocwprawo(S);
			if (stronaOBROTU[zajete] == 'z') obrocwlewo(S);
			break;
		}
	}

	switch (planszaDOPISANIA[zajete])
	{
	case 'q':
		for (int j = 1; j <= rozmiar; j++)
		{
			for (int i = 1; i <= rozmiar; i++)
			{
				if ((rozmiar - j) * rozmiar + i == poleDOPISANIA[zajete])
				{
					Q[j - 1][i - 1] = ' ';
				}
			}
		}
		break;
	case 'w':
		for (int j = 1; j <= rozmiar; j++)
		{
			for (int i = 1; i <= rozmiar; i++)
			{
				if ((rozmiar - j) * rozmiar + i == poleDOPISANIA[zajete])
				{
					W[j - 1][i - 1] = ' ';
				}
			}
		}
		break;
	case'a':
		for (int j = 1; j <= rozmiar; j++)
		{
			for (int i = 1; i <= rozmiar; i++)
			{
				if ((rozmiar - j) * rozmiar + i == poleDOPISANIA[zajete])
				{
					A[j - 1][i - 1] = ' ';
				}
			}
		}
		break;
	case's':
		for (int j = 1; j <= rozmiar; j++)
		{
			for (int i = 1; i <= rozmiar; i++)
			{
				if ((rozmiar - j) * rozmiar + i == poleDOPISANIA[zajete])
				{
					S[j - 1][i - 1] = ' ';
				}
			}
		}
		break;
	}
	wyliczaniewypisan();
}
void wypiszhistoria(char Q[rozmiar][rozmiar], char W[rozmiar][rozmiar], char A[rozmiar][rozmiar], char S[rozmiar][rozmiar], char imiePIERWSZE[dlugosc], char imieDRUGIE[dlugosc], char pierwszygracz, char drugigracz)
{

	system("cls");
	krawedzgorna();
	krawedzgorna();
	cout << endl;
	for (int m = 0; m < rozmiar - 1; m++)
	{
		srodkowapusta(Q);
		srodkowapusta(W);
		cout << endl;
		srodkowapelna();
		srodkowapelna();
		cout << endl;
	}
	srodkowapusta(Q);
	srodkowapusta(W);
	wyliczaniewypisan();
	if (wyliczaniewypisan() == 0)
	{
		cout << "\truch gracza " << imiePIERWSZE << " (" << pierwszygracz << ")" << endl;
	}
	else
	{
		cout << "\truch gracza " << imieDRUGIE << " (" << drugigracz << ")" << endl;
	}
	krawedzdolna();
	krawedzdolna();
	cout << endl;
	krawedzgorna();
	krawedzgorna();
	cout << endl;
	for (int m = 0; m < rozmiar - 1; m++)
	{
		srodkowapusta(A);
		srodkowapusta(S);
		cout << endl;
		srodkowapelna();
		srodkowapelna();
		cout << endl;
	}
	srodkowapusta(A);
	srodkowapusta(S);
	cout << endl;
	krawedzdolna();
	krawedzdolna();
	cout << endl;
}


void historia(int& zajete, char planszaDOPISANIA[rozmiar * rozmiar * 4], int poleDOPISANIA[rozmiar * rozmiar * 4], char  Q[rozmiar][rozmiar], char W[rozmiar][rozmiar], char A[rozmiar][rozmiar], char S[rozmiar][rozmiar], char planszaOBROTU[rozmiar * rozmiar * 4], char stronaOBROTU[rozmiar * rozmiar * 4], char imiePIERWSZE[dlugosc], char imieDRUGIE[dlugosc], char pierwszygracz, char drugigracz, bool kolkoikrzyzyk)
{
	bool wyjscie = true;
	int maxruchow = zajete;
	do
	{
		system("cls");
		if (zajete == maxruchow)
		{
			wypiszwygrana(Q, W, A, S, imiePIERWSZE, imieDRUGIE, pierwszygracz, drugigracz);
		}
		else 	wypiszhistoria(Q, W, A, S, imiePIERWSZE, imieDRUGIE, pierwszygracz, drugigracz);
		if (maxruchow != zajete) {
			cout << " dopisanie: " << planszaDOPISANIA[zajete] << poleDOPISANIA[zajete] << endl;
			if (kolkoikrzyzyk == false)
			{
				cout << " obrot: " << planszaOBROTU[zajete] << stronaOBROTU[zajete] << endl;
			}
		}
		cout << endl;
		cout << " co chcesz zrobic?" << endl;
		cout << " a - ruch do przodu" << endl;
		cout << " s - ruch do tylu" << endl;
		cout << " x - zakoncz analize" << endl;
		int dlugos;
		char akcja[dlugosc];
		do
		{
			dlugos = 0;
			cin >> akcja;
			if ((maxruchow == zajete) and (akcja[0] == 'a'))
			{
				cout << " Nie ma dalszych ruchow!" << endl << " wybierz inna czynnosc: ";
				continue;
			}
			if ((0 == zajete) and (akcja[0] == 's'))
			{
				cout << " Nie mozna cofnac ruchu!" << endl << " wybierz inna czynnosc: ";
				continue;
			}
			dlugos = strlen(akcja);
			if ((akcja[0] == 'x') and (dlugos == 1)) {
				break;
			}
			if ((akcja[0] == 'a') and (dlugos == 1)) {
				break;
			}
			if ((akcja[0] == 's') and (dlugos == 1)) {
				break;
			}
			cout << " Bledne dane!\nPodaj poprawne dane: ";
		} while (true);
		switch (akcja[0])
		{
		case 's': undo(zajete, planszaDOPISANIA, poleDOPISANIA, Q, W, A, S, planszaOBROTU, stronaOBROTU, kolkoikrzyzyk);
			break;
		case 'x': wyjscie = false;
			break;
		case 'a': ruchdoprzodu(zajete, planszaDOPISANIA, poleDOPISANIA, Q, W, A, S, planszaOBROTU, stronaOBROTU, pierwszygracz, drugigracz, kolkoikrzyzyk);
			break;
		}
	} while (wyjscie == true);
}
void ruchdoprzodu(int& zajete, char planszaDOPISANIA[rozmiar * rozmiar * 4], int poleDOPISANIA[rozmiar * rozmiar * 4], char  Q[rozmiar][rozmiar], char W[rozmiar][rozmiar], char A[rozmiar][rozmiar], char S[rozmiar][rozmiar], char planszaOBROTU[rozmiar * rozmiar * 4], char stronaOBROTU[rozmiar * rozmiar * 4], char pierwszygracz, char drugigracz, bool kolkoikrzyzyk)
{

	char znakdopis;
	if (zajete % 2 == 0)
	{
		znakdopis = pierwszygracz;
	}
	else
	{
		znakdopis = drugigracz;
	}
	switch (planszaDOPISANIA[zajete])
	{
	case 'q':
		for (int j = 1; j <= rozmiar; j++)
		{
			for (int i = 1; i <= rozmiar; i++)
			{
				if ((rozmiar - j) * rozmiar + i == poleDOPISANIA[zajete])
				{
					Q[j - 1][i - 1] = znakdopis;
				}
			}
		}
		break;
	case 'w':
		for (int j = 1; j <= rozmiar; j++)
		{
			for (int i = 1; i <= rozmiar; i++)
			{
				if ((rozmiar - j) * rozmiar + i == poleDOPISANIA[zajete])
				{
					W[j - 1][i - 1] = znakdopis;
				}
			}
		}
		break;
	case'a':
		for (int j = 1; j <= rozmiar; j++)
		{
			for (int i = 1; i <= rozmiar; i++)
			{
				if ((rozmiar - j) * rozmiar + i == poleDOPISANIA[zajete])
				{
					A[j - 1][i - 1] = znakdopis;
				}
			}
		}
		break;
	case's':
		for (int j = 1; j <= rozmiar; j++)
		{
			for (int i = 1; i <= rozmiar; i++)
			{
				if ((rozmiar - j) * rozmiar + i == poleDOPISANIA[zajete])
				{
					S[j - 1][i - 1] = znakdopis;
				}
			}
		}
		break;
	}
	if (kolkoikrzyzyk == false)
	{
		switch (planszaOBROTU[zajete])
		{
		case 'q':	if (stronaOBROTU[zajete] == 'z') obrocwprawo(Q);
			if (stronaOBROTU[zajete] == 'x') obrocwlewo(Q);
			break;
		case 'w':	if (stronaOBROTU[zajete] == 'z') obrocwprawo(W);
			if (stronaOBROTU[zajete] == 'x') obrocwlewo(W);
			break;
		case 'a':	if (stronaOBROTU[zajete] == 'z') obrocwprawo(A);
			if (stronaOBROTU[zajete] == 'x') obrocwlewo(A);
			break;
		case 's':	if (stronaOBROTU[zajete] == 'z') obrocwprawo(S);
			if (stronaOBROTU[zajete] == 'x') obrocwlewo(S);
			break;
		}
	}
	zajete++;
	wyliczaniewypisan();
}


