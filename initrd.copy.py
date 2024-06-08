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
        f1=open("f1","w")
        f1.close() 
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END,f"open image")
        filename = tk.filedialog.askopenfilename(title="Select image1 build")
        self.execute_command('dd if=/dev/zero of="out.img" bs=1k count=63000',True)
        self.execute_command('sudo mkfs.vfat -S 4096 "out.img"  ',True)
        self.execute_command('sudo chmod 777 "out.img"',True)
        self.execute_command('sudo chmod 777 "f1"',True)
        self.execute_command("mkdir /mnt/isos",False)
        self.execute_command("mkdir /mnt/isos2",False)
        self.execute_command("sudo chmod 777 /mnt/isos",False)
        self.execute_command('sudo mount "$filename" /mnt/isos -o loop'.replace("$filename",filename),True)
        self.execute_command('sudo mount "out.img" /mnt/isos2 -o loop',True)
        self.execute_command('nautilus --browser /mnt/isos &',True)
        self.execute_command('nautilus --browser /mnt/isos2 &',True)
    def run_kernel(self):
        self.text_area.delete(1.0, tk.END)
        filename = tk.filedialog.askopenfilename(title="Select file to build")
        self.text_area.insert(tk.END,"wait....")
        if 0==0:
            self.execute_command('zip -e "$filename" /mnt/isos'.replace("$filename",filename),True)
        self.text_area.insert(tk.END,"end....")   
       
        


    def copy_file(self):
        self.text_area.delete(1.0, tk.END)
        
        
        if 0==0:
            self.execute_command("sudo umount /mnt/isos",True)
            self.execute_command("sudo umount /mnt/isos2",True)
            


if __name__ == "__main__":
    root = tk.Tk()
    builder = BareboneBuilder(root)
    root.mainloop()
