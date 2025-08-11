import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

def new_searches_percent(self):
  last_date = anvil.server.call('last_import_date_percent')
  day_of_week =last_date.strftime("%A")
  self.label_2.text = 'Date of Last Import from the CRM = ' + str(last_date) + ' ' + str(day_of_week)
