from djongo import models

class Tweets(models.Model):
    nama = models.CharField(max_length=50)
    username = models.CharField(max_length=50, null=True)
    tweet = models.TextField(null=True)
    list_tweet = models.TextField(null=True)
    label = models.CharField(max_length=15)
    tanggal = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

class Datasets(models.Model):
    keyword = models.CharField(max_length=50)
    tipe_data = models.CharField(max_length=25)
    tweets = models.ArrayField(
        model_container = Tweets
    )
    tanggal_update = models.DateTimeField(auto_now=True)