
# Adatbázis kapcsolat beállítása (MySQL példa)
DATABASE_USR = "root"
DATABASE_PSW = "root"
DATABASE_URL = "localhost"
DATABASE_PORT = 3306
DATABASE_NAME = "fitness_db"
DATABASE_URL = f"mysql+pymysql://{DATABASE_USR}:{DATABASE_PSW}@{DATABASE_URL}:{DATABASE_PORT}/{DATABASE_NAME}"
