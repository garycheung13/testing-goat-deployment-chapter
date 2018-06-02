from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.core.exceptions import ValidationError

from lists.forms import ItemForm, ExistingListItemForm
from lists.models import Item, List


def home_page(request):
    return render(request, 'home.html', {'form': ItemForm()})

def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    form = ExistingListItemForm(for_list=list_)
    if request.method == 'POST':
        form = ExistingListItemForm(for_list=list_, data=request.POST)
        if form.is_valid():
            # Item.objects.create(text=request.POST['text'], list=list_)
            form.save()
            return redirect(list_) #implicit get_absolute_url
    return render(request, 'list.html', {'list': list_, 'form': form})

def new_list(request):
    form = ItemForm(data=request.POST)
    # print(request.POST)
    if form.is_valid():
        list_ = List.objects.create()
        # Item.objects.create(text=request.POST['text'], list=list_)
        form.save(for_list=list_)
        return redirect(list_) # get_absolute_url is implicitly called to resolve this function
    else:
        return render(request, 'home.html', {'form': form})