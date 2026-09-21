from django.contrib import admin
from .models import Formation, Question, QuestionPreliminaire, Reponse


class ReponseInline(admin.TabularInline):
    model = Reponse
    extra = 0


class QuestionAdmin(admin.ModelAdmin):
    list_display = ('ordre', 'texte')
    ordering = ('ordre',)
    search_fields = ('texte',)
    inlines = [ReponseInline]

class QuestionPreliminaireAdmin(admin.ModelAdmin):
    list_display = ('texte',)


class FormationAdmin(admin.ModelAdmin):
    list_display = ('nom',)
    search_fields = ('nom',)


admin.site.register(Formation, FormationAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionPreliminaire, QuestionPreliminaireAdmin)
admin.site.register(Reponse)
