import psycopg2 as ps
import cred

def dbConn(user, password, query):
    conn = ps.connect(dbname = cred.dbname, host = cred.host, user = user, password = password, port = cred.port)
    curs = conn.cursor()
    return curs.execute(query)