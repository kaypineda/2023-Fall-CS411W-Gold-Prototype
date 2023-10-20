from django.http import HttpResponse
from django.template import loader

def index(request):
    template = loader.get_template('index.html')
    return HttpResponse(template.render())

def aboutUs(request):
    template = loader.get_template('about-us.html')
    return HttpResponse(template.render())

def problem(request):
    template = loader.get_template('problem.html')
    return HttpResponse(template.render())

def deliverables(request):
    template = loader.get_template('deliverables.html')
    return HttpResponse(template.render())

def presentations(request):
    template = loader.get_template('presentations.html')
    return HttpResponse(template.render())

def labs(request):
    template = loader.get_template('labs.html')
    return HttpResponse(template.render())

def references(request):
    template = loader.get_template('references.html')
    return HttpResponse(template.render())

def login(request):
    template = loader.get_template('login.html')
    return HttpResponse(template.render())
    