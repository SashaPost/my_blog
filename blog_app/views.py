from django.template import loader
from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def check(request):
    hello = '<h1>Hello</h1>'
    return HttpResponse(hello)

def test(request):
    # template_name = 'blog_app/test.html'
    template = loader.get_template('blog_app/test.html')
    context = {
        'test': "This is a test message.",
    }
    return HttpResponse(template.render(context, request))