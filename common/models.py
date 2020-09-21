from django.db import models
from django.contrib.auth.models import AbstractUser


class AvatarUser(AbstractUser):
    server_group_id = models.TextField(max_length=500, default='')
    server_group_address = models.TextField(max_length=500, default='')
    server_group_status = models.TextField(max_length=500, default='CHECKING')
    last_check = models.DateTimeField(null=True, default=None)
