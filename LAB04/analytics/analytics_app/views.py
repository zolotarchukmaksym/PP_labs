from .plotly_dash import (plotly_repair_count_per_customer,
                          plotly_total_cost_per_status,
                          plotly_avg_repair_time_per_technician,
                          plotly_device_count_per_category,
                          plotly_avg_repair_cost_per_customer,
                          plotly_total_cost_per_customer_with_filter)

from .bokeh_dash import (bokeh_repair_count_per_customer,
    bokeh_avg_repair_time_per_technician,
    bokeh_total_cost_per_repair_status,
    bokeh_device_count_per_category,
    bokeh_avg_repair_cost_per_customer,
    bokeh_total_cost_per_customer_with_filter)


import pandas as pd
import numpy as np
from bokeh.embed import components
from django.db.models import Avg, Min, Max, Count,Sum
from django.http import JsonResponse
from rest_framework.views import APIView
from .models import Repair, Device, Feedback

from django.shortcuts import render
from .experiment import run_experiment
import plotly.graph_objects as go
from datetime import timedelta

class RepairCountPerCustomer(APIView):
    def get(self, request):
        repair_count_per_customer = Repair.objects.values('device__customer__name') \
            .annotate(repair_count=Count('id')) \
            .order_by('device__customer__name')

        df = pd.DataFrame(list(repair_count_per_customer))
        return JsonResponse(df.to_dict(orient='records'), safe=False)


class AvgRepairTimePerTechnician(APIView):
    def get(self, request):
        avg_repair_time_per_technician = Repair.objects.values('technician__name') \
            .annotate(avg_repair_time=Avg('repair_time')) \
            .order_by('technician__name')

        df = pd.DataFrame(list(avg_repair_time_per_technician))
        return JsonResponse(df.to_dict(orient='records'), safe=False)


class TotalCostPerRepairStatus(APIView):
    def get(self, request):
        total_cost_per_repair_status = Repair.objects.values('status__status_name') \
            .annotate(total_cost=Sum('cost')) \
            .order_by('status__status_name')

        df = pd.DataFrame(list(total_cost_per_repair_status))
        return JsonResponse(df.to_dict(orient='records'), safe=False)


class DeviceCountPerCategory(APIView):
    def get(self, request):
        device_count_per_category = Device.objects.values('category') \
            .annotate(device_count=Count('id')) \
            .order_by('category')

        df = pd.DataFrame(list(device_count_per_category))
        return JsonResponse(df.to_dict(orient='records'), safe=False)


class AvgRatingPerTechnician(APIView):
    def get(self, request):
        avg_rating_per_technician = Feedback.objects.values('technician__name') \
            .annotate(avg_rating=Avg('rating')) \
            .order_by('technician__name')

        df = pd.DataFrame(list(avg_rating_per_technician))
        return JsonResponse(df.to_dict(orient='records'), safe=False)


class TotalCostPerCustomerWithFilter(APIView):
    def get(self, request):
        total_cost_per_customer_with_filter = Repair.objects.values('device__customer__name') \
            .annotate(total_cost=Sum('cost'), repair_count=Count('id')) \
            .filter(repair_count__gte=1) \
            .order_by('-total_cost')

        df = pd.DataFrame(list(total_cost_per_customer_with_filter))
        return JsonResponse(df.to_dict(orient='records'), safe=False)


class BasicStatistics(APIView):
    def get(self, request):
        stats = Repair.objects.aggregate(
            avg_cost=Avg('cost'),
            min_cost=Min('cost'),
            max_cost=Max('cost')
        )

        costs = list(Repair.objects.values_list('cost', flat=True))

        if costs:
            costs.sort()
            median = np.median(costs)
        else:
            median = None

        stats['median_cost'] = median

        return JsonResponse(stats)

class MedianRepairTime(APIView):
    def get(self, request):
        repair_times = Repair.objects.values_list('repair_time', flat=True)

        repair_times_in_seconds = [
            rt.hour * 3600 + rt.minute * 60 + rt.second for rt in repair_times
        ]

        df = pd.DataFrame(repair_times_in_seconds, columns=['repair_time'])
        median_repair_time_seconds = df['repair_time'].median()

        median_repair_time = str(timedelta(seconds=int(median_repair_time_seconds)))

        return JsonResponse({'median_repair_time': median_repair_time})


class GroupedByCategory(APIView):
    def get(self, request):
        grouped_data = Device.objects.values('category') \
            .annotate(avg_revenue=Avg('repair__cost')) \
            .order_by('category')

        df = pd.DataFrame(list(grouped_data))
        return JsonResponse(df.to_dict(orient='records'), safe=False)


class GroupedByMonth(APIView):
    def get(self, request):
        grouped_data = Repair.objects.extra(
            select={'month': 'EXTRACT(MONTH FROM repair_date)'}
        ).values('month') \
            .annotate(avg_cost=Avg('cost'), total_repairs=Count('id')) \
            .order_by('month')

        df = pd.DataFrame(list(grouped_data))
        return JsonResponse(df.to_dict(orient='records'), safe=False)


def dashboard_v1(request):
    repair_count_plot = plotly_repair_count_per_customer()
    cost_status_plot = plotly_total_cost_per_status()
    avg_time_plot = plotly_avg_repair_time_per_technician()
    device_count_plot = plotly_device_count_per_category()
    avg_repair_cost_plot = plotly_avg_repair_cost_per_customer()
    total_cost_plot = plotly_total_cost_per_customer_with_filter()

    chart_type = request.GET.get('chart_type', 'all')

    plots = {
        'repair_count': {'plot': repair_count_plot, 'type': 'bar'},
        'cost_status': {'plot': cost_status_plot, 'type': 'pie'},
        'avg_time': {'plot': avg_time_plot, 'type': 'line'},
        'device_count': {'plot': device_count_plot, 'type': 'bar'},
        'avg_repair_cost': {'plot': avg_repair_cost_plot, 'type': 'line'},
        'total_cost': {'plot': total_cost_plot, 'type': 'pie'},
    }

    if chart_type != 'all':
        selected_plots = {key: value for key, value in plots.items() if value['type'] == chart_type}
    else:
        selected_plots = plots

    context = {
        'plots': selected_plots,
        'chart_type': chart_type,
    }

    return render(request, 'dashboard_v1.html', context)


def dashboard_v2(request):
    repair_count_script, repair_count_div = bokeh_repair_count_per_customer()
    cost_status_script, cost_status_div = bokeh_total_cost_per_repair_status()
    avg_time_script, avg_time_div = bokeh_avg_repair_time_per_technician()
    device_count_script, device_count_div = bokeh_device_count_per_category()
    avg_repair_cost_script, avg_repair_cost_div = bokeh_avg_repair_cost_per_customer()
    total_cost_script, total_cost_div = bokeh_total_cost_per_customer_with_filter()

    chart_type = request.GET.get('chart_type', 'all')

    plots = {
        'repair_count': {'script': repair_count_script, 'div': repair_count_div, 'type': 'bar'},
        'cost_status': {'script': cost_status_script, 'div': cost_status_div, 'type': 'bar'},
        'avg_time': {'script': avg_time_script, 'div': avg_time_div, 'type': 'line'},
        'device_count': {'script': device_count_script, 'div': device_count_div, 'type': 'pie'},
        'avg_repair_cost': {'script': avg_repair_cost_script, 'div': avg_repair_cost_div, 'type': 'bar'},
        'total_cost': {'script': total_cost_script, 'div': total_cost_div, 'type': 'bar'},
    }

    if chart_type != 'all':
        selected_plots = {key: value for key, value in plots.items() if value['type'] == chart_type}
    else:
        selected_plots = plots

    context = {
        'plots': selected_plots,
        'chart_type': chart_type,
    }

    return render(request, 'dashboard_v2.html', context)


def performance_graphic(results):
    num_threads = [result['num_threads'] for result in results]
    execution_time = [result['execution_time'] for result in results]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=num_threads, y=execution_time, mode='lines+markers'))

    fig.update_layout(
        title='Час виконання запитів залежно від кількості потоків',
        xaxis_title='Кількість потоків',
        yaxis_title='Час виконання (сек.)'
    )

    return fig.to_html(full_html=False)

def performance_dashboard(request):
    results = run_experiment()
    performance_graph = performance_graphic(results)

    return render(request, 'PerfomanceDashboard.html', {'performance_graphic': performance_graph})  # передаємо правильну змінну
