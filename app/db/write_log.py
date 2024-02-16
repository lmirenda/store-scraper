import psycopg2 as ps
import cred
from conn import dbConn
from schemas.user import User
from api.main import get_products

def dbWriteLog():
    dbConn(cred.user_write_logs,
           cred.password_write_logs,
           "INSERT INTO postgres.orders.order_logs (user_id, order) values ('%s', '%s');" % (User.username, get_products))