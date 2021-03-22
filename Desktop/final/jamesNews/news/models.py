import datetime
from django.db import models
from django.contrib.auth.models import User


class Authors(models.Model):
    name = models.CharField(max_length=50, blank=False)
    username = models.CharField(max_length=50, blank=False, unique=True)
    password = models.CharField(max_length=50, blank=False)
    account = models.OneToOneField(User, on_delete=models.CASCADE)

    def __init__(self, *args, **kwargs):
        super(Authors, self).__init__(*args, **kwargs)
        # when create a author, create a responding user
        user = User.objects.create_user(username=self.username, password=self.password)
        user.save()
        self.account = user


class Stories(models.Model):
    key = models.AutoField(auto_created=True, primary_key=True)
    headline = models.CharField(max_length=64)

    POLITICS = 'pol'
    ART = 'art'
    TECHNOLOGY = 'tech'
    TRIVIAL = 'trivia'
    CATEGORY_CHOICES = (
        (POLITICS, 'Politics News'),
        (ART, 'Art News'),
        (TECHNOLOGY, 'Technology News'),
        (TRIVIAL, 'Trivial News'),
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
    )

    UK = 'uk'
    EUROPEAN = 'eu'
    WORLD = 'w'
    REGION_CHOICES = (
        (UK, 'UK News'),
        (EUROPEAN, 'European News'),
        (WORLD, 'World News'),
    )
    region = models.CharField(
        max_length=20,
        choices=REGION_CHOICES,
        default=None
    )

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    details = models.CharField(max_length=512)

    def switchJson(self):
        json = {
            'key': self.key,
            'headline': self.headline,
            'story_cat': self.category,
            'story_region': self.region,
            'author': self.author.username,
            'story_date': datetime.strftime(self.date, "%Y-%m-%d %H:%M:%S"),
            'story_details': self.details,
        }
        return json



