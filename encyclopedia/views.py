import markdown2
import random
from django.shortcuts import render, redirect
from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def topic(request, title): 
    mkdownString = util.get_entry(title) 

    if mkdownString == None: 
        mkdownString = " ** Page was not found"

    html = markdown2.markdown(mkdownString)
    
    return render(request, "encyclopedia/entry.html", { 
            "title": title, 
            "content": html
        })

def search(request): 
    if request.method == "POST": 
        query = request.POST['q']

        html_content = markdown2.markdown(query)
        similar_results = []
        allEntries = util.list_entries()

        if query in allEntries: 
            return redirect("topic", query)
    
        else: 
            for entry in allEntries: 
                if query.lower() in entry.lower(): 
                    similar_results.append(entry)

            return render(request, "encyclopedia/result.html", { 
                "results" : similar_results
            })

def new_page(request): 
    if request.method == "GET": 
        return render(request, "encyclopedia/new.html")
    else: 
        title = request.POST['title']
        content = request.POST['content']
        alreadyExists = util.get_entry(title)
        if alreadyExists is not None: 
            mkString = "ERROR: Entry already exists!"
            return render(request, "encyclopedia/entry.html",  { 
                "title": title,
                "content": mkString
            })
        else: 
            util.save_entry(title, content)
            html_content = markdown2.markdown(title)
            return render(request, "encyclopedia/entry.html", { 
                "title": title,
                "content": html_content
            })


def edit_page(request): 
    if request.method == 'POST': 
        title = request.POST['entry_title']
        content = util.get_entry(title)
        return render(request, "encyclopedia/edit.html", { 
            "title": title,
            "content": content 
        })


def save_edit(request): 
    if request.method == 'POST': 
        title = request.POST['title']
        content = request.POST['content']
        util.save_entry(title, content)
        html_content = markdown2.markdown(title)
        return render(request, "encyclopedia/entry.html", { 
            "title": title,
            "content": html_content
        })


def random_page(request): 
    allEntries = util.list_entries()
    random_entry = random.choice(allEntries)
    return redirect("topic", random_entry)



    
    
    
    




