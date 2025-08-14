import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from datetime import datetime, time , date , timedelta

def new_searches_stages(self):
  last_date = anvil.server.call('last_import_date_stages')
  day_of_week =last_date.strftime("%A")
  self.label_2.text = 'Date of Last Import from the CRM = ' + str(last_date) + ' ' + str(day_of_week)
  
  project= self.drop_down_1.selected_value
  kwargs ={}
  if project:
 
      kwargs['project_name'] = project  #q.like('%' + project['project_name'] + '%') 

    
  stages =  anvil.server.call('stages', kwargs)
  self.label_4.text = 'Number of Records = ' + str(len(stages)) 
  self.repeating_panel_1.items  = stages
  self.repeating_panel_1.items = sorted(
    self.repeating_panel_1.items,
    key=lambda row: row["Update_Date"],
    reverse=True,
      )
   