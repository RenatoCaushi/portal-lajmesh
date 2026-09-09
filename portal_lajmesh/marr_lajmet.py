import os
import sys
import sqlite3
import psycopg2
from pathlib import Path

# 1. Konfigurimi i shtigjeve që Django të ngarkojë settings
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
sys.path.append(str(BASE_DIR / 'portal_lajmesh'))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

import django
django.setup()

from django.contrib.auth.hashers import make_password

# 2. Lidhja me bazën lokale SQLite
SQLITE_PATH = BASE_DIR / 'db.sqlite3'
sqlite_conn = sqlite3.connect(SQLITE_PATH)
sqlite_cursor = sqlite_conn.cursor()

# 3. Lidhja direkte me PostgreSQL në Render (Mos i ndrysho parametrat këtu)
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
    # --- Kopjimi i Kategorive ---
    sqlite_cursor.execute("SELECT * FROM lajmet_kategoria")
    kategorite = sqlite_cursor.fetchall()
    for kat in kategorite:
        placeholders = ", ".join(["%s"] * len(kat))
        pg_cursor.execute(f"INSERT INTO lajmet_kategoria VALUES ({placeholders}) ON CONFLICT DO NOTHING", kat)
    print(f"U kopjuan {len(kategorite)} kategori.")

    # --- Kopjimi i Artikujve ---
    sqlite_cursor.execute("SELECT * FROM lajmet_artikull")
    artikujt = sqlite_cursor.fetchall()
    for artikull in artikujt:
        placeholders = ", ".join(["%s"] * len(artikull))
        pg_cursor.execute(f"INSERT INTO lajmet_artikull VALUES ({placeholders}) ON CONFLICT DO NOTHING", artikull)
    print(f"U kopjuan {len(artikujt)} artikuj/lajme.")

    # --- Krijimi / Përditësimi i Superuser-it me Kredencialet e Tua Lokale ---
    username = "Renatoo"          # Vendos emrin tënd të adminit lokal këtu
    raw_password = "FjalekalimiYtLokal"  # Vendos fjalëkalimin tënd lokal këtu
    hashed_password = make_password(raw_password)

    pg_cursor.execute("SELECT id FROM auth_user WHERE username = %s", (username,))
    user_exists = pg_cursor.fetchone()

    if not user_exists:
        insert_query = """
        INSERT INTO auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
        VALUES (%s, NULL, True, %s, '', '', 'admin@example.com', True, True, NOW())
        """
        pg_cursor.execute(insert_query, (hashed_password, username))
        print(f"Superuser '{username}' u krijua me sukses në Render!")
    else:
        update_query = "UPDATE auth_user SET password = %s, is_superuser = True, is_staff = True WHERE username = %s"
        pg_cursor.execute(update_query, (hashed_password, username))
        print(f"Fjalëkalimi për superuser-in '{username}' u përditësua me sukses!")

    # Ruajtja e ndryshimeve në PostgreSQL
    pg_conn.commit()
    print("\n>>> Procesi u përfundua me sukses! <<<")

except Exception as e:
    print(f"Gabim gjatë procesit: {e}")

finally:
    sqlite_conn.close()
    pg_conn.close()