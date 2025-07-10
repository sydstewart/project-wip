from ._anvil_designer import pie_charts_newTemplate
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


@navigation.register(name="pie_charts_new", title="Pie Charts")
class pie_charts_new(pie_charts_newTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #=============================================================
    piedata, fig, fig1, fig2, fig3, fig4, fig5, fig6, fig7, fig8, fig9= anvil.server.call('piechart')
    print('piedata', piedata)
    self.label_1.text = 'Ten Pie Charts indicating Implementation Project Status Created at ' + datetime.now().strftime('%d %B %Y %H:%M')
    #====================Order Value Pie ============================== 
    self.plot_1.figure =fig
    # Any code you write here will run before the form opens. 
    total_value_of_projects  = piedata['Total_Value_of_Projects']
    self.label_9.text = 'Total Value of projects = ' + '£'+ str('{:,.2f}'.format(total_value_of_projects ))

    #====================Work to do Pie ============================== 
    self.plot_4.figure =fig1
    total_work_to_do = piedata['Work_to_do_on_hold'] + piedata['Work_to_do_in_Progress'] + piedata['Work_to_do_to_Start']
    self.label_10.text = 'Total Work Yet To Do = ' + '£'+ str('{:,.2f}'.format(total_work_to_do  ) )

    #====================Percentage Pie ==============================  
    self.plot_3.figure =fig2
    # Any code you write here will run before the form opens.
    overall_percent_complete = piedata['Overall_Percent_Completion'] 
    self.label_11.text = 'Overall Project Stage Group Completion = ' + str(overall_percent_complete ) + '%'

    #====================No of projects ============================== 
    self.plot_2.figure =fig3
    total_no_projects = piedata['Count_on_hold'] +piedata['Count_in_Progress'] + piedata['Count_of_waiting_to_start']
    self.label_12.text = 'Total No. of projects = ' + str(total_no_projects)  


    #====================Partially Invoiced ============================== 
    self.plot_10.figure =fig4
    total_partially_invoiced = piedata['Total_Partially_Invoiced']  
    self.label_7.text = 'Total Partially Invoiced = ' + '£' + str('{:,.2f}'.format(total_partially_invoiced ) ) 

    #====================Waiting In Progress Status by Count============================== 
    self.plot_5.figure =fig5
    total_projects_In_Progress = piedata['In_Progress_Waiting_on_Customer_count'] + piedata['In_Progress_Waiting_on_4S_count'] + piedata['In_Progress_Waiting_no_state_count']
    self.label_5.text = 'Project Count In Progress= ' + str('{:,.0f}'.format(total_projects_In_Progress ) ) 

    #====================Waiting In Progress Status by Order Value============================== 
    self.plot_6.figure =fig6
    total_value_projects_In_Progress = piedata['In_Progress_Waiting_on_Customer_sum'] + piedata['In_Progress_Waiting_on_4S_sum'] + piedata['In_Progress_Waiting_no_state_sum']
    self.label_4.text = 'Project Order Value In Progress= ' + '£' + str('{:,.2f}'.format(total_value_projects_In_Progress))

    #====================Waiting In Progress Status by To Do Value============================== 
    self.plot_7.figure =fig7
    total_to_do_In_Progress =  piedata['In_Progress_Waiting_on_Customer_sum_work_to_do'] + piedata['In_Progress_Waiting_on_4S_sum_work_to_do'] + piedata['In_Progress_Waiting_no_state_sum_work_to_do']
    self.label_2.text = 'Total To do In Progress= ' + '£' + str('{:,.0f}'.format(total_to_do_In_Progress ))

    #====================Waiting In Progress Percent Complete============================= 
    self.plot_9.figure =fig8
    total_waiting_percent_complete =  piedata['Percent_Completion_in_Progress']  
    self.label_6.text = 'Overall Waiting Percent Completion= ' + str('{:,.01f}'.format(total_waiting_percent_complete ) +'%')

    #====================Waiting In Progress Work Complete============================= 
    self.plot_8.figure =fig9
    total_waiting_complete = piedata['In_Progress_Waiting_on_Customer_work_complete'] + piedata['In_Progress_Waiting_on_4S_work_complete'] + piedata['In_Progress_Waiting_no_state_work_complete']  
    self.label_3.text = 'Overall Waiting Work Complete= ' + '£' + str('{:,.01f}'.format(total_waiting_complete))

  # def button_1_click(self, **event_args):
  #   """This method is called when the button is clicked"""
  #   open_form('Work_in_Progress')
  #   pass

  # def plot_3_click(self, points, **event_args):
  #   """This method is called when a data point is clicked."""
  #   pass


