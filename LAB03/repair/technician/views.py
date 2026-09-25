from django.shortcuts import render, get_object_or_404, redirect
from .models import Technician
from .form import TechnicianForm

def technician_list(request):
    technicians = Technician.objects.all()
    return render(request, 'technician_list.html', {'technicians': technicians})

def technician_detail(request, id):
    technician = get_object_or_404(Technician, id=id)
    return render(request, 'technician_detail.html', {'technician': technician})

def technician_add(request):
    if request.method == 'POST':
        form = TechnicianForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('technician_list')
    else:
        form = TechnicianForm()
    return render(request, 'technician_form.html', {'form': form})

def technician_edit(request, id):
    technician = get_object_or_404(Technician, id=id)
    if request.method == 'POST':
        form = TechnicianForm(request.POST, instance=technician)
        if form.is_valid():
            form.save()
            return redirect('technician_list')
    else:
        form = TechnicianForm(instance=technician)
    return render(request, 'technician_form.html', {'form': form})

def technician_delete(request, id):
    technician = get_object_or_404(Technician, id=id)
    if request.method == 'POST':
        technician.delete()
        return redirect('technician_list')
    return render(request, 'technician_delete_confirmation.html', {'technician': technician})