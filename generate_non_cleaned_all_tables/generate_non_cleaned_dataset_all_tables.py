import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta

# Inizializzare Faker
fake = Faker()

# Liste di nomi di prodotti realmente esistenti per varie categorie
electronics = ['iPhone 13', 'Samsung Galaxy S21', 'MacBook Pro', 'Sony WH-1000XM4', 'iPad Pro']
furniture = ['IKEA Chair', 'IKEA Table', 'Sofa Set', 'Office Desk', 'Bookshelf']
toys = ['Lego Set', 'Barbie Doll', 'Hot Wheels', 'Puzzle', 'Board Game']
clothing = ['Nike T-Shirt', 'Adidas Sneakers', "Levi's Jeans", 'H&M Jacket', 'Zara Dress']
books = ['The Great Gatsby', '1984', 'To Kill a Mockingbird', 'Moby Dick', 'War and Peace']

# Dominio dei valori per la colonna Type
types = {
    'Electronics': ['TV', 'Smartphone', 'Hi-tech'],
    'Furniture': ['Chair', 'Table'],
    'Toys': ['Toy'],
    'Clothing': ['T-Shirt', 'Jacket'],
    'Books': ['EBook'],
    'Unknown': ['TV', 'Smartphone', 'Hi-tech', 'EBook', 'Jacket', 'T-Shirt', 'Chair', 'Table', 'Toy']
}

# Mappatura store con dettagli
store_mapping = {
    1: {'StoreName': 'Coop Marche', 'City': 'Ancona', 'Latitude': 43.6158, 'Longitude': 13.5189, 'Area': 'Centro'},
    2: {'StoreName': 'Coop Lazio', 'City': 'Roma', 'Latitude': 41.9028, 'Longitude': 12.4964, 'Area': 'Centro'},
    3: {'StoreName': 'Coop Campania', 'City': 'Napoli', 'Latitude': 40.8518, 'Longitude': 14.2681, 'Area': 'Sud'},
    4: {'StoreName': 'Coop Lombardia', 'City': 'Milano', 'Latitude': 45.4642, 'Longitude': 9.1900, 'Area': 'Nord'}
}

# Funzione per generare un ID prodotto univoco
def generate_unique_product_id(existing_ids):
    while True:
        product_id = fake.bothify(text='????-####')  # Genera una stringa alfanumerica di 8 caratteri
        if product_id not in existing_ids:
            existing_ids.add(product_id)
            return product_id

# Funzione per generare un singolo prodotto
def generate_product(existing_ids):
    product_id = generate_unique_product_id(existing_ids)

    # Generare categoria con 5% di valori nulli
    category = random.choices(
        [None, 'Electronics', 'Furniture', 'Toys', 'Clothing', 'Books'],
        weights=[5, 19, 19, 19, 19, 19],
        k=1
    )[0]

    if category == 'Electronics':
        product_name = random.choice(electronics)
    elif category == 'Furniture':
        product_name = random.choice(furniture)
    elif category == 'Toys':
        product_name = random.choice(toys)
    elif category == 'Clothing':
        product_name = random.choice(clothing)
    elif category == 'Books':
        product_name = random.choice(books)
    else:
        product_name = fake.word().capitalize() + ' ' + random.choice(['Pro', 'Max', 'Plus', 'Lite'])

    price = round(random.uniform(10, 1000), 2)
    stock = random.randint(1, 200)
    lead_time = random.randint(1, 10)  # Tempo di arrivo a magazzino in giorni

    # Generare "Managed by" con 70% IT, 20% UE, 10% null
    managed_by = random.choices(
        ['IT', 'UE', None],
        weights=[70, 20, 10],
        k=1
    )[0]

    # Assegnare un valore di Type basato sulla categoria
    if category is None:
        type_value = random.choice(types['Unknown'])
    else:
        type_value = random.choice(types[category])

    return {
        'ProductID': product_id,
        'ProductName': product_name,
        'Category': category,
        'Type': type_value,
        'Price': price,
        'Stock': stock,
        'LeadTime': lead_time,
        'ManagedBy': managed_by
    }

# Generare un dataset di prodotti
num_products = 100
existing_ids = set()
products = [generate_product(existing_ids) for _ in range(num_products)]

# Creare il DataFrame dei prodotti
products_df = pd.DataFrame(products)

# Creare una lista di date per il periodo 2022-2023
start_date = datetime(2022, 1, 1)
end_date = datetime(2024, 12, 31)
date_range = pd.date_range(start_date, end_date)

# Funzione per generare le vendite giornaliere per ciascun prodotto
def generate_daily_sales(product, date):
    sales_volume = random.randint(0, 10)  # Numero di pezzi venduti
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

for date in date_range:
    for product in products:
        sales_record = generate_daily_sales(product, date)
        sales_data.append(sales_record)

# Creare il DataFrame delle vendite
sales_df = pd.DataFrame(sales_data)

# Creare il DataFrame di mapping Store
store_df = pd.DataFrame.from_dict(store_mapping, orient='index').reset_index().rename(columns={'index': 'StoreCode'})

# Salvare i dataset
products_df.to_csv('products.csv', index=False)
sales_df.to_csv('daily_sales.csv', index=False)
store_df.to_csv('stores.csv', index=False)
