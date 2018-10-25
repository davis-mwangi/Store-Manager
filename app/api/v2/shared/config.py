import psycopg2

conn = psycopg2.connect(host="localhost", database="store_manager",
                        user="postgres", password="postgres")
