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
collection_name = os.getenv("MONGO_COLLECTION", "Empleados")
records_to_insert = int(os.getenv("RECORDS_TO_INSERT", "10"))

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
        "last_update": datetime.now()}


registros = [generate_record() for _ in range(records_to_insert)]

inicio = time.time()
resultado = collection.insert_many(registros)
fin = time.time()
duracion = fin - inicio
total = collection.count_documents({})
stats = db.command("collstats", collection_name)
db_stats = db.command("dbstats")

print(
    f"\n✅ Se insertaron {len(resultado.inserted_ids)} registros en '{collection_name}'.")
print(f"⏱️ Tiempo de inserción: {duracion:.2f} segundos")
print(f"📄 Total de registros: {total}")
print(f"📦 Tamaño de la colección (solo datos): {stats['size'] / 1024:.2f} KB")
print(
    f"🧮 Tamaño promedio por documento: {stats.get('avgObjSize', 0):.2f} bytes")
print(
    f"💾 Tamaño de almacenamiento (incluye relleno): {stats['storageSize'] / 1024:.2f} KB")
print(
    f"🗃️ Tamaño total de la base de datos: {db_stats['dataSize'] / (1024 * 1024):.2f} MB")


def search_no_document(collection, n: int, chunk_size: int):
    pipeline = [{"$sample": {"size": n}}, {
        "$project": {"no_documento": 1, "_id": 0}}]
    sampled_no_documento = list(collection.aggregate(pipeline))
    no_documentos = [doc["no_documento"] for doc in sampled_no_documento]

    start = time.time()
    for i in range(0, n, chunk_size):
        chunk = no_documentos[i:i+chunk_size]
        list(collection.find({"no_documento": {"$in": chunk}}))
    end = time.time()
    print(
        f"🔎 Tiempo para buscar {n} documentos en chunks de {chunk_size}: {end - start:.4f} segundos")


search_n = int(os.getenv("SEARCH_N", 100))
search_chunk = int(os.getenv("SEARCH_CHUNK", 10))
search_no_document(collection, search_n, search_chunk)


if DISPLAY_NO_DOCUMENTO := os.getenv("DISPLAY_NO_DOCUMENTO", "true").lower() == "true":
    print("\nLista de 'no_documento' en la colección:")
    for doc in collection.find({}, {"_id": 0, "no_documento": 1}):
        print(doc["no_documento"])


client.close()
