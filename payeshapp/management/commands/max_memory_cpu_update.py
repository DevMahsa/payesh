from django.core.management.base import BaseCommand
from django.db.models import Max
from pyzabbix import ZabbixAPI

from payeshapp.models import WindowsServer, LastMemory, LastCpu


def max():
    zapi = login()
    select_save(zapi)


def select_save(zapi):
    for h in zapi.host.get(output="extend"):
        for host in WindowsServer.objects.filter(name=h['name']):
            max_cpu(host)
            max_memory(host)
            host.save()


def max_cpu(host):
    host.maxusedcpu = LastCpu.objects.filter(server_id=host.id).aggregate(Max('cpu'))['cpu__max']


def max_memory(host):
    host.maxusedmemory = LastMemory.objects.filter(server_id=host.id).aggregate(Max('memory'))[
        'memory__max']


def login():
    zapi = ZabbixAPI("http://172.16.16.157:4720")
    zapi.login("riri", "rayta")
    return zapi


class Command(BaseCommand):
    def handle(self, **options):
        max()

