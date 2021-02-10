import random

from django import forms
from django.http import HttpResponseRedirect
from markdown2 import Markdown
from django.shortcuts import render
from django.urls import reverse

from . import util

class NewPageForm(forms.Form):
    title = forms.CharField(label="Title", widget= forms.TextInput(attrs={"placeholder": "Title"}))
    content = forms.CharField(label="Content", widget= forms.Textarea(attrs={"placeholder": "Type in the Markdown content"}))
    
class EditPageForm(forms.Form):
    content = forms.CharField(label="Content", widget= forms.Textarea(attrs={"placeholder": "Type in the Markdown content"}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    entryTitle = util.get_entry(title)
    if entryTitle is None:
        return render(request, "encyclopedia/noneExisting.html", {
         "title": title.capitalize()   
        })
    else:
        markdowner = Markdown()
        return render(request, "encyclopedia/entry.html", {
            "entry": markdowner.convert(entryTitle),
            "title": title.capitalize()
        })          
            
        
def search(request):
    q = request.GET.get("q")
    search = q.strip()
    entryTitle = util.get_entry(search)
    substring = []
    list = util.list_entries()
    if entryTitle is not None:
        return HttpResponseRedirect(reverse("entry", kwargs={"title": search}))
    else:
        for title in list:
            if search.capitalize() in title.capitalize():
                substring.append(title)
        return render(request, "encyclopedia/searchResult.html", {
            "entries": substring
        })
            
def newPage(request):
    if request.method == "POST":
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            entryTitle = util.get_entry(title)
            if entryTitle is not None:
                return render(request, "encyclopedia/existingTitle.html", {
                    "form": form,
                    "title": title.capitalize()
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry", kwargs={"title": title})) 
        else:
            return render(request, "encyclopedia/newPage.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/newPage.html", {
            "form": NewPageForm
        })  

def edit(request, title):
    if request.method == "POST":
        form = EditPageForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"]
            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry", kwargs={"title": title}))
    else:        
        entry = util.get_entry(title)
        form = EditPageForm(initial={'content': entry})
        
        return render(request, "encyclopedia/editpage.html", {
            "form": form,
            "title": title
        })
        
def randomEntry(request):
    list = list = util.list_entries()
    entry = random.choice(list)
    title = util.get_entry(entry)
    markdowner = Markdown()
    return render(request, "encyclopedia/random.html", {
        "entry": markdowner.convert(title),
        "title": entry
    })