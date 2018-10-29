from django.core.management.base import BaseCommand
from pyzabbix import ZabbixAPI
from payeshapp.models import WindowsServer


def update():
    zapi = login()
    count = 0
    length, query = select_host(zapi)
    save_host(length, query)


def select_host(zapi):
    query = zapi.host.get(output="extend", selectInterfaces="extend", selectParentTemplates="Array")
    length = query.__len__()
    return length, query


def save_host(length, query):
    for count in range(length):
        if WindowsServer.objects.filter(ip = query[count]['interfaces'][0]['ip']).exists():
            count += 1
            continue
        get = WindowsServer(name=query[count]['name'])
        get.ip = query[count]['interfaces'][0]['ip']
        get.name = query[count]['name']
        get.hostid = query[count]['hostid']
        get.save()


def login():
    """
    login to zabbix api

    """
    zapi = ZabbixAPI("https://zmonitor.ut.ac.ir")
    # Disable SSL certificate verification
    # zapi.session.verify = False
    #
    # # Specify a timeout (in seconds)
    # zapi.timeout = 5.1
    zapi.login("ririwindows", "ririwindows")
    return zapi


class Command(BaseCommand):
    def handle(self, **options):
        update()

