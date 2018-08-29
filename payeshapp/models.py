from django.db import models


class WindowsServer(models.Model):
    hostid = models.CharField(max_length=500, null=True)
    name = models.CharField(max_length=500)
    ip=models.CharField(max_length=50,null=True)
    date = models.DateField(blank=True, null=True)
    new_system_event = models.TextField(null=True)
    new_app_event = models.TextField(null=True)
    eventlog_max_size = models.TextField(null=True)
    backup_name = models.TextField( null= True)
    freediskc = models.CharField(max_length=500, null=True)
    freediskd = models.CharField(max_length=500, null=True)
    freediske = models.CharField(max_length=500, null=True)
    freediskf = models.CharField(max_length=500, null=True)
    freediskg = models.CharField(max_length=500, null=True)
    freediskh = models.CharField(max_length=500, null=True)
    freediski = models.CharField(max_length=500, null=True)
    maxusedmemory = models.CharField(max_length=500, null=True)
    maxusedcpu = models.CharField(max_length=500, null=True)
    time_win_sync = models.CharField(max_length=500 ,null= True)
    sql_file_size = models.TextField (null= True)
    sql_login_user = models.TextField(null=True)
    sql_xp_cmdshell = models.CharField(max_length=500, null=True)
    microsoft_update = models.CharField(max_length=500 ,null= True)
    windows_version = models.CharField(max_length=500 , null= True)
    sql_version = models.CharField(max_length=500 , null= True)
    firewall = models.CharField(max_length=500, null=True)
    open_port = models.TextField( null= True)
    mcafee = models.CharField(max_length=500, null=True)
    anydesk = models.CharField(max_length=500 ,null= True)
    smb1_config = models.CharField(max_length=500 ,null= True)
    file_sharing_port = models.TextField(null=True)
    telnet = models.CharField(max_length=500, null=True)
    ssl_cert_exp = models.CharField(max_length=500, null=True)
    local_user = models.TextField( null= True)
    win_active = models.CharField(max_length=500, null=True)




    def __str__(self):
        return self.name



class LastMemory(models.Model):
    memory = models.CharField(max_length=500)
    date = models.CharField(max_length=500)
    server = models.ForeignKey(WindowsServer, related_name='memory',on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.server.name


class LastCpu(models.Model):
    cpu = models.CharField(max_length=500)
    date = models.CharField(max_length=500)
    server = models.ForeignKey(WindowsServer, related_name='cpu',on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.server.name

class SqlDataAuth(models.Model):
    name = models.CharField(max_length=500, null=True)
    host = models.CharField(max_length=500, null=True)
    server = models.CharField(max_length=500, null=True)
    port = models.CharField(max_length=500, null=True)
    user = models.CharField(max_length=500, null=True)
    password = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.host,self.name

class SslData(models.Model):
    hostip=models.CharField(max_length=500, null=True)
    addr=models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.addr

# Create your models here.
