from django.core.management.base import BaseCommand
from payeshapp.models import Server, SqlDataAuth
import pymssql


def sql_file_size():
       for sql_data_auth in SqlDataAuth.objects.filter(host__isnull=False).all():
        obj = Server.objects.get(ip=sql_data_auth.host)
        obj.sql_file_size = ''
        try:
            connection = pymssql.connect(host=sql_data_auth.host, server=sql_data_auth.server, port=sql_data_auth.port,
                                         user=sql_data_auth.user,
                                         password=sql_data_auth.password)
            cursor = connection.cursor()
            cursor.execute('''with fs
    as
    (
     select database_id, type, size * 8.0 / 1048576 size
     from sys.master_files
    )
    select 
     name,
     (select sum(size) from fs where type = 0 and fs.database_id = db.database_id) DataFileSizeGB,
     (select sum(size) from fs where type = 1 and fs.database_id = db.database_id) LogFileSizeGB
    from sys.databases db''')
            #cursor.execute("EXEC sp_helpdb @dbname='msdb';")
            result = cursor.fetchall()
            for i in range(len(result)):
                if not str(result[i][0])=='master':
                    if not str(result[i][0])=='tempdb':
                        if not str(result[i][0])=='model':
                            if not str(result[i][0])=='msdb':
                                obj.sql_file_size +=str(result[i][0])+' : '+str(float(result[i][1])+float(result[i][2]))+'\n'
            obj.save()
        except pymssql.OperationalError:
            pass
        # obj.sql_file_size= ""
        # for i in range(len(result)):
        #     obj.sql_file_size += (str(result[i][4]).split(' K')[0])
        # obj.sql_file_size = float(obj.sql_file_size)/(1024*1024)
        # obj.save()



class Command(BaseCommand):
    def handle(self, **options):
        sql_file_size()
