import mysql.connector
from mysql.connector import Error

try:
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="db_bioskop"
    )
    
    if conn.is_connected():
        cursor = conn.cursor()
        
        # Ambil kursi yang sudah ada
        cursor.execute("SELECT kode_kursi FROM kursi WHERE studio_id = 2")
        existing = {row[0] for row in cursor.fetchall()}
        
        # Insert semua kursi A1-D7 untuk studio 2
        kursi_baru = []
        for row in "ABCD":
            for col in range(1, 8):
                kode = f"{row}{col}"
                if kode not in existing:
                    kursi_baru.append((2, kode))  # studio_id=2 (Frozen II)
        
        if kursi_baru:
            query = "INSERT INTO kursi (studio_id, kode_kursi) VALUES (%s, %s)"
            cursor.executemany(query, kursi_baru)
            conn.commit()
            print(f"✅ Berhasil menambahkan {len(kursi_baru)} kursi baru ke database")
            print(f"   Kursi baru: {', '.join([k[1] for k in kursi_baru])}")
        else:
            print("✅ Semua kursi sudah ada di database")
        
        # Tampilkan total kursi per studio
        cursor.execute("SELECT studio_id, COUNT(*) as jumlah FROM kursi GROUP BY studio_id")
        for studio_id, jumlah in cursor.fetchall():
            print(f"   Studio {studio_id}: {jumlah} kursi")
        
        cursor.close()
        conn.close()
        
except Error as e:
    print(f"❌ Error: {e}")
