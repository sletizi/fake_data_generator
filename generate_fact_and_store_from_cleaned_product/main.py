import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Inizializzare Faker
fake = Faker()

# Costante per il numero desiderato di record nella fact table delle vendite
NUM_SALES_RECORDS = 3000000

# Mappatura store con dettagli
store_mapping = {
    1: {'StoreName': 'Coop Marche', 'City': 'Ancona', 'Latitude': 43.6158, 'Longitude': 13.5189, 'Area': 'Centro'},
    2: {'StoreName': 'Coop Lazio', 'City': 'Roma', 'Latitude': 41.9028, 'Longitude': 12.4964, 'Area': 'Centro'},
    3: {'StoreName': 'Coop Campania', 'City': 'Napoli', 'Latitude': 40.8518, 'Longitude': 14.2681, 'Area': 'Sud'},
    4: {'StoreName': 'Coop Lombardia', 'City': 'Milano', 'Latitude': 45.4642, 'Longitude': 9.1900, 'Area': 'Nord'},
    5: {'StoreName': 'Esselunga Toscana', 'City': 'Firenze', 'Latitude': 43.7696, 'Longitude': 11.2558, 'Area': 'Centro'},
    6: {'StoreName': 'Carrefour Piemonte', 'City': 'Torino', 'Latitude': 45.0703, 'Longitude': 7.6869, 'Area': 'Nord'},
    7: {'StoreName': 'Conad Sicilia', 'City': 'Palermo', 'Latitude': 38.1157, 'Longitude': 13.3613, 'Area': 'Sud'},
    8: {'StoreName': 'Pam Veneto', 'City': 'Venezia', 'Latitude': 45.4408, 'Longitude': 12.3155, 'Area': 'Nord'},
    9: {'StoreName': 'Lidl Puglia', 'City': 'Bari', 'Latitude': 41.1256, 'Longitude': 16.8639, 'Area': 'Sud'},
    10: {'StoreName': 'Eurospin Sardegna', 'City': 'Cagliari', 'Latitude': 39.2167, 'Longitude': 9.1106, 'Area': 'Sud'}
}

# Caricare il DataFrame dei prodotti dal file CSV
try:
    products_df = pd.read_csv('./products.csv')
except FileNotFoundError:
    print("Errore: il file 'product.csv' non è stato trovato. Assicurati che il file esista nella stessa directory dello script.")
    exit()

# Creare una lista di prodotti dal DataFrame
products = products_df.to_dict('records')

# Creare una lista di date per il periodo specificato
start_date = datetime(2019, 1, 1)
end_date = datetime(2024, 12, 31)
date_range = pd.date_range(start_date, end_date)

# Funzione per generare una singola riga della fact table delle vendite
def generate_sales_record(product, date):
    sales_volume = random.randint(0, 5)  # Ridotto il volume massimo per generare meno record per transazione
    base_sales_value = sales_volume * product['Price']
    sales_value = round(base_sales_value * (1 + random.uniform(0.05, 0.25)), 2)
    store_code = random.choice(list(store_mapping.keys()))  # Scegliere un codice negozio casuale
    store_warehouse = store_code if random.random() < 0.8 else random.choice(list(store_mapping.keys()))
    currency = random.choice(['EUR', 'USD', 'GBP'])  # Assegnare casualmente una valuta
    return {
        'ProductID': product['ProductID'],
        'Date': date,
        'SalesVolume': sales_volume,
        'SalesValue': sales_value,
        'StoreCode': store_code,
        'StoreWarehouse': store_warehouse,
        'Currency': currency
    }

# Generare la fact table delle vendite
sales_data = []
num_products = len(products)
num_days = len(date_range)

print(f"Generazione di al massimo {NUM_SALES_RECORDS} record di vendita...")

# Tenta di generare il numero target di record, con la possibilità che non tutti i prodotti vengano venduti ogni giorno
for _ in range(NUM_SALES_RECORDS):
    # Scegli un giorno casuale dall'intervallo di date
    random_date = random.choice(date_range)
    # Scegli un prodotto casuale dalla lista dei prodotti
    random_product = random.choice(products)
    # Genera un record di vendita per quel prodotto in quella data
    sales_record = generate_sales_record(random_product, random_date)
    sales_data.append(sales_record)

    if len(sales_data) % 100000 == 0:
        print(f"Generati {len(sales_data)} record di vendita...")
    if len(sales_data) >= NUM_SALES_RECORDS:
        break

# Creare il DataFrame delle vendite
sales_df = pd.DataFrame(sales_data)

# Creare il DataFrame di mapping Store
store_df = pd.DataFrame.from_dict(store_mapping, orient='index').reset_index().rename(columns={'index': 'StoreCode'})

# Salvare i dataset
sales_df.to_csv('daily_sales.csv', index=False)
store_df.to_csv('stores.csv', index=False)

print(f"Numero di record generati nella fact table delle vendite: {len(sales_df)}")
