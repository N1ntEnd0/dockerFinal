from django.conf import settings
from django.db import models
from social_django.models import UserSocialAuth

class GDFile(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    owner = models.ForeignKey('social_django.UserSocialAuth', on_delete=models.CASCADE)
    quota = models.PositiveSmallIntegerField(default=0)

    class Meta:
        db_table = 'gd_files'



class CopyGDFile(models.Model):
    id = models.CharField(primary_key=True, max_length=255)
    original = models.ForeignKey(GDFile, null=False, related_name='original_copies', blank=False, on_delete=models.CASCADE)
    copy = models.ForeignKey('gdrive.CopyGDFile', null=True, blank=True, related_name='copy_copies', on_delete=models.CASCADE)
    owner = models.ForeignKey('social_django.UserSocialAuth', on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    
    class Meta:
        ordering = ['-created_date',]
        db_table = 'copy_files'
    
