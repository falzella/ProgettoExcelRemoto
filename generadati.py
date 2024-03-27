import pandas as pd
import json
import re
import sqlite3

# Leggi il file Excel
df = pd.read_excel('1Sin.xls', header=None)

# Trova la riga contenente l'informazione sulla classe
class_info_row = df[df.apply(lambda row: row.astype(str).str.contains('CLASSE:').any(), axis=1)].iloc[0]

class_info = class_info_row.values[5]


# Trova indice della classe

index_class = 0
while index_class < len(class_info_row):
    if class_info_row.values[index_class] == 'CLASSE:':
        break
    index_class += 1

#trovo valore classe
i = index_class + 1
while i < len(class_info_row):
    if pd.notna(class_info_row.values[i]):
        class_info = class_info_row.values[i]
        break
    i += 1



classe = class_info

# Trova l'indice della riga contenente la tabella degli studenti
start_index = df[df.apply(lambda row: row.astype(str).str.contains('Alunno').any(), axis=1)].index[0]

# Trova l'indice della riga contenente la data e il dirigente scolastico
end_index = df[df.apply(lambda row: row.astype(str).str.contains('Data').any(), axis=1)].index[0]

# Salta le righe vuote e l'ultima riga con data e dirigente scolastico
student_df = df.iloc[start_index:end_index].dropna(how='all')

# Assegna le colonne al DataFrame degli studenti
student_df.columns = student_df.iloc[0]

# Rimuovi la riga di intestazione
student_df = student_df[1:]

# Rimuovi colonne con titolo vuoto
student_df = student_df.dropna(axis=1, how='all')

# Inserisci la colonna 'Classe' con il valore estratto
student_df['Classe'] = classe

# Converte il DataFrame degli studenti in un dizionario di record
student_records = student_df.to_dict(orient='records')

# Scrivi il dizionario di record su un file JSON
with open('studenti.json', 'w') as file:
    json.dump(student_records, file, indent=4)

# Connessione al database SQLite3
conn = sqlite3.connect('studenti.db')
cursor = conn.cursor()

# Crea una tabella nel database SQLite3
cursor.execute('''CREATE TABLE IF NOT EXISTS studenti (
                    Alunno TEXT PRIMARY KEY,
                    RELIGIONE TEXT,
                    LINGUA_E_LETTERATURA TEXT,
                    LINGUA_INGLESE TEXT,
                    STORIA TEXT,
                    EDUCAZIONE_CIVICA TEXT,
                    MATEMATICA TEXT,
                    DIRITTO_ED_ECONOMIA TEXT,
                    FISICA TEXT,
                    CHIMICA TEXT,
                    Tecn_informatiche TEXT,
                    Tecn_e_Tecn_di_rappr TEXT,
                    SC_DELLA_TERRA_GEO TEXT,
                    SCIENZE_MOT_E_SPORT TEXT,
                    COMPORTAMENTO TEXT,
                    Media REAL,
                    Esito TEXT,
                    Classe TEXT
                )''')

# Inserisce i dati degli studenti nel database SQLite3
for record in student_records:
    cursor.execute('''INSERT INTO studenti (Alunno, RELIGIONE, LINGUA_E_LETTERATURA, LINGUA_INGLESE,
                      STORIA, EDUCAZIONE_CIVICA, MATEMATICA, DIRITTO_ED_ECONOMIA, FISICA, CHIMICA,
                      Tecn_informatiche, Tecn_e_Tecn_di_rappr, SC_DELLA_TERRA_GEO, SCIENZE_MOT_E_SPORT,
                      COMPORTAMENTO, Media, Esito, Classe)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (record['Alunno'], record.get('RELIGIONE'), record.get('LINGUA E LETT.IT'),
                       record.get('LINGUA INGLESE'), record.get('STORIA'), record.get('EDUCAZIONE CIVICA'),
                       record.get('MATEMATICA'), record.get('DIRITTO ED ECONOMIA'), record.get('FISICA'),
                       record.get('CHIMICA'), record.get('Tecn.informatiche'), record.get('Tecn.e Tecn.di rappr'),
                       record.get('SC.DELLA TERRA/GEO'), record.get('SCIENZE MOT. E SPORT'),
                       record.get('COMPORTAMENTO'), record.get('Media'), record.get('Esito'), record.get('Classe')))

# Salvataggio dei cambiamenti e chiusura della connessione
conn.commit()
conn.close()

print("Dati degli studenti caricati con successo su SQLite3.")
