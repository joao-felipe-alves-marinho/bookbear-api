from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin


# Create your models here.

# Choices
class Gender(models.TextChoices):
    NOT_SPECIFIED = 'X', 'Not specified'
    MALE_CIS = 'MC', 'Male Cisgender'
    FEMALE_CIS = 'FC', 'Female Cisgender'
    MALE_TRANS = 'MT', 'Male Transgender'
    FEMALE_TRANS = 'FT', 'Female Transgender'
    NON_BINARY = 'NB', 'Non-binary'
    OTHER = 'O', 'Other'


class AgeRating(models.TextChoices):
    ALL_AGES = 'AA', 'All Ages'
    TEEN = 'T', 'Teen'
    MATURE = 'M', 'Mature'
    ADULT = 'A', 'Adult'


class Situation(models.TextChoices):
    READING = 'R', 'Reading'
    STOPPED = 'S', 'Stopped'
    COMPLETED = 'C', 'Completed'
    PENDING = 'P', 'Pending'


# Models
class Author(models.Model):
    avatar = models.ImageField(upload_to='authors', blank=True, null=True)
    name = models.CharField(max_length=250, unique=True)
    birth_date = models.DateField()


class Publisher(models.Model):
    logo = models.ImageField(upload_to='publishers', blank=True, null=True)
    name = models.CharField(max_length=250, unique=True)


class Genre(models.Model):
    name = models.CharField(max_length=250, unique=True)


class Book(models.Model):
    title = models.CharField(max_length=250)
    publication_date = models.DateField()
    synopsis = models.TextField(blank=True)
    score = models.FloatField()
    # noinspection PyUnresolvedReferences
    age_rating = models.CharField(max_length=2, choices=AgeRating.choices, default=AgeRating.ALL_AGES)

    cover = models.ImageField(upload_to='covers', blank=True, null=True)

    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True)
    authors = models.ManyToManyField(Author, related_name='books')
    genres = models.ManyToManyField(Genre, related_name='books')


class User(AbstractUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=250)
    summary = models.TextField(blank=True)
    birth_date = models.DateField()
    # noinspection PyUnresolvedReferences
    gender = models.CharField(max_length=2, choices=Gender.choices, default=Gender.NOT_SPECIFIED)

    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)

    followed_authors = models.ManyToManyField(Author, related_name='followers', blank=True)
    followed_publishers = models.ManyToManyField(Publisher, related_name='followers', blank=True)
    favorite_genres = models.ManyToManyField(Genre, related_name='users', blank=True)

    first_name = None
    last_name = None

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class UserBook(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewed_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    # noinspection PyUnresolvedReferences
    situation = models.CharField(max_length=2, choices=Situation.choices, default=Situation.READING)
    rating = models.FloatField(null=True, blank=True)
    review = models.TextField(blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')
