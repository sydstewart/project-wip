import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, time , date , timedelta

def repeating_panel_calcs(self):
      dicts, dictspip, dictswts, dictsoh, Xmedia,pivotsyd_to_markdown  = anvil.server.call('get_orders_for_pivots', 0, 100, None, None, None)
      def format_currency(amount):
         return '£{:,.2f}'.format(amount)
      a1 = str(len(dictspip))
      a = "Projects in Progress at" 
      b = (datetime.now().strftime("%Y-%m-%d"))
      self.label_1.text = a1 + " " + a + " " + b
      
      self.repeating_panel_1.items = dictspip
      if self.waiting_on_dropdown.selected_value: 
          self.repeating_panel_1.items = [item for item in self.repeating_panel_1.items if item['waiting_on'] == self.waiting_on_dropdown.selected_value]
      order_total = (sum(item['order_value'] 
                        for item in self.repeating_panel_1.items))
      # order_total= str(order_total)
      order_total = format_currency(order_total)
      self.label_5.text = order_total
      
      days_elapsed_sum = (sum(item['days_elapsed'] 
                              for item in self.repeating_panel_1.items))
      days_elapsed_average= (round(days_elapsed_sum))/len(self.repeating_panel_1.items)
      days_elapsed_average= str(round(days_elapsed_average)) 
      self.label_4.text = days_elapsed_average
      
      work_to_do_sum = (sum(item['Work To Do'] 
                            for item in self.repeating_panel_1.items))
      work_to_do_sum= format_currency(work_to_do_sum)
      self.label_8.text = work_to_do_sum
      
      percent_complete_sum = (sum(item['percent_complete'] 
                                  for item in self.repeating_panel_1.items))
      percent_complete_average= (round(percent_complete_sum ))/len(self.repeating_panel_1.items)
      percent_complete_average= str(round(percent_complete_average)) 
      self.label_10.text = percent_complete_average
      
