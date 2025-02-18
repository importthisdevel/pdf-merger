import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PyPDF2 import PdfMerger
import os

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Unir PDFs")
        self.root.geometry("500x300")

        # Variables
        self.selected_files = []

        # Interfaz gráfica
        self.create_widgets()

    def create_widgets(self):
        # Botón para seleccionar archivos
        tk.Button(self.root, text="Seleccionar PDFs", command=self.select_files).pack(pady=10)

        # Lista de archivos seleccionados
        self.file_listbox = tk.Listbox(self.root, selectmode=tk.MULTIPLE, width=50, height=5)
        self.file_listbox.pack(pady=10)

        # Barra de progreso
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack(pady=10)

        # Botón para unir PDFs
        tk.Button(self.root, text="Unir PDFs", command=self.merge_pdfs).pack(pady=10)

        # Menú "Acerca de"
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de", command=self.show_about)

    def select_files(self):
        files = filedialog.askopenfilenames(title="Seleccionar PDFs", filetypes=[("PDF Files", "*.pdf")])
        if files:
            self.selected_files = list(files)
            self.file_listbox.delete(0, tk.END)
            for file in self.selected_files:
                self.file_listbox.insert(tk.END, os.path.basename(file))

    def merge_pdfs(self):
        if not self.selected_files:
            messagebox.showwarning("Advertencia", "Selecciona al menos un archivo PDF.")
            return

        # Preguntar dónde guardar el archivo resultante
        output_file = filedialog.asksaveasfilename(
            title="Guardar PDF unido como",
            defaultextension=".pdf",
            filetypes=[("PDF Files", "*.pdf")]
        )

        if not output_file:  # Si el usuario cancela
            return

        merger = PdfMerger()
        total_files = len(self.selected_files)
        self.progress["maximum"] = total_files

        try:
            for i, file in enumerate(self.selected_files):
                merger.append(file)
                self.progress["value"] = i + 1
                self.root.update_idletasks()

            with open(output_file, "wb") as out_file:
                merger.write(out_file)

            messagebox.showinfo("Éxito", f"PDFs unidos correctamente en {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")
        finally:
            merger.close()
            self.progress["value"] = 0

    def show_about(self):
        messagebox.showinfo("Acerca de", "Unir PDFs v1.0\nCreado con Python, tkinter y PyPDF2.")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
