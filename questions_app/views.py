from django.http import JsonResponse, HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.shortcuts import get_object_or_404
from .models import Question, Answer
from typing import Any, Dict
import json
import logging

logger = logging.getLogger('questions_app')

@method_decorator(csrf_exempt, name='dispatch')
class QuestionListView(View):
    def get(self, request) -> JsonResponse:
        """GET /questions/ — список всех вопросов"""
        questions = Question.objects.all().values('id', 'text', 'created_at')
        return JsonResponse(list(questions), safe=False)

    def post(self, request) -> JsonResponse:
        """POST /questions/ — создать вопрос"""
        try:
            data = json.loads(request.body)
            text = data['text']
            if not text.strip():
                return JsonResponse({'error': 'Text is required'}, status=400)
            question = Question.objects.create(text=text)
            logger.info(f"Created question {question.id}")
            return JsonResponse({
                'id': question.id,
                'text': question.text,
                'created_at': question.created_at.isoformat()
            }, status=201)
        except (KeyError, json.JSONDecodeError) as e:
            return JsonResponse({'error': 'Invalid JSON or missing text'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class QuestionDetailView(View):
    def get(self, request, pk: int) -> JsonResponse:
        """GET /questions/{id} — вопрос + ответы"""
        question = get_object_or_404(Question, pk=pk)
        data = {
            'id': question.id,
            'text': question.text,
            'created_at': question.created_at.isoformat(),
            'answers': list(question.answers.values('id', 'user_id', 'text', 'created_at'))
        }
        return JsonResponse(data)

    def delete(self, request, pk: int) -> JsonResponse:
        """DELETE /questions/{id} — удалить вопрос (и ответы)"""
        question = get_object_or_404(Question, pk=pk)
        question.delete()
        logger.info(f"Deleted question {pk} and all answers")
        return JsonResponse({'status': 'deleted'}, status=204)

@method_decorator(csrf_exempt, name='dispatch')
class AnswerCreateView(View):
    def post(self, request, question_id: int) -> JsonResponse:
        """POST /questions/{id}/answers/ — добавить ответ"""
        question = get_object_or_404(Question, pk=question_id)
        try:
            data = json.loads(request.body)
            user_id = data['user_id']
            text = data['text']
            if not user_id or not text.strip():
                return JsonResponse({'error': 'user_id and text are required'}, status=400)
            answer = Answer.objects.create(question=question, user_id=user_id, text=text)
            logger.info(f"Answer {answer.id} added to question {question_id}")
            return JsonResponse({
                'id': answer.id,
                'user_id': answer.user_id,
                'text': answer.text,
                'created_at': answer.created_at.isoformat()
            }, status=201)
        except (KeyError, json.JSONDecodeError):
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

@method_decorator(csrf_exempt, name='dispatch')
class AnswerDetailView(View):
    def get(self, request, pk: int) -> JsonResponse:
        """GET /answers/{id} — получить ответ"""
        answer = get_object_or_404(Answer, pk=pk)
        return JsonResponse({
            'id': answer.id,
            'question_id': answer.question_id,
            'user_id': answer.user_id,
            'text': answer.text,
            'created_at': answer.created_at.isoformat()
        })

    def delete(self, request, pk: int) -> JsonResponse:
        """DELETE /answers/{id} — удалить ответ"""
        answer = get_object_or_404(Answer, pk=pk)
        answer.delete()
        logger.info(f"Answer {pk} deleted")
        return JsonResponse({'status': 'deleted'}, status=204)
