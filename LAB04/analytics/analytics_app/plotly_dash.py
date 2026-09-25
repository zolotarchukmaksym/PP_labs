import plotly.express as px
from django.shortcuts import render
from django.db.models import Count, Avg, Sum
from .models import Repair

def plotly_repair_count_per_customer():
    repair_count_per_customer = Repair.objects.values('device__customer__name') \
        .annotate(repair_count=Count('id')) \
        .order_by('device__customer__name')

    data = [{'Customer': entry['device__customer__name'], 'Repair Count': entry['repair_count']} for entry in
            repair_count_per_customer]

    fig = px.bar(
        data,
        x='Customer',
        y='Repair Count',
        title="Кількість ремонтів для кожного клієнта",
        labels={'Customer': 'Клієнт', 'Repair Count': 'Кількість ремонтів'},
        color='Customer',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_xaxes(tickangle=45)
    return fig.to_html(full_html=False)

def plotly_total_cost_per_status():
    total_cost_per_repair_status = Repair.objects.values('status__status_name') \
        .annotate(total_cost=Sum('cost')) \
        .order_by('status__status_name')

    data = [{'Repair Status': entry['status__status_name'], 'Total Cost': entry['total_cost']} for entry in
            total_cost_per_repair_status]

    fig = px.pie(
        data,
        names='Repair Status',
        values='Total Cost',
        title="Загальна вартість ремонту по статусу ремонту",
        color='Repair Status',
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    return fig.to_html(full_html=False)

def plotly_avg_repair_time_per_technician():
    avg_repair_time_per_technician = Repair.objects.values('technician__name') \
        .annotate(avg_repair_time=Avg('repair_time')) \
        .order_by('technician__name')

    data = [{'Technician': entry['technician__name'], 'Avg Repair Time': entry['avg_repair_time']} for entry in
            avg_repair_time_per_technician]

    fig = px.line(
        data,
        x='Technician',
        y='Avg Repair Time',
        title="Середній час ремонту для кожного техніка",
        labels={'Technician': 'Технік', 'Avg Repair Time': 'Середній час ремонту'},
        line_shape='linear',
        markers=True,
        color='Technician',
        color_discrete_sequence=px.colors.qualitative.Plotly
    )
    fig.update_xaxes(tickangle=45)
    return fig.to_html(full_html=False)

def plotly_device_count_per_category():
    device_count_per_category = Repair.objects.values('device__category') \
        .annotate(device_count=Count('device__id')) \
        .order_by('device__category')

    data = [{'Category': entry['device__category'], 'Device Count': entry['device_count']} for entry in
            device_count_per_category]

    fig = px.histogram(
        data,
        x='Category',
        y='Device Count',
        title="Кількість пристроїв по категоріях",
        labels={'Category': 'Категорія', 'Device Count': 'Кількість пристроїв'},
        color='Category',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    return fig.to_html(full_html=False)

def plotly_avg_repair_cost_per_customer():
    avg_repair_cost_per_customer = Repair.objects.values('device__customer__name') \
        .annotate(avg_repair_cost=Avg('cost')) \
        .order_by('device__customer__name')

    data = [{'Customer': entry['device__customer__name'], 'Avg Repair Cost': entry['avg_repair_cost']} for entry in
            avg_repair_cost_per_customer]

    fig = px.box(
        data,
        x='Customer',
        y='Avg Repair Cost',
        title="Середня вартість ремонту для кожного клієнта",
        labels={'Customer': 'Клієнт', 'Avg Repair Cost': 'Середня вартість ремонту'},
        color='Customer',
        color_discrete_sequence=px.colors.qualitative.Set2
    )
    fig.update_xaxes(tickangle=45)
    return fig.to_html(full_html=False)

def plotly_total_cost_per_customer_with_filter():
    total_cost_per_customer_with_filter = Repair.objects.values('device__customer__name') \
        .annotate(total_cost=Sum('cost'), repair_count=Count('id')) \
        .filter(repair_count__gte=1) \
        .order_by('-total_cost')

    data = [{'Customer': entry['device__customer__name'], 'Total Cost': entry['total_cost']} for entry in
            total_cost_per_customer_with_filter]

    fig = px.pie(
        data,
        names='Customer',
        values='Total Cost',
        title="Вартість ремонту для кожного клієнта",
        color='Customer',
        color_discrete_sequence=px.colors.qualitative.Bold
    )
    return fig.to_html(full_html=False)