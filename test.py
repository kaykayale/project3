
from pymongo import MongoClient
from pprint import pprint # for "pretty printing"
def connect():
    CONNECTION_STRING = "mongodb://localhost:27017"
    client = MongoClient(CONNECTION_STRING)
    # change this string to match the name of the database you created in Mongo
    return client['homework']
if __name__ == "__main__":
    db = connect()
# The Python API for working with Mongo is very similar to in the Mongosh shell.
# However, we must use dictionary indexing like "db['customers']" instead of "db.customers".
# This is unnecessary, but I like to separate the pipeline stages from the actual aggregate function call.
    usa_customers = [
        {
            "$match": {
                "country": "USA"
            }
        },
        {
            "$project": {
                "customername": 1
            }
        }
    ]
    # Run the pipeline.
    results = db["customers"].aggregate(usa_customers)
    # Pretty-print the results.

    for customer in results:
        print(f"{customer['customername']} (ID {customer['_id']})")
