import sqlite3
import psycopg2
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
SQLITE_PATH = BASE_DIR / 'db.sqlite3'

sqlite_conn = sqlite3.connect(SQLITE_PATH)
sqlite_cursor = sqlite_conn.cursor()

pg_conn = psycopg2.connect(
    dbname='portal_db_4363',
    user='portal_user',
    password='mkGIcXKLkBsZg5cfdlQGqKpeRrdmBsEu',
    host='dpg-dagqhiek1f9s73cjtpqg-a.virginia-postgres.render.com',
    port='5432',
    sslmode='require'
)
pg_cursor = pg_conn.cursor()

try:
    # 1. Kopjojmë Kategoritë (tabela: lajmet_kategoria)
    sqlite_cursor.execute("SELECT * FROM lajmet_kategoria")
    kategorite = sqlite_cursor.fetchall()
    for kat in kategorite:
        placeholders = ", ".join(["%s"] * len(kat))
        pg_cursor.execute(f"INSERT INTO lajmet_kategoria VALUES ({placeholders}) ON CONFLICT DO NOTHING", kat)
    print(f"U kopjuan {len(kategorite)} kategori.")

    # 2. Kopjojmë Artikujt (tabela: lajmet_artikull)
    sqlite_cursor.execute("SELECT * FROM lajmet_artikull")
    artikujt = sqlite_cursor.fetchall()
    for artikull in artikujt:
        placeholders = ", ".join(["%s"] * len(artikull))
        pg_cursor.execute(f"INSERT INTO lajmet_artikull VALUES ({placeholders}) ON CONFLICT DO NOTHING", artikull)
    print(f"U kopjuan {len(artikujt)} artikuj/lajme.")

    pg_conn.commit()
    print("\n>>> Transferimi u krye me sukses! <<<")

except Exception as e:
    print(f"Gabim gjatë transferimit: {e}")

finally:
    sqlite_conn.close()
    pg_conn.close()