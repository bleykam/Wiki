import random
from django import forms
from encyclopedia import util
from django.shortcuts import render, redirect, reverse
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
import markdown2
from markdown2 import Markdown
import re
from django.contrib import messages
from django.http import Http404

markdowner = Markdown()


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    page = util.get_entry(title)
    if page is None:
        return HttpResponseNotFound('<h1> 404 Page Not Found </h1>')

    else:    # get md file of requested entry
    # convert md to html
        html = markdown2.markdown(page)
        return render(request, "encyclopedia/entry.html", {'title': title, 'content': html})

class EditForm(forms.Form):
    title = forms.CharField(label='New Entry Title')
    body = forms.CharField(label="Input entry in markdown format: ", widget=forms.Textarea())

def edit(request, title):
    if request.method == "POST":
        form = EditForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            body = form.cleaned_data.get('body')
            util.save_entry(title, body)
            page = util.get_entry(title)
            html = markdowner.convert(page)
            return HttpResponseRedirect(reverse('entry', args=(title,), current_app='encyclopedia'))
        else:
            return render(request, 'encyclopedia/edit.html', {
                "form": form,
                "title": title})

    form = EditForm(initial={"title":title, "body":util.get_entry(title)})
    return render(request, 'encyclopedia/edit.html', {
            "form": form,
            "title": title})




class SearchForm(forms.Form):
    title = forms.CharField(label='', widget=forms.TextInput())


def search(request):
    if request.method == "POST":
        title = ""
        search_results =[]
        entries = util.list_entries()
        query = request.POST['q']
        for entry in entries:
            if query.upper() == entry.upper():
                title = entry
                search_results.append(entry)
                return redirect('entry', title=title)
            if query.upper() in entry.upper():
                search_results.append(entry)
            if search_results == []:
                return HttpResponseNotFound("404 Page Not Found")
        return render (request, 'encyclopedia/search.html',{"content":search_results, "title":query})



class CreateForm(forms.Form):
    title = forms.CharField(label='New Entry Title:')
    body = forms.CharField(label="Input entry in markdown format: ", widget=forms.Textarea())


def create(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        title = request.POST.get("title")
        if util.get_entry(title) != None:
            return HttpResponse("entry already exists")
        if form.is_valid():
            title = form.cleaned_data.get('title')
            body = form.cleaned_data.get('body')
            util.save_entry(title,body)
            page = util.get_entry(title)
            html = markdowner.convert(page)

        return HttpResponseRedirect(reverse('entry', args=(title,), current_app = 'encyclopedia'))
    else:
        form = CreateForm()
        return render(request, 'encyclopedia/create.html', {'form': form})


def randoms(request):
    title = random.choice(util.list_entries())
    mdcontent = util.get_entry(title)
    htmlcontent = markdowner.convert(mdcontent)
    return render(request, "encyclopedia/randoms.html", {"title": title, "content": htmlcontent})
