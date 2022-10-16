import psycopg2

conn = psycopg2.connect("postgresql://theDucks:vJD1ufdJRASpMJypuopW7Q@free-tier11.gcp-us-east1.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full&options=--cluster%3Dkenthackenough-2373")

with conn.cursor() as cur:
    cur.execute("select * from scan;")
    res = cur.fetchall()
    conn.commit()
    print(res)
