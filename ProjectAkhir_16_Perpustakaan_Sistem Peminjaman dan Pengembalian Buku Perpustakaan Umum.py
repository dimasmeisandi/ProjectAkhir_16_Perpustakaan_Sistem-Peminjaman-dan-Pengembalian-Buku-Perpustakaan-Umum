import datetime # untuk Menghitung jumlah hari keterlambatan dengan mengurangi batas waktu dari tanggal pengembalian.
from prettytable import PrettyTable  # untuk menampilkan data dalam bentuk tabel.

# Data awal
peminjaman_list = []
pengembalian_list = []

buku_list = [
    {"judul": "Laskar Pelangi", "jumlah": 5},
    {"judul": "Dilan", "jumlah": 3},
    {"judul": "Bumi Manusia", "jumlah": 2},
    {"judul": "Negeri 5 Menara", "jumlah": 6},
    {"judul": "Sang Pencinta Buku", "jumlah": 4},
    {"judul": "Hujan Bulan Juni", "jumlah": 2},
    {"judul": "Filosofi Kopi", "jumlah": 3},
    {"judul": "Sapiens", "jumlah": 2},
    {"judul": "Republik", "jumlah": 2},
    {"judul": "Sejagat Raya Singkat", "jumlah": 6},
    {"judul": "Interpretasi Mimpi", "jumlah": 7},
    {"judul": "Inovator", "jumlah": 4},
    {"judul": "7 Habits of Highly Effective People", "jumlah": 2},
    {"judul": "Tubuh Awet Muda Pikiran Abadi", "jumlah": 2},
    {"judul": "The Wealth of Nations", "jumlah": 2},
    {"judul": "Berpikir Cepat dan Lambat", "jumlah": 3},
]


def tampilkan_buku():
    print("\n--- Daftar Buku yang Tersedia ---")
    table = PrettyTable(["No", "Judul", "Jumlah"])
    for i, buku in enumerate(buku_list, start=1):
        table.add_row([i, buku['judul'], buku['jumlah']])
    print(table)


def tambah_buku():
    judul_baru = input("Masukkan judul buku baru: ")
    jumlah_baru = int(input("Masukkan jumlah buku: "))
    buku_list.append({"judul": judul_baru, "jumlah": jumlah_baru})
    print(f"Buku '{judul_baru}' berhasil ditambahkan dengan jumlah {jumlah_baru}.")


def tambah_peminjaman(id_peminjaman, nama_peminjam, judul_buku_list):
    # memeriksa ID duplikat
    if any(peminjaman[0] == id_peminjaman for peminjaman in peminjaman_list):
        print(f"ID peminjaman '{id_peminjaman}' sudah ada, mohon buat ID yang lain.")
        return False  

    tanggal_peminjaman = input("Masukkan tanggal peminjaman (YYYY-MM-DD): ")
    tanggal_peminjaman = datetime.datetime.strptime(tanggal_peminjaman, "%Y-%m-%d").date()
    batas_waktu = tanggal_peminjaman + datetime.timedelta(days=3)

    for judul_buku in judul_buku_list:  # Loop untuk setiap judul buku yang dipinjam
        found = False
        for buku in buku_list:  # mencari buku yang ingin dipinjam
            if buku['judul'].lower() == judul_buku.lower():
                if buku['jumlah'] > 0:
                    peminjaman = (id_peminjaman, nama_peminjam, judul_buku, tanggal_peminjaman, batas_waktu) 
                    peminjaman_list.append(peminjaman)
                    buku['jumlah'] -= 1
                    print(f"Peminjaman buku '{judul_buku}' berhasil ditambahkan.")
                    found = True
                else:
                    print(f"Buku '{judul_buku}' sudah habis.")
                break
        
        if not found:
            print(f"Buku '{judul_buku}' tidak ditemukan.")

    tampilkan_peminjaman()  


def tampilkan_peminjaman():
    print("\n--- Daftar Peminjaman Buku ---")
    if not peminjaman_list:
        print("Belum ada data peminjaman!")
        return
    

    # Dictionary untuk menyimpan peminjaman berdasarkan ID peminjaman
    peminjaman_dict = {}
    
    for peminjaman in peminjaman_list:
        id_peminjaman, nama_peminjam, judul_buku, tanggal_pinjam, batas_waktu = peminjaman
        if id_peminjaman not in peminjaman_dict:
            peminjaman_dict[id_peminjaman] = {
                "nama": nama_peminjam,
                "judul": [],
                "tanggal_pinjam": tanggal_pinjam,
                "batas_waktu": batas_waktu
            }
        peminjaman_dict[id_peminjaman]["judul"].append(judul_buku)
    
    # Menampilkan tabel
    table = PrettyTable(["ID", "Nama", "Judul Buku", "Tanggal Pinjam", "Batas Waktu"])
    for id_peminjaman, data in peminjaman_dict.items():
        judul_buku_str = ", ".join(data["judul"])  # Menggabungkan judul buku
        table.add_row([id_peminjaman, data["nama"], judul_buku_str, data["tanggal_pinjam"], data["batas_waktu"]])
    
    print(table)



def update_peminjaman(id_peminjaman, nama_baru, judul_baru):
    for i in range(len(peminjaman_list)):
        if peminjaman_list[i][0] == id_peminjaman:
            peminjaman_lama = peminjaman_list[i]
            judul_lama = peminjaman_lama[2]
            
            # Hanya jika judul baru berbeda dari judul lama
            if judul_lama.lower() != judul_baru.lower():
                # Mengembalikan jumlah buku lama
                for buku in buku_list:
                    if buku['judul'].lower() == judul_lama.lower():
                        buku['jumlah'] += 1  # Kembalikan satu buku dari judul lama
                        break
            
                # Cek apakah judul baru ada dan cukup
                for buku in buku_list:
                    if buku['judul'].lower() == judul_baru.lower():
                        if buku['jumlah'] > 0:
                            # Perbarui peminjaman
                            peminjaman_list[i] = (id_peminjaman, nama_baru, judul_baru, peminjaman_lama[3], peminjaman_lama[4])
                            buku['jumlah'] -= 1  # Kurangi satu buku dari judul baru
                            print(f"Peminjaman dengan ID '{id_peminjaman}' berhasil diperbarui!")
                            tampilkan_buku()
                            return
                        else:
                            print(f"Buku '{judul_baru}' sudah habis.")
                            return
                print(f"Buku '{judul_baru}' tidak ditemukan.")
                return
            
            # Jika judul tidak berubah
            peminjaman_list[i] = (id_peminjaman, nama_baru, judul_baru, peminjaman_lama[3], peminjaman_lama[4])
            print(f"Peminjaman dengan ID '{id_peminjaman}' berhasil diperbarui!")
            tampilkan_buku()
            return   
    print(f"Peminjaman dengan ID '{id_peminjaman}' tidak ditemukan!")


def delete_peminjaman(id_peminjaman):
    # Cek apakah peminjaman sudah dikembalikan
    sudah_dikembalikan = any(peminjaman[0] == id_peminjaman for peminjaman in pengembalian_list)
    
    if sudah_dikembalikan:
        print(f"Peminjaman dengan ID '{id_peminjaman}' sudah dikembalikan. Data peminjaman dapat dihapus.")
        
        # penghapusan
        for i in range(len(peminjaman_list)):
            if peminjaman_list[i][0] == id_peminjaman:
                del peminjaman_list[i]
                print(f"Peminjaman dengan ID '{id_peminjaman}' berhasil dihapus!")
                return  
    else:
        # Jika belum dikembalikan
        print(f"Peminjaman dengan ID '{id_peminjaman}' belum dikembalikan. Data tidak dapat dihapus.")



def cari_peminjaman(id_peminjaman):
    for peminjaman in peminjaman_list:
        if peminjaman[0] == id_peminjaman:
            print(f"Data peminjaman dengan ID {id_peminjaman}:")
            print(f"Nama: {peminjaman[1]}")
            print(f"Judul Buku: {peminjaman[2]}")
            return
    print(f"Peminjaman dengan ID '{id_peminjaman}' tidak ditemukan!")



def kembalikan_buku(id_peminjaman):
    for i in range(len(peminjaman_list)):
        if peminjaman_list[i][0] == id_peminjaman:
            peminjaman = peminjaman_list.pop(i)
            pengembalian_list.append(peminjaman)

            batas_waktu_sekarang = datetime.date.today()
            denda_per_hari = 1000
            keterlambatan = (batas_waktu_sekarang - peminjaman[4]).days
            
            if keterlambatan > 0:
                denda = keterlambatan * denda_per_hari
                print(f"Buku dengan ID '{id_peminjaman}' berhasil dikembalikan.")
                print(f"Buku terlambat {keterlambatan} hari. Total denda: Rp {denda}.")
            else:
                print(f"Buku dengan ID '{id_peminjaman}' berhasil dikembalikan tepat waktu.")
            return
    print(f"Peminjaman dengan ID '{id_peminjaman}' tidak ditemukan!")


def tampilkan_pengembalian():
    print("\n--- Daftar Pengembalian Buku ---")
    if not pengembalian_list:
        print("Belum ada buku yang dikembalikan!")
        return

    table = PrettyTable(["ID", "Nama", "Judul Buku"])
    for pengembalian in pengembalian_list:
        table.add_row([pengembalian[0], pengembalian[1], pengembalian[2]])
    print(table)


def lihat_aktivitas_tanggal():
    tanggal_dicari = input("Masukkan tanggal (YYYY-MM-DD): ")
    tanggal_dicari = datetime.datetime.strptime(tanggal_dicari, "%Y-%m-%d").date()

    print("\n--- Aktivitas Peminjaman pada Tanggal yang Dicari ---")
    table_peminjaman = PrettyTable(["ID", "Nama", "Judul Buku", "Tanggal Pinjam"])
    for peminjaman in peminjaman_list:
        if peminjaman[3] == tanggal_dicari:
            table_peminjaman.add_row([peminjaman[0], peminjaman[1], peminjaman[2], peminjaman[3]])
    if table_peminjaman.rows:
        print(table_peminjaman)
    else:
        print("Tidak ada peminjaman pada tanggal tersebut.")


while True:
    print("\n=== Sistem Peminjaman dan Pengembalian Buku Perpustakaan Umum ===")
    print("1. Kelola Buku")
    print("2. Kelola Peminjaman")
    print("3. Kembalikan Buku")
    print("4. Lihat Rekaman")
    print("5. Keluar")

    pilihan = input("Pilih kategori yang Anda inginkan: ")

    if pilihan == "1":  # Kelola Buku
        while True:
            print("\n--- Kelola Buku ---")
            print("1. Tampilkan daftar buku")
            print("2. Tambah buku baru")
            print("3. Kembali ke menu utama")

            sub_pilihan = input("Pilih aksi: ")
            if sub_pilihan == "1":
                tampilkan_buku()
            elif sub_pilihan == "2":
                tambah_buku()
            elif sub_pilihan == "3":
                break  # Keluar dari sub-menu "Kelola Buku"
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")

    elif pilihan == "2":  # Kelola Peminjaman
        while True:
            print("\n--- Kelola Peminjaman ---")
            print("1. Tambah peminjaman")
            print("2. Lihat daftar peminjaman")
            print("3. Update peminjaman")
            print("4. Hapus peminjaman")
            print("5. Cari data peminjaman")
            print("6. Kembali ke menu utama")

            sub_pilihan = input("Pilih aksi: ")
            if sub_pilihan == "1":
                id_peminjaman = input("Masukkan ID Peminjaman: ")
                nama_peminjam = input("Masukkan Nama Peminjam: ")
                judul_buku_input = input("Masukkan Judul Buku (pisahkan dengan koma jika lebih dari satu): ")
                judul_buku_list = [judul.strip() for judul in judul_buku_input.split(",")]
                tambah_peminjaman(id_peminjaman, nama_peminjam, judul_buku_list)
            elif sub_pilihan == "2":
                tampilkan_peminjaman()
            elif sub_pilihan == "3":
                id_peminjaman = input("Masukkan ID Peminjaman yang ingin diperbarui: ")
                nama_baru = input("Masukkan Nama Baru: ")
                judul_baru = input("Masukkan Judul Buku Baru: ")
                update_peminjaman(id_peminjaman, nama_baru, judul_baru)
            elif sub_pilihan == "4":
                id_peminjaman = input("Masukkan ID Peminjaman yang ingin dihapus: ")
                delete_peminjaman(id_peminjaman)
            elif sub_pilihan == "5":  # Tambahkan logika pencarian
                id_peminjaman = input("Masukkan ID peminjam yang ingin dicari: ").strip()
                cari_peminjaman(id_peminjaman)
            elif sub_pilihan == "6":
                break
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")

    elif pilihan == "3":  # Kembalikan Buku
        id_peminjaman = input("Masukkan ID Peminjaman yang ingin dikembalikan: ")
        kembalikan_buku(id_peminjaman)

    elif pilihan == "4":  # Lihat Rekaman
        while True:
            print("\n--- Lihat Rekaman ---")
            print("1. Lihat aktivitas berdasarkan tanggal")
            print("2. Lihat daftar pengembalian")
            print("3. Kembali ke menu utama")

            sub_pilihan = input("Pilih aksi: ")
            if sub_pilihan == "1":
                lihat_aktivitas_tanggal()
            elif sub_pilihan == "2":
                tampilkan_pengembalian()
            elif sub_pilihan == "3":
                break  # Keluar dari sub-menu "Lihat Rekaman"
            else:
                print("Pilihan tidak valid. Silakan coba lagi.")

    elif pilihan == "5":
        print("Program selesai. Terima kasih!")
        break

    else:
        print("Pilihan tidak valid. Silakan coba lagi.")
