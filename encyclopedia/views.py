from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import Http404, HttpResponseBadRequest, HttpResponseRedirect
from django import forms
from markdown2 import Markdown

import random

from . import util

class NewEntryForm(forms.Form):
    title = forms.CharField(label="Title", widget=forms.TextInput())
    content = forms.CharField(label="Content", widget=forms.Textarea())


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    try:
        md = Markdown()
        entry = md.convert(util.get_entry(title))
    except TypeError:
        raise Http404("The requested page was not found") 
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "entry": entry
    })


def search(request):
    query = request.GET["q"]
    entries = util.list_entries()
    if query in entries:
        return entry(request, query)
    else:
        return render(request, "encyclopedia/search_results.html", {
            "results": [entry for entry in entries if query.lower() in entry.lower()]
        })


def create(request):
    if request.method == "POST":

        form = NewEntryForm(request.POST)

        if form.is_valid():

            title = form.cleaned_data["title"]
            content = '#'+title+'\r\n'+form.cleaned_data["content"]

            if title in util.list_entries():
                messages.warning(request, "Entry with such title already exists!")

            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry-view", args=[title]))

        else:
            return render(request, "encyclopedia/create.html", {
                "form": form
            })

    return render(request, "encyclopedia/create.html", {
        "form": NewEntryForm()
    })


def edit(request, title):
    entry = util.get_entry(title)

    if request.method == "POST":
        form = NewEntryForm(request.POST, {"title": title, "content": entry})

        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            util.save_entry(title, content)
            return HttpResponseRedirect(reverse("entry-view", args=[title]))

    else:
        form = NewEntryForm({"title": title, "content": entry})

    return render(request, "encyclopedia/edit.html", {
    	"title": title,
        "form": form
    })


def random_entry(request):
    return HttpResponseRedirect(reverse(
                                "entry-view", 
                                args=[random.choice(util.list_entries())]))