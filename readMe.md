# Rozwiązywacz Sudoku

Program mający za zadanie rozwiązywać diagramy sudoku dowolnego rozmiaru.

### Wymagania

Python wersji 3.6 lub wyższej

### Instalacja

Ściągnij wszystkie pliki ze strony https://github.com/PPokorski/SudokuSolverWUT/tree/AnnaSkupinska-patch-1. Uruchom wiersz poleceń i przejdź 
do ścieżki w której rozpakowałeś program. Uruchom program za pomocą polecenia:

```
python matrix.py
```

### Uruchamianie testów jednostkowych

Testy można przeprowadzić uruchmiając plik matrix_unittest.py. Rozwiąże on zadania zawarte w plikach 'sudoku_4x4_solution.csv' i 'sudoku_9x9_solution.csv' oraz porówna uzyskane wyniki z wynikami zawartymi w plikach.

```
python matrix_unittest.py
```

## Używanie programu

Interface użytkownika jest realizowany za pomocą terminala tekstowego. Opcje i akcje są ponumerowane, a użytkownik wybiera je wpisując cyfry odpowiadające funkcjom które chce wykonać.

###Przeprowadzenie baterii testów.

Testy standardowe przygotowane są przez nas (twórców) programu. Wyniki są przechowywane w pliku 'test_Result_n.csv', gdzie n jest bazą sudoku.

```
python matrix.py test <n>
```

Testy wygenerowane to testy, w których algorytm samodzielnie generuje zadania do wykonania (bez pomocy biblioteki opisanej w sprawozdaniu). Ten sposób generowania zadań zapewnia mniej opcji niż użyta biblioteka, dlatego też te zadania nie zostały użyte w testach. n - baza sudoku, m - ilość testów do wygenerowania. Wyniki są przechowywane w pliku 'test_Result_n.csv'.

```
python matrix.py test <n> <m>
```

Testy użytkownika to testy z pliku pochodzącego od użytkownika. n - baza sudoku, nazwa_pliku - nazwa pliku z którego ściągane są zadania.Wyniki są przechowywane w pliku 'test_User_Result_n.csv'

```
python matrix.py test-from-file <n> <nazwa_pliku>
