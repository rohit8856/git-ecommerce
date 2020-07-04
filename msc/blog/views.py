from django.http import HttpResponse
from django.shortcuts import render
from . models import Blogpost

# Create your views here.
def index(request):
    myposts = Blogpost.objects.all()
    print(myposts)
    return render(request,'blog/indexb.html',
    {'myposts':myposts})


def blogpost(request,id):
    post = Blogpost.objects.filter(post_id = id)[0]
    print(post)
    return render(request,'blog/blogpost.html',{'post': post})