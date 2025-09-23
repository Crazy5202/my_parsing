from pymongo import AsyncMongoClient
from datetime import datetime
import json
import asyncio

MONGO_URI = "mongodb://admin:password123@localhost:27017/"
DB_NAME = "html_storage"
COLLECTION_NAME = "html_documents"

async def connect_to_mongodb():
    """Connect to MongoDB and return client and database objects"""
    try:
        client = AsyncMongoClient(MONGO_URI)

        await client.admin.command("ping")
        print("Connected successfully")
        
        db = client[DB_NAME]
        print("Successfully connected to MongoDB!")
        return client, db
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None, None

async def upload_html_document(db, html_content, url, metadata=None):
    """Upload HTML content to MongoDB"""
    
    if metadata is None:
        metadata = {}
    
    document = {
        "url": url,
        "html_content": html_content,
        "metadata": metadata,
        "upload_date": datetime.now(),
        "content_type": "text/html",
        "size_bytes": len(html_content.encode('utf-8'))
    }
    
    collection = db[COLLECTION_NAME]
    result = await collection.insert_one(document)
    
    print(f"HTML document uploaded successfully! Document ID: {result.inserted_id}")
    return result.inserted_id

async def main():
    client, db = await connect_to_mongodb()
    
    if not client is None:
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Test Document</title>
        </head>
        <body>
            <h1>Hello, MongoDB!</h1>
            <p>This HTML content is stored in MongoDB.</p>
        </body>
        </html>
        """
        
        doc_id = await upload_html_document(
            db=db,
            html_content=html_content,
            url="example.com",
        )
        
        await client.close()

asyncio.run(main())