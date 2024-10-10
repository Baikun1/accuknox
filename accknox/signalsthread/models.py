python
Copy code
# models.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
import threading

class MyModel(models.Model):
    name = models.CharField(max_length=100)

@receiver(post_save, sender=MyModel)
def my_signal_handler(sender, instance, **kwargs):
    print(f"Signal handler running in thread: {threading.current_thread().name}")

# To test:
print(f"Caller running in thread: {threading.current_thread().name}")
instance = MyModel.objects.create(name="Test")