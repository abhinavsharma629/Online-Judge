from django.db import models
from django.contrib import admin
from django.contrib.auth.models import User
from .choices import *

class LanguageData(models.Model):
    languageChoice=models.PositiveIntegerField(choices = LANGUAGE_CHOICES, blank=True, null=True)
    problemMandatoryData=models.TextField(max_length=1000, null=True, blank=True)

class SubmissionData(models.Model):
    username= models.CharField(max_length=100)
    problemData=models.FileField(upload_to='portal/runCode',blank=True)
    inputFile=models.FileField(upload_to='portal/runCode',blank=True, null=True)
    submissionId=models.CharField(max_length=1000, primary_key=True)
    outputFile=models.FileField(upload_to='portal/runCode',blank=True, null=True)
    status= models.CharField(max_length=100, blank=True, null=True)

class savedCodeData(models.Model):
    codeId=models.AutoField(primary_key=True)
    username= models.CharField(max_length=100)
    problemData=models.FileField(upload_to='portal/savedCodes', blank=True)
    createdAt=models.DateTimeField(auto_now=True)
    lastUpdated=models.DateTimeField()

class savedNoteData(models.Model):
    noteId=models.AutoField(primary_key=True)
    username= models.CharField(max_length=100)
    noteData=models.FileField(upload_to='portal/savedNotes', blank=True)
    createdAt=models.DateTimeField(auto_now=True)
    lastUpdated=models.DateTimeField()