from typing import Text
from django.db import models
from numpy.lib.twodim_base import triu_indices_from

# Create your models here.
class intents(models.Model):
    name = models.CharField(max_length=128)
    def __str__(self) -> str:
        return '['+str(self.id)+'] '+self.name

class conversations(models.Model):
    name = models.CharField(max_length=128)
    def __str__(self) -> str:
        return '['+str(self.id)+'] '+self.name

class responses(models.Model):
    name = models.CharField(max_length=128)
    def __str__(self) -> str:
        return '['+str(self.id)+'] '+self.name

class intentSamples(models.Model):
    intent = models.ForeignKey(intents,on_delete=models.CASCADE)
    text = models.CharField(max_length=2048)
    product_ref = models.IntegerField(null=True)
    def __str__(self) -> str:
        return '['+self.intent+'] '+self.text+'|'+self.product_ref

class responseSamples(models.Model):
    response = models.ForeignKey(responses,on_delete=models.CASCADE)
    text = models.CharField(max_length=2048)
    def __str__(self) -> str:
        return '['+self.response+'] '+self.text

class conversationSamples(models.Model):
    conversation = models.ForeignKey(conversations,on_delete=models.CASCADE)
    index_ref = models.IntegerField()
    intent = models.ForeignKey(intents,null=True,on_delete=models.DO_NOTHING)
    response = models.ForeignKey(responses,null=True,on_delete=models.DO_NOTHING)
    def __str__(self) -> str:
        return '['+self.conversation+'] '+self.intent+'->'+self.response

class trainingModels(models.Model):
    fileModel = models.FileField(null=True)
    fileCountVect = models.FileField(null=True)
    fileFitTransform = models.FileField(null=True)
    acc_train = models.FloatField(null=True)
    acc_validate = models.FloatField(null=True)
    insert_time = models.DateField(auto_now=True)
    active = models.BooleanField(default=False)