from django.shortcuts import render, redirect
from .form import CustomerForm
from .NetworkHelper import NetworkHelper


def customer_list(request):
    api = NetworkHelper(base_url="http://localhost:8000", username="max", password="maxzol321")
    customers = api.get_items()
    return render(request, 'customer_list.html', {'customers': customers})


def customer_detail(request, pk):
    api = NetworkHelper(base_url="http://localhost:8000", username="max", password="maxzol321")
    customer = api.get_item_by_id(pk)
    return render(request, 'customer_detail.html', {'customer': customer})


def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            api = NetworkHelper(base_url="http://localhost:8000", username="max", password="maxzol321")
            item_data = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'phone': form.cleaned_data['phone']
            }
            api.create_item(item_data)
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customer_form.html', {'form': form})


def customer_edit(request, pk):
    api = NetworkHelper(base_url="http://localhost:8000", username="max", password="maxzol321")
    customer = api.get_item_by_id(pk)

    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            item_data = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['email'],
                'phone': form.cleaned_data['phone']
            }
            api.update_item(pk, item_data)
            return redirect('customer_detail', pk=pk)
    else:
        form = CustomerForm(initial={
            'name': customer['name'],
            'email': customer['email'],
            'phone': customer['phone']
        })

    return render(request, 'customer_form.html', {'form': form})


def customer_delete(request, pk):
    api = NetworkHelper(base_url="http://localhost:8000", username="max", password="maxzol321")
    api.delete_item(pk)
    return redirect('customer_list')