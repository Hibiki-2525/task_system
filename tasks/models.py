from django.db import models

class Task(models.Model):
    name = models.CharField(max_length=255)
    hosoku = models.CharField(max_length=255)

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

class SubFunction(models.Model):
    task = models.ForeignKey(Task, related_name='subfunctions', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    hosoku = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    is_special = models.BooleanField(default=False)  # 特別なサブ関数かどうかを示すフィールド
    
    def __str__(self):
        return self.name
    
class SubFunctionVarValue(models.Model):
    subfunction = models.ForeignKey(SubFunction, on_delete=models.CASCADE, related_name='var_values')
    var = models.ForeignKey(BehaviorModel_A, on_delete=models.CASCADE)
    value = models.FloatField()  # 必要に応じてデータ型を変更

    def __str__(self):
        return f"{self.var.name}: {self.value}"


class Answer_bemodel(models.Model):
    sub_function = models.ForeignKey(SubFunction, related_name='answer_bemodels', on_delete=models.CASCADE)
    behavior_model_a_1 = models.ForeignKey(BehaviorModel_A, related_name='first_part', on_delete=models.CASCADE,default=1 )
    behavior_model_a_2 = models.ForeignKey(BehaviorModel_A, related_name='middle_part', on_delete=models.CASCADE,default=1 )
    behavior_model_b = models.ForeignKey(BehaviorModel_B, related_name='last_part', on_delete=models.CASCADE,default=1 )


    def __str__(self):
        return f"{self.behavior_model_a_1.name} {self.behavior_model_b.name} {self.behavior_model_a_2.name}"

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
    
class TaskVarValue(models.Model):
    task = models.ForeignKey(Task, related_name='TaskVarValue', on_delete=models.CASCADE)
    var = models.ForeignKey(BehaviorModel_A, on_delete=models.CASCADE)
    value = models.FloatField()  # 必要に応じてデータ型を変更

    def __str__(self):
        return f"{self.var.name}: {self.value}"


class task_Answer_bemodel(models.Model):
    task = models.ForeignKey(Task, related_name='task_Answer_bemodel', on_delete=models.CASCADE)
    behavior_model_a_1 = models.ForeignKey(BehaviorModel_A, related_name='first', on_delete=models.CASCADE,default=1 )
    behavior_model_a_2 = models.ForeignKey(BehaviorModel_A, related_name='middle', on_delete=models.CASCADE,default=1 )
    behavior_model_b = models.ForeignKey(BehaviorModel_B, related_name='last', on_delete=models.CASCADE,default=1 )


    def __str__(self):
        return f"{self.behavior_model_a_1.name} {self.behavior_model_b.name} {self.behavior_model_a_2.name}"
    
class task_Answer_code(models.Model):  
    task = models.ForeignKey(Task, related_name='task_Answer_code', on_delete=models.CASCADE)
    correct_code = models.TextField()

    def get_correct_answer_list(self):
        # 正解コードを行ごとに分割してリストにする
        return self.correct_code.strip().replace('\r\n', '\n').replace('\r', '\n').split('\n')
    
class Test(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
class TestCard(models.Model):
    test = models.ForeignKey(Test, related_name='TestCard', on_delete=models.CASCADE)
    testcard = models.CharField(max_length=200)


    def __str__(self):
        return self.testcard
    
class PreTestAnswer(models.Model):
    user_name = models.CharField(max_length=255)  # 名前（セッションから取得）
    test = models.ForeignKey(Test, on_delete=models.CASCADE)  # 対象のテスト
    answers = models.TextField()  # 回答内容（JSON文字列などで保存）
    submitted_at = models.DateTimeField(auto_now_add=True)  # 提出日時

    def __str__(self):
        return f"{self.user_name} - {self.test.name}"
    
class ProTestAnswer(models.Model):
    user_name = models.CharField(max_length=255)  # 名前（セッションから取得）
    test = models.ForeignKey(Test, on_delete=models.CASCADE)  # 対象のテスト
    answers = models.TextField()  # 回答内容（JSON文字列などで保存）

    def __str__(self):
        return f"{self.user_name} - {self.test.name}"

