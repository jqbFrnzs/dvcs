Projekt 'Projektowanie systemów rozproszonych'

Temat projektu:
10.Implementacja rozproszonego systemu kontroli wersji

1. techstack

python
libs?

2. założenia

1) otwiera 2 pliki
2) porównywanie zawartości (identyczności) dwóch plików
3) wyświetlanie różnic
4) wybór wersji pliku (chronologia)
5) zapis pliku wynikowego
6) tagowanie wersji pliku
7) zachowanie poprzednich wersji
8) możliwość przeglądania poprzednich wersji
9) możliwość korzystania z systemu bez zakłóceń z wielu klientów
10) calosc w architekturze client-server
11) dwa foldery operacyjny i systemu kontroli wersji
12) okreslenie zasad nazywania plikow

3. funkcjonalności

1) diff - porównywanie plików i zwracanie wyniku (porównanie tekstu)
2) add - dodanie pliku do kontroli wersji
3) ignore - okreslanie ktorych plikow nie wersjonowac
4) commit - zatwierdzanie zmian i dodanie tagu
5) push - zapis pliku wynikowego
6) ls-files - wylistowanie plikow wersjonowanych (aktualnie/poprzednie)
7) remove - usuwanie plikow z kontroli wersji
8) pull - synchronizacja repozytorium z wersją lokalną

4. wyjątki

1) błędny plik konfiguracyjny
2) niemożliwość stworzenia katalogu (uprawnienia)
3) system kontroli wersjilista ignorowanych plikow nie obsluguje rozszerzenia
4) brak dostepu do zasobu repozytorium (zajety przez innego klienta)
5) brak możliwości dodania pliku do kontroli wersji (już jest kontrolowany)
6) brak mozliwosci dodania pliku o istniejacej nazwie w systemie
7) brak mozliwosci dodania pliku bez zastosowania sie do zasad nazywania plikow
