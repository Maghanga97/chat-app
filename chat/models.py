from django.db import models

# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=255, unique=True)

class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    text_msg = models.CharField(max_length=1000)
    time_stamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time_stamp']