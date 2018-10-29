from django.core.exceptions import MultipleObjectsReturned
from django.core.management.base import BaseCommand, CommandError
from payeshapp.models import WindowsServer, LastMemory, LastCpu


class Command(BaseCommand):
    help = "delete a server"

    def add_arguments(self, parser):
        parser.add_argument('ip', nargs='+', type=str)

    def handle(self, *args, **options):
        for i in options['ip']:
            try:
                try:

                    server = WindowsServer.objects.get(ip=i)
                except MultipleObjectsReturned:
                    server = WindowsServer.objects.get(ip=i)[0]
                self.delete_server(server)
            except WindowsServer.DoesNotExist:
                raise CommandError('journal "%s" does not exist' % i)

            self.stdout.write(self.style.SUCCESS('Successfully closed server "%s"' % i))

    def delete_server(self, server):
        LastCpu.objects.filter(server=server).all().delete()
        LastMemory.objects.filter(server=server).all().delete()
        server.delete()
