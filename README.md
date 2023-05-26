# ProjektGrupowy22-23

Repozytorium projektu grupowego poświęconego tematowi "Opracowanie aplikacji do klonowania głosu w języku python"

# Dependencje
Python 3.9 z modułem tkinter.
Instalacja:
```bash
sudo apt install python3.9-tk
```

# Konfiguracja i użycie
Uruchomienie skryptu konfiguracyjnego:
`$ python3 initialize.py`
<hr>
Aby przeprowadzić klonowanie głosu potrzebujemy pliku audio. Powinien on zawierać głos jednego mówcy i mieścić się w przedziale od 1 do 2 godzin.
<hr>
Odpowiednio dobrany plik należy umieścić następnie w folderze audiofiles/raw i wywołać skrypt, który podzieli oryginalny plik audio na próbki, bazując na długości ciszy między wypowiedziami w celu wychwycenia zdań oraz odrzuci te zawierające w znacznej części ciszę i umieści je w folderze audiofiles/splits:

`$ python3 splits_silence.py`

`-t` (threshold) pozwala na wybranie poziomu, od którego uznajemy dany dźwięk za ciszę **(domyślnie -45)**

`-l` (length) pozwala na wybranie długości ciszy która określa punkt podziału **(domyślnie 300ms)**

`-d` (destination) pozwala na wybranie miejsca docelowego, do którego trafią pocięte próbki **(domyślnie audiofiles/splits)**

`-s` (source) pozwala na określenie lokalizacji pliku wejściowego **(domyślnie audiofiles/raw)**
<hr>
Możliwy jest podział bez odrzucania próbek na podstawie tego ile ciszy zawierają:

`$ python3 splits_equal.py`

`-l` (length) pozwala na wybranie długości próbki **(domyślnie 8 sekund)**

`-d` (destination) pozwala na wybranie miejsca docelowego, do którego trafią pocięte próbki **(domyślnie audiofiles/splits)**

`-s` (source) pozwala na określenie lokalizacji pliku wejściowego **(domyślnie audiofiles/raw)**
<hr>
Następnie istnieje możliwość odszumiania pociętych próbek:

`$ python3 noise.py`

`-d` (destination) pozwala na wybranie miejsca docelowego, do którego trafią odszumione próbki **(domyślnie audiofiles/datasets/dataset/wavs)**

`-s` (source) pozwala na określenie lokalizacji katalogu z pociętymi próbkami **(domyślnie audiofiles/splits)**
<hr>
Potem należy wywołać skrypt do transkrypcji.

`$ python3 whispertrans.py`

`-l` (language) pozwala wybrać język, w którym mówi osoba, której głos chcemy sklonować **(domyślnie en)**

`-n` (name) pozwala na określenie nazwy zbioru uczącego w katalogu audiofiles/datasets **(domyślnie dataset)**

`-v` (vram) pozwala na określenie ilości pamięci VRAM karty graficznej w GB **(domyślnie 10)**

`-g` (gpu) pozwala na określenie numeru karty graficznej, której chcemy użyć **(brak domyślnej wartości)**
<hr>
Następnym procesem jest odrzucenie części błędnych transkrypcji.

`$ python3 discard_transcriptions.py` 

`-l` (language) pozwala wybrać język, w którym mówi osoba, której głos chcemy sklonować **(domyślnie en)**

`-s` (source-directory) pozwala na określenie ścieżki do zbioru uczącego **(domyślnie audiofiles/datasets/dataset)**

`-m` (min-words) pozwala na określenie minimalnej długości transkrypcji **(domyślnie 3)**
<hr>
W kolejnym kroku możemy uruchomić uczenie na podstawie jakiegoś modelu lub “od zera”.

`$ python3 train.py`

`-m` (model) pozwala na określenie lokalizacji modelu wejściowego. Jeżeli nie zostanie podany uczenie będzie “od zera” **(domyślnie brak)**

`-n` (name) pozwala na określenie nazwy przebiegu uczenia **(domyślnie dataset)**

`-l` (language) pozwala wybrać język, w którym mówi osoba, której głos chcemy sklonować **(domyślnie en)**

`-d` (dataset) pozwala na określenie nazwy zbioru uczącego w katalogu audiofiles/datasets **(domyślnie dataset)**

`-g` (gpu) pozwala na określenie numeru karty graficznej, której chcemy użyć **(brak domyślnej wartości)**

### Aby syntezować mowę można użyć komendy "tts" z następującymi argumentami:
`--text` tekst, który będzie syntezowany

`--model_path` ścieżka do modelu

`--config_path` ścieżka do pliku konfiguracyjnego modelu

`--out_path` ścieżka do miejsca, gdzie ma zostać zapisany plik

# Instrukcja obsługi GUI
### Trening modelu

Aby wytrenować model można również skorzystać z GUI. Program uruchamiamy komendą:
```bash
python3 app/main.py
```
Z menu głównego wybieramy przycisk `Stwórz nowy model głosu` lub `Dotrenuj model głosu` w zależności od naszych potrzeb.
![Menu glowne](https://github.com/MAJ0RRR/ProjektGrupowy22-23/blob/main/gui_images/menu.png)
W kolejnym kroku wybieramy płeć mówcy oraz język, którym się posługuje. Następnie klikamy przycisk `Dalej`.
![Wybierz język](https://github.com/MAJ0RRR/ProjektGrupowy22-23/blob/main/gui_images/choose_language.png)
Jeżeli wybraliśmy opcję trenowania modelu, teraz następuje wybranie modelu. Aby ułatwić wybór, istnieje możliwość odsłuchania bazowego pliku audio każdego modelu. Aby przejść dalej klikamy przycisk `Dalej`.
![Wybierz model](https://github.com/MAJ0RRR/ProjektGrupowy22-23/blob/main/gui_images/choose_model.png)
Następnie należy wybrać pliki audio do uczenia modelu. Można to zrobić dodając pojedyncze pliki, jak i całe foldery. Na dole ekranu należy również wybrać ilość VRAM. Jeżeli użytkownik posiada więcej niż jedną kartę graficzną, należy wskazać, której algorytm będzie miał użyć. Po wybraniu przycisku ‘Rozpocznij proces’ pliki audio zostaną przygotowane do treningu, a następnie zostanie uruchomiony proces trenowania modelu. 
![Wybierz audio](https://github.com/MAJ0RRR/ProjektGrupowy22-23/blob/main/gui_images/choose_audio.png)
Po zainicjalizowaniu treningu po około 2 minutach ukaże się poniższe okienko:
![Trenuj](https://github.com/MAJ0RRR/ProjektGrupowy22-23/blob/main/gui_images/train.png)
Klikając w link w przeglądarce zostanie otwarty 'Tensoarboard', dzięki któremu możemy śledzić wyniki nauki. Zalecamy, aby trenować model przynajmiej godzinę. Po zakończonym treningu zostaną automatycznie wygenerowane pliki audio. 
![Po treningu probki](https://github.com/MAJ0RRR/ProjektGrupowy22-23/blob/main/gui_images/after1.png)
Proces ten potrwa kilka minut. Następnie ukaże nam się taki widok:
![Po treningu](https://github.com/MAJ0RRR/ProjektGrupowy22-23/blob/main/gui_images/after2.png)
Aby zapisać wybrany model należy wybrać przycisk ‘Zapisz wybrany model’, a następnie wpisać nazwę dla modelu. Aby sprawdzić jak brzmią dane głosy można je odsłuchać. Aby sprawdzić, jak model radzi sobie z wybrany tekstem należy wpisać go w pole pod napisem ‘Wpisz tekst’, a następnie kliknąć przycisk ‘Odsłuchaj’ znajdujący się poniżej. Jeżeli żaden z modeli nie spełnia naszych oczekiwań, należy wybrać najlepszy z nich i wybrać opcję ‘Dotrenuj model’. Po wybraniu tej opcji zostanie na nowo uruchomiony proces trenowania. 
### Synteza głosu
Aby syntezować głos należy:
```bash
1.Wybrać z menu głównego "Syntezuj mowę na podstawie modelu".
2.Wybrać płeć oraz język z kolejnego widoku.
3.Wybrać model głosu z listy.
```
Następnie zostanie wyświetlony ten widok.
![generowanie probek](https://github.com/MAJ0RRR/ProjektGrupowy22-23/blob/main/gui_images/generate_audio.png)
W lewym górnym roku możemy wpisać tekst wybrany tekst. Aby rozpoczać syntezę należy kliknąć przycisk "Generuj audio". Wygenerowane audio będzie znajdowało się w liście po prawej stronie.
Aby zobaczyć wszystkie nagrania głosu należy kliknąć "Wszystkie nagrania głosu".
![generowanie probek](https://github.com/MAJ0RRR/ProjektGrupowy22-23/blob/main/gui_images/all_recordings.png)

### Generowanie próbek do uczenia
Aby wygenerować próbki należy:
```bash
1.Wybrać z menu głównego "Wygeneruj próbki do uczenia".
2.Wybrać język z kolejnego widoku i kliknąć "Dalej".
3.Wybrać pliki audio i kliknąć rozpocznij proces.
4.Po zakończonym procesie gotowe próbki znajdują się w folderze 'audiofiles/datasets/dataset_n'
```

