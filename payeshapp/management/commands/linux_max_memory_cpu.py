from django.core.management.base import BaseCommand
from django.db.models import Max
from pyzabbix import ZabbixAPI

from payeshapp.models import LinuxServer, LastLinuxCpu, LastLinuxMemory


def max():
    zapi = login()
    select_save(zapi)


def select_save(zapi):
    for h in zapi.host.get(output="extend"):
        for host in LinuxServer.objects.filter(name=h['name']):
            max_cpu(host)
            max_memory(host)
            host.save()


def max_cpu(host):
    host.maxusedcpu = LastLinuxCpu.objects.filter(server_id=host.id).aggregate(Max('cpu'))['cpu__max']


def max_memory(host):
    host.maxusedmemory = LastLinuxMemory.objects.filter(server_id=host.id).aggregate(Max('memory'))[
        'memory__max']


def login():
    zapi = ZabbixAPI("https://zmonitor.ut.ac.ir")
    # zapi.session.verify = False
    zapi.login("ririlinux", "ririlinux")
    return zapi


class Command(BaseCommand):
    def handle(self, **options):
        max()

