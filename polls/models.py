from django.db import models


# Create your models here.
from django import forms


class Poll(models.Model):
    title = models.CharField(max_length=100)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    del_flag = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Question(models.Model):
    text = models.TextField()
    SINGLE = '01'
    MULTIPLE = '02'
    TYPES = (
        (SINGLE, 'Single answer'),
        (MULTIPLE, 'Multiple answer')
    )
    type = models.CharField(max_length=2, default='01')
    poll = models.ForeignKey(Poll, on_delete=models.PROTECT)

    def __str__(self):
        return '(%s) %s' % (self.poll.title, self.text)


class Choice(models.Model):
    text = models.CharField(max_length=100)
    value = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)

    def __str__(self):
        return '(%s) %s' % (self.question.text, self.text)


class Answer(models.Model):
    choice = models.OneToOneField(Choice, on_delete=models.PROTECT)
    question = models.ForeignKey(Question, on_delete=models.PROTECT)


class Comment(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=500)
    email = models.EmailField(blank=True)
    tel = models.CharField(max_length=10)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title
