from django.db import models


class Logs(models.Model):
    action_choices = (('created', 'created'),
                      ('updated', 'updated'),
                      ('refresh', 'refresh'))
    created_at = models.DateTimeField(auto_now=True, blank=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    action = models.CharField(max_length=10, choices=action_choices)
    url = models.CharField(max_length=100)
