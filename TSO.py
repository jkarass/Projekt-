import tkinter as tk
from tkinter import filedialog, Listbox, Scrollbar, SINGLE, END
import requests
import os

class FileEncryptionApp:
    def __init__(self, root):
        self.root = root
        self.root.title("File Encryption App")

        self.file_path_label = tk.Label(root, text="Selected File: None")
        self.file_path_label.pack(pady=10)

        self.browse_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.browse_button.pack(pady=10)

        self.upload_button = tk.Button(root, text="Upload and Encrypt", command=self.upload_and_encrypt)
        self.upload_button.pack(pady=10)

        self.download_button = tk.Button(root, text="Download and Decrypt", command=self.download_and_decrypt)
        self.download_button.pack(pady=10)

        self.delete_button = tk.Button(root, text="Delete Selected", command=self.delete_selected_file)
        self.delete_button.pack(pady=10)

        self.file_listbox = Listbox(root, selectmode=SINGLE, width=50)
        self.file_listbox.pack(pady=10)

        self.refresh_button = tk.Button(root, text="Refresh File List", command=self.refresh_file_list)
        self.refresh_button.pack(pady=10)

    def browse_file(self):
        file_path = filedialog.askopenfilename()
        self.file_path_label.config(text="Selected File: " + file_path)
        self.selected_file_path = file_path

    def upload_and_encrypt(self):
        if hasattr(self, 'selected_file_path'):
            files = {'file': open(self.selected_file_path, 'rb')}
            try:
                response = requests.post('http://127.0.0.1:5000/upload', files=files)
                response.raise_for_status()
                print(response.text)
                self.refresh_file_list()  
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
        else:
            print("No file selected")

    def download_and_decrypt(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_file = self.file_listbox.get(selected_index)
            try:
                response = requests.get(f'http://127.0.0.1:5000/download/{selected_file}', stream=True)
                response.raise_for_status()

                save_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
                with open(save_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=128):
                        f.write(chunk)
                print(f"File saved to {save_path}")
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
        else:
            print("No file selected")

    def delete_selected_file(self):
        selected_index = self.file_listbox.curselection()
        if selected_index:
            selected_file = self.file_listbox.get(selected_index)
            try:
                response = requests.delete(f'http://127.0.0.1:5000/delete/{selected_file}')
                response.raise_for_status()
                print(response.text)
                self.refresh_file_list() 
            except requests.exceptions.RequestException as e:
                print(f"Error: {e}")
        else:
            print("No file selected")

    def refresh_file_list(self):
        try:
            response = requests.get('http://127.0.0.1:5000/browse')
            response.raise_for_status()
            file_list = response.json()

            self.file_listbox.delete(0, END)
            for file_name in file_list:
                self.file_listbox.insert(END, file_name)
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    root = tk.Tk()
    app = FileEncryptionApp(root)
    root.mainloop()
