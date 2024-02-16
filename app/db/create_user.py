import psycopg2 as ps
import cred
from conn import dbConn
from schemas.user import User

def dbWriteUser():
    dbConn(cred.user_write_logs,
           cred.password_write_logs,
           "INSERT INTO postgres.user.user (username, password, email) values ('%s', crypt('%s', gen_salt('bf')), '%s');" % (User.username, User.password, User.email))