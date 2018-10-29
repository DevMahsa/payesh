from  datetime import datetime
from django.core.management.base import BaseCommand
from pyzabbix import ZabbixAPI
from payeshapp.models import WindowsServer, LastCpu, LastMemory


def export():
    zapi = login()
    select_host(zapi)


def select_host(zapi):
    for h in zapi.host.get(output="extend"):
        for host in WindowsServer.objects.filter(name=h['name']):
            for i in zapi.item.get(filter={'host': host.name}):
                cpu_usage(host, i)
                memory_usage(host, i)


def login():
    zapi = ZabbixAPI("http://zmonitor.ut.ac.ir")
    zapi.login("ririwindows", "ririwindows")
    return zapi


def memory_usage(host, i):
    if i['name'].lower().find('used memory') == 0:
        LastMemory.objects.get_or_create(server=host, memory=i['lastvalue'],
                                         date=datetime.now())


def cpu_usage(host, i):
    if i['name'].lower().find('cpu usage') == 0:
        LastCpu.objects.get_or_create(server=host, cpu=i['lastvalue'],
                                      date=datetime.now())


class Command(BaseCommand):
    def handle(self, **options):
        export()

