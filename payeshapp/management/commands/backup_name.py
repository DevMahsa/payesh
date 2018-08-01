from django.core.management.base import BaseCommand
from payeshapp.models import Server,SqlDataAuth
import pymssql



def backup_url():

    for sql_data_auth in SqlDataAuth.objects.filter(name__isnull=False).all():

        obj = Server.objects.get(ip=sql_data_auth.host)
        try:

            connection = pymssql.connect(host=sql_data_auth.host, server=sql_data_auth.server, port=sql_data_auth.port, user=sql_data_auth.user,
                                         password=sql_data_auth.password)
            cursor = connection.cursor()
            cursor.execute('''WITH LastBackUp AS
    (
    SELECT  bs.database_name,
            bs.backup_size,
            bs.backup_start_date,
            bmf.physical_device_name,
            Position = ROW_NUMBER() OVER( PARTITION BY bs.database_name ORDER BY bs.backup_start_date DESC )
    FROM  msdb.dbo.backupmediafamily bmf
    JOIN msdb.dbo.backupmediaset bms ON bmf.media_set_id = bms.media_set_id
    JOIN msdb.dbo.backupset bs ON bms.media_set_id = bs.media_set_id
    WHERE   bs.[type] = 'D'
    AND bs.is_copy_only = 0
    )
    SELECT 
            database_name AS [Database],
            CAST(backup_size / 1048576 AS DECIMAL(10, 2) ) AS [BackupSizeMB],
            backup_start_date AS [Last Full DB Backup Date],
            physical_device_name AS [Backup File Location]
    FROM LastBackUp
    WHERE Position = 1
    ORDER BY [Database];''')


            # cursor.execute(
            #    "SELECT CONVERT(INT, ISNULL(value, value_in_use)) AS config_value FROM sys.configurations WHERE name = N'xp_cmdshell' ;''')
            result = cursor.fetchall()
            obj.backup_name = ""
            for i in range(len(result)):
                obj.backup_name+= str(result[i][0])+' , '+str(result[i][1])+' , '+str(result[i][2])+' , '+str(result[i][3])+', '+'\n'
            obj.save()
        except pymssql.OperationalError:
            pass


class Command(BaseCommand):
    def handle(self, **options):
        backup_url()

