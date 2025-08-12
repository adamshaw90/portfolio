from django.db import models


class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    tech_stack = models.CharField(max_length=200)
    image = models.ImageField(upload_to='project_images/')
    live_link = models.URLField(blank=True, null=True)
    code_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title
