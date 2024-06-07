import tkinter as tk
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import subprocess
import shutil
import os



class BareboneBuilder:
    def __init__(self, root):
        self.root = root
        self.root.title("Barebone Builder")

        # Janela amarela
        self.root.configure(bg='yellow')

        # Área de texto
        self.text_area = tk.Text(self.root, height=10, width=50)
        self.text_area.pack(pady=10)

        # Botões
        self.build_button = tk.Button(self.root, text="open", command=self.build_kernel)
        self.build_button.pack(pady=5)

        self.run_button = tk.Button(self.root, text="copy", command=self.run_kernel)
        self.run_button.pack(pady=5)

        self.copy_button = tk.Button(self.root, text="unmount", command=self.copy_file)
        self.copy_button.pack(pady=5)

    def execute_command(self, command,show:bool):
        try:
            
            result = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True, text=True)
            self.text_area.insert(tk.END, result)
        except subprocess.CalledProcessError as e:
            if show:
                self.text_area.insert(tk.END,f"Error executing command:\n{e.output}")

    def build_kernel(self):#filename = tk.filedialog.askdirectory(title="Select folder to build")
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END,f"open image")
        filename = tk.filedialog.askopenfilename(title="Select file")
        self.execute_command("mkdir /mnt/isos",False)
        self.execute_command("sudo chmod 777 /mnt/isos",False)
        self.execute_command('sudo mount "$filename" /mnt/isos -o loop'.replace("$filename",filename),True)
        
    def run_kernel(self):
        self.text_area.delete(1.0, tk.END)
        filename = tk.filedialog.asksaveasfilename(title="save file")
        if 0==0:
            self.execute_command("find /mnt/isos | cpio  -ov -H tar > $filename".replace("$filename",filename),True)
            self.execute_command("chmod 777 $filename".replace("$filename",filename),True)
       
        


    def copy_file(self):
        self.text_area.delete(1.0, tk.END)
        
        if 0==0:
            self.execute_command("sudo umount /mnt/isos",True)
            


if __name__ == "__main__":
    root = tk.Tk()
    builder = BareboneBuilder(root)
    root.mainloop()
