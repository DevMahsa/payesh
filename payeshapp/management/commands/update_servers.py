from django.core.management.base import BaseCommand
from pyzabbix import ZabbixAPI
from payeshapp.models import Server


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
        if Server.objects.filter(name=query[count]['name']).exists():
            count += 1
            continue
        get = Server(name=query[count]['name'])
        get.ip = query[count]['interfaces'][0]['ip']
        get.name = query[count]['name']
        get.hostid = query[count]['hostid']
        get.save()


def login():
    zapi = ZabbixAPI("http://192.168.112.157:4720")
    zapi.login("riri", "rayta")
    return zapi


class Command(BaseCommand):
    def handle(self, **options):
        update()

