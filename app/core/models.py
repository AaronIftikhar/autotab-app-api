import uuid
import os

""" Database models """
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


def getProjectName(instance):
    project_name = instance.project_instance_tab_instance.project_instance.project_title
    return project_name

def getProjectInstanceName(instance):
    project_instance_name = instance.project_instance_tab_instance.project_instance_name
    return project_instance_name

def getProjectInstanceTabName(instance):
    project_instance_tab_name = instance.tab_instance_name
    return project_instance_tab_name

def project_data_file_path(instance, filename):
    """ Generate file path for new project datafile"""
    ext = os.path.splitext(filename)[1]
    """" Here we tale the extenstion of the filename"""
    filename = f'{uuid.uuid4()}{ext}'
    """ Now create a new filname, which is the uuid and the extention, (uuid).png"""
    user_company_name = instance.user.company_name
    user_email = instance.user.email

    project_name = getProjectName(instance)

    return os.path.join('uploads',user_company_name,user_email,project_name,'main_data',filename)

def project_data_file_path_weights(instance, filename):
    """ Generate file path for new project datafile"""
    ext = os.path.splitext(filename)[1]
    """" Here we tale the extenstion of the filename"""
    filename = f'{uuid.uuid4()}{ext}'
    """ Now create a new filname, which is the uuid and the extention, (uuid).png"""
    user_company_name = instance.user.company_name
    user_email = instance.user.email

    project_name = getProjectName(instance)
    return os.path.join('uploads',user_company_name,user_email,project_name,'weights',filename)


def project_data_file_path_dicts(instance, filename):
    """ Generate file path for new project datafile"""
    ext = os.path.splitext(filename)[1]
    """" Here we tale the extenstion of the filename"""
    filename = f'{uuid.uuid4()}{ext}'
    """ Now create a new filname, which is the uuid and the extention, (uuid).png"""
    user_company_name = instance.user.company_name
    user_email = instance.user.email

    project_name = getProjectName(instance)

    return os.path.join('uploads',user_company_name,user_email,project_name,'dictionaries',filename)


def project_data_file_path_recode(instance, filename):
    """ Generate file path for new project datafile"""
    ext = os.path.splitext(filename)[1]
    """" Here we tale the extenstion of the filename"""
    filename = f'{uuid.uuid4()}{ext}'
    """ Now create a new filname, which is the uuid and the extention, (uuid).png"""
    user_company_name = instance.user.company_name
    user_email = instance.user.email

    project_name = getProjectName(instance)

    return os.path.join('uploads',user_company_name,user_email,project_name,'recode',filename)


def project_data_file_path_regroup(instance, filename):
    """ Generate file path for new project datafile"""
    ext = os.path.splitext(filename)[1]
    """" Here we tale the extenstion of the filename"""
    filename = f'{uuid.uuid4()}{ext}'
    """ Now create a new filname, which is the uuid and the extention, (uuid).png"""
    user_company_name = instance.user.company_name
    user_email = instance.user.email

    project_name = getProjectName(instance)

    return os.path.join('uploads',user_company_name,user_email,project_name,'regroup',filename)




def get_original_file_name(instance, filename):

    og_filename = os.path.splitext(filename)[1]

    return og_filename

class UserManager(BaseUserManager):
    """ Manager for users """

    def create_user(self,email,password=None,**extra_field):
        """ Create, save and return a new user, extra fields allows more key word arguments to be called"""
        if not email:
            raise ValueError('User must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_field)
        user.set_password(password)
        """ Sets encrypted password """
        user.save(using = self.db)
        """ self.db is used to support using more databases, which I won't be I don't think, but just best practice"""

        return user

    def create_superuser(self, email, password):
        """ Create and return a new superuser """
        user = self.create_user(email,password)
        user.is_staff = True
        user.is_superuser = True

        user.save(using = self.db)

        return user

class User(AbstractBaseUser, PermissionsMixin):
    """ User in the system """
    email = models.EmailField(max_length =255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    """Users active by default"""
    is_staff = models.BooleanField(default=False)
    """ Can users log into admin? """
    company_name = models.CharField(max_length=255)
    objects = UserManager()
    """ Assign user manager to model """
    USERNAME_FIELD = 'email'
    """ This is the field we use for authentication """
    """ Overwrite the save method to add the logic to split the company from the"""
    def save(self, *args, **kwargs):
        self.company_name = ((str(self.email)).split("@",1)[1]).split('.')[0]
        super(User, self).save(*args, **kwargs) # Call the "real" save() method.


class Project(models.Model):

    """ Project object """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="linked_projects",
    )

    company_name_project = models.CharField(max_length=255)
    project_title = models.CharField(max_length=255)
    project_title_slug = models.SlugField(max_length=255,unique=True)

    def __str__(self):
        return self.project_title

    def save(self, *args, **kwargs):
        self.company_name_project = ((str(self.user.email)).split("@",1)[1]).split('.')[0]
        super(Project, self).save(*args, **kwargs) # Call the "real" save() method.


class ProjectInstance(models.Model):

    """ Project = HMT """
    """ Project Instance = Wave 11 """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="linked_project_instances",
    )

    company_name_project_instance = models.CharField(max_length=255)

    project_instance_name = models.CharField(null = True,max_length=255,unique=True)
    project_instance = models.ForeignKey(Project, on_delete=models.CASCADE,
                                          null=True, related_name="projectinstances")
    project_instance_slug = models.SlugField(max_length=255,unique=True)

    def __str__(self):
        return self.project_instance_name

    def save(self, *args, **kwargs):
        self.company_name_project_instance = ((str(self.user.email)).split("@",1)[1]).split('.')[0]
        super(ProjectInstance, self).save(*args, **kwargs) # Call the "real" save() method.


# need some functions to save files somewhere #

class TabInstance(models.Model):

    """ Project = HMT """
    """ Project Instance = HMT, Wave 11 """
    """ Tab Instance = HMT, Wave 11, Xtab_v1 """
    """ Here we need all the files, weighting, dictionary, regrourp, recode"""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="linked_project_tab_instances",
    )

    tab_instance_name = models.CharField(null = True,max_length=255,unique=True)
    project_instance_tab_instance = models.ForeignKey(ProjectInstance, on_delete=models.CASCADE,
                                                      null=True, related_name="tabinstances")
    company_name_project_instance_tab = models.CharField(max_length=255)

    """ Now the main data file field """

    main_data = models.FileField(null=True, blank= True, upload_to= project_data_file_path)
    main_data_og_name = models.CharField(max_length=255, null=True, blank = True)

    def get_filename(self):

        if self.main_data.name is None:
            return ""
        else:
            return os.path.basename(self.main_data.name)

    """ Now the weights file field """

    weight_data = models.FileField(null=True,blank=True, upload_to= project_data_file_path_weights)
    weight_data_og_name = models.CharField(max_length=255,null=True, blank = True)

    def get_filename_weights(self):
        if self.weight_data.name is None:
            return ""
        else:
            return os.path.basename(self.weight_data.name)

    """ Now the dictionary file field """

    dictionary_data = models.FileField(null=True,blank=True, upload_to= project_data_file_path_dicts)
    dictionary_data_og_name = models.CharField(max_length=255,null=True, blank = True)

    def get_filename_dictionary(self):
        if self.dictionary_data.name is None:
            return ""
        else:
            return os.path.basename(self.dictionary_data.name)

    """ Now the recoding file field """

    recoding_data = models.FileField(null=True,blank=True, upload_to= project_data_file_path_recode)
    recoding_data_og_name = models.CharField(max_length=255,null=True, blank = True)

    def get_filename_recode(self):
        if self.recoding_data.name is None:
            return ""
        else:
            return os.path.basename(self.recoding_data.name)

    """ Now the regroup file field """

    regroup_data = models.FileField(null=True,blank=True, upload_to= project_data_file_path_regroup)
    regroup_data_og_name = models.CharField(max_length=255,null=True, blank = True)

    def get_filename_regroup(self):
        if self.regroup_data.name is None:
            return ""
        else:
            return os.path.basename(self.regroup_data.name)

    """" Over write save method """

    def save(self, *args, **kwargs):

        self.company_name_project_instance_tab = ((str(self.user.email)).split("@",1)[1]).split('.')[0]

        if self.get_filename() == "":
            # This means it should be null
            self.main_data_og_name = None
        else:
            self.main_data_og_name = self.get_filename()

        if self.get_filename_weights() == "":
            # This means it should be null
            self.weight_data_og_name = None
        else:
            self.weight_data_og_name = self.get_filename_weights()

        if self.get_filename_dictionary() == "":
            # This means it should be null
            self.dictionary_data_og_name = None
        else:
            self.dictionary_data_og_name = self.get_filename_dictionary()

        if self.get_filename_recode() == "":
            # This means it should be null
            self.recoding_data_og_name = None
        else:
            self.recoding_data_og_name = self.get_filename_recode()

        if self.get_filename_regroup() == "":
            # This means it should be null
            self.regroup_data_og_name = None
        else:
            self.regroup_data_og_name = self.get_filename_regroup()

        super(TabInstance, self).save(*args, **kwargs) # Call the "real" save() method.









# class Recipe(models.Model):
#     """ Recipe object """

#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#     )
#     title = models.CharField(max_length=255)
#     description = models.TextField(blank=True)
#     time_minutes = models.IntegerField()
#     price = models.DecimalField(max_digits=5, decimal_places=2)
#     link = models.CharField(max_length=255, blank=True)
#     tags = models.ManyToManyField('Tag')
#     ingredients = models.ManyToManyField('Ingredient')
#     image = models.ImageField(null=True, upload_to=recipe_image_file_path)


#     def __str__(self):
#         return self.title
#     """ Special method of a class which allows you to return something, this shows in the django admin"""


# class Tag(models.Model):
#     """ Tag for filtering recipes """
#     name = models.CharField(max_length=255)
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#     )

#     def __str__(self):
#         return self.name

# class Ingredient(models.Model):
#     """Ingredient for recipes"""
#     name = models.CharField(max_length=255)
#     user = models.ForeignKey(
#         settings.AUTH_USER_MODEL,
#         on_delete=models.CASCADE,
#     )

#     def __str__(self):
#         return self.name