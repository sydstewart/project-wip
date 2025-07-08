from ._anvil_designer import Run_Chart_NewTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, time , date , timedelta
from anvil_extras import navigation
# SPDX-License-Identifier: MIT
#
# Copyright (c) 2021 The Anvil Extras project team members listed at
# https://github.com/anvilistas/anvil-extras/graphs/contributors
#
# Derived from the Anvil Extras Demo published at https://github.com/anvilistas/anvil-extras


@navigation.register(name="Run_Chart_New", title="Run Chart")
class Run_Chart_New(Run_Chart_NewTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.start_date_picker.date = date(year= 2024, month = 7, day =17)
    fig = anvil.server.call('work_to_do_chart', self.start_date_picker.date)

    layout_1 = {
      'title': 'Run_Chart of Work Still to be Done Value created at ' + datetime.now().strftime('%d %B %Y %H:%M'),
      'yaxis': {'title': '£ Value'},
      'yaxis_range':[0,600,000],
      'autosize' : False, 
      'width': 700, 
      'height': 2400,
      'showlegend': True
    }

    self.plot_1.figure = fig




  def Return_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Work_in_Progress')
    pass

  def start_date_picker_change(self, **event_args):
    """This method is called when the selected date changes"""
    line_plots_1 = anvil.server.call('work_to_do_chart', self.start_date_picker.date)

    # layout_1 = {
    #   'title': 'Run_Chart of Work Still to be Done Value created at ' + datetime.now().strftime('%d %B %Y %H:%M'),
    #   'yaxis': {'title': '£ Value'},
    #   'yaxis_range':[0,600,000],
    #    'autosize' : False, 
    #    'width': 700, 
    #    'height': 2400,
    #    'showlegend': True
    #  }
    # self.run_chart_plot.figure = line_plots_1
    # self.run_chart_plot.layout = layout_1
    self.plot_1.figure = line_plots_1
    pass


