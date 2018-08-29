from django.core.management.base import BaseCommand
from payeshapp.models import WindowsServer, SqlDataAuth
import pymssql


def sql_version():
    for sql_data_auth in SqlDataAuth.objects.filter(host__isnull=False).all():

        obj = WindowsServer.objects.get(ip=sql_data_auth.host)
        try:
            connection = pymssql.connect(host=sql_data_auth.host, server=sql_data_auth.host, port=sql_data_auth.port,
                                         user=sql_data_auth.user,
                                         password=sql_data_auth.password)
            cursor = connection.cursor()
            cursor.execute("SELECT @@version;")
            result = cursor.fetchall()
            obj.sql_version = str(result[0][0]).split('\n')[0]
            obj.save()
        except pymssql.OperationalError:
            pass

class Command(BaseCommand):
    def handle(self, **options):
        sql_version()
