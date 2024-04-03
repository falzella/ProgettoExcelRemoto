import sys
import os
import pandas as pd
import json

# Verifica che sia stato fornito il nome del file Excel come argomento
if len(sys.argv) != 2:
    print("Lo script va richiamato così: python3 generadati.py <Excel_file>")
    sys.exit(1)

# Ottieni il nome del file Excel dall'argomento della riga di comando
excel_file = sys.argv[1]

# Verifica se il file Excel specificato esiste
if not os.path.exists(excel_file):
    print(f"Error: Excel file '{excel_file}' not found.")
    sys.exit(1)

# Leggi il file Excel
df = pd.read_excel(excel_file, header=None)

# Trova la riga contenente l'informazione sulla classe
class_info_row = df[df.apply(lambda row: row.astype(str).str.contains('CLASSE:').any(), axis=1)].iloc[0]

# Trova indice della classe
index_class = 0
while index_class < len(class_info_row):
    if class_info_row.values[index_class] == 'CLASSE:':
        break
    index_class += 1

# Trova valore classe
i = index_class + 1
while i < len(class_info_row):
    if pd.notna(class_info_row.values[i]):
        class_info = class_info_row.values[i]
        break
    i += 1

classe = class_info.split(' ')[0]

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

# Converti i nomi delle colonne in maiuscolo
student_df.columns = student_df.columns.str.upper()

# Converte il DataFrame degli studenti in un dizionario di record
student_records = student_df.to_dict(orient='records')

# Scrivi il dizionario di record su un file JSON
with open('studenti.json', 'w') as file:
    json.dump(student_records, file, indent=4)

print("Dati degli studenti scritti su studenti.json.")
