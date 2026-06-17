from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100) # Maximo 100 letras para este campo
    birth_date = models.DateField(null=True, blank=True) # Se puede dejar vacío

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_date = models.DateField(null=True, blank=True)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, related_name = 'books')
    pages = models.IntegerField()
    isbn = models.CharField(max_length=50)

    ## Modelado Muchos a Muchos
    genres = models.ManyToManyField(Genre, related_name = 'books')
    
    ## Tabla intermedia personalizada
    recommended_by = models.ManyToManyField(get_user_model(), through="Recomendation", related_name="recommendations")

    # Con esto configuramos los settings de la clase.
    class Meta:
        verbose_name = 'Libro'
        verbose_name_plural = 'Libros'

    def __str__(self):
        return self.title
    

## Modelado Uno a Uno    
class BookDetail(models.Model):
    summary = models.TextField()
    cover_url = models.CharField()
    language = models.CharField()
    book = models.OneToOneField(Book, on_delete=models.CASCADE, related_name = 'detail')


class Review(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveIntegerField()
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} -> {self.book.title} - ({self.rating}/5)"
    
class Loans(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="loans")
    loan_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank = True)
    is_returned = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user} -> {self.book.title} - ({'Devuelto' if self.is_returned else 'Prestado'})"
    
class Recomendation(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    recommended_at = models.DateField(auto_now_add=True)
    note = models.TextField(blank=True)

    # Esto funciona como un settings, es una clase de configuración:
    class Meta:
        unique_together = ("user", "book")
