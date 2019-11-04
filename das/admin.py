from django.contrib import admin
from das.models import *

class UnivercityAdmin(admin.ModelAdmin):
    # list_display = ['tag_list']

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('project_tags')

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.project_tags.all())

admin.site.register(Rank)
admin.site.register(Univercity)
admin.site.register(Province)
# admin.site.register(ExamDivision)
admin.site.register(AdmissionBatch)
admin.site.register(AdmissionYear)
# admin.site.register(SchoolType)
# admin.site.register(SchoolFeature)
# admin.site.register(SchoolLevel)
# admin.site.register(Affiliation)
admin.site.register(City)
admin.site.register(SubjectType)
admin.site.register(Subject)
admin.site.register(ScoreLine)
admin.site.register(UnivercityCode)
