import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os

class Pasien:
    def _init_(self, nama, keluhan):
        self.nama = nama
        self.keluhan = keluhan

    def edit_data(self, nama_baru, keluhan_baru):
        self.nama = nama_baru
        self.keluhan = keluhan_baru


class ManajerAntrian:
    def _init_(self):
        self.queue = []
        self.history = []
        self.filepath = "data_pasien.json"
        self.load_data()

    def save_data(self):
        data = [{"nama": p.nama, "keluhan": p.keluhan} for p in self.queue]
        with open(self.filepath, "w") as f:
            json.dump(data, f, indent=4)

    def load_data(self):
        if not os.path.exists(self.filepath):
            return
        with open(self.filepath, "r") as f:
            data = json.load(f)
            for item in data:
                self.queue.append(Pasien(item["nama"], item["keluhan"]))

    def tambah_pasien(self, nama, keluhan):
        pasien = Pasien(nama, keluhan)
        self.queue.append(pasien)
        self.save_data()

    def panggil_pasien(self):
        if not self.queue:
            return None
        pasien = self.queue.pop(0)
        self.history.append(pasien)
        self.save_data()
        return pasien

    def edit_pasien(self, index, nama_baru, keluhan_baru):
        if 0 <= index < len(self.queue):
            self.queue[index].edit_data(nama_baru, keluhan_baru)
            self.save_data()

    def daftar(self):
        return self.queue


class AplikasiKlinik:
    def _init_(self, root):
        self.root = root
        self.root.title("Manajemen Antrian Klinik")

        self.manajer = ManajerAntrian()
        self.dark = False

        self.light_theme = {
            "bg": "#F0F0F0",
            "panel": "#FFFFFF",
            "btn": "#D9D9D9",
            "fg": "#000000"
        }

        self.dark_theme = {
            "bg": "#1F1F1F",
            "panel": "#2C2C2C",
            "btn": "#3D3D3D",
            "fg": "#FFFFFF"
        }

        # Panel kiri
        self.left_frame = tk.Frame(root, width=270, height=400)
        self.left_frame.pack(side="left", fill="y")

        tk.Label(self.left_frame, text="Nama Pasien:", font=("Poppins", 11, "bold")).pack(pady=6)
        self.entry_nama = tk.Entry(self.left_frame, width=26, font=("Poppins", 10))
        self.entry_nama.pack(pady=3)

        tk.Label(self.left_frame, text="Keluhan:", font=("Poppins", 11, "bold")).pack(pady=6)
        self.entry_keluhan = tk.Entry(self.left_frame, width=26, font=("Poppins", 10))
        self.entry_keluhan.pack(pady=3)

        self.btn_tambah = tk.Button(self.left_frame, text="+ Tambah Pasien", width=20, command=self.tambah_pasien)
        self.btn_tambah.pack(pady=10)

        self.btn_edit = tk.Button(self.left_frame, text="Edit Data", width=20, command=self.edit_pasien)
        self.btn_edit.pack(pady=5)

        self.btn_panggil = tk.Button(self.left_frame, text="Panggil Pasien", width=20, command=self.panggil_pasien)
        self.btn_panggil.pack(pady=5)

        self.btn_tema = tk.Button(self.left_frame, text="Ganti Tema", width=20, command=self.ganti_tema)
        self.btn_tema.pack(pady=20)

        # Panel kanan
        self.right_frame = tk.Frame(root)
        self.right_frame.pack(side="right", fill="both", expand=True)

        tk.Label(self.right_frame, text="Daftar Antrian Pasien",
                 font=("Poppins", 14, "bold")).pack(pady=12)

        self.listbox = tk.Listbox(
            self.right_frame, width=50, height=18, font=("Poppins", 11),
            activestyle="dotbox"
        )
        self.listbox.pack(padx=10, pady=5)

        self.apply_theme()
        self.update_list()
        self.warning_antrian_panjang()

    def apply_theme(self):
        tema = self.dark_theme if self.dark else self.light_theme

        self.root.config(bg=tema["bg"])
        self.left_frame.config(bg=tema["panel"])
        self.right_frame.config(bg=tema["panel"])

        buttons = [self.btn_tambah, self.btn_edit, self.btn_panggil, self.btn_tema]

        for btn in buttons:
            btn.config(bg=tema["btn"], fg=tema["fg"], relief="flat")

        self.entry_nama.config(bg="#FFFFFF", fg="#000000")
        self.entry_keluhan.config(bg="#FFFFFF", fg="#000000")
        self.listbox.config(bg="#FFFFFF", fg="#000000")

        for frame in [self.left_frame, self.right_frame]:
            for child in frame.winfo_children():
                if isinstance(child, tk.Label):
                    child.config(bg=tema["panel"], fg=tema["fg"])

    def ganti_tema(self):
        self.dark = not self.dark
        self.apply_theme()

    def tambah_pasien(self):
        nama = self.entry_nama.get()
        keluhan = self.entry_keluhan.get()

        if not nama or not keluhan:
            messagebox.showwarning("Peringatan", "Nama dan keluhan harus diisi.")
            return

        self.manajer.tambah_pasien(nama, keluhan)
        self.entry_nama.delete(0, tk.END)
        self.entry_keluhan.delete(0, tk.END)
        self.update_list()

    def panggil_pasien(self):
        pasien = self.manajer.panggil_pasien()

        if pasien:
            messagebox.showinfo("Pasien Dipanggil", f"Nama: {pasien.nama}\nKeluhan: {pasien.keluhan}")
        else:
            messagebox.showinfo("Info", "Antrian kosong.")

        self.update_list()

    def edit_pasien(self):
        try:
            idx = self.listbox.curselection()[0]
        except:
            messagebox.showwarning("Peringatan", "Pilih pasien yang ingin diedit.")
            return

        pasien = self.manajer.daftar()[idx]

        nama_baru = simpledialog.askstring("Edit Nama", "Nama baru:", initialvalue=pasien.nama)
        keluhan_baru = simpledialog.askstring("Edit Keluhan", "Keluhan baru:", initialvalue=pasien.keluhan)

        if nama_baru and keluhan_baru:
            self.manajer.edit_pasien(idx, nama_baru, keluhan_baru)
            self.update_list()

    def update_list(self):
        self.listbox.delete(0, tk.END)
        for i, p in enumerate(self.manajer.daftar()):
            self.listbox.insert(tk.END, f"{i+1}. {p.nama} | {p.keluhan}")

    def warning_antrian_panjang(self):
        if len(self.manajer.daftar()) >= 6:
            messagebox.showwarning("Warning", "Antrian sudah lebih dari 6 pasien!")
        self.root.after(7000, self.warning_antrian_panjang)


if _name_ == "_main_":
    root = tk.Tk()
    app = AplikasiKlinik(root)
    root.mainloop()
