from payeshapp.models import LastCpu, LastMemory, WindowsServer, SslData
from django.core.management.base import BaseCommand



class Command(BaseCommand):
    def handle(self, **options):
        data = SslData.objects.filter.all()
        delete_server(data)


def delete_server(servers):
    for server in servers:
        server.delete()