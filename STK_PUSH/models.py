from django.db import models
from django.contrib.auth.hashers import make_password

class Meetings(models.Model):
    venue = models.CharField(max_length=60)
    date = models.DateField()
    time = models.TimeField()

    def __str__(self):
        return self.venue

# RegisterChama model
class RegisterChama(models.Model):
    first_name = models.CharField(max_length=50)  # Required
    last_name = models.CharField(max_length=50)  # Required
    name_of_chama = models.CharField(max_length=50)  # Required
    phone_number = models.CharField(max_length=50)  # Required
    email = models.EmailField(unique=True)  # Required
    id_number = models.IntegerField()  # Required
    county = models.CharField(max_length=50)  # Required
    password = models.CharField(max_length=128)  # Required and hashed

    def save(self, *args, **kwargs):
        """Ensure password is stored securely."""
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_of_chama

# Member SignUp model
class SignUp(models.Model):
    first_name = models.CharField(max_length=50)  # Required
    last_name = models.CharField(max_length=50)  # Required
    phone_number = models.CharField(max_length=15)  # Required
    email = models.EmailField(unique=True)  # Required
    name_of_chama = models.CharField(max_length=50)  # Required
    password = models.CharField(max_length=128)  # Required and hashed

    def save(self, *args, **kwargs):
        """Ensure password is stored securely."""
        self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Article(models.Model):
    title = models.CharField(max_length=200)  # Title of the article
    headline = models.CharField(max_length=300)  # Short headline/description
    link = models.URLField(max_length=500)  # Link to the article
    image = models.ImageField(upload_to='articles/')  # Image for the article

    def __str__(self):
        return self.title

