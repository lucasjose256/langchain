import customtkinter as ctk
from tkinter import filedialog

class TermoDeReferenciaFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.pack(fill="both", expand=True, padx=20, pady=20)
        self.create_widgets()

    def create_widgets(self):
        self.entry_objeto = ctk.CTkEntry(self, width=700, placeholder_text="Objeto da compra")
        self.entry_objeto.pack(pady=10)

        self.entry_justificativa = ctk.CTkTextbox(self, height=60, width=700)
        self.entry_justificativa.insert("1.0", "Justificativa...")
        self.entry_justificativa.pack(pady=5)

        self.entry_especificacoes = ctk.CTkTextbox(self, height=80, width=700)
        self.entry_especificacoes.insert("1.0", "Especificações técnicas...")
        self.entry_especificacoes.pack(pady=5)

        self.entry_base_legal = ctk.CTkTextbox(self, height=50, width=700)
        self.entry_base_legal.insert("1.0", "Base legal...")
        self.entry_base_legal.pack(pady=5)

        self.btn_gerar = ctk.CTkButton(self, text="Gerar Documento", command=self.gerar_documento)
        self.btn_gerar.pack(pady=10)

        self.btn_salvar = ctk.CTkButton(self, text="Salvar como .txt", command=self.salvar_como_txt)
        self.btn_salvar.pack()

        self.text_output = ctk.CTkTextbox(self, height=200, width=700)
        self.text_output.pack(pady=10)

    def gerar_documento(self):
        objeto = self.entry_objeto.get()
        justificativa = self.entry_justificativa.get("1.0", "end").strip()
        especificacoes = self.entry_especificacoes.get("1.0", "end").strip()
        base_legal = self.entry_base_legal.get("1.0", "end").strip()

        documento = f"""TERMO DE REFERÊNCIA

Objeto:
{objeto}

Justificativa:
{justificativa}

Especificações Técnicas:
{especificacoes}

Base Legal:
{base_legal}

__________________________________
Responsável Técnico
"""
        self.text_output.delete("1.0", "end")
        self.text_output.insert("1.0", documento)

    def salvar_como_txt(self):
        documento = self.text_output.get("1.0", "end")
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivo de texto", "*.txt")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(documento)
