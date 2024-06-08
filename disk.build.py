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
        self.build_button = tk.Button(self.root, text="Build", command=self.build_kernel)
        self.build_button.pack(pady=5)

        self.run_button = tk.Button(self.root, text="mount", command=self.run_kernel)
        self.run_button.pack(pady=5)

        self.copy_button = tk.Button(self.root, text="run", command=self.copy_file)
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
        f1=open("f1","w")
        
        f1.close()
        self.text_area.insert(tk.END,f"writing 150 mega...")
        self.execute_command('dd if=/dev/zero of="my.img" bs=1M count=150',True)
        self.execute_command('sudo mkfs.vfat "./my.img"  ',True)
        self.execute_command('sudo chmod 777 "my.img"',True)
        self.execute_command('sudo chmod 777 "f1"',True)
        
    def run_kernel(self):
        self.text_area.delete(1.0, tk.END)
        self.execute_command("mkdir /mnt/isos",False)
        self.execute_command("sudo chmod 777 my.img",False)
        self.execute_command("sudo chmod 777 /mnt/isos",False)
        self.execute_command("sudo umount /mnt/isos",False)
        self.execute_command('sudo mount ./my.img /mnt/isos -o loop=/dev/loop1 -t vfat   ',True)
        self.execute_command("unzip -u ./file/CD_root.zip -d /mnt/isos",False)
 
        self.execute_command('cp ./vmlinuz /mnt/isos/boot',True)
        self.execute_command('cp ./image.gz /mnt/isos/boot',True)
        self.execute_command('cp ./file/syslinux.cfg /mnt/isos/boot/syslinux',True)
        
        self.execute_command('sudo syslinux /dev/loop1',True)
 
        #self.execute_command("nautilus --browser /mnt/isos",False)
        self.execute_command("sudo umount /mnt/isos",True)
        

    def copy_file(self):
        self.text_area.delete(1.0, tk.END)
        
        if 0==0:
            self.execute_command("qemu-system-i386 -boot c -hda my.img",True)
            


if __name__ == "__main__":
    root = tk.Tk()
    builder = BareboneBuilder(root)
    root.mainloop()
