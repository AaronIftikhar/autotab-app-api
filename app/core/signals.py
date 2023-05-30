from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Project, ProjectInstance
from django.utils.text import slugify

@receiver(pre_save, sender = Project)
def add_slug(sender,instance, *args, **kwargs):
    if instance and not instance.project_title_slug:
        project_title_slug = slugify(instance.project_title)
        instance.project_title_slug = project_title_slug



@receiver(pre_save, sender = ProjectInstance)
def add_slug(sender,instance, *args, **kwargs):
    if instance and not instance.project_instance_slug:
        project_instance_slug = slugify(instance.project_instance_name)
        instance.project_instance_slug = project_instance_slug