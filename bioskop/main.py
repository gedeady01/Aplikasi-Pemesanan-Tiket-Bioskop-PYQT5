import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget, QWidget, QMessageBox, QLabel, QPushButton, QTableWidgetItem, QHeaderView, QFileDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap, QFont, QColor, QBrush, QTextDocument, QTextCursor, QTextCharFormat
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
import webbrowser
from datetime import datetime

# Import helper database dari file database.py
from database import (
    Database, FilmDB, JadwalDB, TransaksiDB, UserDB, KursiDB, StudioDB
)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.db = Database()
        if not self.db.connect():
            QMessageBox.critical(self, "Error", "Gagal terhubung ke database!")
            return
        
        # Inisialisasi Helper
        self.film_db = FilmDB(self.db)
        self.jadwal_db = JadwalDB(self.db)
        self.transaksi_db = TransaksiDB(self.db)
        self.user_db = UserDB(self.db)
        self.kursi_db = KursiDB(self.db)
        self.studio_db = StudioDB(self.db)
        
        # Session Data
        self.current_user = {'id_user': 1, 'nama': 'Customer'} 
        self.current_selected_film = None
        self.current_selected_jadwal = None
        self.current_selected_kursi = []
        self.cart_total = 0
        
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Load Halaman
        self.homepage = HomePage(self)
        self.detail_film = DetailFilm(self)
        self.tiket_page = TiketPage(self)
        self.pembayaran = HalamanPembayaran(self)
        self.riwayat = RiwayatPemesanan(self)

        self.stacked_widget.addWidget(self.homepage)     # Index 0
        self.stacked_widget.addWidget(self.detail_film)   # Index 1
        self.stacked_widget.addWidget(self.tiket_page)     # Index 2
        self.stacked_widget.addWidget(self.pembayaran)    # Index 3
        self.stacked_widget.addWidget(self.riwayat)       # Index 4
        
        self.setWindowTitle("Aplikasi Bioskop Digital")
        # self.setFixedSize(1200, 900)
        self.show()

class HomePage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        loadUi('HomePage.ui', self)
        
        # Data film
        self.all_films = []  # Semua film dari database
        self.filtered_films = []  # Film hasil pencarian
        
        # Setup search input
        self.setup_search()
        
        # Setup tombol navigasi
        self.setup_navigation_buttons()
    
    def setup_search(self):
        """Setup search input dan event handler"""
        if hasattr(self, 'searchInput'):
            # Connect ke event textChanged untuk real-time search
            self.searchInput.textChanged.connect(self.on_search_text_changed)
            
            # Set placeholder text
            self.searchInput.setPlaceholderText("Cari film berdasarkan judul...")
            
            print("✅ Fitur pencarian film berhasil di-setup")
        else:
            print("⚠️  Search input tidak ditemukan di UI")
    
    def on_search_text_changed(self, text):
        """Handler ketika text search berubah - Real-time search"""
        search_query = text.strip()
        
        if search_query == "":
            # Jika search kosong, tampilkan semua film
            print("\n🔍 Pencarian dikosongkan - Tampilkan semua film")
            self.filtered_films = self.all_films
        else:
            # Filter film berdasarkan query
            print(f"\n🔍 Mencari film: '{search_query}'")
            self.search_films(search_query)
        
        # Update tampilan poster
        self.display_films()
    
    def search_films(self, keyword):
        """Cari film berdasarkan keyword"""
        # Cari di database
        results = self.main.film_db.search_films(keyword)
        
        if results:
            self.filtered_films = results
            print(f"   ✅ Ditemukan {len(results)} film:")
            for film in results:
                print(f"      - {film['judul']}")
        else:
            self.filtered_films = []
            print(f"   ❌ Tidak ada film yang cocok dengan '{keyword}'")
    
    def setup_navigation_buttons(self):
        """Setup tombol-tombol navigasi di homepage"""
        
        # Tombol Riwayat Pesanan (pushButton_3)
        if hasattr(self, 'pushButton_3'):
            self.pushButton_3.clicked.connect(self.go_to_riwayat)
            print("✅ Tombol Riwayat Pesanan berhasil di-setup")
        
        # Tombol Masuk (pushButton) - opsional
        if hasattr(self, 'pushButton'):
            self.pushButton.clicked.connect(self.show_login_message)
        
        # Tombol Buat Akun (pushButton_2) - opsional
        if hasattr(self, 'pushButton_2'):
            self.pushButton_2.clicked.connect(self.show_register_message)
    
    def go_to_riwayat(self):
        """Navigasi ke halaman Riwayat Pemesanan"""
        print("\n" + "=" * 50)
        print("📄 NAVIGASI KE RIWAYAT PEMESANAN")
        print("=" * 50)
        
        # Cek apakah user sudah login
        if not self.main.current_user:
            print("⚠️  User belum login")
            QMessageBox.warning(
                self,
                "Login Diperlukan",
                "Silakan login terlebih dahulu untuk melihat riwayat pemesanan Anda."
            )
            return
        
        print(f"✅ User login: {self.main.current_user.get('nama', 'Customer')}")
        print(f"   User ID: {self.main.current_user['id_user']}")
        print("   Redirect ke halaman Riwayat Pemesanan (index 4)")
        print("=" * 50 + "\n")
        
        # Pindah ke halaman Riwayat Pemesanan (index 4)
        self.main.stacked_widget.setCurrentIndex(4)
    
    def show_login_message(self):
        """Placeholder untuk tombol Masuk"""
        QMessageBox.information(
            self,
            "Info",
            "Fitur login belum diimplementasikan.\n\nUntuk sementara, Anda login sebagai user default."
        )
    
    def show_register_message(self):
        """Placeholder untuk tombol Buat Akun"""
        QMessageBox.information(
            self,
            "Info",
            "Fitur registrasi belum diimplementasikan.\n\nSilakan hubungi admin untuk membuat akun baru."
        )
    
    def showEvent(self, event):
        """Dipanggil saat halaman ditampilkan"""
        super().showEvent(event)
        self.load_films()
    
    def load_films(self):
        """Load semua film dari database"""
        # Ambil semua film yang sedang tayang
        self.all_films = self.main.film_db.get_all_films(status='tayang')
        
        if not self.all_films: 
            print("⚠️  Tidak ada film yang sedang tayang")
            QMessageBox.information(
                self,
                "Info",
                "Saat ini tidak ada film yang sedang tayang."
            )
            return
        
        print(f"\n🎽️  Berhasil load {len(self.all_films)} film dari database")
        for film in self.all_films:
            print(f"   - {film['judul']} ({film['genre']})")
        
        # Set filtered_films = semua film (belum ada filter)
        self.filtered_films = self.all_films
        
        # Tampilkan poster
        self.display_films()
    
    def display_films(self):
        """Tampilkan poster film (dari filtered_films)"""
        films = self.filtered_films
        
        if not films:
            # Jika tidak ada hasil pencarian
            print("\n📋 Tidak ada film untuk ditampilkan")
            self.hide_all_posters()
            return
        
        print(f"\n🎬 Menampilkan {len(films)} film...")
        
        # ===== POSTER VERTIKAL (Daftar Film) - 5 poster =====
        poster_labels = [
            'label_poster1', 'label_poster2', 'label_poster3', 
            'label_poster4', 'label_poster5'
        ]
        
        for idx, label_name in enumerate(poster_labels):
            if hasattr(self, label_name):
                label = getattr(self, label_name)
                
                if idx < len(films):
                    # Ada film untuk slot ini
                    film = films[idx]
                    f_id = film['id_film']
                    
                    # Load gambar poster
                    img_path = os.path.join(os.path.dirname(__file__), 'images', film['poster'])
                    
                    if os.path.exists(img_path):
                        pixmap = QPixmap(img_path)
                        label.setPixmap(
                            pixmap.scaled(label.size(), 
                                        Qt.IgnoreAspectRatio, 
                                        Qt.SmoothTransformation)
                        )
                        label.setVisible(True)
                        print(f"   ✅ {label_name}: {film['judul']}")
                    else:
                        print(f"   ⚠️  {label_name}: Poster tidak ditemukan ({film['poster']})")
                        label.setVisible(False)
                    
                    # Setup click event untuk detail film
                    label.setCursor(Qt.PointingHandCursor)
                    # Gunakan functools.partial atau method yang benar untuk binding
                    def make_click_handler(film_id):
                        return lambda event: self.on_poster_clicked(film_id)
                    label.mousePressEvent = make_click_handler(f_id)
                else:
                    # Tidak ada film untuk slot ini - sembunyikan
                    label.setVisible(False)
        
        # ===== POSTER HORIZONTAL (Sedang Tayang) - 5 poster =====
        # Menampilkan film ke-6 sampai ke-10 (index 5-9)
        horizontal_labels = [
            'label_poster6', 'label_poster7', 'label_poster8',
            'label_poster9', 'label_poster10'
        ]
        
        for idx, label_name in enumerate(horizontal_labels):
            if hasattr(self, label_name):
                label = getattr(self, label_name)
                
                # Gunakan offset +5 agar poster 6-10 menampilkan film berbeda (film ke-6 sampai ke-10)
                film_idx = idx + 5  # idx=0 -> film[5], idx=1 -> film[6], dst.
                
                if film_idx < len(films):
                    film = films[film_idx]
                    f_id = film['id_film']
                    
                    # Load gambar poster
                    img_path = os.path.join(os.path.dirname(__file__), 'images', film['poster'])
                    
                    if os.path.exists(img_path):
                        pixmap = QPixmap(img_path)
                        label.setPixmap(
                            pixmap.scaled(label.size(), 
                                        Qt.IgnoreAspectRatio, 
                                        Qt.SmoothTransformation)
                        )
                        label.setVisible(True)
                        print(f"   ✅ {label_name}: {film['judul']}")
                    else:
                        print(f"   ⚠️  {label_name}: Poster tidak ditemukan ({film['poster']})")
                        label.setVisible(False)
                    
                    # Setup click event
                    label.setCursor(Qt.PointingHandCursor)
                    # Gunakan functools.partial atau method yang benar untuk binding
                    def make_click_handler(film_id):
                        return lambda event: self.on_poster_clicked(film_id)
                    label.mousePressEvent = make_click_handler(f_id)
                else:
                    label.setVisible(False)
        
        print("✅ Poster berhasil ditampilkan\n")
    
    def hide_all_posters(self):
        """Sembunyikan semua poster (untuk kasus tidak ada hasil search)"""
        all_labels = [
            'label_poster1', 'label_poster2', 'label_poster3', 
            'label_poster4', 'label_poster5',
            'label_poster6', 'label_poster7', 'label_poster8',
            'label_poster9', 'label_poster10'
        ]
        
        for label_name in all_labels:
            if hasattr(self, label_name):
                label = getattr(self, label_name)
                label.setVisible(False)
    
    def on_poster_clicked(self, film_id):
        """Handler ketika poster diklik - pindah ke detail film"""
        print(f"\n🎬 Poster film ID {film_id} diklik")
        
        # Ambil data film dari database
        film = self.main.film_db.get_film_by_id(film_id)
        
        if film:
            print(f"   Film: {film['judul']}")
            print(f"   Genre: {film['genre']}")
            print(f"   Durasi: {film['durasi']} menit")
            
            # Simpan film yang dipilih ke main window
            self.main.current_selected_film = film
            
            # Pindah ke halaman detail film (index 1)
            print("   → Redirect ke Detail Film (index 1)\n")
            self.main.stacked_widget.setCurrentIndex(1)
        else:
            print(f"   ❌ Film ID {film_id} tidak ditemukan di database!\n")
            QMessageBox.warning(
                self,
                "Error",
                "Film tidak ditemukan!"
            )
    
    def on_poster_clicked(self, film_id):
        """Handler ketika poster diklik - pindah ke detail film"""
        print(f"\n🎬 Poster film ID {film_id} diklik")
        
        # Ambil data film dari database
        film = self.main.film_db.get_film_by_id(film_id)
        
        if film:
            print(f"   Film: {film['judul']}")
            print(f"   Genre: {film['genre']}")
            print(f"   Durasi: {film['durasi']} menit")
            
            # Simpan film yang dipilih ke main window
            self.main.current_selected_film = film
            
            # Pindah ke halaman detail film (index 1)
            print("   → Redirect ke Detail Film (index 1)\n")
            self.main.stacked_widget.setCurrentIndex(1)
        else:
            print(f"   ❌ Film ID {film_id} tidak ditemukan di database!\n")
            QMessageBox.warning(
                self,
                "Error",
                "Film tidak ditemukan!"
            )

class DetailFilm(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        loadUi('DetailFilm.ui', self)
        
        # Tombol Kembali ke Homepage
        self.pushButton.clicked.connect(lambda: self.main.stacked_widget.setCurrentIndex(0))
        
        # Tombol Pesan Tiket
        self.pushButton_2.clicked.connect(lambda: self.main.stacked_widget.setCurrentIndex(2))
        
        # Tombol Lihat Trailer (trailler_button)
        if hasattr(self, 'trailler_button'):
            self.trailler_button.clicked.connect(self.open_trailer)
            self.trailler_button.setCursor(Qt.PointingHandCursor)
            print("✅ Tombol Trailer (trailler_button) berhasil di-setup")
        else:
            print("⚠️  Tombol trailler_button tidak ditemukan di UI")
    
    def open_trailer(self):
        """Buka trailer film di browser"""
        film = self.main.current_selected_film
        
        if not film:
            QMessageBox.warning(
                self,
                "Error",
                "Data film tidak ditemukan!"
            )
            return
        
        trailer_url = film.get('trailer_url', '')
        
        if not trailer_url:
            QMessageBox.information(
                self,
                "Info",
                f"Trailer untuk film '{film['judul']}' belum tersedia."
            )
            return
        
        print(f"\n🎬 Membuka trailer: {film['judul']}")
        print(f"   URL: {trailer_url}")
        
        try:
            # Buka URL di browser default
            import webbrowser
            webbrowser.open(trailer_url)
            
            print("   ✅ Trailer berhasil dibuka di browser")
            
            # Optional: Tampilkan notifikasi sukses
            # QMessageBox.information(
            #     self,
            #     "Sukses",
            #     f"Trailer '{film['judul']}' dibuka di browser!"
            # )
            
        except Exception as e:
            print(f"   ❌ Error membuka trailer: {str(e)}")
            QMessageBox.critical(
                self,
                "Error",
                f"Gagal membuka trailer!\n\nError: {str(e)}\n\nURL: {trailer_url}"
            )
    
    def showEvent(self, event):
        """Dipanggil setiap kali halaman detail film ditampilkan"""
        super().showEvent(event)
        self.display_film_detail()
    
    def display_film_detail(self):
        """Tampilkan detail film yang dipilih"""
        film = self.main.current_selected_film
        if not film:
            return
        
        print(f"\n{'='*60}")
        print(f"📽️  DETAIL FILM: {film['judul']}")
        print(f"{'='*60}")
        
        # Update Poster (label_poster1)
        if hasattr(self, 'label_poster1'):
            img_path = os.path.join(os.path.dirname(__file__), 'images', film['poster'])
            if os.path.exists(img_path):
                pixmap = QPixmap(img_path)
                self.label_poster1.setPixmap(
                    pixmap.scaled(
                        self.label_poster1.size(), 
                        Qt.IgnoreAspectRatio, 
                        Qt.SmoothTransformation
                    )
                )
                print(f"✅ Poster: {film['poster']}")
            else:
                print(f"⚠️  Poster tidak ditemukan: {film['poster']}")
        
        # Update Judul Film (label dan label_3)
        if hasattr(self, 'label'):
            self.label.setText(film['judul'])
        if hasattr(self, 'label_3'):
            self.label_3.setText(film['judul'])
            print(f"🎬 Judul: {film['judul']}")
        
        # Update Durasi (label_9)
        if hasattr(self, 'label_9'):
            durasi = film.get('durasi', 0)
            self.label_9.setText(f"🕒 {durasi} Menit")
            print(f"⏱️  Durasi: {durasi} Menit")
        
        # Update Sinopsis/Deskripsi (label_4)
        if hasattr(self, 'label_4'):
            deskripsi = film.get('deskripsi', '')
            self.label_4.setText(f"Sinopsis: {deskripsi}")
            print(f"📝 Sinopsis: {deskripsi[:50]}...")
        
        # Update Genre (bisa ditambahkan di label_5 atau label lainnya)
        # Karena di UI asli tidak ada label khusus genre, kita skip atau ganti label_5
        if hasattr(self, 'label_5'):
            genre = film.get('genre', '')
            rating = film.get('rating', '')
            self.label_5.setText(f"Genre: {genre} | Rating: {rating}")
            print(f"🎭 Genre: {genre}")
            print(f"⭐ Rating: {rating}")
        
        # Label lainnya bisa disesuaikan dengan data yang ada
        # label_6 = Direktor (tidak ada di database, bisa di-skip atau di-hide)
        # label_7 = Distributor (tidak ada di database)
        # label_8 = Budget (tidak ada di database)
        
        # Hide label yang tidak ada datanya
        if hasattr(self, 'label_6'):
            self.label_6.setText("")
        if hasattr(self, 'label_7'):
            self.label_7.setText("")
        if hasattr(self, 'label_8'):
            self.label_8.setText("")
        
        # Cek apakah ada trailer
        trailer_url = film.get('trailer_url', '')
        if trailer_url:
            print(f"🎥 Trailer: {trailer_url}")
            # Enable tombol trailer
            if hasattr(self, 'trailler_button'):
                self.trailler_button.setEnabled(True)
                self.trailler_button.setStyleSheet("""
                    padding:20px;
                    background-color:black;
                    border-radius:10px;
                    color:white;
                """)
        else:
            print(f"⚠️  Trailer: Tidak tersedia")
            # Disable tombol trailer
            if hasattr(self, 'trailler_button'):
                self.trailler_button.setEnabled(False)
                self.trailler_button.setStyleSheet("""
                    padding:20px;
                    background-color:gray;
                    border-radius:10px;
                    color:darkgray;
                """)
        
        print(f"{'='*60}\n")

class TiketPage(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        loadUi('Tiket.ui', self)
        
        # Data Tiket
        self.harga_per_tiket = 0  # Akan di-load dari database
        self.selected_kursi = []
        self.selected_jam = None
        self.selected_jadwal_id = None
        self.kursi_terpesan = set()
        self.jam_data = ['12:55', '14:25', '16:35', '18:35', '20:55']
        self.jam_labels = ['label_36', 'label_37', 'label_38', 'label_39', 'label_40']
        
        # Setup jam buttons
        self.setup_jam_buttons()
        
        # Setup quantity buttons
        self.setup_quantity_buttons()
        
        # Tombol Navigasi
        self.pushButton.clicked.connect(lambda: self.main.stacked_widget.setCurrentIndex(1))
        self.pushButton_2.clicked.connect(self.proses_ke_pembayaran)

    def setup_jam_buttons(self):
        """Setup click handlers untuk jam"""
        for idx, label_name in enumerate(self.jam_labels):
            if hasattr(self, label_name):
                label = getattr(self, label_name)
                jam = self.jam_data[idx]
                label.setCursor(Qt.PointingHandCursor)
                label.mousePressEvent = lambda e, j=jam, l=label_name: self.select_jam(j, l)

    def select_jam(self, jam, label_name):
        """Handle pemilihan jam"""
        self.selected_jam = jam
        print(f"DEBUG: Jam dipilih: {jam}")
        self.update_jam_display(label_name)

    def update_jam_display(self, selected_label):
        """Update tampilan jam yang dipilih"""
        for label_name in self.jam_labels:
            if hasattr(self, label_name):
                label = getattr(self, label_name)
                if label_name == selected_label:
                    label.setStyleSheet("background-color: rgb(0, 0, 0); color: rgb(255, 255, 0); border: 3px solid yellow; border-radius:10px; font-weight: bold;")
                else:
                    label.setStyleSheet("background-color: rgb(0, 0, 0); color: rgb(255, 255, 255); border-radius:10px;")

    def setup_quantity_buttons(self):
        """Setup click handlers untuk tombol +/- jumlah tiket"""
        all_buttons = self.findChildren(QPushButton)
        for btn in all_buttons:
            if '➕' in btn.text() or '+' in btn.text():
                btn.clicked.connect(self.increase_quantity)
            elif '➖' in btn.text() or '-' in btn.text():
                btn.clicked.connect(self.decrease_quantity)

    def increase_quantity(self):
        """Tambah jumlah kursi yang dipilih (tidak perlu, otomatis dari jumlah kursi)"""
        if hasattr(self, 'label_41'):
            current = int(self.label_41.text() or "1")
            self.label_41.setText(str(current + 1))

    def decrease_quantity(self):
        """Kurangi jumlah kursi yang dipilih"""
        if hasattr(self, 'label_41'):
            current = int(self.label_41.text() or "1")
            if current > 1:
                self.label_41.setText(str(current - 1))

    def showEvent(self, event):
        super().showEvent(event)
        self.reset_form()
        self.muat_data_kursi()

    def reset_form(self):
        """Reset form ke kondisi awal"""
        self.selected_kursi = []
        self.selected_jam = None
        if hasattr(self, 'label_41'):
            self.label_41.setText("0")
        self.update_harga_display()
        
        # Reset jam display
        for label_name in self.jam_labels:
            if hasattr(self, label_name):
                label = getattr(self, label_name)
                label.setStyleSheet("background-color: rgb(0, 0, 0); color: rgb(255, 255, 255); border-radius:10px;")

    def muat_data_kursi(self):
        """Load data kursi dari database"""
        film = self.main.current_selected_film
        if not film: 
            return
        
        # Ambil jadwal untuk film ini
        jadwal_list = self.main.jadwal_db.get_jadwal_by_film(film['id_film'])
        if not jadwal_list:
            QMessageBox.information(self, "Info", "Tidak ada jadwal tersedia")
            return
        
        # Gunakan jadwal pertama
        jadwal = jadwal_list[0]
        self.selected_jadwal_id = jadwal['id_jadwal']
        self.main.current_selected_jadwal = jadwal
        self.studio_id = jadwal.get('studio_id')
        
        # Load harga dari database jadwal
        self.harga_per_tiket = float(jadwal.get('harga', 50000))
        print(f"DEBUG: Harga per tiket: Rp {self.harga_per_tiket:,.0f}")
        
        print(f"DEBUG: Studio ID: {self.studio_id}, Nama: {jadwal.get('nama_studio')}")
        
        # Ambil kursi yang sudah terpesan untuk jadwal ini
        terpesan_list = self.main.kursi_db.get_kursi_terpesan(self.selected_jadwal_id)
        self.kursi_terpesan = {k['kode_kursi'] for k in terpesan_list} if terpesan_list else set()
        
        print(f"DEBUG: Kursi terpesan: {self.kursi_terpesan}")
        
        # Setup UI kursi
        self.setup_kursi_ui()

    def setup_kursi_ui(self):
        """Setup semua kursi A1-D7 di UI menggunakan objectName (name) dari label"""
        self.kursi_labels = {}  # {kode_kursi: [label_widgets]}
        
        for label in self.findChildren(QLabel):
            # Gunakan objectName (name) dari label, bukan text
            obj_name = label.objectName().strip()
            
            # Cek apakah objectName adalah kursi (A1-D7)
            if len(obj_name) == 2 and obj_name[0] in 'ABCD' and obj_name[1] in '1234567':
                kode = obj_name
                
                # Simpan reference label ke dict (bisa multiple label dengan kode sama)
                if kode not in self.kursi_labels:
                    self.kursi_labels[kode] = []
                self.kursi_labels[kode].append(label)
                
                # Hapus event handler lama
                label.mousePressEvent = None
                
                # Simpan kode kursi sebagai property label
                label.kursi_kode = kode
                
                # Setup warna berdasarkan status
                if kode in self.kursi_terpesan:
                    # Kursi penuh = Merah
                    label.setStyleSheet("background-color: #FF4444; color: white; border-radius:5px; font-weight: bold; border: 2px solid darkred;")
                    label.setCursor(Qt.ForbiddenCursor)
                else:
                    # Kursi kosong = Hitam
                    label.setStyleSheet("background-color: #333333; color: white; border-radius:5px; font-weight: bold; border: 2px solid #555555;")
                    label.setCursor(Qt.PointingHandCursor)
                    # Attach click handler
                    label.mousePressEvent = lambda e, k=kode: self.toggle_kursi(k)
        
        print(f"DEBUG: Kursi yang di-setup (unique): {sorted(self.kursi_labels.keys())}")
        for kode, labels in self.kursi_labels.items():
            print(f"   {kode}: {len(labels)} label(s)")

    def toggle_kursi(self, kode):
        """Toggle kursi dipilih/dibatalkan"""
        if kode not in self.kursi_labels:
            print(f"DEBUG: Label untuk kursi {kode} tidak ditemukan!")
            return
        
        labels = self.kursi_labels[kode]
        
        print(f"DEBUG: Toggle kursi {kode}, current list: {self.selected_kursi}")
        
        if kode in self.selected_kursi:
            # Batalkan pilihan
            self.selected_kursi.remove(kode)
            # Update semua label dengan kode ini
            for lbl in labels:
                lbl.setStyleSheet("background-color: #333333; color: white; border-radius:5px; font-weight: bold; border: 2px solid #555555;")
            print(f"   → Dihapus dari pilihan")
        else:
            # Pilih kursi
            self.selected_kursi.append(kode)
            # Update semua label dengan kode ini
            for lbl in labels:
                lbl.setStyleSheet("background-color: #00AA00; color: white; border-radius:5px; font-weight: bold; border: 2px solid darkgreen;")
            print(f"   → Ditambahkan ke pilihan")
        
        print(f"   Final list: {self.selected_kursi}")
        self.update_harga_display()

    def update_harga_display(self):
        """Update tampilan harga dan jumlah tiket"""
        jumlah = len(self.selected_kursi)
        total = jumlah * self.harga_per_tiket
        self.main.cart_total = total
        
        # Update label jumlah (label_41)
        if hasattr(self, 'label_41'):
            self.label_41.setText(str(jumlah))
        
        # Update label harga total (label_harga)
        if hasattr(self, 'label_harga'):
            if jumlah > 0:
                harga_text = f"Rp {total:,.0f}".replace(',', '.')
                self.label_harga.setText(harga_text)
            else:
                self.label_harga.setText("Rp 0")

    def proses_ke_pembayaran(self):
        """Validasi dan lanjut ke pembayaran"""
        if not self.selected_jam:
            QMessageBox.warning(self, "Peringatan", "Silakan pilih jam terlebih dahulu!")
            return
        
        if not self.selected_kursi:
            QMessageBox.warning(self, "Peringatan", "Silakan pilih minimal satu kursi!")
            return
        
        # Simpan data ke main window
        self.main.current_selected_kursi = self.selected_kursi
        self.main.current_selected_jadwal = {
            'id': self.selected_jadwal_id,
            'studio_id': self.studio_id,
            'jam': self.selected_jam,
            'kursi': self.selected_kursi,
            'jumlah': len(self.selected_kursi),
            'harga_per_tiket': self.harga_per_tiket,
            'total': len(self.selected_kursi) * self.harga_per_tiket
        }
        
        print(f"DEBUG: Melanjut ke pembayaran...")
        print(f"   Jadwal ID: {self.selected_jadwal_id}")
        print(f"   Jam: {self.selected_jam}")
        print(f"   Kursi: {self.selected_kursi}")
        print(f"   Jumlah: {len(self.selected_kursi)}")
        print(f"   Harga per tiket: Rp {self.harga_per_tiket:,.0f}")
        print(f"   Total: Rp {self.main.current_selected_jadwal['total']:,.0f}")
        
        self.main.stacked_widget.setCurrentIndex(3)

class HalamanPembayaran(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        loadUi('HalamanPembayaran.ui', self)
        
        # Inisialisasi variabel
        self.metode_pembayaran = None
        self.kode_promo = None
        self.diskon_promo = 0
        self.biaya_admin = 0
        
        # Setup event handlers
        self.setup_payment_methods()
        self.setup_buttons()
        
        # Setup promo input (jika ada)
        if hasattr(self, 'lineEdit_promo'):
            self.lineEdit_promo.textChanged.connect(self.cek_promo)

    def setup_payment_methods(self):
        """Setup radio buttons untuk metode pembayaran"""
        payment_methods = {
            'radioButton': {'name': 'Credit/Debit Card', 'admin': 2500},
            'radioButton_5': {'name': 'E-Wallet', 'admin': 1000},
            'radioButton_6': {'name': 'Virtual Account', 'admin': 4000},
            'radioButton_7': {'name': 'Cash on Delivery', 'admin': 0}
        }
        
        for radio_name, info in payment_methods.items():
            if hasattr(self, radio_name):
                radio = getattr(self, radio_name)
                radio.toggled.connect(
                    lambda checked, m=info['name'], a=info['admin']: 
                    self.pilih_metode(checked, m, a)
                )

    def setup_buttons(self):
        """Setup tombol navigasi dan pembayaran"""
        # Tombol kembali (pushButton_2)
        if hasattr(self, 'pushButton_2'):
            self.pushButton_2.clicked.connect(self.kembali_ke_tiket)
        
        # Tombol bayar (pushButton)
        if hasattr(self, 'pushButton'):
            self.pushButton.clicked.connect(self.proses_pembayaran)

    def showEvent(self, event):
        """Dipanggil setiap kali halaman ditampilkan"""
        super().showEvent(event)
        self.reset_form()
        if self.main.current_selected_film and self.main.current_selected_jadwal:
            self.tampilkan_detail_pemesanan()

    def reset_form(self):
        """Reset form ke kondisi awal"""
        self.metode_pembayaran = None
        self.kode_promo = None
        self.diskon_promo = 0
        self.biaya_admin = 0
        
        # Uncheck semua radio button
        radio_buttons = ['radioButton', 'radioButton_5', 'radioButton_6', 'radioButton_7']
        for radio_name in radio_buttons:
            if hasattr(self, radio_name):
                getattr(self, radio_name).setChecked(False)

    def tampilkan_detail_pemesanan(self):
        """Tampilkan detail film dan pemesanan"""
        film = self.main.current_selected_film
        jadwal_info = self.main.current_selected_jadwal
        
        if not film or not jadwal_info:
            return
        
        # Ambil data jadwal lengkap dari database
        jadwal_detail = self.main.jadwal_db.get_jadwal_by_id(jadwal_info['id'])
        
        # Update poster film
        if hasattr(self, 'label_poster1'):
            img_path = os.path.join(os.path.dirname(__file__), 'images', film['poster'])
            if os.path.exists(img_path):
                pixmap = QPixmap(img_path)
                self.label_poster1.setPixmap(
                    pixmap.scaled(self.label_poster1.size(), 
                                Qt.IgnoreAspectRatio, 
                                Qt.SmoothTransformation)
                )
        
        # Update judul film (label_5)
        if hasattr(self, 'label_5'):
            self.label_5.setText(film['judul'])
        
        # Update nama cinema (lineEdit)
        if hasattr(self, 'lineEdit'):
            cinema_name = jadwal_detail.get('nama_studio', 'Studio') if jadwal_detail else 'Studio'
            self.lineEdit.setText(cinema_name)
            self.lineEdit.setReadOnly(True)
        
        # Update tanggal & waktu (lineEdit_2)
        if hasattr(self, 'lineEdit_2'):
            if jadwal_detail:
                tanggal = jadwal_detail.get('tanggal', '')
                jam = jadwal_detail.get('jam_mulai', '')
                
                # Format tanggal
                try:
                    if isinstance(tanggal, str):
                        from datetime import datetime
                        tgl_obj = datetime.strptime(str(tanggal), '%Y-%m-%d')
                        hari = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
                        bulan = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Jun', 
                                'Jul', 'Agu', 'Sep', 'Okt', 'Nov', 'Des']
                        
                        tanggal_formatted = f"{hari[tgl_obj.weekday()]}, {tgl_obj.day} {bulan[tgl_obj.month-1]} {tgl_obj.year}"
                    else:
                        tanggal_formatted = str(tanggal)
                    
                    # Format jam (hilangkan detik jika ada)
                    jam_str = str(jam)
                    if len(jam_str) > 5:
                        jam_str = jam_str[:5]
                    
                    datetime_text = f"{tanggal_formatted} - {jam_str}"
                except:
                    datetime_text = f"{tanggal} - {jam}"
            else:
                datetime_text = f"{jadwal_info.get('jam', '00:00')}"
            
            self.lineEdit_2.setText(datetime_text)
            self.lineEdit_2.setReadOnly(True)
        
        # Update kursi (lineEdit_3)
        if hasattr(self, 'lineEdit_3'):
            kursi_list = jadwal_info.get('kursi', [])
            kursi_text = ', '.join(kursi_list) if kursi_list else '-'
            self.lineEdit_3.setText(kursi_text)
            self.lineEdit_3.setReadOnly(True)
        
        # Update detail pembayaran
        self.update_detail_pembayaran()

    def pilih_metode(self, checked, metode_nama, biaya_admin):
        """Handle pemilihan metode pembayaran"""
        if checked:
            self.metode_pembayaran = metode_nama
            self.biaya_admin = biaya_admin
            print(f"DEBUG: Metode pembayaran dipilih: {metode_nama}, Biaya admin: Rp {biaya_admin:,}")
            self.update_detail_pembayaran()

    def cek_promo(self):
        """Cek kode promo yang dimasukkan"""
        if not hasattr(self, 'lineEdit_promo'):
            return
        
        kode = self.lineEdit_promo.text().strip().upper()
        
        # Daftar promo (bisa dipindah ke database)
        promo_list = {
            'DISKON10': 10,  # Diskon 10%
            'DISKON20': 20,  # Diskon 20%
            'WELCOME': 15,   # Diskon 15%
            'NEWUSER': 25,   # Diskon 25%
        }
        
        if kode in promo_list:
            self.kode_promo = kode
            self.diskon_promo = promo_list[kode]
            print(f"DEBUG: Promo '{kode}' diterapkan: {self.diskon_promo}%")
        else:
            self.kode_promo = None
            self.diskon_promo = 0
        
        self.update_detail_pembayaran()

    def update_detail_pembayaran(self):
        """Update tampilan detail pembayaran"""
        jadwal_info = self.main.current_selected_jadwal
        
        if not jadwal_info:
            return
        
        # Hitung harga
        harga_tiket = jadwal_info.get('total', 0)
        jumlah_tiket = jadwal_info.get('jumlah', 0)
        
        # Hitung diskon promo
        nominal_diskon = 0
        if self.diskon_promo > 0:
            nominal_diskon = (harga_tiket * self.diskon_promo) / 100
        
        # Hitung total
        subtotal = harga_tiket - nominal_diskon
        total_bayar = subtotal + self.biaya_admin
        
        # Update harga tiket (lineEdit_7)
        if hasattr(self, 'lineEdit_7'):
            self.lineEdit_7.setText(f"Rp {harga_tiket:,.0f}".replace(',', '.'))
            self.lineEdit_7.setReadOnly(True)
        
        # Update promo (lineEdit_16)
        if hasattr(self, 'lineEdit_16'):
            if nominal_diskon > 0:
                self.lineEdit_16.setText(f"-Rp {nominal_diskon:,.0f}".replace(',', '.'))
                self.lineEdit_16.setStyleSheet("border: none; color: rgb(0, 200, 0);")
            else:
                self.lineEdit_16.setText("Rp 0")
                self.lineEdit_16.setStyleSheet("border: none;")
            self.lineEdit_16.setReadOnly(True)
        
        # Update biaya admin (lineEdit_17)
        if hasattr(self, 'lineEdit_17'):
            if self.biaya_admin == 0:
                self.lineEdit_17.setText("Free")
                self.lineEdit_17.setStyleSheet("border: none; color: rgb(0, 255, 0);")
            else:
                self.lineEdit_17.setText(f"Rp {self.biaya_admin:,.0f}".replace(',', '.'))
                self.lineEdit_17.setStyleSheet("border: none;")
            self.lineEdit_17.setReadOnly(True)
        
        # Update total harga (lineEdit_18)
        if hasattr(self, 'lineEdit_18'):
            self.lineEdit_18.setText(f"Rp {total_bayar:,.0f}".replace(',', '.'))
            self.lineEdit_18.setReadOnly(True)
        
        # Simpan total untuk proses pembayaran
        self.total_bayar = total_bayar
        
        print(f"DEBUG: Detail Pembayaran")
        print(f"   Harga Tiket: Rp {harga_tiket:,.0f}")
        print(f"   Diskon ({self.diskon_promo}%): -Rp {nominal_diskon:,.0f}")
        print(f"   Biaya Admin: Rp {self.biaya_admin:,.0f}")
        print(f"   Total: Rp {total_bayar:,.0f}")

    def kembali_ke_tiket(self):
        """Kembali ke halaman pemilihan tiket"""
        self.main.stacked_widget.setCurrentIndex(2)

    def proses_pembayaran(self):
        """Proses pembayaran dan simpan transaksi"""
        # Validasi metode pembayaran
        if not self.metode_pembayaran:
            QMessageBox.warning(
                self, 
                "Peringatan", 
                "Silakan pilih metode pembayaran terlebih dahulu!"
            )
            return
        
        # Validasi user
        if not self.main.current_user:
            QMessageBox.warning(
                self, 
                "Peringatan", 
                "Silakan login terlebih dahulu!"
            )
            return
        
        try:
            jadwal_info = self.main.current_selected_jadwal
            
            # Buat transaksi di database
            transaksi_id = self.main.transaksi_db.create_transaksi(
                user_id=self.main.current_user['id_user'],
                jadwal_id=jadwal_info['id'],
                total_harga=self.total_bayar,
                status='paid'
            )
            
            if not transaksi_id:
                QMessageBox.critical(
                    self, 
                    "Error", 
                    "Gagal membuat transaksi! Silakan coba lagi."
                )
                return
            
            # Simpan detail transaksi (kursi yang dipesan)
            for kode_kursi in jadwal_info['kursi']:
                # Cari id_kursi dari kode_kursi
                kursi_detail = self.main.kursi_db.get_kursi_by_kode(
                    jadwal_info['studio_id'], 
                    kode_kursi
                )
                
                if kursi_detail:
                    self.main.transaksi_db.add_detail_transaksi(
                        transaksi_id, 
                        kursi_detail['id_kursi']
                    )
            
            # Tampilkan pesan sukses
            pesan_sukses = f"""
Pembayaran Berhasil!

No. Transaksi: {transaksi_id}
Metode Pembayaran: {self.metode_pembayaran}
Total Pembayaran: Rp {self.total_bayar:,.0f}

Terima kasih telah memesan tiket!
Silakan tunjukkan e-ticket di kasir.
            """
            
            QMessageBox.information(self, "Sukses", pesan_sukses.strip())
            
            # Log transaksi
            print(f"DEBUG: Transaksi berhasil!")
            print(f"   ID Transaksi: {transaksi_id}")
            print(f"   User ID: {self.main.current_user['id_user']}")
            print(f"   Jadwal ID: {jadwal_info['id']}")
            print(f"   Kursi: {', '.join(jadwal_info['kursi'])}")
            print(f"   Metode: {self.metode_pembayaran}")
            print(f"   Total: Rp {self.total_bayar:,.0f}")
            
            # Reset data dan kembali ke beranda
            self.main.current_selected_kursi = []
            self.main.current_selected_jadwal = None
            self.main.stacked_widget.setCurrentIndex(0)
            
        except Exception as e:
            QMessageBox.critical(
                self, 
                "Error", 
                f"Terjadi kesalahan saat memproses pembayaran:\n{str(e)}"
            )
            print(f"ERROR: {str(e)}")
            import traceback
            traceback.print_exc()

class RiwayatPemesanan(QWidget):
    def __init__(self, main):
        super().__init__()
        self.main = main
        loadUi('RiwayatPemesanan.ui', self)
        
        # Data riwayat
        self.riwayat_list = []
        
        # Setup tombol kembali
        if hasattr(self, 'pushButton_3'):
            self.pushButton_3.clicked.connect(lambda: self.main.stacked_widget.setCurrentIndex(0))
        
        # Setup tombol cetak tiket untuk Card 1
        if hasattr(self, 'pushButton_4'):
            self.pushButton_4.clicked.connect(lambda: self.cetak_tiket_card(0))
        
        # Setup tombol cetak tiket untuk Card 2
        if hasattr(self, 'pushButton_5'):
            self.pushButton_5.clicked.connect(lambda: self.cetak_tiket_card(1))
        
        # Setup tombol selesai untuk Card 1
        if hasattr(self, 'pushButton'):
            self.pushButton.clicked.connect(lambda: self.konfirmasi_selesai(0))
        
        # Setup tombol selesai untuk Card 2
        if hasattr(self, 'pushButton_2'):
            self.pushButton_2.clicked.connect(lambda: self.konfirmasi_selesai(1))
    
    def showEvent(self, event):
        """Dipanggil saat halaman ditampilkan"""
        super().showEvent(event)
        self.load_riwayat()
    
    def load_riwayat(self):
        """Load data riwayat dari database dan tampilkan di card"""
        if not self.main.current_user:
            QMessageBox.warning(self, "Info", "Silakan login terlebih dahulu!")
            return
        
        # Ambil riwayat transaksi user (maksimal 2 terbaru untuk 2 card)
        self.riwayat_list = self.main.transaksi_db.get_transaksi_by_user(
            self.main.current_user['id_user']
        )
        
        if not self.riwayat_list:
            # Sembunyikan kedua card jika tidak ada riwayat
            if hasattr(self, 'frame_3'):
                self.frame_3.setVisible(False)
            if hasattr(self, 'frame_5'):
                self.frame_5.setVisible(False)
            
            QMessageBox.information(self, "Info", "Belum ada riwayat pemesanan")
            return
        
        # Tampilkan Card 1
        if len(self.riwayat_list) > 0:
            self.tampilkan_card(0, self.riwayat_list[0])
            if hasattr(self, 'frame_3'):
                self.frame_3.setVisible(True)
        else:
            if hasattr(self, 'frame_3'):
                self.frame_3.setVisible(False)
        
        # Tampilkan Card 2
        if len(self.riwayat_list) > 1:
            self.tampilkan_card(1, self.riwayat_list[1])
            if hasattr(self, 'frame_5'):
                self.frame_5.setVisible(True)
        else:
            if hasattr(self, 'frame_5'):
                self.frame_5.setVisible(False)
    
    def tampilkan_card(self, card_index, transaksi):
        """
        Tampilkan data transaksi di card
        card_index: 0 untuk card pertama (frame_3), 1 untuk card kedua (frame_5)
        """
        # Mapping label untuk setiap card
        if card_index == 0:
            # Card 1 (frame_3)
            poster_label = 'label_21'
            judul_label = 'label'
            tanggal_label = 'label_2'
            kursi_label = 'label_3'
            durasi_label = 'label_4'
            harga_label = 'label_5'
        else:
            # Card 2 (frame_5)
            poster_label = 'label_22'
            judul_label = 'label_10'
            tanggal_label = 'label_11'
            kursi_label = 'label_12'
            durasi_label = 'label_13'
            harga_label = 'label_14'
        
        # Update Poster
        if hasattr(self, poster_label):
            label = getattr(self, poster_label)
            
            # Cari data film untuk mendapatkan poster
            film = self.main.film_db.get_film_by_id(
                self.get_film_id_from_transaksi(transaksi)
            )
            
            if film and film.get('poster'):
                img_path = os.path.join(os.path.dirname(__file__), 'images', film['poster'])
                if os.path.exists(img_path):
                    pixmap = QPixmap(img_path)
                    label.setPixmap(
                        pixmap.scaled(label.size(), 
                                    Qt.IgnoreAspectRatio, 
                                    Qt.SmoothTransformation)
                    )
                    label.setScaledContents(True)
        
        # Update Judul Film
        if hasattr(self, judul_label):
            getattr(self, judul_label).setText(transaksi['judul'])
        
        # Update Tanggal
        if hasattr(self, tanggal_label):
            tanggal = str(transaksi['tanggal'])
            # Format tanggal jika perlu
            try:
                from datetime import datetime
                if isinstance(tanggal, str):
                    tgl_obj = datetime.strptime(tanggal, '%Y-%m-%d')
                    bulan = ['Januari', 'Februari', 'Maret', 'April', 'Mei', 'Juni',
                            'Juli', 'Agustus', 'September', 'Oktober', 'November', 'Desember']
                    tanggal_formatted = f"{tgl_obj.day} {bulan[tgl_obj.month-1]} {tgl_obj.year}"
                    getattr(self, tanggal_label).setText(tanggal_formatted)
                else:
                    getattr(self, tanggal_label).setText(str(tanggal))
            except:
                getattr(self, tanggal_label).setText(str(tanggal))
        
        # Update Kursi
        if hasattr(self, kursi_label):
            kursi = transaksi.get('kursi', '-')
            getattr(self, kursi_label).setText(kursi if kursi else '-')
        
        # Update Durasi
        if hasattr(self, durasi_label):
            durasi = transaksi.get('durasi', '-')
            getattr(self, durasi_label).setText(f"{durasi} Menit" if durasi else '-')
        
        # Update Total Harga
        if hasattr(self, harga_label):
            total = f"Rp {transaksi['total_harga']:,.0f}".replace(',', '.')
            getattr(self, harga_label).setText(f"Total Harga : {total}")
    
    def get_film_id_from_transaksi(self, transaksi):
        """Helper untuk mendapatkan film_id dari transaksi"""
        # Ambil jadwal_id dari transaksi untuk mendapatkan film_id
        jadwal = self.main.jadwal_db.get_jadwal_by_id(transaksi.get('jadwal_id'))
        if jadwal:
            return jadwal.get('film_id')
        return None
    
    def cetak_tiket_card(self, card_index):
        """Cetak tiket dari card tertentu"""
        if card_index >= len(self.riwayat_list):
            QMessageBox.warning(self, "Error", "Data transaksi tidak ditemukan!")
            return
        
        transaksi = self.riwayat_list[card_index]
        transaksi_id = transaksi['id_transaksi']
        
        # Ambil detail lengkap transaksi
        transaksi_detail = self.main.transaksi_db.get_transaksi_by_id(transaksi_id)
        
        if not transaksi_detail:
            QMessageBox.warning(self, "Error", "Data transaksi tidak ditemukan!")
            return
        
        # Dialog pilihan cetak
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Question)
        msg.setWindowTitle("Cetak Tiket")
        msg.setText(f"Cetak tiket untuk:\n{transaksi['judul']}\n\nPilih cara mencetak:")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel)
        
        btn_printer = msg.button(QMessageBox.Yes)
        btn_printer.setText("🖨️ Printer")
        
        btn_pdf = msg.button(QMessageBox.No)
        btn_pdf.setText("📄 Save PDF")
        
        btn_cancel = msg.button(QMessageBox.Cancel)
        btn_cancel.setText("Batal")
        
        result = msg.exec_()
        
        if result == QMessageBox.Yes:
            self.cetak_ke_printer(transaksi_detail)
        elif result == QMessageBox.No:
            self.cetak_ke_pdf(transaksi_detail)
    
    def cetak_ke_printer(self, transaksi):
        """Cetak tiket ke printer"""
        from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
        
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPrinter.A4)
        
        dialog = QPrintDialog(printer, self)
        
        if dialog.exec_() == QPrintDialog.Accepted:
            self.print_ticket(printer, transaksi)
            QMessageBox.information(
                self, 
                "Sukses", 
                f"Tiket No. {transaksi['id_transaksi']} berhasil dicetak!"
            )
    
    def cetak_ke_pdf(self, transaksi):
        """Cetak tiket ke PDF"""
        from PyQt5.QtWidgets import QFileDialog
        from PyQt5.QtPrintSupport import QPrinter
        
        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Simpan Tiket",
            f"E-Ticket_{transaksi['id_transaksi']}_{transaksi['judul']}.pdf",
            "PDF Files (*.pdf)"
        )
        
        if filename:
            printer = QPrinter(QPrinter.HighResolution)
            printer.setOutputFormat(QPrinter.PdfFormat)
            printer.setOutputFileName(filename)
            printer.setPageSize(QPrinter.A4)
            
            self.print_ticket(printer, transaksi)
            
            QMessageBox.information(
                self, 
                "Sukses", 
                f"Tiket berhasil disimpan ke:\n{filename}"
            )
    
    def print_ticket(self, printer, transaksi):
        """Generate dan print tiket dengan format profesional"""
        from PyQt5.QtGui import QTextDocument, QTextCursor, QTextCharFormat, QFont
        
        document = QTextDocument()
        cursor = QTextCursor(document)
        
        # Style untuk header
        header_format = QTextCharFormat()
        header_format.setFontPointSize(24)
        header_format.setFontWeight(QFont.Bold)
        
        # Style untuk title
        title_format = QTextCharFormat()
        title_format.setFontPointSize(16)
        title_format.setFontWeight(QFont.Bold)
        
        # Style untuk label
        label_format = QTextCharFormat()
        label_format.setFontPointSize(12)
        label_format.setFontWeight(QFont.Bold)
        
        # Style untuk value
        value_format = QTextCharFormat()
        value_format.setFontPointSize(12)
        
        # Header Cinema
        cursor.setCharFormat(header_format)
        cursor.insertText("🎬 CINEMATION BIOSKOP\n")
        cursor.insertText("=" * 50 + "\n\n")
        
        # E-Ticket Title
        cursor.setCharFormat(title_format)
        cursor.insertText("E-TICKET PEMESANAN\n\n")
        
        # Nomor Transaksi
        cursor.setCharFormat(label_format)
        cursor.insertText("No. Transaksi: ")
        cursor.setCharFormat(value_format)
        cursor.insertText(f"{transaksi['id_transaksi']}\n")
        
        cursor.setCharFormat(label_format)
        cursor.insertText("Tanggal Pesan: ")
        cursor.setCharFormat(value_format)
        cursor.insertText(f"{transaksi['tanggal_pesan']}\n\n")
        
        # Separator
        cursor.insertText("-" * 50 + "\n\n")
        
        # Detail Film
        cursor.setCharFormat(title_format)
        cursor.insertText("DETAIL FILM\n\n")
        
        cursor.setCharFormat(label_format)
        cursor.insertText("Judul Film: ")
        cursor.setCharFormat(value_format)
        cursor.insertText(f"{transaksi['judul']}\n")
        
        cursor.setCharFormat(label_format)
        cursor.insertText("Durasi: ")
        cursor.setCharFormat(value_format)
        durasi = transaksi.get('durasi', '-')
        cursor.insertText(f"{durasi} Menit\n\n")
        
        # Detail Jadwal
        cursor.setCharFormat(title_format)
        cursor.insertText("DETAIL JADWAL\n\n")
        
        cursor.setCharFormat(label_format)
        cursor.insertText("Studio: ")
        cursor.setCharFormat(value_format)
        cursor.insertText(f"{transaksi['nama_studio']}\n")
        
        cursor.setCharFormat(label_format)
        cursor.insertText("Tanggal: ")
        cursor.setCharFormat(value_format)
        cursor.insertText(f"{transaksi['tanggal']}\n")
        
        cursor.setCharFormat(label_format)
        cursor.insertText("Jam Mulai: ")
        cursor.setCharFormat(value_format)
        jam = str(transaksi['jam_mulai'])[:5]
        cursor.insertText(f"{jam}\n")
        
        cursor.setCharFormat(label_format)
        cursor.insertText("Kursi: ")
        cursor.setCharFormat(value_format)
        kursi = transaksi.get('kursi', '-')
        cursor.insertText(f"{kursi if kursi else '-'}\n\n")
        
        # Separator
        cursor.insertText("-" * 50 + "\n\n")
        
        # Total Pembayaran
        cursor.setCharFormat(title_format)
        cursor.insertText("TOTAL PEMBAYARAN\n\n")
        
        cursor.setCharFormat(label_format)
        cursor.insertText("Total: ")
        cursor.setCharFormat(value_format)
        total = f"Rp {transaksi['total_harga']:,.0f}".replace(',', '.')
        cursor.insertText(f"{total}\n")
        
        cursor.setCharFormat(label_format)
        cursor.insertText("Status: ")
        cursor.setCharFormat(value_format)
        status = transaksi.get('status', 'pending').upper()
        cursor.insertText(f"{status}\n\n")
        
        # Footer
        cursor.insertText("=" * 50 + "\n\n")
        cursor.setCharFormat(value_format)
        cursor.insertText("Terima kasih telah menggunakan layanan kami!\n")
        cursor.insertText("Harap tunjukkan e-ticket ini di loket kasir.\n")
        cursor.insertText("Selamat menikmati film!\n\n")
        
        cursor.insertText("* Tiket tidak dapat dikembalikan\n")
        cursor.insertText("* Harap datang 15 menit sebelum film dimulai\n")
        cursor.insertText("* Dilarang membawa makanan dan minuman dari luar\n")
        
        # Print dokumen
        document.print_(printer)
    
    def konfirmasi_selesai(self, card_index):
        """Konfirmasi pesanan selesai"""
        if card_index >= len(self.riwayat_list):
            return
        
        transaksi = self.riwayat_list[card_index]
        
        reply = QMessageBox.question(
            self,
            'Konfirmasi',
            f'Apakah pesanan untuk film "{transaksi["judul"]}" sudah selesai?',
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            # Update status transaksi jika diperlukan
            # Atau bisa hapus dari tampilan
            QMessageBox.information(
                self,
                "Sukses",
                "Terima kasih! Pesanan telah dikonfirmasi selesai."
            )
            
            # Reload riwayat
            self.load_riwayat()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = MainWindow()
    sys.exit(app.exec_())