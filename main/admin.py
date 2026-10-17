from django.contrib import admin
from.models import Contact, Tag,Project,ProjectImage

class projectImageInline(admin.TabularInline):
    model = ProjectImage
    extra=1

class projectAdmin(admin.ModelAdmin):
    list_display = ("title","link")
    inlines = [projectImageInline]
    search_fields = ("title","description")
    list_filter= ("tags",)

class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

admin.site.register(Project,projectAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(ProjectImage)
admin.site.register(Contact)

from .models import BetaTester
admin.site.register(BetaTester)