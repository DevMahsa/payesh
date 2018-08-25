import csv
from datetime import datetime

from django.contrib import admin
from django.http import HttpResponse
from .models import Server, LastMemory, LastCpu


@admin.register(Server)
class ServerModelAdmin(admin.ModelAdmin):
    actions = ["export_as_csv"]
    list_display = (
        'name', 'date', 'firewall', 'mcafee', 'telnet', 'anydesk','time_win_sync','smb1_config','file_sharing_port','new_system_event','new_app_event','microsoft_update','local_user','maxusedmemory', 'maxusedcpu', 'freediskc', 'freediskd',
        'freediske', 'freediskf', 'freediskg',
        'freediskh', 'freediski','ssl_cert_exp','win_active','sql_login_user', 'sql_xp_cmdshell','sql_version', 'sql_file_size','backup_name','windows_version','open_port', 'eventlog_max_size')
    search_fields = ('name','ip')

    def export_as_csv(self, request, queryset):
        list  = self.list_display
        meta = self.model._meta
        field_names = [field for field in list]
        field_names = [field.name for field in meta.fields]

        return self.response_write_to_csv(field_names, queryset, meta)

    def response_write_to_csv(self, field_names, queryset, meta):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;  filename=%s.csv' % str(queryset[0]).replace('.', '_')
        writer = csv.writer(response)
        # writer.writerow(field_names)
        self.wirte_rows(field_names, queryset, writer)
        # for obj in queryset:
        #     row = writer.writerow([getattr(obj, field) for field in field_names])
        return response

    def wirte_rows(self, field_names, queryset, writer):
        for field in field_names:
            row = [field]
            for obj in queryset:
                row.append(getattr(obj, field))
            writer.writerow(row)

    export_as_csv.short_description = "Export Selected"


@admin.register(LastMemory)
class LastMemoryModelAdmin(admin.ModelAdmin):
    list_display = ('server', 'memory', 'date')


@admin.register(LastCpu)
class LastCpuModelAdmin(admin.ModelAdmin):
    list_display = ('server', 'cpu', 'date')


# Register your models here.
