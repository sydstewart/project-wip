from ._anvil_designer import pie_chartTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class pie_chart(pie_chartTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    piedata, fig, fig1 = anvil.server.call('piechart')
    print('piedata', piedata)
    self.plot_1.figure =fig
        # Any code you write here will run before the form opens.
    
    self.text_box_1.text = piedata['Sum_on_hold'] + piedata['Sum_in_Progress']+ piedata['Sum_in_Waiting_to_Start']
    
    self.plot_2.figure =fig1
    # Any code you write here will run before the form opens.
    
    self.text_box_2.text = piedata['Work_to_do_on_hold'] + piedata['Work_to_do_in_Progress'] + piedata['Work_to_do_to_Start']
    percent_complete_overall= (piedata['Total_Value_of_Projects'] - piedata['Total_Work_To_Do'])*100 /piedata['Total_Value_of_Projects'] 
    
    self.text_box_3.text = round(float(percent_complete_overall),1)
    
    Percent_Completion_On_Hold = piedata['Percent_Completion_On_Hold'] 
    self.text_box_4.text = round(float(Percent_Completion_On_Hold),1)
    
    Percent_Completion_in_Progress = piedata['Percent_Completion_in_Progress'] 
    self.text_box_5.text = round(float(Percent_Completion_in_Progress),1)  
    
    Percent_Completion_to_start = piedata['Percent_Completion_to_start'] 
    self.text_box_6.text = round(float(Percent_Completion_to_start),1)  

    Count_on_hold = piedata['Count_on_hold'] 
    self.text_box_7.text = round(float(Count_on_hold),0)

    Count_in_Progress = piedata['Count_in_Progress'] 
    self.text_box_8.text = round(float(Count_in_Progress),0)  

    Count_of_waiting_to_start = piedata['Count_of_waiting_to_start'] 
    self.text_box_9.text = round(float(Count_of_waiting_to_start),0)  
    
  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Work_in_Progress')
    pass
 