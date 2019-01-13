from  datetime import datetime
from django.core.management.base import BaseCommand
from pyzabbix import ZabbixAPI
from payeshapp.models import LinuxServer


def get_items():
    zapi = login()

    for h in zapi.host.get(output="extend"):
        for host in LinuxServer.objects.filter(name=h['name']):

            for i in zapi.item.get(filter={'host': host.name}):
                host.date = datetime.now()
                time_sync(host, i)
                firewall_status(host, i)
                user(host, i)
                servcie(host, i)
                version(host,i)
            host.save()


""" last_db_backup = models.TextField( null= True)
    db_backup_size = models.TextField( null= True)
    maxusedmemory = models.CharField(max_length=500, null=True)
    maxusedcpu = models.CharField(max_length=500, null=True)
    access_db_config = models.CharField(max_length=500 , null= True)
    linux_update = models.CharField(max_length=500 , null= True)
    linux_version = models.CharField(max_length=500 , null= True)
    db_version = models.CharField(max_length=500 , null= True)
    firewall = models.CharField(max_length=500, null=True)
    iptables = models.CharField(max_length=500, null=True)
    open_port = models.TextField( null= True)
    ssh_port = models.CharField(max_length=500, null=True)
    root_login = models.CharField(max_length=500, null=True)
    ssl_cert_exp_date = models.CharField(max_length=500, null=True)
    pass_exp_date = models.CharField(max_length=500, null=True)
"""


def version(host,i):
    if i['name'].lower().find('linux version') ==0:
        host.linux_version=['lastvalue']

def servcie(host, i):
    if i['name'].lower().find('all running services centos') == 0:
        if i['lastvalue'].split('Permission denied').__len__() >= 2:
            if i['name'].lower().find('all running services ubuntu') == 0:
                ubuntulist = ""
                if i['lastvalue'].split('telnet').__len__() >= 2:
                    host.telnet = "enable"
                else:
                    host.telnet = "No such service"
                if i['lastvalue'].split('anydesk').__len__() >= 2:
                    host.anydesk = "enable"
                else:
                    host.anydesk = "No such service"
                if i['lastvalue'].split('puppet').__len__() >= 2:
                    host.puppet = "enable"
                else:
                    host.puppet = "No such service"
                if i['lastvalue'].split('chef').__len__() >= 2:
                    host.chef = "enable"
                else:
                    host.chef = "No such service"
        else:
            centoslist = ""
            # if i['lastvalue'].split('sshd').__len__() >= 2:
            #     host
            # if i['lastvalue'].split('firewalld').__len__() >= 2:
            #     return ""
            if i['lastvalue'].split('telnet').__len__() >= 2:
                host.telnet = "enable"
            else:
                host.telnet = "No such service"
            if i['lastvalue'].split('anydesk').__len__() >= 2:
                host.anydesk = "enable"
            else:
                host.anydesk = "No such service"
            if i['lastvalue'].split('puppet').__len__() >= 2:
                host.puppet = "enable"
            else:
                host.puppet = "No such service"
            if i['lastvalue'].split('chef').__len__() >= 2:
                host.chef = "enable"
            else:
                host.chef = "No such service"

            # if i['lastvalue'].split('iptables').__len__() >= 2:
            #     return ""


def local_user(i):
    if i['name'].lower().find('local user') == 0:
        mylist = ""
        temp = i['lastvalue'].split(':x:')
        mylist += temp[0]
        for j in range(1, len(temp)):
            mylist += temp[j].split('/bin/bash')[1]
        flist = mylist.split('\n')
        return flist


def user(host, i):
    if i['name'].lower().find('local user') == 0:
        mylist = ""
        temp = i['lastvalue'].split(':x:')
        mylist += temp[0]
        for j in range(1, len(temp)):
            mylist += temp[j].split('/bin/bash')[1]
        flist = mylist.split('\n')
        host.local_user = str(flist)


def firewall_status(host, i):
    try:
        if i['name'].lower().find('firewall status deb based') == 0:
            firewall2 = i['lastvalue'].split('exited')

            if len(firewall2) >= 2:
                host.firewall = "ON"
            else:
                host.firewall = "OFF"
        elif i['name'].lower().find('firewall status rpm based') == 0:
            firewall1 = i['lastvalue'].split('running')
            if len(firewall1) >= 2:
                host.firewall = "ON"

            else:
                host.firewall = "OFF"
        elif i['name'].lower().find('firewall alternative') == 0:
            firewall1 = i['lastvalue'].split('running')
            firewall2 = i['lastvalue'].split('exited')
            if len(firewall1) >= 2:
                host.firewall = "ON"

            elif len(firewall2) >= 2:
                host.firewall = "ON"
            else:
                host.firewall = "OFF"
    except IndexError:
        pass


def time_sync(host, i):
    if i['name'].lower().find('is time sync') == 0:
        time = i['lastvalue'].split('192.168.20.23')
        if len(time) >= 2:
            host.ut_time_sync = "YES"
        else:
            host.ut_time_sync = "NO"


def login():
    zapi = ZabbixAPI("https://zmonitor.ut.ac.ir")
    # zapi.session.verify = False
    zapi.login("ririlinux", "ririlinux")
    return zapi


class Command(BaseCommand):
    def handle(self, **options):
        get_items()
