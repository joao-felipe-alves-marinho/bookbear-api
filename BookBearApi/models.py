from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models


# Create your models here.
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
    # Age rating choices
    EVERYONE = 'E'
    TEEN = 'T'
    MATURE = 'M'
    ADULT = 'A'
    AGE_RATING_CHOICES = {
        EVERYONE: 'Everyone',
        TEEN: 'Teen',
        MATURE: 'Mature',
        ADULT: 'Adult'
    }

    title = models.CharField(max_length=250)
    publication_date = models.DateField()
    synopsis = models.TextField(blank=True)
    score = models.FloatField(default=0.0)
    age_rating = models.CharField(max_length=2, choices=AGE_RATING_CHOICES, default=EVERYONE)

    cover = models.ImageField(upload_to='covers', blank=True, null=True)

    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, blank=True, null=True, related_name='books')
    authors = models.ManyToManyField(Author, related_name='books')
    genres = models.ManyToManyField(Genre, related_name='books')


class User(AbstractUser, PermissionsMixin):
    # Gender choices
    NOT_SPECIFIED = 'X'
    MALE_CIS = 'MC'
    FEMALE_CIS = 'FC'
    MALE_TRANS = 'MT'
    FEMALE_TRANS = 'FT'
    NON_BINARY = 'NB'
    OTHER = 'O'
    GENDER_CHOICES = {
        NOT_SPECIFIED: 'Not specified',
        MALE_CIS: 'Male Cisgender',
        FEMALE_CIS: 'Female Cisgender',
        MALE_TRANS: 'Male Transgender',
        FEMALE_TRANS: "Female Transgender",
        NON_BINARY: 'Non-binary',
        OTHER: 'Other'
    }

    email = models.EmailField(unique=True)
    username = models.CharField(max_length=250)
    summary = models.TextField(blank=True)
    birth_date = models.DateField()
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, default=NOT_SPECIFIED)

    avatar = models.ImageField(upload_to='avatars', blank=True, null=True)

    followed_authors = models.ManyToManyField(Author, related_name='followers', blank=True)
    followed_publishers = models.ManyToManyField(Publisher, related_name='followers', blank=True)
    favorite_genres = models.ManyToManyField(Genre, related_name='users', blank=True)

    first_name = None
    last_name = None

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'birth_date', 'gender']


class UserBook(models.Model):
    # Situation choices
    READING = 'R'
    STOPPED = 'S'
    COMPLETED = 'C'
    PENDING = 'P'
    ABANDONED = 'A'
    SITUATION_CHOICES = {
        READING: 'Reading',
        STOPPED: 'Stopped',
        COMPLETED: 'Completed',
        PENDING: 'Pending',
        ABANDONED: 'Abandoned'
    }

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviewed_books')
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    situation = models.CharField(max_length=2, choices=SITUATION_CHOICES, default=PENDING)
    rating = models.FloatField(null=True, blank=True)
    review = models.TextField(blank=True)
    date_added = models.DateField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')
