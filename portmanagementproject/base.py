from django.db import models
import time        

def get_fingerprint():
    return time.time()

# Create your models here.
class AbstractBaseModel(models.Model):
    """
    Captures BaseContent as created On and modified On and active field.
    common field accessed for the following classes.
    """

    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
   
  
    class Meta:
        abstract = True

    def __str__(self):
        return self.id
