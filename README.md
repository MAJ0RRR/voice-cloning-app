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
# Instrukcja obsługi CLI
Aby wykonać automatyczne klonowanie głosu przy użyciu jednej komendy należy wykonać skrypt `whole_pipeline.py`
Skrypt przyjmuje następujące wymagane argumenty:

  `--gpu` (gpu) Pozwala na określenie numeru używanej karty graficznej.

  `--run_dir` (run_dir) Folder w którym będą przechowywane przetworzone próbki audio.

  `--raw_source` (raw_source) Folder w którym znajdują się wejściowe próbki audio.

Oraz następujące opcjonalne argumenty pozwalające dostosować parametry procesowania audio i uczenia modelu:

  `--trim_source_length` (trim_source_length) Długość do której będzie przycięte wejściowe audio w minutach. W przypadku podania 0 audio wejściowe nie bedzie przycinane.
  Domyślnie 0
  
  `--silence_split_type` (silence_split_type) Metoda która będzie użyta do podziału wejściowych próbek audio, może przyjmować wartości "equal" lub "silence".
  **Domyślnie "equal"**
  
  `--split_len` (split_len) Długość na jakie kawałki zostaną pocięte próbki wejściowe. Używane tylko wtedy gdy silence_split_type = "equal".
  **Domyślnie 8**
  
  `--split_min_silence_lens` (split_min_silence_lens) Długości ciszy według której zostaną pocięte próbki wejściowe. Używane tylko wtedy gdy silence_split_type = "silence".
  **Domyślnie [300]**
  
  `--split_silence_threshs` (split_silence_threshs) Poziom dźwięku w dBm uznawany za ciszę. Używane tylko wtedy gdy silence_split_type = "silence"
  **Domyślnie [-45]**
  
  `--whisper_vram` (whisper_vram) Ilość VRAM dostępnych dla STT.
  **Domyślnie 10**
  
  `--discard_transcripts` (discard_transcripts)  Parametr określający czy niepoprawnie przeprocesowane przez technologię STT próbki będą odrzucane.
  **Domyślnie True**
  
  `--discard_word_count` (discard_word_count) Minimalna długość słów w próbce. Używane tylko wtedy gdy discard_transcripts = true.
  **Domyślnie 3**
  
  `--language` (language) Język wejściowy, może przyjmować wartości "en" lub "pl.
  **Domyślnie "en"**
  
  `--model_path` (model_path) Ścieżka do modelu bazowego, jeśli nie zostanie podana stworzony zostanie nowy model.
  **Domyślnie None**
  
  `--run_name` (run_name) Nazwa folderu z wynikami działania.
  **Domyślnie "experiment"**
  
  `--timeout_seconds` (timeout_seconds) Czas w sekundach po którym zostanie zakończony proces uczenia.
  **Domyślnie 32400**

Po zakończeniu procesu przetwarzania audio i uczenia modelu wynikowy model głosu będzie dostępny w folderze `output/<run_name>`
# Eksperymenty
Możliwe jest przeprowadzenie eksperymentów pozwalających na ustalenie optymalnych parametrów procesowania głosu i uczenia modelu. W tym celu należy podjąć następujące kroki :

1) Najpierw należy wypełnić plik `experiments/definitions.json`, co można osiągnąć na dwa sposoby:
    
   - wypełnić plik ręcznie zachowując odpowiedni format (opisany w [tej sekcji](#format-pliku-definitionsjson))
   - skorzystać ze skryptu `experiments/generate_definitions.py` (sposób wykorzystania opisany w [tej sekcji](#skrypt-do-automatycznego-generowania-definicji-eksperymentów))
2) Następnie należy uruchomić skrypt `experiments/execute_experiments.py`. Skrypt pobierze wygenerowane wcześniej definicje i zacznie wykonywać eksperymenty. Przeprocesowane próbki podane do każdego z nich znajdować się będą w folderze `experiments/<nazwa_eksperymentu>` a wyniki działania w folderze `output/<nazwa_eksperymentu>`.

## Format pliku definitions.json
Główną część pliku stanowi sekcja "Definitions" będąca tablicą definicji poszczególnych eksperymentów.
W pliku również definicji zawarte są dwie zmienne globalne dla wszystkich eksperymentów - numer GPU na którym wykonywane będą obliczenia oraz ilośc dostępnej pamięci na danym GPU.
```json
{
   "Definitions": [
    { ... },
    { ... },
  ],
  "Gpu": 0,
  "WhisperVram": 8
}
```
### Format definicji jednego eksperymentu
Każda definicja zawiera komplet zmiennych potrzebnych do przeprowadzenia eksperymentu. Zmienne te to:
 - `Name` - nazwa eksperymentu,
 - `RawSource` - ścieżka do folderu z wejściowymi plikami audio
 - `TrimSourceLengthMs` - długość do której próbki audio będą przycięte, w przypadku podania 0 próbki nie będą przycinane
 - `ModelPath` - ścieżka do modelu bazowego, w przypadku nie podania parametru model będzie tworzony od początku
 - `Language` - język próbek wejściowych
 - `SilenceSplitType` - sposób w jaki dzielone będą próbki wejściowe, może przyjmować wartosci `equal` lub `silence`
 - `RemoveNoise` - zmienna określająca czy próbki wejściowe będą odszumiane
 - `DiscardTranscripts` - zmienna określająca czy próbki, które zostały niepoprawnie odczytane przez technologię STT
 - `DiscardWordCount` - uzywane w przypadku ustawienia `DiscardTranscripts = true` minimalna długość zdania podanego do algorytmu (w słowach)
 - `SplitSilenceLength` - używane w przypadku ustawienia `SilenceSplitType = "equal"` - długość próbek na które będzie podzielone audio wejściowe przed podaniem do algorytmu uczenia
 - `SplitSilenceMinLength` - używane w przypadku ustawienia `SilenceSplitType = "silence"` - minimalna długość próbek na które będzie podzielone audio wejściowe przed podaniem do algorytmu uczenia
 - `SplitSilenceThresh` - używane w przypadku ustawienia `SilenceSplitType = "silence"` - poziom ciszy według którego podzielone zostanie audio wejściowe przed podaniem do algorytmu uczenia

Oto przykładowa definicja eskperymentu

```json
{
   "Name": "experiment_1",
   "RawSource": "audiofiles/raw",
   "TrimSourceLengthMs": 0,
   "ModelPath": "models/default/checkpoint_700000.pth",
   "Language": "pl",
   "SilenceSplitType": "equal",
   "RemoveNoise": false,
   "DiscardTranscripts": false,
   "SplitSilenceLength": 14
}
```
## Skrypt do automatycznego generowania definicji eksperymentów
Skrypt `generate_definitions.py` działa na podstawie pliku `experiments_description.json` zawierającego opis eksperymentów do wykonania.
### Struktura pliku opisu eksperymentów
 - Dokładny sposób generowania definicji określa pole `Mode`, mogące przyjmować wartości `diff` lub `product`
 - Pole `DefaultConfig` - używane tylko w trybie `diff` - opisane [poniżej](#tryb-diff)
 - Dalsza część pliku składa się z pól zgodnych z [opisem definicji eksperymentu](#format-definicji-jednego-eksperymentu) z tym wyjątkiem że parametry `RawSource`, `ModelPath`, `Language` są zgrupowane w jedną strukturę `Source`, a pole `Name` nie występuje.
   ```json
   "Source":
   {
   "RawSource": "...",
   "ModelPath": "...",
   "Language": "..."
   }
   ```
   Pola te to: `Source`, `TrimSourceLengthMins` , `SilenceSplitType`, `RemoveNoise`, ` DiscardWordCount`, `SplitSilenceLength`, `SplitSilenceMinLength`, `SplitSilenceThresh`, `Gpu`, `WhisperVram`, gdzie każde z tych pól (oprócz `Gpu` i `WhisperVram`) przyjmuje wartość w postaci tablicy parametrów które będą uwzględnione w eksperymencie.
### Tryb diff
W trybie diff przeprowadzany jest jeden eksperyment o domyślnych parametrach a kolejne eksperymenty zmieniają jeden parametr w stosunku do domyślnego zestawu.
Parametry zdefiniowane jako domyślne znajdują się w polu `DefaultConfig` i są zgodne  z [opisem definicji eksperymentu](#format-definicji-jednego-eksperymentu) z tym wyjątkiem że parametry `RawSource`, `ModelPath`, `Language` są zgrupowane w jedną strukturę `Source` oraz nie występują pola `Name` (ustawiane automatycznie)  i `DiscardTranscripts` (domyślnie ustawiane na true) .

Poniżej przedstawiona została struktura pliku `experiments_description.json` dla trybu `diff` pozwalająca wygenerować definicję 4 eksperymentów:
 - domyślnego 
 - domyślnego z dlugością przyciętych próbek ustawioną na 2 (zamiast 4)
 - domyślnego z dlugością przyciętych próbek ustawioną na 8 (zamiast 4)
 - domyślnego z audio wejściowym przyciętym do 10 minut

```json
{
  "Mode" : "diff",
  "DefaultConfig": {
    "Source":
      {
        "RawSource": "audiofiles/raw",
        "ModelPath": "models/default/checkpoint_700000.pth",
        "Language": "pl"
      },
    "TrimSourceLengthMins": 0,
    "SilenceSplitType": "equal",
    "RemoveNoise": false,
    "DiscardWordCount": 0,
    "SplitSilenceLength": 4,
    "SplitSilenceMinLength" : 0,
    "SplitSilenceThresh" : 0
  },
  "Source": [],
  "TrimSourceLengthMins": [10],
  "SilenceSplitType": ["equal"],
  "RemoveNoise": [],
  "DiscardWordCount": [],
  "SplitSilenceLength": [2, 8],
  "SplitSilenceMinLength" : [0],
  "SplitSilenceThresh" : [0],
  "Gpu": 0,
  "WhisperVram": 8
}
```

### Tryb product
W trybie diff iteracja po parametrach odbywa się w trybie "każdy z każdym" (produkt kartezjański). Poniżej przedstawiona została struktura pliku `experiments_description.json` dla trybu `product` pozwalająca wygenerować definicję 4 eksperymentów różniących się między sobą wartościami `TrimSourceLengthMins` i `SplitSilenceLength`:
 - `TrimSourceLengthMins = 0`,  `SplitSilenceLength = 2`
 - `TrimSourceLengthMins = 0`,  `SplitSilenceLength = 4`
 - `TrimSourceLengthMins = 10`,  `SplitSilenceLength = 2`
 - `TrimSourceLengthMins = 10`,  `SplitSilenceLength = 4`
```json
{
  "Mode" : "product",
  "Source": [
     {
        "RawSource": "audiofiles/raw",
        "ModelPath": "models/default/checkpoint_700000.pth",
        "Language": "pl"
     }
  ],
  "TrimSourceLengthMins": [0, 10],
  "SilenceSplitType": ["equal"],
  "RemoveNoise": [false],
  "DiscardWordCount": [0],
  "SplitSilenceLength": [2, 8],
  "SplitSilenceMinLength" : [0],
  "SplitSilenceThresh" : [0],
  "Gpu": 0,
  "WhisperVram": 8
}
```
