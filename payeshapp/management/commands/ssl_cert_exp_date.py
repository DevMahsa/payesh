from django.core.management.base import BaseCommand
from payeshapp.models import Server, SslData
import OpenSSL
import ssl


def ssl_cert_exp():
    for ssl_data in SslData.objects.filter(hostip__isnull=False):
        obj = Server.objects.get(ip=ssl_data.hostip)
        x509 = chack_ssl_cert(ssl_data)
        day, month, year = extract_day(x509)
        # dt = datetime(int(year), int(month), int(day))
        obj.ssl_cert_exp = str(year + '-' + month + '-' + day)
        obj.save()


def chack_ssl_cert(ssl_data):
    cert = ssl.get_server_certificate(addr=(ssl_data.addr, 443))
    x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
    return x509


def extract_day(x509):
    rawdate = x509.get_notAfter().decode('utf-8')
    year = rawdate[0:4]
    month = rawdate[4:6]
    day = rawdate[6:8]
    return day, month, year


class Command(BaseCommand):
    def handle(self, **options):
        ssl_cert_exp()

