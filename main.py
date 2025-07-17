import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import keyboard
import pyperclip
import threading
import google.generativeai as genai
import sys
import os
import json
from tkinter import font

class PromptEnhancerApp:
    def __init__(self):
        self.dialog_window = None
        self.api_key = None
        self.window_visible = False
        self.config_file = "config.json"
        
        # Stwórz ukryty root window
        self.root = tk.Tk()
        self.root.withdraw()  # Ukryj główne okno
        
        # Konfiguracja
        self.setup_api()
        self.setup_hotkey()
        
    def setup_api(self):
        """Konfiguracja API Gemini z automatycznym odczytem z konfiguracji"""
        # Najpierw sprawdź plik konfiguracyjny
        self.api_key = self.load_api_key_from_config()
        
        # Jeśli nie ma w pliku, sprawdź zmienną środowiskową
        if not self.api_key:
            self.api_key = os.getenv('GEMINI_API_KEY')
        
        # Jeśli nadal nie ma klucza, poproś o wprowadzenie
        if not self.api_key:
            self.root.after(100, self.show_api_key_dialog)
        else:
            try:
                genai.configure(api_key=self.api_key)
                print("Klucz API Gemini załadowany pomyślnie.")
            except Exception as e:
                print(f"Błąd konfiguracji API: {e}")
                self.root.after(100, self.show_api_key_dialog)
    
    def load_api_key_from_config(self):
        """Ładuje klucz API z pliku konfiguracyjnego"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                    return config.get('gemini_api_key', '')
        except Exception as e:
            print(f"Błąd odczytu pliku konfiguracyjnego: {e}")
        return None
    
    def save_api_key_to_config(self, api_key):
        """Zapisuje klucz API do pliku konfiguracyjnego"""
        try:
            config = {}
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
            
            config['gemini_api_key'] = api_key
            
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            print("Klucz API zapisany w pliku konfiguracyjnym.")
        except Exception as e:
            print(f"Błąd zapisu pliku konfiguracyjnego: {e}")
    
    def show_api_key_dialog(self):
        """Pokazuje okno dialogowe do wprowadzenia klucza API"""
        api_window = tk.Toplevel(self.root)
        api_window.title("Konfiguracja API")
        api_window.geometry("600x300")
        api_window.resizable(False, False)
        
        # Wyśrodkowanie okna
        api_window.transient(self.root)
        api_window.grab_set()
        
        # Wyśrodkowanie na ekranie
        api_window.update_idletasks()
        x = (api_window.winfo_screenwidth() // 2) - (api_window.winfo_width() // 2)
        y = (api_window.winfo_screenheight() // 2) - (api_window.winfo_height() // 2)
        api_window.geometry(f"+{x}+{y}")
        
        # Główna ramka
        main_frame = ttk.Frame(api_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(main_frame, text="Wprowadź klucz API Google Gemini:", 
                 font=('Arial', 12)).pack(pady=(0, 10))
        
        # Informacja o tym, jak uzyskać klucz
        info_text = """Aby uzyskać klucz API:
1. Idź na https://makersuite.google.com/app/apikey
2. Zaloguj się do Google AI Studio
3. Kliknij "Create API Key"
4. Skopiuj wygenerowany klucz"""
        
        ttk.Label(main_frame, text=info_text, 
                 font=('Arial', 9), foreground="gray").pack(pady=(0, 20))
        
        api_entry = ttk.Entry(main_frame, width=70, show="*")
        api_entry.pack(pady=(0, 10))
        
        # Checkbox do zapamiętania klucza
        remember_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Zapamiętaj klucz API (zapisz w pliku konfiguracyjnym)", 
                       variable=remember_var).pack(pady=(0, 20))
        
        button_frame = ttk.Frame(main_frame)
        button_frame.pack()
        
        def save_api_key():
            key = api_entry.get().strip()
            if key:
                self.api_key = key
                try:
                    genai.configure(api_key=key)
                    
                    # Zapisz klucz jeśli użytkownik chce
                    if remember_var.get():
                        self.save_api_key_to_config(key)
                    
                    api_window.destroy()
                    print("Klucz API skonfigurowany pomyślnie.")
                except Exception as e:
                    messagebox.showerror("Błąd", f"Nieprawidłowy klucz API: {e}")
            else:
                messagebox.showerror("Błąd", "Klucz API nie może być pusty!")
        
        def cancel():
            api_window.destroy()
            print("Anulowano konfigurację API. Aplikacja może nie działać poprawnie.")
        
        ttk.Button(button_frame, text="Zapisz", command=save_api_key).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="Anuluj", command=cancel).pack(side=tk.LEFT)
        
        # Focus na pole wejściowe
        api_entry.focus_set()
        
        # Bind Enter key
        api_entry.bind('<Return>', lambda e: save_api_key())
        
        # Pokaż okno na wierzchu
        api_window.lift()
        api_window.attributes('-topmost', True)
        api_window.attributes('-topmost', False)
    
    def setup_hotkey(self):
        """Konfiguracja globalnego skrótu klawiszowego"""
        def hotkey_callback():
            self.root.after(0, self.toggle_window)
        
        try:
            keyboard.add_hotkey('ctrl+alt+p', hotkey_callback)
            print("Aplikacja działa. Naciśnij Ctrl+Alt+P aby pokazać/ukryć okno.")
        except Exception as e:
            print(f"Błąd podczas konfiguracji skrótu: {e}")
    
    def toggle_window(self):
        """Przełącza widoczność okna (pokazuje/ukrywa)"""
        if self.window_visible and self.dialog_window and self.dialog_window.winfo_exists():
            # Ukryj okno
            self.hide_window()
        else:
            # Pokaż okno
            self.show_window()
    
    def show_window(self):
        """Pokazuje okno dialogowe"""
        if self.dialog_window and self.dialog_window.winfo_exists():
            # Jeśli okno już istnieje, po prostu je pokaż
            self.dialog_window.deiconify()
            self.dialog_window.lift()
            self.dialog_window.attributes('-topmost', True)
            self.dialog_window.attributes('-topmost', False)
        else:
            # Stwórz nowe okno
            self.create_window()
        
        self.window_visible = True
    
    def hide_window(self):
        """Ukrywa okno"""
        if self.dialog_window and self.dialog_window.winfo_exists():
            self.dialog_window.withdraw()
        self.window_visible = False
    
    def create_window(self):
        """Tworzy nowe okno dialogowe"""
        self.dialog_window = tk.Toplevel(self.root)
        self.dialog_window.title("Ulepszacz Promptów - Gemini AI")
        self.dialog_window.geometry("800x600")
        self.dialog_window.resizable(True, True)
        
        # Wyśrodkowanie okna
        self.dialog_window.update_idletasks()
        x = (self.dialog_window.winfo_screenwidth() // 2) - (self.dialog_window.winfo_width() // 2)
        y = (self.dialog_window.winfo_screenheight() // 2) - (self.dialog_window.winfo_height() // 2)
        self.dialog_window.geometry(f"+{x}+{y}")
        
        # Obsługa zamykania okna (ukryj zamiast zamknij)
        self.dialog_window.protocol("WM_DELETE_WINDOW", self.hide_window)
        
        # Skrót klawiszowy Escape do ukrycia okna
        self.dialog_window.bind('<Escape>', lambda e: self.hide_window())
        
        # Główny frame
        main_frame = ttk.Frame(self.dialog_window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Konfiguracja grid
        self.dialog_window.columnconfigure(0, weight=1)
        self.dialog_window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        # Etykieta i pole do wprowadzenia prompta
        ttk.Label(main_frame, text="Wprowadź prompt do ulepszenia:", 
                 font=('Arial', 12, 'bold')).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))
        
        self.input_text = scrolledtext.ScrolledText(main_frame, height=8, width=80,
                                                   font=('Arial', 10))
        self.input_text.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Ramka dla przycisków
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=10)
        
        # Przycisk ulepszania
        self.enhance_button = ttk.Button(button_frame, text="Ulepsz Prompt", 
                                        command=self.enhance_prompt)
        self.enhance_button.pack(side=tk.LEFT, padx=(0, 10))
        
        # Przycisk wklejania ze schowka
        ttk.Button(button_frame, text="Wklej ze schowka", 
                  command=self.paste_from_clipboard).pack(side=tk.LEFT, padx=(0, 10))
        
        # Przycisk czyszczenia
        ttk.Button(button_frame, text="Wyczyść", 
                  command=self.clear_input).pack(side=tk.LEFT, padx=(0, 10))
        
        # Przycisk ukrycia okna
        ttk.Button(button_frame, text="Ukryj", 
                  command=self.hide_window).pack(side=tk.LEFT)
        
        # Etykieta i pole dla ulepszonego prompta
        ttk.Label(main_frame, text="Ulepszony prompt:", 
                 font=('Arial', 12, 'bold')).grid(row=3, column=0, sticky=tk.W, pady=(20, 5))
        
        self.output_text = scrolledtext.ScrolledText(main_frame, height=8, width=80,
                                                    font=('Arial', 10))
        self.output_text.grid(row=4, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Ramka dla przycisków wyjściowych
        output_button_frame = ttk.Frame(main_frame)
        output_button_frame.grid(row=5, column=0, pady=10, sticky=tk.N)
        
        # Przycisk kopiowania
        ttk.Button(output_button_frame, text="Kopiuj do schowka", 
                  command=self.copy_to_clipboard).pack(side=tk.LEFT, padx=(0, 10))
        
        # Przycisk konfiguracji API
        ttk.Button(output_button_frame, text="Konfiguruj API", 
                  command=self.show_api_key_dialog).pack(side=tk.LEFT, padx=(0, 10))
        
        # Przycisk zamknięcia aplikacji
        ttk.Button(output_button_frame, text="Zamknij aplikację", 
                  command=self.quit_application).pack(side=tk.LEFT)
        
        # Pasek postępu
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=6, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        
        # Ustawienie focus na pole wejściowe
        self.input_text.focus_set()
        
        # Automatyczne wklejenie z schowka
        self.paste_from_clipboard()
        
        # Pokaż okno na wierzchu
        self.dialog_window.lift()
        self.dialog_window.attributes('-topmost', True)
        self.dialog_window.attributes('-topmost', False)
    
    def quit_application(self):
        """Całkowite zamknięcie aplikacji"""
        if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz zamknąć aplikację?"):
            self.root.quit()
            self.root.destroy()
            sys.exit(0)
    
    def paste_from_clipboard(self):
        """Wkleja tekst ze schowka do pola wejściowego"""
        try:
            clipboard_text = pyperclip.paste()
            if clipboard_text and hasattr(self, 'input_text'):
                self.input_text.delete(1.0, tk.END)
                self.input_text.insert(1.0, clipboard_text)
        except Exception as e:
            if hasattr(self, 'dialog_window') and self.dialog_window:
                messagebox.showerror("Błąd", f"Nie można wkleić ze schowka: {e}")
    
    def clear_input(self):
        """Czyści pole wejściowe"""
        if hasattr(self, 'input_text'):
            self.input_text.delete(1.0, tk.END)
    
    def copy_to_clipboard(self):
        """Kopiuje ulepszony prompt do schowka"""
        try:
            if hasattr(self, 'output_text'):
                enhanced_text = self.output_text.get(1.0, tk.END).strip()
                if enhanced_text:
                    pyperclip.copy(enhanced_text)
                    messagebox.showinfo("Sukces", "Ulepszony prompt został skopiowany do schowka!")
                else:
                    messagebox.showwarning("Ostrzeżenie", "Brak tekstu do skopiowania.")
        except Exception as e:
            messagebox.showerror("Błąd", f"Nie można skopiować do schowka: {e}")
    
    def enhance_prompt(self):
        """Ulepsza prompt za pomocą Gemini AI"""
        if not hasattr(self, 'input_text'):
            return
            
        input_prompt = self.input_text.get(1.0, tk.END).strip()
        
        if not input_prompt:
            messagebox.showwarning("Ostrzeżenie", "Wprowadź prompt do ulepszenia!")
            return
        
        if not self.api_key:
            messagebox.showerror("Błąd", "Brak klucza API Gemini! Kliknij 'Konfiguruj API'")
            return
        
        # Rozpoczęcie animacji paska postępu
        self.progress.start()
        self.enhance_button.config(state='disabled')
        
        # Uruchomienie w osobnym wątku
        threading.Thread(target=self._enhance_prompt_thread, args=(input_prompt,), daemon=True).start()
    
    def _enhance_prompt_thread(self, input_prompt):
        """Funkcja do ulepszania prompta w osobnym wątku"""
        try:
            # Konfiguracja modelu - używamy gemini-2.0-flash (free tier)
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            # Prompt systemowy do ulepszania
            system_prompt = """
            Ulepsz poniższy prompt dla AI, aby był bardziej precyzyjny i dawał lepsze rezultaty.
            
            ZASADY ULEPSZANIA:
            - Dodaj konkretne szczegóły i kontekst
            - Strukturyzuj instrukcje w logiczną kolejność
            - Unikaj zbędnych słów i powtórzeń
            - Zachowaj oryginalny język tekstu
            - Dodaj przykłady jeśli to pomoże
            - Określ format oczekiwanej odpowiedzi
            
            ZWRÓĆ TYLKO ULEPSZONY PROMPT, BEZ DODATKOWYCH KOMENTARZY.
            
            Prompt do ulepszenia:
            """
            
            full_prompt = f"{system_prompt}\n\n{input_prompt}"
            
            # Wysłanie zapytania do API
            response = model.generate_content(full_prompt)
            enhanced_prompt = response.text
            
            # Aktualizacja GUI w głównym wątku
            self.root.after(0, self._update_output, enhanced_prompt)
            
        except Exception as e:
            error_msg = f"Błąd podczas ulepszania prompta: {str(e)}"
            self.root.after(0, self._show_error, error_msg)
    
    def _update_output(self, enhanced_prompt):
        """Aktualizuje pole wyjściowe z ulepszonym promptem"""
        if hasattr(self, 'output_text'):
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(1.0, enhanced_prompt)
            
            # Zatrzymanie paska postępu
            self.progress.stop()
            self.enhance_button.config(state='normal')
            
            # Automatyczne kopiowanie do schowka
            pyperclip.copy(enhanced_prompt)
            messagebox.showinfo("Sukces", "Prompt został ulepszony i skopiowany do schowka!")
    
    def _show_error(self, error_msg):
        """Pokazuje komunikat o błędzie"""
        if hasattr(self, 'progress') and hasattr(self, 'enhance_button'):
            self.progress.stop()
            self.enhance_button.config(state='normal')
        messagebox.showerror("Błąd", error_msg)
    
    def run(self):
        """Uruchamia aplikację"""
        print("Aplikacja Ulepszacz Promptów uruchomiona!")
        print("Naciśnij Ctrl+Alt+P aby pokazać/ukryć okno.")
        print("Naciśnij Ctrl+C aby zakończyć aplikację.")
        
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            print("\nAplikacja została zakończona.")
            sys.exit(0)

def main():
    app = PromptEnhancerApp()
    app.run()

if __name__ == "__main__":
    main()