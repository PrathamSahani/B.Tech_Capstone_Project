from django.db import models

class Municipality(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    state = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)

    def __str__(self):
        return self.name
    
    
class Dump(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    current_location = models.CharField(max_length=100)
    image = models.ImageField(upload_to='dump_images/')
    current_city = models.CharField(max_length=100)
    dump_type = models.CharField(max_length=20, choices=(('Sukha', 'Sukha'), ('Gilla', 'Gilla')))
    dump_size = models.CharField(max_length=20, choices=(('Small', 'Small'), ('Normal', 'Normal'), ('Large', 'Large')))
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
