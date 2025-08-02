import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q

def new_searches(self):

      partname = self.text_box_1.text
      stagegroup = self.drop_down_1.selected_value
      waitingon = self.drop_down_2.selected_value
      assignedto = self.drop_down_3.selected_value

      print('syd here')
      
      # Setup search dictionary
      kwargs ={}
      
      
      #Project Name
      if partname:
        kwargs['project_name'] =  q.ilike('%' + partname +'%')
      
      #stage
      if stagegroup:

        if stagegroup == 'Work in Progress':
              stages = ['Awaiting Sign-Off','Work In Progress - 4S', 'Pre-requisites in progress' ,'Ready for GoLive', 'Ready for UAT','Ready to Start','UAT WIP']
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
        
      print('kwargs=', kwargs)
     
      orders = anvil.server.call('orders',kwargs)
       
      self.repeating_panel_1.items = orders
      self.label_1.text ='No. of projects found = ' + str(len(self.repeating_panel_1.items ))