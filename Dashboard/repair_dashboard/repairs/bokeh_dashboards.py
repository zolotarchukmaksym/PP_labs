from bokeh.plotting import figure, show
from bokeh.io import output_file
from bokeh.embed import components
from bokeh.resources import CDN
from django.shortcuts import render
import pandas as pd
from .models import Technician, Device, Repair, Customer
from django.db.models import Count, Avg, Sum, F, ExpressionWrapper, fields

def bokeh_dashboard(request):
    # Приклад 1: Кількість ремонтів для кожного техніка
    technician_data = Technician.objects.annotate(repair_count=Count('repair')).order_by('-repair_count')
    technician_df = pd.DataFrame(list(technician_data.values()))
    p1 = figure(x_range=technician_df['name'], title="Кількість ремонтів для кожного техніка")
    p1.vbar(x=technician_df['name'], top=technician_df['repair_count'], width=0.9)

    # Приклад 2: Середня вартість ремонтів за типом пристроїв
    device_data = Device.objects.values('device_type').annotate(avg_price=Avg('repairs__parts__price')).order_by('-avg_price')
    device_df = pd.DataFrame(list(device_data))
    p2 = figure(title="Середня вартість ремонтів за типом пристроїв", x_axis_label='Тип пристрою', y_axis_label='Середня ціна')
    p2.vbar(x=device_df['device_type'], top=device_df['avg_price'], width=0.9)

    # Приклад 3: Кількість ремонтів за статусом
    repair_status_data = Repair.objects.values('status').annotate(count=Count('id')).order_by('-count')
    repair_status_df = pd.DataFrame(list(repair_status_data))
    p3 = figure(title="Кількість ремонтів за статусом", x_axis_label='Статус', y_axis_label='Кількість')
    p3.vbar(x=repair_status_df['status'], top=repair_status_df['count'], width=0.9)

    # Приклад 4: Середній рейтинг зворотного зв'язку для кожного клієнта
    feedback_data = Customer.objects.annotate(avg_rating=Avg('feedback__rating')).order_by('-avg_rating')
    feedback_df = pd.DataFrame(list(feedback_data.values()))
    p4 = figure(x_range=feedback_df['name'], title="Середній рейтинг зворотного зв'язку для кожного клієнта")
    p4.vbar(x=feedback_df['name'], top=feedback_df['avg_rating'], width=0.9)

    # Приклад 5: Загальна вартість деталей для кожного ремонту
    parts_cost_data = Repair.objects.annotate(total_cost=Sum('parts__price')).order_by('-total_cost')
    parts_cost_df = pd.DataFrame(list(parts_cost_data.values()))
    p5 = figure(title="Загальна вартість деталей для кожного ремонту", x_axis_label='ID Пристрою', y_axis_label='Загальна вартість')
    p5.vbar(x=parts_cost_df['device_id'], top=parts_cost_df['total_cost'], width=0.9)

    # Приклад 6: Середня тривалість ремонту (у днях)
    repair_duration_data = Repair.objects.annotate(duration=ExpressionWrapper(F('completion_date') - F('repair_date'), output_field=fields.DurationField())).aggregate(average_duration=Avg('duration'))
    repair_duration_df = pd.DataFrame([repair_duration_data])
    p6 = figure(title="Середня тривалість ремонту (у днях)", x_axis_label='Дата ремонту', y_axis_label='Тривалість (дні)')
    p6.line(x=repair_duration_df['repair_date'], y=repair_duration_df['duration'])

    scripts, divs = [], []
    for p in [p1, p2, p3, p4, p5, p6]:
        script, div = components(p)
        scripts.append(script)
        divs.append(div)

    return render(request, 'dashboard_bokeh.html', {'scripts': scripts, 'divs': divs, 'cdn_js': CDN.js_files[0]})
