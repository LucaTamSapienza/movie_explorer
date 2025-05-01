# on docker-compose up --build, this file is executed to populate the database

import os
from backend.utils import inserisci_dati_da_file

data_file = "/app/data.tsv"

if os.path.exists(data_file): # just a check. 
    """ print("Inizio popolamento database...") """ # debugging purpose
    inserisci_dati_da_file(data_file)
    """ print("✅ Popolamento completato.") """
else:
    print(f"⚠️ File {data_file} non trovato, popolamento saltato.")