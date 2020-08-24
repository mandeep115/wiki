from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import render
from django.urls import reverse
from markdown2 import Markdown
from django import forms
import random
import re

from . import util

class wikiform(forms.Form):
    title = forms.CharField(label="Title for your wiki entry")
    content = forms.CharField(label="Content for your wiki entry", widget=forms.Textarea)
class editform(forms.Form):
    title = forms.CharField(label="Edit title for your wiki entry")
    content = forms.CharField(label="Edit content for your wiki entry", widget=forms.Textarea)

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def title(request, title):
    title_data = util.get_entry(title)
    if not title_data:
        return render(request, "encyclopedia/appology.html", {
            "error": "Wiki title does not exit"
        })
    markdowner = Markdown()
    return render(request, "encyclopedia/title.html", {
        "title": title,
        "content": markdowner.convert(title_data),
    })

def search(request):
    q = request.GET['q']
    # print(q)
    title_list = util.list_entries()
    # print(title_list)
    found_list = []

    for title in title_list:
        # print(title)
        if re.match(f"{q.strip()}", title.lower()):
            # print("i'm in")
            found_list.append(title)
    # print(found_list)
    return render(request, "encyclopedia/index.html", {
        "entries": found_list
    })

def create(request):
    if request.method == "POST":
        form = wikiform(request.POST)
        
        if form.is_valid():
            
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("index"))

        else:
            return render(request, "tasks/add.html", {
                "title": title,
                "form": form
            })
    return render(request, "encyclopedia/create.html", {
        "form": wikiform()
    })

def edit(request, title):
    form = editform(initial={'title': title, 'content': util.get_entry(title)})
    return render(request, "encyclopedia/create.html", {
        "title": title,
        "form": form
    })

def random_page(request):
    
    title = random.choice(util.list_entries())
    title_data = util.get_entry(title)
    
    markdowner = Markdown()
    return render(request, "encyclopedia/title.html", {
        "title": title,
        "content": markdowner.convert(title_data)
    })