from django.contrib import admin

'''
from .models import Choice, Question

class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date']}),
    ]
    inlines = [ChoiceInline]
    list_display = ('question_text', 'pub_date', 'was_published_recently')
    list_filter = ['pub_date']
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
'''

# from .models import *
# admin.site.register(AppUser, AppUserAdmin)
# admin.site.register(Resume, ResumeAdmin)
# admin.site.register(Job, JobAdmin)
# admin.site.register(Qualification, QualificationAdmin)
# admin.site.register(SuitableJob, SuitableJobAdmin)