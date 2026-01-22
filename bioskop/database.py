import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self):
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = "db_bioskop"
        self.connection = None
        
    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Koneksi ke database berhasil")
                return True
        except Error as e:
            print(f"Error saat koneksi ke database: {e}")
            return False
    
    def disconnect(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Koneksi database ditutup")
    
    def execute_query(self, query, params=None):
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor.lastrowid
        except Error as e:
            print(f"Error executing query: {e}")
            print(f"Query: {query}")
            print(f"Params: {params}")
            return None
    
    def fetch_data(self, query, params=None):
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchall()
            cursor.close()
            return result
        except Error as e:
            print(f"Error fetching data: {e}")
            print(f"Query: {query}")
            return None
    
    def fetch_one(self, query, params=None):
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            print(f"Error fetching data: {e}")
            print(f"Query: {query}")
            return None


class FilmDB:
    def __init__(self, db):
        self.db = db
    
    def get_all_films(self, status='tayang'):
        """Mendapatkan semua film berdasarkan status"""
        query = "SELECT * FROM film WHERE status = %s ORDER BY id_film"
        return self.db.fetch_data(query, (status,))
    
    def get_film_by_id(self, id_film):
        """Mendapatkan detail film berdasarkan ID"""
        query = "SELECT * FROM film WHERE id_film = %s"
        return self.db.fetch_one(query, (id_film,))
    
    def search_films(self, keyword):
        """Mencari film berdasarkan judul"""
        query = "SELECT * FROM film WHERE judul LIKE %s AND status = 'tayang'"
        return self.db.fetch_data(query, (f"%{keyword}%",))
    
    def add_film(self, judul, genre, durasi, rating, deskripsi, poster, status='tayang'):
        """Menambah film baru"""
        query = """
            INSERT INTO film (judul, genre, durasi, rating, deskripsi, poster, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        return self.db.execute_query(query, (judul, genre, durasi, rating, deskripsi, poster, status))


class JadwalDB:
    def __init__(self, db):
        self.db = db
    
    def get_jadwal_by_film(self, film_id):
        """Mendapatkan semua jadwal untuk film tertentu"""
        query = """
            SELECT j.*, s.nama_studio, s.kapasitas 
            FROM jadwal j
            JOIN studio s ON j.studio_id = s.id_studio
            WHERE j.film_id = %s
            ORDER BY j.tanggal, j.jam_mulai
        """
        return self.db.fetch_data(query, (film_id,))
    
    def get_jadwal_by_id(self, jadwal_id):
        """Mendapatkan detail jadwal beserta info film dan studio"""
        query = """
            SELECT j.*, s.nama_studio, s.kapasitas, f.judul, f.poster, f.durasi, f.genre
            FROM jadwal j
            JOIN studio s ON j.studio_id = s.id_studio
            JOIN film f ON j.film_id = f.id_film
            WHERE j.id_jadwal = %s
        """
        return self.db.fetch_one(query, (jadwal_id,))
    
    def get_all_jadwal(self):
        """Mendapatkan semua jadwal"""
        query = """
            SELECT j.*, s.nama_studio, f.judul
            FROM jadwal j
            JOIN studio s ON j.studio_id = s.id_studio
            JOIN film f ON j.film_id = f.id_film
            ORDER BY j.tanggal, j.jam_mulai
        """
        return self.db.fetch_data(query)


class KursiDB:
    def __init__(self, db):
        self.db = db
    
    def get_kursi_by_studio(self, studio_id):
        """Mendapatkan semua kursi di studio tertentu"""
        query = "SELECT * FROM kursi WHERE studio_id = %s ORDER BY kode_kursi"
        return self.db.fetch_data(query, (studio_id,))
    
    def get_kursi_terpesan(self, jadwal_id):
        """Mendapatkan kursi yang sudah dipesan untuk jadwal tertentu"""
        query = """
            SELECT DISTINCT k.kode_kursi, k.id_kursi
            FROM kursi k
            JOIN detail_transaksi dt ON k.id_kursi = dt.kursi_id
            JOIN transaksi t ON dt.transaksi_id = t.id_transaksi
            WHERE t.jadwal_id = %s AND t.status IN ('paid', 'pending')
        """
        return self.db.fetch_data(query, (jadwal_id,))
    
    def get_kursi_by_kode(self, studio_id, kode_kursi):
        """Mendapatkan kursi berdasarkan kode dan studio"""
        query = "SELECT * FROM kursi WHERE studio_id = %s AND kode_kursi = %s"
        return self.db.fetch_one(query, (studio_id, kode_kursi))


class TransaksiDB:
    def __init__(self, db):
        self.db = db
    
    def create_transaksi(self, user_id, jadwal_id, total_harga, status='pending'):
        """Membuat transaksi baru"""
        query = """
            INSERT INTO transaksi (user_id, jadwal_id, total_harga, status, tanggal_pesan)
            VALUES (%s, %s, %s, %s, NOW())
        """
        return self.db.execute_query(query, (user_id, jadwal_id, total_harga, status))
    
    def add_detail_transaksi(self, transaksi_id, kursi_id):
        """Menambah detail transaksi (kursi yang dipesan)"""
        query = """
            INSERT INTO detail_transaksi (transaksi_id, kursi_id)
            VALUES (%s, %s)
        """
        return self.db.execute_query(query, (transaksi_id, kursi_id))
    
    def update_status_transaksi(self, transaksi_id, status):
        """Update status transaksi"""
        query = "UPDATE transaksi SET status = %s WHERE id_transaksi = %s"
        return self.db.execute_query(query, (status, transaksi_id))
    
    def get_transaksi_by_user(self, user_id):
        """Mendapatkan riwayat transaksi user"""
        query = """
            SELECT t.id_transaksi, t.user_id, t.jadwal_id, t.tanggal_pesan, 
                   t.total_harga, t.status,
                   j.tanggal, j.jam_mulai, j.film_id,
                   f.judul, f.poster, f.durasi, f.genre, f.rating,
                   s.nama_studio, s.kapasitas,
                   GROUP_CONCAT(k.kode_kursi ORDER BY k.kode_kursi SEPARATOR ', ') as kursi
            FROM transaksi t
            JOIN jadwal j ON t.jadwal_id = j.id_jadwal
            JOIN film f ON j.film_id = f.id_film
            JOIN studio s ON j.studio_id = s.id_studio
            LEFT JOIN detail_transaksi dt ON t.id_transaksi = dt.transaksi_id
            LEFT JOIN kursi k ON dt.kursi_id = k.id_kursi
            WHERE t.user_id = %s
            GROUP BY t.id_transaksi
            ORDER BY t.tanggal_pesan DESC
        """
        return self.db.fetch_data(query, (user_id,))
    
    def get_transaksi_by_id(self, transaksi_id):
        """Mendapatkan detail transaksi berdasarkan ID"""
        query = """
            SELECT t.id_transaksi, t.user_id, t.jadwal_id, t.tanggal_pesan, 
                   t.total_harga, t.status,
                   j.tanggal, j.jam_mulai, j.film_id,
                   f.judul, f.poster, f.durasi, f.genre, f.rating,
                   s.nama_studio, s.kapasitas,
                   GROUP_CONCAT(k.kode_kursi ORDER BY k.kode_kursi SEPARATOR ', ') as kursi
            FROM transaksi t
            JOIN jadwal j ON t.jadwal_id = j.id_jadwal
            JOIN film f ON j.film_id = f.id_film
            JOIN studio s ON j.studio_id = s.id_studio
            LEFT JOIN detail_transaksi dt ON t.id_transaksi = dt.transaksi_id
            LEFT JOIN kursi k ON dt.kursi_id = k.id_kursi
            WHERE t.id_transaksi = %s
            GROUP BY t.id_transaksi
        """
        return self.db.fetch_one(query, (transaksi_id,))
    
    def get_all_transaksi(self):
        """Mendapatkan semua transaksi (untuk admin)"""
        query = """
            SELECT t.*, u.nama as nama_user, j.tanggal, f.judul
            FROM transaksi t
            JOIN users u ON t.user_id = u.id_user
            JOIN jadwal j ON t.jadwal_id = j.id_jadwal
            JOIN film f ON j.film_id = f.id_film
            ORDER BY t.tanggal_pesan DESC
        """
        return self.db.fetch_data(query)


class UserDB:
    def __init__(self, db):
        self.db = db
    
    def login(self, email, password):
        """Login user"""
        query = "SELECT * FROM users WHERE email = %s AND password = %s"
        return self.db.fetch_one(query, (email, password))
    
    def register(self, nama, email, password, no_hp, role='customer'):
        """Register user baru"""
        # Cek apakah email sudah terdaftar
        check_query = "SELECT * FROM users WHERE email = %s"
        existing = self.db.fetch_one(check_query, (email,))
        
        if existing:
            return None
        
        query = """
            INSERT INTO users (nama, email, password, no_hp, role)
            VALUES (%s, %s, %s, %s, %s)
        """
        return self.db.execute_query(query, (nama, email, password, no_hp, role))
    
    def get_user_by_id(self, user_id):
        """Mendapatkan user berdasarkan ID"""
        query = "SELECT * FROM users WHERE id_user = %s"
        return self.db.fetch_one(query, (user_id,))
    
    def get_all_users(self):
        """Mendapatkan semua user"""
        query = "SELECT * FROM users ORDER BY id_user"
        return self.db.fetch_data(query)
    
    def update_user(self, user_id, nama, email, no_hp):
        """Update data user"""
        query = """
            UPDATE users 
            SET nama = %s, email = %s, no_hp = %s
            WHERE id_user = %s
        """
        return self.db.execute_query(query, (nama, email, no_hp, user_id))


class StudioDB:
    def __init__(self, db):
        self.db = db
    
    def get_all_studios(self):
        """Mendapatkan semua studio"""
        query = "SELECT * FROM studio ORDER BY id_studio"
        return self.db.fetch_data(query)
    
    def get_studio_by_id(self, studio_id):
        """Mendapatkan studio berdasarkan ID"""
        query = "SELECT * FROM studio WHERE id_studio = %s"
        return self.db.fetch_one(query, (studio_id,))