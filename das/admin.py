from django.contrib import admin
from das.models import *

class UnivercityAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_city_name', 'tag_list']
    search_fields = ['name', 'city__name']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('project_tags', 'city')

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.project_tags.all())

    def get_city_name(self, obj):
        return obj.city.name if obj.city else ""

class CityAdmin(admin.ModelAdmin):
    # list_display = ['name']
    search_fields = ['name']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('province')

admin.site.register(Rank)
admin.site.register(Univercity, UnivercityAdmin)
admin.site.register(Province)
# admin.site.register(ExamDivision)
admin.site.register(AdmissionBatch)
admin.site.register(AdmissionYear)
# admin.site.register(SchoolType)
# admin.site.register(SchoolFeature)
# admin.site.register(SchoolLevel)
# admin.site.register(Affiliation)
admin.site.register(City, CityAdmin)
admin.site.register(SubjectType)
admin.site.register(Subject)
admin.site.register(ScoreLine)
admin.site.register(UnivercityCode)
admin.site.register(Plan)
