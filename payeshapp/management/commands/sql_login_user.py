from django.core.management.base import BaseCommand
from payeshapp.models import WindowsServer, SqlDataAuth
import pymssql


def sql_login_user():
    for sql_data_auth in SqlDataAuth.objects.filter(host__isnull=False).all():
        obj = WindowsServer.objects.get(ip=sql_data_auth.host)
        #obj = '192.168.112.219'
        try:
            connection = pymssql.connect(host=sql_data_auth.host, server=sql_data_auth.server, port=sql_data_auth.port,
                                         user=sql_data_auth.user,
                                         password=sql_data_auth.password)

            cursor = connection.cursor()
            cursor.execute("select * from sys.sql_logins where is_disabled=0")
                    # cursor.execute(
                    #    "SELECT CONVERT(INT, ISNULL(value, value_in_use)) AS config_value FROM sys.configurations WHERE name = N'xp_cmdshell' ;")
            result = cursor.fetchall()
            obj.sql_login_user = ""
            for i in range(len(result)):
                obj.sql_login_user += str(result[i][0]) + ', '+'\n'
            obj.save()
        except pymssql.OperationalError:
            pass


class Command(BaseCommand):
    def handle(self, **options):
        sql_login_user()
