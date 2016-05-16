
from django.contrib import admin
from .models import Topic, Poll


class TopicAdmin(admin.ModelAdmin):
    raw_id_fields = ("user",)
    list_display = ("id", "user", "name", "polls", "photo")


class PollAdmin(admin.ModelAdmin):
    raw_id_fields = ("user", "topic")
    list_display = ("user", "topic")


admin.site.register(Topic, TopicAdmin)
admin.site.register(Poll, PollAdmin)
