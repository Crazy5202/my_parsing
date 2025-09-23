import asyncio
from pymongo import AsyncMongoClient

async def main():
    uri = "mongodb://admin:password123@localhost:27017/"
    client = AsyncMongoClient(uri)

    try:

        await client.admin.command("ping")
        print("Connected successfully")

        collection = client["html_storage"]["html_documents"]

        results = collection.find()

        async for document in results:
            print(document)

        #print(await client.list_database_names())

        # database = client["test_database"]
        # await database.create_collection("example_collection")

        # print("Collection created")

        # database = client.get_database("sample_mflix")
        # movies = database.get_collection("movies")

        # query = { "title": "Back to the Future" }
        # movie = await movies.find_one(query)

        #print(movie)

        await client.close()

    except Exception as e:
        raise Exception("Unable to find the document due to the following error: ", e)

asyncio.run(main())
