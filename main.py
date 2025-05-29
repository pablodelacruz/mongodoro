import os
import random
import time
from datetime import datetime
from pymongo import MongoClient
from dotenv import load_dotenv
from faker import Faker

load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("MONGO_DB")
collection_name = os.getenv("MONGO_COLLECTION")
records_to_insert = int(os.getenv("RECORDS_TO_INSERT", 10))

client = MongoClient(mongo_uri)
db = client[db_name]

if collection_name in db.list_collection_names():
    db.drop_collection(collection_name)
    print(
        f"🗑️ Colección '{collection_name}' eliminada. Sera creada al insertar los datos")

collection = db[collection_name]
faker = Faker()


def generate_record() -> dict[str, str | int | float | datetime]:
    return {
        "no_documento": faker.numerify(text="###-#######-#").replace("-", ""),
        "nss": int(faker.numerify(text="##########")),
        "salario_ss": round(random.uniform(10000, 999999999.99), 2),
        "last_update": datetime.utcnow()
    }


registros = [generate_record() for _ in range(records_to_insert)]

inicio = time.time()
resultado = collection.insert_many(registros)
fin = time.time()
duracion = fin - inicio

print(
    f"\n✅ Se insertaron {len(resultado.inserted_ids)} registros en '{collection_name}'.")
print(f"⏱️ Tiempo de inserción: {duracion:.2f} segundos")

total = collection.count_documents({})
stats = db.command("collstats", collection_name)
db_stats = db.command("dbstats")

print(f"📄 Total de registros: {total}")
print(f"📦 Tamaño de la colección (solo datos): {stats['size'] / 1024:.2f} KB")
print(
    f"🧮 Tamaño promedio por documento: {stats.get('avgObjSize', 0):.2f} bytes")
print(
    f"💾 Tamaño de almacenamiento (incluye relleno): {stats['storageSize'] / 1024:.2f} KB")
print(
    f"🗃️ Tamaño total de la base de datos: {db_stats['dataSize'] / (1024 * 1024):.2f} MB\n")
client.close()
