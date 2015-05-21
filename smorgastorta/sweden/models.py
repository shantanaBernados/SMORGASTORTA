from django.db import models

from django.contrib.auth.models import User

# Create your models here.
class HWQuestion(models.Model):
	srh = models.FloatField()	
	sleep = models.FloatField()	
	concentration = models.FloatField()	
	stress = models.FloatField()
	energy = models.FloatField()	
	control = models.FloatField()	
	social = models.FloatField()	
	efficiency = models.FloatField()	
	satisfaction = models.FloatField()	
	work_load = models.FloatField()	
	atmosphere = models.FloatField()	


class SleepQuestion(models.Model):
	sleep_1 = models.IntegerField()
	sleep_2 = models.IntegerField()
	sleep_3 = models.IntegerField()
	sleep_4 = models.IntegerField()
	sleep_5 = models.IntegerField()


class Assessment(models.Model):
	srh = models.BooleanField()	
	sleep = models.BooleanField()	
	sick_leave = models.BooleanField()	
	
	
class User_HWQ_Assessment(models.Model):
	user = models.ForeignKey(User)
	hwQ = models.ForeignKey(HWQuestion)
	ass = models.ForeignKey(Assessment)
	date = models.DateField(auto_now=True)


