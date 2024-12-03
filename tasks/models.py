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
    
class Answer_bemodel(models.Model):
    sub_function = models.ForeignKey(SubFunction, related_name='Answer_bemodel', on_delete=models.CASCADE)
    bemodel = models.CharField(max_length=255)  # 正解のテキスト

    def __str__(self):
        return self.bemodel

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

class Card(models.Model):
    task = models.ForeignKey(Task, related_name='Card', on_delete=models.CASCADE)
    card = models.CharField(max_length=200)


    def __str__(self):
        return self.card

class Answer_code(models.Model):  
    sub_function = models.ForeignKey(SubFunction, related_name='Answer_code', on_delete=models.CASCADE)
    correct_code = models.TextField()

    def get_correct_answer_list(self):
        # 正解コードを行ごとに分割してリストにする
        return self.correct_code.strip().replace('\r\n', '\n').replace('\r', '\n').split('\n')