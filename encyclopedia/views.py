from http.client import HTTPResponse

import markdown2
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
import markdown2
from . import util
from django import forms
from django.urls import reverse
import pathlib
import random

class Searchform(forms.Form):
    search=forms.CharField(label="search")

class Editform(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'
    title = forms.CharField(label="title")
    content = forms.CharField(widget=forms.Textarea, label="content")

class Createform(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'
    title = forms.CharField(label="title")
    content = forms.CharField(widget=forms.Textarea, label="content")
def index(request):
    print("i am inside index")
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": Searchform()
    })
def title(request, title_name):
    print("i am inside title")
    content=util.get_entry(title_name)
    # print(content)
    if content == None:
        # print("inside")
        return render(request, "encyclopedia/title.html", {
            "content": "<h1>404 Not Found</h1>",
            "title_name": "404 Not Found",
            "form": Searchform()
        })
    return render(request, "encyclopedia/title.html", {
        "content": markdown2.markdown(content),
        "title_name": title_name,
        "form": Searchform()
    })
def search(request):
    form = Searchform(request.POST)

    print("i am inside search")
    if form.is_valid():
        print(form.cleaned_data["search"])
        print(util.list_entries())
        sure_result = list(filter(lambda result: result.lower()==form.cleaned_data["search"].lower(), util.list_entries()))
        possible_results = list(filter(lambda result: result.lower().find(form.cleaned_data["search"].lower()) != -1, util.list_entries()))
        print("sure_result", sure_result)
        if len(sure_result):
            return title(request, form.cleaned_data["search"])
        return render(request, "encyclopedia/search_result.html", {
            "search_name": form.cleaned_data["search"],
            "results": possible_results
        })
    else:
        nxt = request.POST["next"]
        return HttpResponseRedirect(nxt)

def edit(request, title_name):
    if request.method == "POST":
        try:
            rt = request.form["return"]
            if rt == True:
                HttpResponseRedirect(reverse("title", args=(title_name,)))
        except:
            form = Createform(request.POST)
            if form.is_valid():
                title_name = form.cleaned_data["title"]
                content = form.cleaned_data["content"]
                file = open("entries/" + title_name + ".md", 'w')
                file.write('# ' + title_name + '\n')
                file.write(content)
                file.close()
                print(title_name)
                return HttpResponseRedirect(reverse("title", args=(title_name,)))
    print("inside edit")
    file = open("entries/" + title_name + ".md", 'r')
    title = file.readline()[2:]
    content = file.read()
    # content =
    file.close()

    return render(request, "encyclopedia/edit.html", {
        "form": Searchform(),
        "edit_form": Editform({'title': title, 'content': content}),
        "title": title,
    })

def create(request):

    if request.method == "POST":
        form = Createform(request.POST)
        if form.is_valid():
            title_name = form.cleaned_data["title"]
            content = form.cleaned_data["content"]
            if pathlib.Path("entries/" + title_name + ".md").is_file():
                return render(request, "encyclopedia/create.html", {
                    "create_form": Createform(),
                    "form": Searchform(),
                    "error": True
                })
            file = open("entries/" + title_name + ".md", 'w')
            file.write('# ' + title_name + '\n')
            file.write(content)
            file.close()
            print(title_name)
            return HttpResponseRedirect(reverse("title", args=(title_name,)))

    return render(request, "encyclopedia/create.html", {
        "create_form": Createform(),
        "form": Searchform(),
        "error": False
    })
def random_page(request):
    titles = util.list_entries()
    titles_len = len(titles)
    page = titles[random.randrange(0, titles_len)]
    return HttpResponseRedirect(reverse("title", args=(page, )))