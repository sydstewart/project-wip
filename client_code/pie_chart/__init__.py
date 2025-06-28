from ._anvil_designer import pie_chartTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, time , date , timedelta

class pie_chart(pie_chartTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #=============================================================
    piedata, fig, fig1, fig2, fig3 = anvil.server.call('piechart')
    print('piedata', piedata)
    self.label_1.text = 'Created at ' + datetime.now().strftime('%d %B %Y %H:%M')
    #====================Order Value Pie ============================== 
    self.plot_1.figure =fig
        # Any code you write here will run before the form opens. 
    total_value_of_projects  = piedata['Total_Value_of_Projects']
    self.label_9.text = 'Total Value of projects = ' + '£'+ str(total_value_of_projects )

    #====================Work to do Pie ============================== 
    self.plot_3.figure =fig2
    total_work_to_do = piedata['Work_to_do_on_hold'] + piedata['Work_to_do_in_Progress'] + piedata['Work_to_do_to_Start']
    self.label_10.text = 'Total Work Yet To Do = ' + '£'+ str(total_work_to_do  ) 
    
   #====================Percentage Pie ==============================  
    self.plot_2.figure =fig1
    # Any code you write here will run before the form opens.
    overall_percent_complete = piedata['Overall_Percent_Completion'] 
    self.label_11.text = 'Overall project Complation = ' + str(overall_percent_complete ) + '%'
   
    #====================No of projects ============================== 
    self.plot_4.figure =fig3
    total_no_projects = piedata['Count_on_hold'] +piedata['Count_in_Progress'] + piedata['Count_of_waiting_to_start']
    self.label_12.text = 'Total No. of projects = ' + str(total_no_projects)  

    #===================================================



 