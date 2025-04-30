import customtkinter as ctk
import tkinter as tk
from datetime import datetime
from gerarDocumento import TermoDeReferenciaFrame

def get_bot_response(user_message):
    return f"Bot: Echoing your message - '{user_message}' (This is a placeholder response)"

class ChatApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chat Interface")
        self.root.geometry("800x700")
        
        # Configure CustomTkinter appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.main_frame.pack(padx=10, pady=10, fill="both", expand=True)
        
        # Chat display (scrollable text area)
        self.chat_display = ctk.CTkTextbox(
            self.main_frame,
            height=500,
            wrap="word",
            state="disabled",
            font=("Arial", 14)
        )
        self.chat_display.pack(padx=10, pady=(10, 5), fill="both", expand=True)
        
        # Input frame
        self.input_frame = ctk.CTkFrame(self.main_frame)
        self.input_frame.pack(padx=10, pady=5, fill="x")
        
        # Message entry
        self.message_entry = ctk.CTkEntry(
            self.input_frame,
            placeholder_text="Escreva sua mensagem...",
            height=40,
            font=("Arial", 14)
        )
        self.message_entry.pack(side="left", padx=(0, 5), pady=5, fill="x", expand=True)
        self.message_entry.bind("<Return>", self.send_message)
        
        # Send button
        self.send_button = ctk.CTkButton(
            self.input_frame,
            text="Send",
            width=100,
            height=40,
            command=self.send_message
        )
        self.send_button.pack(side="right", pady=5)
        
        # Initial welcome message
        self.add_message("Bot: Welcome to the chat! How can I assist you today?", is_bot=True)
        self.back_button = ctk.CTkButton(
                self.main_frame,
                text="Back",
                width=100,
                height=40,
                command=self.back_to_start
            )
        self.back_button.pack(pady=(10, 5), anchor="nw", padx=10)
    def back_to_start(self):
        """Close chat interface and open start screen."""
        self.root.destroy()  # Close chat window
        start_root = ctk.CTk()  # Create new root for start screen
        app = StartScreen(start_root)
        start_root.mainloop()

    def add_message(self, message, is_bot=False):
        """Add a message to the chat display."""
        self.chat_display.configure(state="normal")
        
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = "Bot" if is_bot else "You"
        formatted_message = f"[{timestamp}] {prefix}: {message}\n"
        
        self.chat_display.insert(tk.END, formatted_message)
        self.chat_display.see(tk.END)
        self.chat_display.configure(state="disabled")
    

    def send_message(self, event=None):
        """Handle sending a message."""
        user_message = self.message_entry.get().strip()
        if not user_message:
            return

        self.add_message(user_message, is_bot=False)
        
        self.message_entry.delete(0, tk.END)
        
        bot_response = get_bot_response(user_message)
        self.add_message(bot_response, is_bot=True)

# Start screen class
class StartScreen:
    def __init__(self, root):
        self.root = root
        self.root.title("Welcome")
        self.root.geometry("800x400")
        
        # Configure CustomTkinter appearance
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Create main frame
        self.main_frame = ctk.CTkFrame(self.root, corner_radius=10)
        self.main_frame.pack(padx=20, pady=20, fill="both", expand=True)
        
        # Welcome label
        self.welcome_label = ctk.CTkLabel(
            self.main_frame,
            text="Bem-vindo ao UTFPR.IA!",
            font=("Arial", 24, "bold")
        )
        self.welcome_label.pack(pady=20)

        self.AUX = ctk.CTkLabel(
        self.main_frame,
        text="Bem-vindodsadsadsadsa a UTFPR.IA!",
        font=("Arial", 24, "bold")
        )
        self.AUX.pack(pady=50)
        # Start button
        self.start_button = ctk.CTkButton(
            self.main_frame,
            text="Start Chatting",
            height=50,
            font=("Arial", 16),
            command=self.open_chat
        )
        self.start_button.pack(pady=20)
        self.document_button = ctk.CTkButton(
        self.main_frame,
        text="Gerar Termo de Referência",
        height=50,
        font=("Arial", 16),
        command=self.open_generateDocument)
        self.document_button.pack(pady=10)

    def open_generateDocument(self):
        self.root.destroy()
        chat_root=ctk.CTk()
        app=TermoDeReferenciaFrame(chat_root)
        chat_root.mainloop()
        
    def open_chat(self):
        """Close start screen and open chat interface."""
        self.root.destroy()  # Close start screen
        chat_root = ctk.CTk()  # Create new root for chat
        app = ChatApp(chat_root)
        chat_root.mainloop()

# Run the application
if __name__ == "__main__":
    root = ctk.CTk()
    app = StartScreen(root)
    root.mainloop()