from decimal import Decimal
from bokeh.embed import components
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource
from bokeh.palettes import Spectral11, Category20c
from bokeh.transform import cumsum
import pandas as pd
import numpy as np
from .queries import (repair_count_per_customer,
                      avg_repair_time_per_technician,
                      avg_repair_cost_per_customer,
                      total_cost_per_repair_status,
                      device_count_per_category,
                      total_cost_per_customer_with_filter)

def convert_decimal_to_float(data):
    if isinstance(data, dict):
        return {key: float(value) if isinstance(value, Decimal) else value for key, value in data.items()}
    elif isinstance(data, pd.DataFrame):
        for col in data.select_dtypes(include=[object]).columns:
            data[col] = data[col].apply(lambda x: float(x) if isinstance(x, Decimal) else x)
        return data
    return data

def print_data(data):
    print(data.head())

def bokeh_repair_count_per_customer():
    data = pd.DataFrame(list(repair_count_per_customer))
    data = convert_decimal_to_float(data)
    source = ColumnDataSource(data)

    p = figure(x_range=data['device__customer__name'], title="Кількість ремонтів по клієнтах",
               toolbar_location=None, tools="")
    p.vbar(x='device__customer__name', top='repair_count', width=0.9, source=source,
           legend_field="device__customer__name", line_color="white", fill_color=Spectral11[0])

    p.xaxis.axis_label = "Клієнт"
    p.yaxis.axis_label = "Кількість ремонтів"
    p.xaxis.major_label_orientation = 1.2
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"

    script, div = components(p)
    return script, div

def bokeh_avg_repair_time_per_technician():
    data = pd.DataFrame(list(avg_repair_time_per_technician))
    data = convert_decimal_to_float(data)
    source = ColumnDataSource(data)

    p = figure(title="Середній час ремонту по техніках", x_axis_label="Технік", y_axis_label="Середній час ремонту",
               x_range=data['technician__name'])
    p.line(x='technician__name', y='avg_repair_time', source=source, line_width=2, color=Spectral11[1])

    script, div = components(p)
    return script, div

def bokeh_total_cost_per_repair_status():
    data = pd.DataFrame(list(total_cost_per_repair_status))
    data = convert_decimal_to_float(data)
    source = ColumnDataSource(data)

    p = figure(x_range=data['status__status_name'], title="Загальна вартість ремонту по статусу",
               toolbar_location=None, tools="")
    p.vbar(x='status__status_name', top='total_cost', width=0.9, source=source,
           legend_field="status__status_name", line_color="white", fill_color=Spectral11[2])

    p.xaxis.axis_label = "Статус"
    p.yaxis.axis_label = "Загальна вартість"
    p.xaxis.major_label_orientation = 1.2
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"

    script, div = components(p)
    return script, div

def bokeh_device_count_per_category():
    data = pd.DataFrame(list(device_count_per_category))
    data = convert_decimal_to_float(data)
    data['angle'] = data['device_count'] / data['device_count'].sum() * 2 * np.pi
    data['color'] = Category20c[len(data)]

    p = figure(title="Кількість пристроїв по категоріях", toolbar_location=None,
               tools="hover", tooltips="@category: @device_count", x_range=(-1, 1))
    p.wedge(x=0, y=1, radius=0.4, start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend_field='category', source=ColumnDataSource(data))

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"

    script, div = components(p)
    return script, div

def bokeh_avg_repair_cost_per_customer():
    data = pd.DataFrame(list(avg_repair_cost_per_customer))
    data = convert_decimal_to_float(data)
    source = ColumnDataSource(data)

    p = figure(x_range=data['device__customer__name'], title="Середня вартість ремонту по клієнтах",
               toolbar_location=None, tools="")
    p.vbar(x='device__customer__name', top='avg_repair_cost', width=0.9, source=source,
           legend_field="device__customer__name", line_color="white", fill_color=Spectral11[3])

    p.xaxis.axis_label = "Клієнт"
    p.yaxis.axis_label = "Середня вартість ремонту"
    p.xaxis.major_label_orientation = 1.2
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"

    script, div = components(p)
    return script, div

def bokeh_total_cost_per_customer_with_filter():
    data = pd.DataFrame(list(total_cost_per_customer_with_filter))
    data = convert_decimal_to_float(data)
    source = ColumnDataSource(data)

    p = figure(x_range=data['device__customer__name'], title="Вартість ремонту для кожного клієнта",
               toolbar_location=None, tools="")
    p.vbar(x='device__customer__name', top='total_cost', width=0.9, source=source,
           legend_field="device__customer__name", line_color="white", fill_color=Spectral11[4])

    p.xaxis.axis_label = "Клієнт"
    p.yaxis.axis_label = "Загальна вартість ремонту"
    p.xaxis.major_label_orientation = 1.2
    p.legend.orientation = "horizontal"
    p.legend.location = "top_center"

    script, div = components(p)
    return script, div