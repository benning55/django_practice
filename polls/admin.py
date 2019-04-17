from django.contrib import admin

# Register your models here.
from django.contrib.auth.models import Permission

from polls.models import Poll, Question, Choice


admin.site.register(Permission)


class QuestionInLine(admin.StackedInline):
    model = Question
    extra = 1  # เพิ่มช่องแอดแค่อันเดียว


class PollAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'start_date', 'end_date', 'del_flag']
    list_per_page = 10

    list_filter = ['start_date', 'end_date', 'del_flag']
    search_fields = ['title']

    # fields = ['title', 'del_flag'] เอามาเฉพาะ
    # exclude = ['title', 'del_flag'] เอาออก 2 ตัว
    fieldsets = [
        (None, {'fields': ['title', 'del_flag']}),
        ("Active Duration", {'fields': ['start_date', 'end_date'], 'classes': ['collapse']})
    ]
    # จัดกลุ่มของข้อมูล

    inlines = [QuestionInLine]


admin.site.register(Poll, PollAdmin)


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 1


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['id', 'poll', 'text']
    list_per_page = 15

    inlines = [ChoiceInLine]


admin.site.register(Question, QuestionAdmin)


class ChoiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'question', 'text', 'value']
    list_per_page = 15


admin.site.register(Choice, ChoiceAdmin)
