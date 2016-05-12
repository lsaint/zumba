
from django.contrib import admin
from .models import Topic, Poll


class TopicAdmin(admin.ModelAdmin):
    raw_id_fields = ("user",)
    list_display = ("user", "name", "polls", "photo")


admin.site.register(Topic, TopicAdmin)
admin.site.register(Poll)
