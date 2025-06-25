import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, time , date , timedelta

class Run_Chart(Run_ChartTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.start_date_picker.date = date(year= 2024, month = 7, day =17)
    fig = anvil.server.call('test_chart', self.start_date_picker.date)


    self.plot_1.figure = fig.
