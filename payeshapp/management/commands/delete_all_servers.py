from models import LastCpu, LastMemory, WindowsServer
from django.core.management.base import BaseCommand



class Command(BaseCommand):
    def handle(self, **options):
        servers = WindowsServer.objects.filter.all()
        delete_server(servers)


def delete_server(servers):
    for server in servers:
        LastCpu.objects.filter(server=server).all().delete()
        LastMemory.objects.filter(server=server).all().delete()
        server.delete()
