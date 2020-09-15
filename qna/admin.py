from django.contrib import admin

from .models import Question, Answer

class AnswerInline(admin.TabularInline):
  model = Answer
  extra = 3

class QuestionAdmin(admin.ModelAdmin):
  fieldsets = [
    (None, {'fields': ['question_text']}),
    ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
  ]
  inlines = [AnswerInline]
  list_display = ('question_text', 'pub_date', 'was_published_recently')
  list_filter = ['pub_date']
  search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Answer)

# Register your models here.
