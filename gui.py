import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
from sistempakar import preprocess, Greetings, engine, get_details, get_treatments, Fact

class AplikasiDiagnosaPenyakitKulit:
    def __init__(self, root):
        self.root = root
        self.root.title("Aplikasi Diagnosa Penyakit Kulit")

        # preprocess()
        # self.engine = Greetings()

        self.inisialisasi_gui()

    def inisialisasi_gui(self):
        self.var_gejala = {
            "kulit_membengkak": tk.StringVar(),
            "benjolan_di_kulit": tk.StringVar(),
            "mengeluarkan_nanah": tk.StringVar(),
            "demam": tk.StringVar(),
            "mata_merah": tk.StringVar(),
            "kulit_kepala_berminyak": tk.StringVar(),
            "rasa_gatal": tk.StringVar(),
            "luka_dari_bagian_mulut": tk.StringVar(),
            "memiliki_gelembung_berisi_air": tk.StringVar(),
            "rasa_nyeri": tk.StringVar(),
            "kulit_melepuh": tk.StringVar(),
            "memiliki_bercak_bercak_merah": tk.StringVar(),
            "iritasi_kulit": tk.StringVar(),
            "uban_muncul_sebelum_waktunya": tk.StringVar(),
            "muncul_keringat_berlebihan": tk.StringVar(),
            "menimbulkan_warna_kekuningan": tk.StringVar(),
        }

        self.frame_utama = ttk.Frame(self.root, padding="20")
        self.frame_utama.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.buat_input_gejala()

        ttk.Button(self.frame_utama, text="Diagnosa", command=self.diagnosa).grid(column=0, row=17, columnspan=2, pady=10)

    def buat_input_gejala(self):
        ttk.Label(self.frame_utama, text="Silakan jawab 'yes' atau 'no' untuk setiap gejala:").grid(column=0, row=0, columnspan=2, pady=10)

        indeks_baris = 1
        for gejala, var in self.var_gejala.items():
            ttk.Label(self.frame_utama, text=gejala.replace("_", " ").capitalize() + ":").grid(column=0, row=indeks_baris, sticky=tk.W)
            ttk.Entry(self.frame_utama, textvariable=var).grid(column=1, row=indeks_baris, sticky=tk.W)
            indeks_baris += 1

    def diagnosa(self):
        gejala = [var.get() for var in self.var_gejala.values()]
        engine = Greetings()
        engine.reset()
        engine.declare(Fact(action='find_disease', **dict(zip(self.var_gejala.keys(), gejala))))
        engine.run()
        penyakit = engine.facts[-1].get("disease")

        if penyakit:
            self.tampilkan_hasil(penyakit)
        else:
            messagebox.showinfo("Tidak Cocok", "Tidak ditemukan penyakit yang cocok berdasarkan gejala yang diberikan.")

    def tampilkan_hasil(self, penyakit):
        detail = get_details(penyakit)
        pengobatan = get_treatments(penyakit)

        jendela_hasil = tk.Toplevel(self.root)
        jendela_hasil.title("Hasil Diagnosa")

        ttk.Label(jendela_hasil, text=f"Hasil Diagnosa: {penyakit}").grid(column=0, row=0, pady=10)

        path_gambar = f"./img/{penyakit}.jpg"
        try:
            img = Image.open(path_gambar)
            img = img.resize((300, 300), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            label = ttk.Label(jendela_hasil, image=img)
            label.image = img
            label.grid(column=0, row=1)
        except FileNotFoundError:
            ttk.Label(jendela_hasil, text="Gambar tidak ditemukan").grid(column=0, row=1)

        # ttk.Label(jendela_hasil, text="Deskripsi:").grid(column=0, row=2, pady=5)
        # ttk.Label(jendela_hasil, text=detail).grid(column=0, row=3, pady=5)

        # ttk.Label(jendela_hasil, text="Pengobatan:").grid(column=0, row=4, pady=5)
        # ttk.Label(jendela_hasil, text=pengobatan).grid(column=0, row=5, pady=5)

        

if __name__ == "__main__":
    preprocess()
    root = tk.Tk()
    app = AplikasiDiagnosaPenyakitKulit(root)
    root.mainloop()
