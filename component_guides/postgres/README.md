- https://www.freecodecamp.org/news/postgresql-in-python/

- pip install psycopg[binary]

```python
import psycopg2

conn = psycopg2.connect(database="db_name",
                        host="db_host",
                        user="db_user",
                        password="db_pass",
                        port="db_port")

cur = conn.cursor()

cur.execute("CREATE TABLE test (id serial PRIMARY KEY, num integer, data varchar);")
cur.execute("INSERT INTO test (num, data) VALUES (%s, %s)", (100, "abc'def"))
cur.execute("SELECT * FROM test;")
cur.fetchone()
cur.fetchall()
conn.commit()

cur.close()
conn.close()
```