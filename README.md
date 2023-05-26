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

# Instrukcja obsługi GUI

Aby wytrenować model można również skorzystać z GUI. Program uruchamiamy komendą:
```bash
python3 app/main.py
```
Z menu głównego wybieramy przycisk `Stwórz nowy model głosu` lub `Dotrenuj model głosu` w zależności od naszych potrzeb.
![Menu glowne](https://github.com/MAJ0RRR/ProjektGrupowy22-23/blob/main/gui_images/choose_audio.png)