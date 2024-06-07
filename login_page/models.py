from django.db import models

# Stores Registered Users Data (username and email should be UNIQUE and country is NULLABLE)
class UserAuth(models.Model):
  username = models.CharField(max_length=20, unique=True, null=False, blank=False)
  email = models.EmailField(max_length=100, unique=True,)
  password = models.CharField(max_length=50, null=False, blank=False)
  country = models.CharField(max_length=50, null=True)


# Stores Registered Admins Data (username and email should be UNIQUE)
class AdminSuper(models.Model):
  username = models.CharField(max_length=20, unique=True)
  email = models.EmailField(max_length=100, unique=True,)
  password = models.CharField(max_length=50)


# Stores Deleted Users Data (username and email are Repeatable and country is NULLABLE)
class DeletedUser(models.Model):
    username = models.CharField(max_length=20, null=False, blank=False)
    email = models.EmailField(max_length=100)
    password = models.CharField(max_length=50, null=False, blank=False)
    country = models.CharField(max_length=50, null=True)


# Stores Updated Users Data (username and email are Repeatable and country is NULLABLE)
class UpdatedUser(models.Model):
    username = models.CharField(max_length=20, null=False, blank=False)
    email = models.EmailField(max_length=100, )
    password = models.CharField(max_length=50, null=False, blank=False)
    country = models.CharField(max_length=50, null=True)

