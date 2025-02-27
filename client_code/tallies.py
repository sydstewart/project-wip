import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

def tallies(self, dicts):

    average_completion = sum([int(x['percent_complete']) / len(dicts)  for x in dicts])
    subtotal = sum([int(x['order_value'] ) for x in dicts])
    invoiced_total = sum([int(x['partially_invoiced_total'] ) for x in dicts])
    work_to_do = (subtotal * (100 - average_completion))/ 100
    self.total_value_label.text = f"TOTAL_VALUE_OF_ORDERS : £{subtotal:,}"
    self.average_completion_label.text = f"Average_COMPLETION : {average_completion:.1f}%"
    self.work_to_do_label.text = f"Value_of_Work_TO_DO : £{work_to_do:,}"
    self.invoiced_total.text =  f"TOTAL_INVOICED : £{invoiced_total:,}"