# **Gites** - distributed version control system  
## Projekt 'Projektowanie systemów rozproszonych' 
### Temat projektu:
### **Implementacja rozproszonego systemu kontroli wersji**
### _Zespół projektowy: Jakub Francuz, Damian Gaszewski_

### Opis projektu:

**Gites** to rozproszony system kontrolii wersji 
(vcs - (distributed) version control system).

Ten projekt został pomyślany jako niskopoziomowa implementacja rozproszonego systemu wersjonowania plików w Pythonie przy użyciu tylko modułów stdlib (np. 'socket' dla sieci) do przesyłania i przechowywania wersji plików w rozproszony i odporny sposób.

**Gites** jest tu zdefiniowany po prostu jako klaster serwerów w architekturze serwer-klient, hostujący potencjalnie duże pliki tekstowe, które muszą być przesyłane i przechowywane niezawodnie i bezpiecznie w sposób odporny na błędy.

Poniżej pokazano, jak uruchomić **Gites lokalnie, symulując rozproszony klaster. Dany plik jest dystrybuowany `(PUT <nazwa pliku>`) z klienta DFC (distributed file client) do czterech serwerów DFS (distributed file system) w kawałkach (chunks), które mogą być pobrane (`GET <nazwa pliku>`) i użyte do rekonstrukcji pliku u klienta lokalnego.

Istnieje wbudowana redundancja w sposobie przechowywania kawałków plików w serwerach, co zapewnia, że jeśli dany (pojedynczy) serwer ulegnie awarii, plik nadal może zostać zrekonstruowany. Optymalizacja ruchu jest osiągana poprzez nie wysyłanie żadnych nadmiarowych kawałków (chunks) plików, jeśli nie jest to konieczne. Pewne bezpieczeństwo jest zaimplementowane poprzez uwierzytelnianie i przechowywanie haszy haseł (md5).

### **Uruchamianie** **projektu**

RUN (dowolna liczba) serwerów najpierw, potem klient:

`$ py dfs1.py 10001`

`$ py dfs2.py 10002`

`$ py dfs3.py 10003`

`$ py dfs4.py 10004`

`$ py dfc.py dfc.conf`

**UŻYTKOWNICY i HASŁA:**

>Jakub : Francuz1

>Admin : Admin0

>Damian : Gaszewski2

Nazwy użytkowników i hasła mogą być zmieniane w plikach konfiguracyjnych. Zmiany muszą być zgodne z odstępami i składnią plików conf i być identyczne we wszystkich plikach .conf (pliki .conf dfs i dfc są identyczne z wyjątkiem nazwy).

Algorytm haszowania hasła to md5. Jeśli chcieć wykorzystać inny, wszystkie odpowiednie hashe muszą być ponownie obliczone w pliku dfc.py (ctrl+f: 'hashlib').

### **Polecenia**
Program wyswietla liste dostepnych komend:

`[create, init, add, list_stage_local, list_vcs_local, list_remote]`

Komenda `[create]`
> Tworzy plik tekstowy o wprowadzonej nazwie w `stage/` directory  

Komenda `[init]`
> Inicjalizuje system wersjonowania i tworzy repozytorium lokalne `.gites\files\`

Komenda `[add]`
> Dodaje wybrane/wszystkie pliki ze stage

Komenda `[list_stage_local]`
> Wyświetla listing zawartości `stage/` directory 

Komenda `[list_vcs_local]`
> Wyświetla listing zawartości `.gites/files/` directory 
Komenda `[list_stage_local]`

Komenda `[list_remote]`
> Wyświetla możliwość operacji do przeprowadzenia na klastrze serwerów:

- Operacja `[put]`:
>>PUT wysyła wszelkie pliki tekstowe znajdujące się w folderze DFC do folderów DFS w celu rozproszonego przechowywania.

>>`put` dzieli pliki na 4 kawałki (chunks), przechowuje pary kawałków na każdym serwerze po zhaszowaniu pliku i określenie modułu hasha (modulo) w celu zapewnienia sprawiedliwej dystrybucji, zgodnie z poniższą tabelą. Duplikacja plików zapewnia niezawodność w przypadku awarii jednego serwera.

>Lokalizacje par plików
hash mod **DFS1 DFS2 DFS3 DFS4**

|hash mod|DFS1|DFS2|DFS3|DFS4|
|:--:|:-----:|:-----:|:-----:|:-----:|
| 0  | (1,2) | (2,3) | (3,4) | (4,1) | 
| 1  | (4,1) | (1,2) | (2,3) | (3,4) |
| 2  | (3,4) | (4,1) | (1,2) | (2,3) |
| 3  | (2,3) | (3,4) | (4,1) | (1,2) |

- Operacja `[get]`:

>>pobiera pliki z serwerów do folderu użytkownika `(username/)` w folderze głównym DFC klienta.

>>`get` łączy 4 kawałki w jeden plik. Jeśli jeden serwer jest uszkodzony, operacja ta może się udać. Jeśli operacja się nie powiedzie, plik nie zostanie utworzony, a użytkownik otrzyma komunikat 'Transfer failed'.

- Operacja `[list]`:
>>`list` dostarcza listę wszystkich części (chunks) plików, które użytkownik zapisał na serwerze. Z listy użytkownik może wyłuskać nazwy plików i określić plik do operacji GET. Jeśli użytkownik wybierze PUT w ramach LIST, może określić plik do wysłania do rozproszonego przechowywania.






























