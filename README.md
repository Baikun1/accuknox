
## Question 1: By default, are Django signals executed synchronously or asynchronously?
### Answer:
    By default, Django signals are executed synchronously. This means that the signal handler runs in the same process and thread as the code that triggered the signal, and it blocks execution until the handler completes.

```python
# models.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import models
import time

class MyModel(models.Model):
    name = models.CharField(max_length=100)

@receiver(post_save, sender=MyModel)
def my_signal_handler(sender, instance, **kwargs):
    print("Signal handler starts")
    time.sleep(5)  # Simulating a long-running task
    print("Signal handler ends")

# To test:
instance = MyModel.objects.create(name="Test")  # Signal handler will block for 5 seconds
print("This prints after the signal handler is done")

```
## Explanation:
    In this example, when a new MyModel instance is created, the post_save signal is triggered. Since the signal handler is synchronous by default, the "This prints after the signal handler is done" message will not be printed until after the signal handler completes its 5-second delay.
## Question 2: Do Django signals run in the same thread as the caller?
### Answer:
    Yes, Django signals run in the same thread as the caller by default. This means that if the caller is running in the main thread, the signal handler also runs in the main thread.

```python
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
```
## Explanation:
    When you run this code, both the caller and the signal handler will print the same thread name (typically MainThread), demonstrating that they run in the same thread.

## Question 3: By default, do Django signals run in the same database transaction as the caller?
### Answer:
    Yes, by default, Django signals are executed in the same database transaction as the caller. If a transaction is rolled back, the signal handler's effects (like database operations) will also be rolled back.

```python
python
Copy code
# models.py
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db import transaction

class MyModel(models.Model):
    name = models.CharField(max_length=100)

@receiver(post_save, sender=MyModel)
def my_signal_handler(sender, instance, **kwargs):
    print("Signal handler running")
    instance.name = "Modified by signal"
    instance.save()

# To test in the shell:
with transaction.atomic():
    instance = MyModel.objects.create(name="Test")
    raise Exception("Rolling back transaction")

# After this, check if "Modified by signal" was saved; it will not be because the transaction was rolled back.
```
## Explanation:
    The signal handler modifies the name of the MyModel instance, but because an exception is raised in the atomic block, the entire transaction, including the changes made by the signal, is rolled back.

### Custom Classes in Python
### Rectangle Class
### Requirements:
- The Rectangle class should have length and width as attributes.
- The instance should be iterable.
- Iterating over the instance should first return the length as {'length': <VALUE>} and then the width as {'width': <VALUE>}.
### Code Implementation:
```python
class Rectangle:
    def __init__(self, length: int, width: int):
        self.length = length
        self.width = width

    def __iter__(self):
        yield {'length': self.length}
        yield {'width': self.width}

# Example usage:
rectangle = Rectangle(10, 5)

# Iterating over the instance
for dimension in rectangle:
    print(dimension)
```
## Explanation:

- The __init__ method initializes the rectangle with a length and width.
- The __iter__ method makes the object iterable, yielding the length and width in dictionary format as per the requirements.
## Output:

```python
{'length': 10}
{'width': 5}
```