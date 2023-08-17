from django.contrib import admin

from .models import Card, Benefit

# Register your models here.

class BenefitInline(admin.StackedInline): # StackedInline은 세로 정렬 # TabularInline은 가로 정렬
    model = Benefit
    verbose_name = '혜택'
    verbose_name_plural = '혜택들' # 복수형

@admin.register(Card)
class CardModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'card', 'brand', 'image', 'view_count')
    list_editable = ('view_count',)
    search_fields = ('id', 'card') # 사용자는 lookup 방식
    search_help_text = '카드id, 카드명 검색이 가능합니다'
    inlines = (BenefitInline, )