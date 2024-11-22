from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class SubFunction(models.Model):
    task = models.ForeignKey(Task, related_name='subfunctions', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class BehaviorModel_A(models.Model):
    task = models.ForeignKey(Task, related_name="a_choices", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class BehaviorModel_B(models.Model):
    task = models.ForeignKey(Task, related_name="b_choices", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name