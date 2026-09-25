from django.db.models import Count, Avg, Sum, F, ExpressionWrapper, fields
from django.shortcuts import render
import plotly.express as px
import pandas as pd
from .models import Technician, Device, Repair, Customer

def plotly_dashboard(request):
    # Приклад 1: Кількість ремонтів для кожного техніка
    technician_data = Technician.objects.annotate(repair_count=Count('repair')).order_by('-repair_count')
    technician_df = pd.DataFrame(list(technician_data.values()))
    fig1 = px.bar(technician_df, x='name', y='repair_count', title='Кількість ремонтів для кожного техніка')

    # Приклад 2: Середня вартість ремонтів за типом пристроїв
    device_data = Device.objects.values('device_type').annotate(avg_price=Avg('repairs__parts__price')).order_by('-avg_price')
    device_df = pd.DataFrame(list(device_data))
    fig2 = px.pie(device_df, names='device_type', values='avg_price', title='Середня вартість ремонтів за типом пристроїв')

    # Приклад 3: Кількість ремонтів за статусом
    repair_status_data = Repair.objects.values('status').annotate(count=Count('id')).order_by('-count')
    repair_status_df = pd.DataFrame(list(repair_status_data))
    fig3 = px.pie(repair_status_df, names='status', values='count', title='Кількість ремонтів за статусом')

    # Приклад 4: Середній рейтинг зворотного зв'язку для кожного клієнта
    feedback_data = Customer.objects.annotate(avg_rating=Avg('feedback__rating')).order_by('-avg_rating')
    feedback_df = pd.DataFrame(list(feedback_data.values()))
    fig4 = px.bar(feedback_df, x='name', y='avg_rating', title='Середній рейтинг зворотного зв\'язку для кожного клієнта')

    # Приклад 5: Загальна вартість деталей для кожного ремонту
    parts_cost_data = Repair.objects.annotate(total_cost=Sum('parts__price')).order_by('-total_cost')
    parts_cost_df = pd.DataFrame(list(parts_cost_data.values()))
    fig5 = px.bar(parts_cost_df, x='device_id', y='total_cost', title='Загальна вартість деталей для кожного ремонту')

    # Приклад 6: Середня тривалість ремонту (у днях)
    repair_duration_data = Repair.objects.annotate(duration=ExpressionWrapper(F('completion_date') - F('repair_date'), output_field=fields.DurationField())).aggregate(average_duration=Avg('duration'))
    repair_duration_df = pd.DataFrame([repair_duration_data])
    fig6 = px.line(repair_duration_df, x='repair_date', y='duration', title='Середня тривалість ремонту (у днях)')

    charts = [fig1.to_html(full_html=False), fig2.to_html(full_html=False), fig3.to_html(full_html=False), fig4.to_html(full_html=False), fig5.to_html(full_html=False), fig6.to_html(full_html=False)]
    return render(request, 'dashboard_plotly.html', {'charts': charts})
