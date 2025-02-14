from tkinter import Tk, Listbox, Button, filedialog, END, Frame, Scrollbar
from PyPDF2 import PdfMerger

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Merger")
        self.root.geometry("475x260")

        frame = Frame(root)
        frame.pack(pady=5)

        scrollbar = Scrollbar(frame, orient="vertical")
        self.file_list = Listbox(frame, selectmode='single', width=50, height=10, font=("Arial", 12), yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.file_list.yview)

        self.file_list.pack(side="left", fill="y")
        scrollbar.pack(side="right", fill="y")

        button_frame = Frame(root)
        button_frame.pack(pady=5)

        Button(button_frame, text="Dodaj pliki", command=self.add_files, font=("Arial", 12), padx=10, pady=5).grid(row=0, column=0, padx=3)
        Button(button_frame, text="Usuń plik", command=self.remove_file, font=("Arial", 12), padx=10, pady=5).grid(row=0, column=1, padx=3)
        Button(button_frame, text="Góra", command=self.move_up, font=("Arial", 12), padx=10, pady=5).grid(row=0, column=2, padx=3)
        Button(button_frame, text="Dół", command=self.move_down, font=("Arial", 12), padx=10, pady=5).grid(row=0, column=3, padx=3)
        Button(button_frame, text="Scal PDF", command=self.merge_pdfs, font=("Arial", 12), padx=10, pady=5).grid(row=0, column=4, padx=3)

        self.files = []

    def add_files(self):
        new_files = filedialog.askopenfilenames(filetypes=[("PDF files", "*.pdf")])
        for file in new_files:
            self.files.append(file)
            self.file_list.insert(END, file)

    def remove_file(self):
        selected = self.file_list.curselection()
        if selected:
            index = selected[0]
            self.file_list.delete(index)
            self.files.pop(index)

    def move_up(self):
        selected = self.file_list.curselection()
        if selected and selected[0] > 0:
            index = selected[0]
            item = self.files.pop(index)
            self.files.insert(index - 1, item)
            self.file_list.delete(index)
            self.file_list.insert(index - 1, item)
            self.file_list.select_set(index - 1)
            self.file_list.yview(index - 1)

    def move_down(self):
        selected = self.file_list.curselection()
        if selected and selected[0] < len(self.files) - 1:
            index = selected[0]
            item = self.files.pop(index)
            self.files.insert(index + 1, item)
            self.file_list.delete(index)
            self.file_list.insert(index + 1, item)
            self.file_list.select_set(index + 1)
            self.file_list.yview(index + 1)

    def merge_pdfs(self):
        if not self.files:
            return

        output_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if not output_path:
            return

        merger = PdfMerger()
        for pdf in self.files:
            merger.append(pdf)

        merger.write(output_path)
        merger.close()
        print(f"PDF zapisany jako: {output_path}")

if __name__ == "__main__":
    root = Tk()
    app = PDFMergerApp(root)
    root.mainloop()
