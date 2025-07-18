# AI Prompt Prettify by KPZsProductions

[![Commit Activity](https://img.shields.io/github/commit-activity/m/KPZsProductions/AI-Prompt-Prettify)](https://github.com/KPZsProductions/AI-Prompt-Prettify/graphs/commit-activity)

---

## Opis Aplikacji

**AI Prompt Prettify** to aplikacja desktopowa stworzona przez KPZsProductions, która umożliwia ulepszanie promptów (poleceń) do modeli AI, takich jak Gemini od Google. Dzięki intuicyjnemu interfejsowi użytkownika, aplikacja pozwala na szybkie i wygodne poprawianie jakości promptów, co przekłada się na lepsze i bardziej precyzyjne odpowiedzi generowane przez sztuczną inteligencję.

Aplikacja korzysta z API Gemini, automatycznie wykrywa i zapisuje klucz API, a także oferuje szereg funkcji ułatwiających codzienną pracę z promptami.

---

## Funkcje

- **Ulepszanie promptów AI** – automatyczne poprawianie i rozbudowywanie poleceń dla modeli AI.
- **Wygodny interfejs graficzny** – aplikacja oparta na Tkinter z nowoczesnym wyglądem.
- **Obsługa schowka** – szybkie wklejanie i kopiowanie tekstu.
- **Konfiguracja klucza API** – łatwe wprowadzanie i zapisywanie klucza Gemini API.
- **Skrót klawiszowy** – globalny hotkey `Ctrl+Alt+P` do szybkiego otwierania/ukrywania okna.
- **Automatyczne kopiowanie ulepszonego prompta** – po ulepszeniu prompt jest od razu w schowku.
- **Pasek postępu** – informacja o trwającym procesie ulepszania.
- **Wielojęzyczność** – aplikacja zachowuje język oryginalnego prompta.
- **Bezpieczeństwo** – klucz API może być zapisany lokalnie lub używany tymczasowo.

---

## Instrukcja Użycia

1. **Uruchom aplikację** (`python main.py`).
2. **Wprowadź swój prompt** w górnym polu tekstowym lub wklej go ze schowka.
3. Kliknij **"Enhance Prompt"**, aby ulepszyć polecenie.
4. Ulepszony prompt pojawi się w dolnym polu i zostanie automatycznie skopiowany do schowka.
5. Użyj przycisków, aby skopiować, wyczyścić pole, wkleić nowy tekst lub skonfigurować klucz API.
6. Okno aplikacji możesz ukryć lub pokazać skrótem `Ctrl+Alt+P`.
7. Aby zamknąć aplikację, kliknij **"Quit application"**.

---

## Instalacja

1. **Wymagania:**
   - Python 3.8 lub nowszy
   - System Windows (zalecany)
   - Klucz API Gemini (do uzyskania na [Google AI Studio](https://makersuite.google.com/app/apikey))

2. **Instalacja zależności:**
   ```bash
   pip install tkinter keyboard pyperclip google-generativeai
   ```

3. **Uruchomienie aplikacji:**
   ```bash
   python main.py
   ```

4. **Pierwsze uruchomienie:**
   - Przy pierwszym uruchomieniu zostaniesz poproszony o podanie klucza API Gemini.
   - Możesz zapisać klucz lokalnie w pliku `config.json` lub używać go tymczasowo.

---

## Wkład (Contributing)

Chcesz pomóc w rozwoju projektu? Zapraszamy do współpracy!

- Zgłaszaj błędy i propozycje funkcji przez [Issues](https://github.com/KPZsProductions/AI-Prompt-Prettify/issues).
- Forkuj repozytorium, twórz własne gałęzie i wysyłaj Pull Requesty.
- Przestrzegaj zasad dobrego stylu kodowania i opisuj swoje zmiany.

---

## Licencja

Projekt **AI Prompt Prettify** jest objęty prawami autorskimi © 2025 KPZsProductions. Wszelkie prawa zastrzeżone.

---


---

> **Author:** KPZsProductions  
> **Contact:** [GitHub Profile](https://github.com/KPZsProductions)
