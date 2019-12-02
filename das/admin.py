from django.contrib import admin
from das.models import *

class UnivercityAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'get_city_name',
        'tag_list',
    ]

    search_fields = [
        'name',
    ]

    autocomplete_fields = [
        'city',
    ]

    list_filter = [
        'project_tags',
        'is_private',
        'city__province__name',
        'city__tags'
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('project_tags', 'city')

    def tag_list(self, obj):
        return ", ".join(o.name for o in obj.project_tags.all())

    def get_city_name(self, obj):
        return obj.city.name if obj.city else ""

    get_city_name.short_description = '所在城市'
    get_city_name.admin_order_field = 'city'


class CityAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_province_name']
    search_fields = ['name']

    list_filter = [
        'province__name',
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('province')

    def get_province_name(self, obj):
        return obj.province.name

class UnivercityCodeAdmin(admin.ModelAdmin):

    list_display = [
        'code',
        'univercity_name_alias',
        'get_univercity_name',
    ]

    search_fields = [
        'code',
        'univercity_name_alias',
    ]

    autocomplete_fields = [
        'univercity',
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('univercity')

    def get_univercity_name(self, obj):
        return obj.univercity.name if obj.univercity else ""

    get_univercity_name.short_description = '实际高校名称'
    get_univercity_name.admin_order_field = 'univercity'


class ScoreLineAdmin(admin.ModelAdmin):

    list_display = [
        'get_admission_year_name',
        'get_uadmission_batch_name',
        'get_subject_type_name',
        'score',
    ]

    search_fields = [
        'score',
        'subject_type__type_name',
        'admission_year__year',
        'score'
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('subject_type', 'admission_batch', 'admission_year')


    def get_admission_year_name(self, obj):
        return obj.admission_year.year if obj.admission_year else ""

    def get_uadmission_batch_name(self, obj):
        return obj.admission_batch.batch_name if obj.admission_batch else ""

    def get_subject_type_name(self, obj):
        return obj.subject_type.type_name if obj.subject_type else ""

    get_admission_year_name.short_description = '录取年份'
    get_subject_type_name.short_description = '考生类型'
    get_uadmission_batch_name.short_description = '录取批次'


class PlanAdmin(admin.ModelAdmin):

    list_display = [
        'get_admission_year_name',
        'get_subject_type_name',
        'get_admission_batch_name',
        'get_code',
        'get_univercity_name_alias',
        'plan_amount',
        'actual_amount',
        'highest_score',
        'highest_rank',
        'lowest_score',
        'lowest_rank',
        'average_score',
        'average_rank',
    ]

    # list_editable = [
    #     'actual_amount',
    #     'highest_score',
    #     'highest_rank',
    #     'lowest_score',
    #     'lowest_rank',
    #     'average_score',
    # ]

    search_fields = [
        'univercity_code__univercity_name_alias',
        'univercity_code__code',
    ]

    list_filter = [
        'admission_year__year',
        'admission_batch__batch_name',
        'subject_type__type_name',
    ]

    autocomplete_fields = [
        'univercity_code',
    ]

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related(
            'univercity_code',
            'subject_type',
            'admission_batch',
            'admission_year',
        )

    def get_code(self, obj):
        return obj.univercity_code.code if obj.univercity_code else ""

    def get_univercity_name_alias(self, obj):
        return obj.univercity_code.univercity_name_alias if obj.univercity_code else ""

    def get_admission_year_name(self, obj):
        return obj.admission_year.year if obj.admission_year else ""

    def get_admission_batch_name(self, obj):
        return obj.admission_batch.batch_name if obj.admission_batch else ""

    def get_subject_type_name(self, obj):
        return obj.subject_type.type_name if obj.subject_type else ""

    get_admission_year_name.short_description = '录取年份'
    get_subject_type_name.short_description = '考生类型'
    get_admission_batch_name.short_description = '录取批次'
    get_code.short_description = '院校代码'
    get_univercity_name_alias.short_description = '高校名称'
    get_admission_year_name.admin_order_field = 'admission_year'
    get_subject_type_name.admin_order_field = 'subject_type'
    get_admission_batch_name.admin_order_field = 'admission_batch'
    get_code.admin_order_field = 'univercity_code__code'
    get_univercity_name_alias.admin_order_field = 'univercity_code__univercity_name_alias'


class ScoreStatisticAdmin(admin.ModelAdmin):
    list_display = [
        'get_admission_year_name',
        'get_subject_type_name',
        'score',
        'number',
        'cumulative_number',
    ]

    def get_admission_year_name(self, obj):
        return obj.admission_year.year if obj.admission_year else ""

    def get_subject_type_name(self, obj):
        return obj.subject_type.type_name if obj.subject_type else ""

    get_admission_year_name.short_description = '录取年份'
    get_subject_type_name.short_description = '考生类型'

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
admin.site.register(ScoreLine, ScoreLineAdmin)
admin.site.register(UnivercityCode, UnivercityCodeAdmin)
admin.site.register(Plan, PlanAdmin)
admin.site.register(ScoreStatistic, ScoreStatisticAdmin)
