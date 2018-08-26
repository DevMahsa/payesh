import csv
from datetime import datetime

import xlwt
from django.contrib import admin
from django.http import HttpResponse
from .models import Server, LastMemory, LastCpu


@admin.register(Server)
class ServerModelAdmin(admin.ModelAdmin):
    actions = ["export_as_csv", "export_users_xls"]
#     list_display = \
#     ('hostid',
#     'name',
#     'ip',
#     'date',
#     'new_system_event',
#     'new_app_event',
#     'eventlog_max_size',
#     'backup_name',
#     'freediskc',
#     'freediskd',
#     'freediske',
#     'freediskf',
#     'freediskg',
#     'freediskh',
#     'freediski',
#     'maxusedmemory',
#     'maxusedcpu',
#     'time_win_sync',
#     'sql_file_size',
#     'sql_login_user',
#     'sql_xp_cmdshell',
#     'microsoft_update',
#     'windows_version',
#     'sql_version' ,
#     'firewall' ,
#     'open_port',
#     'mcafee',
#     'anydesk',
#     'smb1_config',
#     'file_sharing_port' ,
#     'telnet',
#     'ssl_cert_exp',
#     'local_user' ,
#     'win_active' ,
# )
    search_fields = ('name','ip')

    def export_as_csv(self, request, queryset):
        list  = self.list_display
        meta = self.model._meta
        field_names = [field for field in list]
        field_names = [field.name for field in meta.fields]

        return self.response_write_to_csv(field_names, queryset, meta)

    def response_write_to_csv(self, field_names, queryset, meta):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;  filename=%s.csv' % str(queryset[0]) .replace('.', '_')
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

    export_as_csv.short_description = "Export as .csv"

    def export_users_xls(self, request, queryset):
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = 'attachment; filename=%s.xls' % str(queryset[0]) .replace('.', '_')

        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet(str(queryset[0]))
        #text_format = wb.add_style({'rotation': 270})

        # Sheet header, first row
        row_num = 0

        font_style = xlwt.XFStyle()
        font_style.font.bold = True

        #columns = self.model._meta
        columns = \
    ['id',
        'hostid',
    'name',
    'ip',
    'date',
    'new_system_event',
    'new_app_event',
    'eventlog_max_size',
    'backup_name',
    'freediskc',
    'freediskd',
    'freediske',
    'freediskf',
    'freediskg',
    'freediskh',
    'freediski',
    'maxusedmemory',
    'maxusedcpu',
    'time_win_sync',
    'sql_file_size',
    'sql_login_user',
    'sql_xp_cmdshell',
    'microsoft_update',
    'windows_version',
    'sql_version' ,
    'firewall' ,
    'open_port',
    'mcafee',
    'anydesk',
    'smb1_config',
    'file_sharing_port' ,
    'telnet',
    'ssl_cert_exp',
    'local_user' ,
    'win_active'

]
        # meta = self.model._meta
        # field_names = [field.name for field in meta.fields]
        # for field in field_names:
        #     row = [field]
        #     for obj in queryset:
        #         row.append(getattr(obj, field))
        #     ws.write(int(row[1]), str(row[0]))

        # for field in columns:
        #     row = [field]
        #     for obj in queryset:
        #         row.append(getattr(obj,field))
        #         ws.write(field, row)


        for col_num in range(len(columns)):
            ws.write(row_num, col_num, columns[col_num], font_style)

        # Sheet body, remaining rows
        font_style = xlwt.XFStyle()

        rows = queryset.values_list().all()
        for row in rows:
            row_num += 1
            for col_num in range(len(row)):
                ws.write(row_num, col_num, row[col_num], font_style)

        wb.save(response)
        return response
    export_users_xls.short_description = "Export as .xls"

@admin.register(LastMemory)
class LastMemoryModelAdmin(admin.ModelAdmin):
    list_display = ('server', 'memory', 'date')


@admin.register(LastCpu)
class LastCpuModelAdmin(admin.ModelAdmin):
    list_display = ('server', 'cpu', 'date')


# Register your models here.
