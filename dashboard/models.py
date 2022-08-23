from django.db import models
from django.conf import settings
from portmanagementproject.base import AbstractBaseModel, get_fingerprint

""" File Model - stores uploaded files as it is. """

class File(models.Model):
    file = models.FileField(blank=False, null=False)
    remark = models.CharField(max_length=20)
    timestamp = models.DateTimeField(auto_now_add=True)

class Dump(AbstractBaseModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='owner_dumps')
    original_file = models.CharField(max_length=254, blank=True, editable=True)  
    file_name = models.CharField(max_length=254, blank=True, editable=True)
    class Meta:
        ordering = ['-created_on']
  
    def __str__(self):
        return f'{self.owner}-{self.created_on}-{self.id}'

class Table(AbstractBaseModel):
    dump = models.ForeignKey(Dump,on_delete=models.CASCADE,related_name='dump_tables')
    delta_path = models.CharField(max_length=254, null=True, blank=True)
    # sample_path = models.CharField(max_length=254, null=True, blank=True)
    table_name = models.CharField(blank=False, max_length=254)
    fingerprint = models.CharField(unique=True, max_length=254, blank=False, editable=False, default=get_fingerprint)
   
    class Meta:
        ordering = ['-created_on']
  
    def __str__(self):
        return f'{self.dump}-{self.created_on}-{self.id}'

class Field(AbstractBaseModel):
    table = models.ForeignKey(Table,on_delete=models.CASCADE,related_name='table_fields', blank=True,
        null=True)
    dump = models.ForeignKey(Dump,on_delete=models.CASCADE,related_name='dump_fields', blank=True,
        null=True)
    field_name = models.CharField(blank=False, max_length=254)
    field_type = models.CharField(blank=False, max_length=254)
    fingerprint = models.CharField( max_length=254, blank=True,editable=False,unique=True,default=get_fingerprint)
   
    class Meta:
        ordering = ['-created_on']
  
    def __str__(self):
        return f'{self.table}-{self.created_on}-{self.id}'