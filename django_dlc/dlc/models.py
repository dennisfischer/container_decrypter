from django.db import models

#LEXERS = [item for item in get_all_lexers() if item[1]]
#LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
#STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class DLC(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    dlc = models.TextField()
    links = models.TextField(blank=True)

    class Meta:
        ordering = ('created',)