import json

from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from django.shortcuts import render

from blog.models import Article
from blog.schemas import ArticleSchema, ArticleResponseSchema

@csrf_exempt #Testing purposes only
@require_http_methods('POST')
def create_article(request):
    try:
        json_data = json.loads(request.body)
        # fetch the user and pass it to schema
        author = User.objects.get(id=json_data['author'])
        schema = ArticleSchema.create(
            author=author,
            title=json_data['title'],
            content=json_data['content']
        )
        return JsonResponse({
            'article': schema.dict()
        })
    except User.DoesNotExist:
        return JsonResponse({'detail': 'Cannot find a user with this id.'}, status=404)

def get_article(request, article_id):
    try:
        article = Article.objects.get(id=article_id)
        schema = ArticleSchema.from_django(article)
        return JsonResponse({
            'article': schema.dict()
        })
    except Article.DoesNotExist:
        return JsonResponse({'detail': 'Cannot find an article with this id.'}, status=404)

def get_all_articles(request):
    articles = Article.objects.all()
    data = []

    for article in articles:
        schema = ArticleResponseSchema.from_django(article)
        data.append(schema.dict())

    return JsonResponse({
        'articles': data
    })