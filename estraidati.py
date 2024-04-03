import sqlite3

# Connessione al database SQLite3
conn = sqlite3.connect('studenti.db')
cursor = conn.cursor()

# Funzione per vedere tutti i cognomi degli studenti
def vedere_cognomi():
    query = "SELECT ALUNNO FROM studenti"
    cursor.execute(query)
    cognomi = cursor.fetchall()
    for cognome in cognomi:
        print(cognome[0])

# Funzione per vedere tutte le classi
def vedere_classi():
    query = "SELECT DISTINCT CLASSE FROM studenti"
    cursor.execute(query)
    classi = cursor.fetchall()
    for classe in classi:
        print(classe[0])

# Funzione per vedere gli studenti in base a determinati criteri
def vedere_studenti():
    classe = input("Inserisci la classe su cui operare: ")
    print("Scegli il criterio:")
    print("1. Ammessi")
    print("2. Non ammessi")
    print("3. Sospensione del giudizio")
    print("4. Media superiore a valore specifico")
    scelta_criterio = input("Scelta: ")

    if scelta_criterio == '4':
        media = float(input("Inserisci la media soglia: "))
        query = f"SELECT ALUNNO FROM studenti WHERE CLASSE=? AND MEDIA > {media}"
    else:
        criteri = {
            '1': 'Ammesso/a',
            '2': 'Non Ammesso/a',
            '3': 'Sospensione del giudizio'
        }
        criterio = criteri.get(scelta_criterio)
        query = f"SELECT ALUNNO FROM studenti WHERE CLASSE=? AND ESITO='{criterio}'"
    
    cursor.execute(query, (classe,))
    studenti = cursor.fetchall()
    for studente in studenti:
        print(studente[0])

# Funzione principale per eseguire le azioni richieste dall'utente
def main():
    while True:
        print("\nCosa desideri fare?")
        print("1. Vedere tutti i cognomi degli studenti")
        print("2. Vedere tutte le classi")
        print("3. Vedere gli studenti in base a determinati criteri")
        print("4. Uscire")
        scelta = input("Scelta: ")

        if scelta == '1':
            vedere_cognomi()
        elif scelta == '2':
            vedere_classi()
        elif scelta == '3':
            vedere_studenti()
        elif scelta == '4':
            break
        else:
            print("Scelta non valida. Riprova.")

# Esecuzione della funzione principale
if __name__ == "__main__":
    main()

# Chiusura della connessione al database
conn.close()
