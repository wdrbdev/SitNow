from django.contrib import admin
from django.contrib.sessions.models import Session
from sitnow.models import UserProfile, Place,  Comment

# Register your models here.


# Access the session in admin
# https://stackoverflow.com/questions/4976015/django-how-to-see-session-data-in-the-admin-interface
# class SessionAdmin(admin.ModelAdmin):
#     def _session_data(self, obj):
#         return pprint.pformat(obj.get_decoded()).replace('\n', '<br>\n')
#     _session_data.allow_tags = True
#     list_display = ['session_key', '_session_data', 'expire_date']
#     readonly_fields = ['_session_data']
#     # exclude = ['session_data']
# admin.site.register(Session, SessionAdmin)

admin.site.register(UserProfile)
admin.site.register(Comment)
admin.site.register(Place)
