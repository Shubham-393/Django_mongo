import os
from pymongo import MongoClient
from pymongo.errors import ConnectionError, ConfigurationError

# Cache the MongoDB client to reuse the connection in serverless environments
client = None

def get_db():
    global client

    # Check if the client is already connected to avoid reconnecting on each request
    if client is None:
        try:
            # Fetch connection string from environment variables
            connection_string = os.getenv("MONGODB_URI")
            if not connection_string:
                raise ValueError("MongoDB connection string not found in environment variables.")
            
            # Establish the MongoDB client connection
            client = MongoClient(connection_string, serverSelectionTimeoutMS=5000, connectTimeoutMS=10000)

            
        except (ConnectionError, ConfigurationError, ValueError) as e:
            # Log and return an error if connection fails
            print("MongoDB Connection Error:", e)
            return None

    # Return the specified database
    return client['database1']
