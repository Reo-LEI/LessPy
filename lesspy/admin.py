from django.contrib import admin

from .models import *


admin.site.register(UserProfile)
admin.site.register(Text)
admin.site.register(TagList)
admin.site.register(Library)
admin.site.register(LibraryRequest)
admin.site.register(Function)
admin.site.register(FunctionRequest)
admin.site.register(Topic)
admin.site.register(TopicRequest)
admin.site.register(Skill)
admin.site.register(SkillRequest)
