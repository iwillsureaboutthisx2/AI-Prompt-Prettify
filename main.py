# Copyright © 2025 KPZsProductions
# All rights reserved.
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

# --- ToolTip class for tooltips ---
class ToolTip:
    def __init__(self, widget, text):
        self.widget = widget
        self.text = text
        self.tipwindow = None
        widget.bind("<Enter>", self.show_tip)
        widget.bind("<Leave>", self.hide_tip)

    def show_tip(self, event=None):
        if self.tipwindow or not self.text:
            return
        x, y, _, cy = self.widget.bbox("insert") if hasattr(self.widget, 'bbox') else (0,0,0,0)
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tipwindow = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)
        tw.wm_geometry(f"+{x}+{y}")
        label = tk.Label(tw, text=self.text, background="#FFFFE0", relief="solid", borderwidth=1, font=("Segoe UI", 10))
        label.pack(ipadx=1)

    def hide_tip(self, event=None):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

class PromptEnhancerApp:
    def __init__(self):
        self.dialog_window = None
        self.api_key = None
        self.window_visible = False
        self.config_file = "config.json"
        
        # Stwórz ukryty root window
        self.root = tk.Tk()
        self.root.withdraw()  # Ukryj główne okno
        self.setup_styles()
        
        # Konfiguracja
        self.setup_api()
        self.setup_hotkey()
        self.root.after(500, self.show_intro)
    
    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TFrame', background='#F5F5F5')
        style.configure('TLabel', background='#F5F5F5', foreground='#212121', font=('Segoe UI', 12))
        style.configure('TButton', background='#2196F3', foreground='#FFFFFF', font=('Segoe UI', 11), padding=10)
        style.map('TButton', background=[('active', '#1976D2')])
        style.configure('TCheckbutton', background='#F5F5F5', foreground='#212121', font=('Segoe UI', 10))
    
    def show_intro(self):
        messagebox.showinfo(
            "Welcome!",
            "Welcome to the Gemini AI Prompt Enhancer!\n\n"
            "• Enter your prompt in the top field.\n"
            "• Click 'Enhance Prompt' to get a better version.\n"
            "• Use the buttons to copy, paste, or configure the API key.\n"
            "• Hover over elements to see tooltips."
        )
    
    def show_about_dialog(self):
        messagebox.showinfo(
            "About",
            "Gemini AI Prompt Enhancer\n"
            "Copyright © 2025 KPZsProductions\n"
            "All rights reserved."
        )
    
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
                if self.api_key:
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
        try:
            api_window = tk.Toplevel(self.root)
            api_window.title("API Configuration")
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
            
            ttk.Label(main_frame, text="Enter your Google Gemini API key:", 
                     font=('Arial', 12)).pack(pady=(0, 10))
            
            # Informacja o tym, jak uzyskać klucz
            info_text = """To get an API key:\n1. Go to https://makersuite.google.com/app/apikey\n2. Sign in to Google AI Studio\n3. Click 'Create API Key'\n4. Copy the generated key"""
            
            ttk.Label(main_frame, text=info_text, 
                     font=('Arial', 9), foreground="gray").pack(pady=(0, 20))
            
            api_entry = ttk.Entry(main_frame, width=70, show="*")
            api_entry.pack(pady=(0, 10))
            
            # Checkbox do zapamiętania klucza
            remember_var = tk.BooleanVar(value=True)
            ttk.Checkbutton(main_frame, text="Remember API key (save in config file)", 
                           variable=remember_var).pack(pady=(0, 20))
            
            button_frame = ttk.Frame(main_frame)
            button_frame.pack()
            
            def save_api_key():
                try:
                    key = api_entry.get().strip()
                    if key:
                        self.api_key = key
                        
                        # Konfiguracja Gemini API
                        genai.configure(api_key=key)
                        
                        # Zapisz klucz jeśli użytkownik chce
                        if remember_var.get():
                            self.save_api_key_to_config(key)
                        
                        api_window.destroy()
                        messagebox.showinfo("Success", "API key configured successfully!")
                        print("API key configured successfully.")
                    else:
                        messagebox.showerror("Error", "API key cannot be empty!")
                except Exception as e:
                    messagebox.showerror("Error", f"Error configuring API key: {e}")
            
            def cancel():
                api_window.destroy()
                print("API configuration cancelled. The application may not work properly.")
            
            ttk.Button(button_frame, text="Save", command=save_api_key).pack(side=tk.LEFT, padx=(0, 10))
            ttk.Button(button_frame, text="Cancel", command=cancel).pack(side=tk.LEFT)
            
            # Focus na pole wejściowe
            api_entry.focus_set()
            
            # Bind Enter key
            api_entry.bind('<Return>', lambda e: save_api_key())
            
            # Pokaż okno na wierzchu
            api_window.lift()
            api_window.attributes('-topmost', True)
            api_window.attributes('-topmost', False)
            
        except Exception as e:
            print(f"Error creating API dialog: {e}")
            messagebox.showerror("Error", f"Error creating API configuration dialog: {e}")
    
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
        self.dialog_window.title("Prompt Enhancer - Gemini AI")
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
        main_frame = ttk.Frame(self.dialog_window, padding="15")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Konfiguracja grid
        self.dialog_window.columnconfigure(0, weight=1)
        self.dialog_window.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        main_frame.rowconfigure(5, weight=1)
        
        # Etykieta i pole do wprowadzenia prompta
        ttk.Label(main_frame, text="Enter a prompt to enhance:", font=('Segoe UI', 13, 'bold')).grid(row=0, column=0, sticky="w", pady=(0, 5))
        self.input_text = scrolledtext.ScrolledText(main_frame, height=8, width=80, font=('Segoe UI', 11), bg="#FFFFFF", fg="#212121")
        self.input_text.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        ToolTip(self.input_text, "Enter your prompt here to enhance it.")
        
        # Ramka dla przycisków
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, pady=10)
        
        # Przycisk ulepszania
        self.enhance_button = ttk.Button(button_frame, text="Enhance Prompt", command=self.enhance_prompt)
        self.enhance_button.pack(side=tk.LEFT, padx=(0, 10))
        ToolTip(self.enhance_button, "Click to enhance your prompt using AI.")
        
        # Przycisk wklejania ze schowka
        self.paste_button = ttk.Button(button_frame, text="Paste from clipboard", command=self.paste_from_clipboard)
        self.paste_button.pack(side=tk.LEFT, padx=(0, 10))
        ToolTip(self.paste_button, "Click to paste text from the clipboard.")
        
        # Przycisk czyszczenia
        self.clear_button = ttk.Button(button_frame, text="Clear", command=self.clear_input)
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))
        ToolTip(self.clear_button, "Click to clear the input field.")
        
        # Przycisk ukrycia okna
        self.hide_button = ttk.Button(button_frame, text="Hide", command=self.hide_window)
        self.hide_button.pack(side=tk.LEFT)
        ToolTip(self.hide_button, "Click to hide the application window.")
        
        # Etykieta i pole dla ulepszonego prompta
        ttk.Label(main_frame, text="Enhanced prompt:", font=('Segoe UI', 13, 'bold')).grid(row=3, column=0, sticky="w", pady=(20, 5))
        self.output_text = scrolledtext.ScrolledText(main_frame, height=8, width=80, font=('Segoe UI', 11), bg="#FFFFFF", fg="#212121")
        self.output_text.grid(row=4, column=0, sticky="nsew", pady=(0, 10))
        ToolTip(self.output_text, "The enhanced prompt will appear here.")
        
        # Ramka dla przycisków wyjściowych
        output_button_frame = ttk.Frame(main_frame)
        output_button_frame.grid(row=5, column=0, pady=10, sticky="n")
        
        # Przycisk kopiowania
        self.copy_button = ttk.Button(output_button_frame, text="Copy to clipboard", command=self.copy_to_clipboard)
        self.copy_button.pack(side=tk.LEFT, padx=(0, 10))
        ToolTip(self.copy_button, "Click to copy the enhanced prompt.")
        

        
        # Przycisk zamknięcia aplikacji
        self.quit_button = ttk.Button(output_button_frame, text="Quit application", command=self.quit_application)
        self.quit_button.pack(side=tk.LEFT, padx=(0, 10))
        ToolTip(self.quit_button, "Click to quit the application.")
        
        # Przycisk O programie
        self.about_button = ttk.Button(output_button_frame, text="About", command=self.show_about_dialog)
        self.about_button.pack(side=tk.LEFT, padx=(0, 10))
        ToolTip(self.about_button, "Information about the author and copyright.")
        
        # Pasek postępu
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=6, column=0, sticky="we", pady=(10, 0))
        
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
        if messagebox.askyesno("Confirmation", "Are you sure you want to quit the application?"):
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
                messagebox.showerror("Error", f"Cannot paste from clipboard: {e}")
    
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
                    messagebox.showinfo("Success", "The enhanced prompt has been copied to the clipboard!")
                else:
                    messagebox.showwarning("Warning", "No text to copy.")
        except Exception as e:
            messagebox.showerror("Error", f"Cannot copy to clipboard: {e}")
    
    def enhance_prompt(self):
        """Ulepsza prompt za pomocą Gemini AI"""
        if not hasattr(self, 'input_text'):
            return
            
        input_prompt = self.input_text.get(1.0, tk.END).strip()
        
        if not input_prompt:
            messagebox.showwarning("Warning", "Enter a prompt to enhance!")
            return
        
        if not self.api_key:
            messagebox.showerror("Error", "No Gemini API key! Click 'Configure API'")
            return
        
        # Rozpoczęcie animacji paska postępu
        self.progress.start()
        self.enhance_button.config(state='disabled')
        
        # Uruchomienie w osobnym wątku
        threading.Thread(target=self._enhance_prompt_thread, args=(input_prompt,), daemon=True).start()
    
    def _enhance_prompt_thread(self, input_prompt):
        """Function to enhance prompt in a separate thread"""
        try:
            # Konfiguracja API (na wszelki wypadek)
            genai.configure(api_key=self.api_key)
            
            # System prompt for enhancement
            system_prompt = """
            Enhance the following prompt for AI to be more precise and provide better results.
            
            ENHANCEMENT RULES:
            - Add specific details and context
            - Structure instructions in a logical order
            - Avoid unnecessary words and repetitions
            - Maintain the original text language
            - Add examples if it helps
            - Specify the expected format of the response
            
            RETURN ONLY THE ENHANCED PROMPT, WITHOUT ADDITIONAL COMMENTS.
            
            Prompt to enhance:
            """
            
            full_prompt = f"{system_prompt}\n\n{input_prompt}"
            
            # Użyj poprawnej składni dla nowej wersji API
            model = genai.GenerativeModel('gemini-2.0-flash')
            response = model.generate_content(full_prompt)
            
            # Wyciągnij tekst z odpowiedzi
            enhanced_prompt = response.text
            
            # Update GUI in main thread
            self.root.after(0, self._update_output, enhanced_prompt)
            
        except Exception as e:
            error_msg = f"Error enhancing prompt: {str(e)}"
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
            messagebox.showinfo("Success", "The prompt has been enhanced and copied to the clipboard!")
    
    def _show_error(self, error_msg):
        """Pokazuje komunikat o błędzie"""
        if hasattr(self, 'progress') and hasattr(self, 'enhance_button'):
            self.progress.stop()
            self.enhance_button.config(state='normal')
        messagebox.showerror("Error", error_msg)
    
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