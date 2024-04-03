import json
import sqlite3

# Carica i dati dal file JSON
with open('studenti.json', 'r') as file:
    student_records = json.load(file)

# Connessione al database SQLite3
conn = sqlite3.connect('studenti.db')
cursor = conn.cursor()

# Comandi SQL per la creazione della tabella studenti con tutte le materie
cursor.execute('''CREATE TABLE IF NOT EXISTS studenti (
                    ID INTEGER PRIMARY KEY AUTOINCREMENT,
                    ALUNNO TEXT,
                    RELIGIONE TEXT,
                    LINGUA_E_LETTERATURA TEXT,
                    LINGUA_INGLESE TEXT,
                    STORIA TEXT,
                    EDUCAZIONE_CIVICA TEXT,
                    MATEMATICA TEXT,
                    DIRITTO_ED_ECONOMIA TEXT,
                    FISICA TEXT,
                    CHIMICA TEXT,
                    TECN_INFORMATICHE TEXT,
                    TECN_E_TECN_DI_RAPPR TEXT,
                    SC_DELLA_TERRA_GEO TEXT,
                    SCIENZE_MOT_E_SPORT TEXT,
                    SECONDA_LINGUA TEXT,
                    SISTEMI TEXT,
                    COMPLEMENTI TEXT,
                    STA TEXT,
                    COMPORTAMENTO TEXT,
                    MEDIA REAL,
                    ESITO TEXT,
                    CLASSE TEXT
                )''')

# Inserisce i dati degli studenti nel database SQLite3
for record in student_records:
    cursor.execute('''INSERT INTO studenti (ALUNNO, RELIGIONE, LINGUA_E_LETTERATURA, LINGUA_INGLESE,
                      STORIA, EDUCAZIONE_CIVICA, MATEMATICA, DIRITTO_ED_ECONOMIA, FISICA, CHIMICA,
                      TECN_INFORMATICHE, TECN_E_TECN_DI_RAPPR, SC_DELLA_TERRA_GEO, SCIENZE_MOT_E_SPORT,
                      SECONDA_LINGUA, SISTEMI, COMPLEMENTI, STA, COMPORTAMENTO, MEDIA, ESITO, CLASSE)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (record.get('ALUNNO'), record.get('RELIGIONE'), record.get('LINGUA E LETT.IT'),
                       record.get('LINGUA INGLESE'), record.get('STORIA'), record.get('EDUCAZIONE CIVICA'),
                       record.get('MATEMATICA'), record.get('DIRITTO ED ECONOMIA'), record.get('FISICA'),
                       record.get('CHIMICA'), record.get('TECN.INFORMATICHE'), record.get('TECN.E TECN.DI RAPPR'),
                       record.get('SC.DELLA TERRA/GEO'), record.get('SCIENZE MOT. E SPORT'),
                       record.get('SECONDA LINGUA'), record.get('SISTEMI'), record.get('COMPLEMENTI'),
                       record.get('STA'), record.get('COMPORTAMENTO'), record.get('MEDIA'),
                       record.get('ESITO'), record.get('CLASSE')))

# Salvataggio dei cambiamenti e chiusura della connessione
conn.commit()
conn.close()

print("Dati degli studenti caricati con successo su SQLite3.")
