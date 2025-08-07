import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from datetime import datetime, time , date , timedelta

def new_searches(self):
      # self.drop_down_1.selected_value = 'Work in Progress'
      partname = self.text_box_1.text
      stagegroup = self.drop_down_1.selected_value
      waitingon = self.drop_down_2.selected_value
      assignedto = self.drop_down_3.selected_value
      apparea = self.app_area_drop_down.selected_value
      category = self.category_drop_down.selected_value

      print('syd here')
      
      # Setup search dictionary
      kwargs ={}
      
      
      #Project Name
      if partname:
        kwargs['project_name'] =  q.ilike('%' + partname +'%')
      
      #stage
      if stagegroup:

        if stagegroup == 'Work in Progress':
              stages = ['Awaiting Sign-Off','Work In Progress - 4S', 'Pre-requisites in progress' ,'Ready for GoLive', 'Ready for UAT','Ready to Start','UAT WIP','Invoiced, still work to be completed']
        elif stagegroup == 'On Hold':
          stages = ['On Hold']
        elif stagegroup == 'Waiting to Start':
          stages = [ 'Order Approved', 'Order Submitted for Approval','Ordered']
        elif stagegroup == 'Closed':
          stages = ['Closed']
          
        kwargs['stage'] =  q.any_of(*stages) 
    
      if waitingon:
        kwargs['waiting_on'] =  waitingon 

      if assignedto:
        kwargs['assigned_to'] = assignedto

      if apparea:
        kwargs['app_area'] = apparea

      if category:
          kwargs['order_category'] = category
        
      print('kwargs=', kwargs)
     
      orders = anvil.server.call('orders',kwargs)
      if len(orders) >= 0:
          self.link_5.icon = ''
          self.link_6.icon = ''  
          self.link_7.icon = ''  
          self.link_10.icon = ''  
          self.link_11.icon = ''  
    
          self.repeating_panel_1.items = orders
      if len(self.repeating_panel_1.items) > 0:  
    
          def format_currency(amount):
            return '£{:,.2f}'.format(amount)
          self.label_1.foreground ='black'
          self.label_1.text ='No. of projects found = ' + str(len(self.repeating_panel_1.items ))
          order_total = (sum(item['order_value'] 
                        for item in self.repeating_panel_1.items))
          order_total = format_currency(order_total)
          self.label_8.foreground ='black'
          self.label_8.text = 'Order Total = ' + str(order_total) 
          
          days_elapsed_sum = (sum(item['days_elapsed'] 
                              for item in self.repeating_panel_1.items))
          days_elapsed_average= (round(days_elapsed_sum))/len(self.repeating_panel_1.items)
          days_elapsed_average= str(round(days_elapsed_average)) 
          self.label_9.foreground ='black'
          self.label_9.text = 'Average days Elapsed= ' + str(days_elapsed_average)
    
          work_to_do_sum = (sum(item['work_to_do'] 
                                for item in self.repeating_panel_1.items))
          work_to_do_sum= format_currency(work_to_do_sum)
          self.label_10.foreground ='black'
          self.label_10.text = 'Work To Do Value = ' + str(work_to_do_sum)
        
          percent_complete_sum = (sum(item['percent_complete'] 
                                    for item in self.repeating_panel_1.items))
          percent_complete_average= (round(percent_complete_sum ))/len(self.repeating_panel_1.items)
          percent_complete_average= str(round(percent_complete_average)) 
          self.label_11.foreground ='black'
          self.label_11.text = 'Average Percent Complete = ' + str(percent_complete_average)

          partially_invoiced_total_sum = (sum(item['partially_invoiced_total'] 
                                      for item in self.repeating_panel_1.items))
          partially_invoiced_total_sum= format_currency(partially_invoiced_total_sum)
          self.label_13.foreground ='black'
          self.label_13.text = 'Patially Invoiced Sum = ' + str(partially_invoiced_total_sum)
         
          last_date = anvil.server.call('last_import_date')
          day_of_week =last_date.strftime("%A")
          self.label_12.text = 'Date of Last Import from the CRM = ' + str(last_date) + ' ' + str(day_of_week)

      else:
         self.label_1.foreground ='red'
         self.label_1.text ='No. of projects found = ' + str(len(self.repeating_panel_1.items ))# alert("Combination of Search Criteria finds no Projects")
         
         self.label_8.foreground ='red'
         self.label_8.text = 'Order Total = ' + str(0) 
        
         self.label_9.foreground ='red'
         self.label_9.text = 'Average days Elapsed= ' + str(0)
         
         self.label_10.foreground ='red'
         self.label_10.text = 'Work To Do Value = ' + str(0)
        
         self.label_11.foreground ='red'
         self.label_11.text = 'Average Percent Complete = ' + str(0)
        