from django.contrib import admin

from .models import Taskspace, Task


admin.site.register(Taskspace)
admin.site.register(Task)
