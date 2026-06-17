from django.contrib import admin
from .models import Author, Genre, Book, BookDetail, Review, Loans

## Se deben importar estos de Django
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin



# Register your models here.
admin.site.site_header = "Administrador MiniLibrary"
admin.site.site_title = "MiniLibrary panel"
admin.site.index_title = "Bienvenidos al panel de MiniLibrary"

## Inline a User (default de Django)
User = get_user_model()

# Aquí tenemos el action
@admin.action(description="Marcar préstamos como devueltos")
def mark_as_returned(modeladmin, request, queryset):
    queryset.update(is_returned = True)


class LoanInline(admin.TabularInline):
    model = Loans
    extra = 1

# Más modificaciones 
@admin.register(Loans)
class LoanAdmin(admin.ModelAdmin):
    readonly_fields = ("loan_date",)
    list_display = ("user", "book", "loan_date", "is_returned")
    actions = [mark_as_returned]
    raw_id_fields = ["user", "book"]


## Inline One to many
class ReviewInline(admin.TabularInline):
    model = Review
    extra = 1

## Inline One to One
class BookDetailInline(admin.StackedInline):
    model = BookDetail
    can_delete = False
    verbose_name_plural = "Detalle del libro"

## Creando el custom admin
class CustomUserAdmin(BaseUserAdmin):
    inlines = [LoanInline]
    list_display = ("username", "email")

## Registro de modelos
@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    search_fields = ["name"]

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    search_fields = ["name"]

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    readonly_fields = ("pages",)
    # Inline
    inlines = [ReviewInline, BookDetailInline]

    list_display = ('title', 'author', 'pages', 'publication_date')

    # No olvidar que author es una llave foranea y que con el __ podemos acceder a ella
    search_fields = ('title', 'author__name') 
    
    list_filter = ('author', 'genres', 'publication_date')

    # Autocomplete field
    autocomplete_fields = ["author", "genres"] # Para que esto funcione debemos crear el AuthorAdmin

    # Ordenar, de forma decendente (usa lista)
    ordering = ['-publication_date'] 

    date_hierarchy = 'publication_date'

    fieldsets = (
        ("Información general",{
            "fields": ("title", "author", "publication_date", "genres"),
        }),
        ("Detalles", {
            "fields": ("isbn", "pages"),
            "classes": ("collapse",)
        }
        )
    )

    def has_add_permission(self, request):
        return request.user.is_superuser
    
    def has_change_permission(self, request, obj = None):
        return request.user.is_staff

# admin.site.register(Author)
# admin.site.register(Genre)
# admin.site.register(Book, BookAdmin)
admin.site.register(BookDetail)
admin.site.register(Review)
# admin.site.register(Loans)

## Desregistrar y volcer a asignar
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered: 
    pass

admin.site.register(User, CustomUserAdmin)