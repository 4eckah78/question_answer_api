from django.db import models

class Question(models.Model):
    text = models.TextField("Текст вопроса")
    created_at = models.DateTimeField(auto_now_add=True)

class Answer(models.Model):
    question = models.ForeignKey(
        Question,
        on_delete=models.CASCADE,
        related_name='answers',
        db_column='question_id'
    )
    user_id = models.CharField("ID пользователя", max_length=36)
    text = models.TextField("Текст ответа")
    created_at = models.DateTimeField(auto_now_add=True)