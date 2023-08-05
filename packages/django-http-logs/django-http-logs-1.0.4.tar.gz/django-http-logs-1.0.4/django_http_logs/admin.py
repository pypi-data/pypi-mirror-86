from django.contrib import admin

# Register your models here.
from .models import Logs


@admin.register(Logs)
class LogsAdministrator(admin.ModelAdmin):
    list_display = ["created", 'name', 'levelname', "short_message"]
    search_fields = ["msg"]
    date_hierarchy = "created"
    list_filter = ["levelname"]
    fieldsets = [
        (
            "Detail", {
                "fields": [
                    "name",
                    "levelname",
                    "msg",
                    "args"
                ]
            }), (
            "File Infor", {
                "fields": [
                    "pathname",
                    "funcname",
                    "lineno",
                    "threadName",
                    "processName",
                ]
            }
        ), (
            "Exc Infor", {
                "fields": [
                    "exc_info",
                    "exc_text",
                    "stack_info"
                ],
                "classes": ("collapse",),
            }
        ), (
            "Not Userful", {
                "fields": [
                    "created",
                    "msecs",
                    "relativeCreated",
                    "thread",
                    "process",
                    "levelno",
                ],
                "classes": ("collapse",),
            })
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
