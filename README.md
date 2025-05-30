## 🚀 Ejecución con Docker

Para ejecutar el script con Docker instalado, siga estos pasos:

1.  **📥 Clonar el repositorio**

    ```bash
    git clone https://github.com/pablodelacruz/mongodoro
    cd mongodoro
    ```

2.  **⚙️ Crear archivo `.env`**  
    Cree un archivo `.env` en el directorio raíz con este contenido:

    ```env
    DB_USER= #Usuario
    DB_PASSWORD= #password
    
    MONGO_HOST=mongo
    MONGO_PORT=27017
    MONGO_USER=${DB_USER}
    MONGO_PASSWORD=${DB_PASSWORD}
    MONGO_URI=mongodb://${MONGO_USER}:${MONGO_PASSWORD}@${MONGO_HOST}:${MONGO_PORT}
    MONGO_DB=mongodorodb
    MONGO_COLLECTION= #Nombre de la coleccion, default: Empleados
    MONGO_EXPRESS_PORT=8081
    
    RECORDS_TO_INSERT= #Cantidad de registros a insertar.
    SEARCH_N= #Cantidad de registros a buscar
    SEARCH_CHUNK= # Cantidad de registros a buscar juntos
    DISPLAY_NO_DOCUMENTO=false #Para que no imprima todos los no_documentos buscados
    ```

3.  **🐳 Ejecutar el contenedor**
    ```bash
    docker compose up mongodoro
    ```

### ✅ Salida esperada

Al ejecutar correctamente verá:

```plaintext
mongodoro  | 🗑️ Colección 'tss' eliminada. Sera creada al insertar los datos
mongodoro  |
mongodoro  | ✅ Se insertaron 12000000 registros en 'tss'.
mongodoro  | ⏱️ Tiempo de inserción: 174.27 segundos
mongodoro  | 📄 Total de registros: 12000000
mongodoro  | 📦 Tamaño de la colección (solo datos): 1232127.76 KB
mongodoro  | 🧮 Tamaño promedio por documento: 105.00 bytes
mongodoro  | 💾 Tamaño de almacenamiento (incluye relleno): 523544.00 KB
mongodoro  | 🗃️ Tamaño total de la base de datos: 1203.25 MB
mongodoro  |
mongodoro exited with code 0


```

## 🌐 Acceder a los datos

Visite **Mongo Express** en su navegador:  
http://localhost:8081/

Podrá realizar las siguientes acciones:

- 🔍 **Ver información de la base de datos**
- 📂 **Inspeccionar la colección**
- 🔎 **Realizar consultas a los datos**
