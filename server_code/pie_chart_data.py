import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server
from datetime import datetime, time, date, timedelta

@anvil.server.callable
def piechart():

  last_row = app_tables.stage_summary.search(tables.order_by('Date_of_WIP', ascending=False))[0]
  dicts_pie = dict(last_row)

  #====================================Total Order value =======================
  import plotly.graph_objects as go
  colors = ['gold', 'mediumturquoise', 'lightgreen' ]
  labels = ['On Hold','In_Progress','Waiting_to_Start']
  values = [dicts_pie['Sum_on_hold'], dicts_pie['Sum_in_Progress'], dicts_pie['Sum_in_Waiting_to_Start']]
                                      
  fig = go.Figure(data=[go.Pie(labels=labels, values=values)])
  fig.update_layout(
    title=dict(
      text='Stage Groups Order Value' + '<br>' + 'GBP Excl VAT'  # + '<br>' + 'created at ' + datetime.now().strftime('%d %B %Y %H:%M')
    ))
  fig.update_traces(hoverinfo='label+percent', textinfo='value +percent', textfont_size=20,
                    marker=dict(colors=colors, line=dict(color='#000000', width=2)))

#===========================================Work to Do ==========================================================
  colors1 = ['gold', 'mediumturquoise', 'lightgreen' ]
  labels1 = ['On Hold','In_Progress','Waiting_to_Start']
  values1 = [ dicts_pie['Work_to_do_on_hold'], dicts_pie['Work_to_do_in_Progress'], dicts_pie['Work_to_do_to_Start']]
  
  fig1 = go.Figure(data=[go.Pie(labels=labels1, values=values1)])
  fig1.update_layout(
  title=dict(
    text='Stage Groups Work Yet To Do Value' + '<br>' + 'GBP Excl VAT')) # + '<br>' + 'created at ' + datetime.now().strftime('%d %B %Y %H:%M')
  
  fig1.update_traces(hoverinfo='label+percent', textinfo='value +percent', textfont_size=20,
                  marker=dict(colors=colors1, line=dict(color='#000000', width=2)))
#======================================Percentage Completion===================================================================
  colors2 = ['gold', 'mediumturquoise', 'lightgreen' ]
  labels2 = ['On Hold','In_Progress','Waiting_to_Start']
  values2 = [ dicts_pie['Percent_Completion_On_Hold'], dicts_pie['Percent_Completion_in_Progress'], dicts_pie['Percent_Completion_to_start']]
    
  fig2 = go.Figure(data=[go.Pie(labels=labels2, values=values2)])
  fig2.update_layout(
    title=dict(
      text='Stage Groups Percentage Completion')) # + '<br>' + 'created at ' + datetime.now().strftime('%d %B %Y %H:%M')) )
   
  fig2.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                     marker=dict(colors=colors2, line=dict(color='#000000', width=2)))

  #======================No of projects =======================================================
  colors3 = ['gold', 'mediumturquoise', 'lightgreen' ]
  labels3 = ['On Hold','In_Progress','Waiting_to_Start']
  values3 = [ dicts_pie['Count_on_hold'], dicts_pie['Count_in_Progress'], dicts_pie['Count_of_waiting_to_start']]
  
  fig3 = go.Figure(data=[go.Pie(labels=labels3, values=values3)])
  
  fig3.update_layout(
    title=dict(
      text='Stage Group No. of Projects' )) #+ '<br>' + 'created at ' + datetime.now().strftime('%d %B %Y %H:%M') )) # + '<br>'  + '<b> Total No. of projects =' 
    #  + str(total_no_projects) + '<b>'   ))
      
  fig3.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                     marker=dict(colors=colors3, line=dict(color='#000000', width=2)))

  #======================Partially Invoiced =======================================================
  colors4 = ['gold', 'mediumturquoise', 'lightgreen' ]
  labels4 = ['On Hold','In_Progress','Waiting_to_Start']
  values4 = [ dicts_pie['On_hold_Partially_Invoiced'], dicts_pie['In_Progress_Partially_Invoiced'], dicts_pie['To_Start_Partially_Invoiced']]

  fig4 = go.Figure(data=[go.Pie(labels=labels4, values=values4)])

  fig4.update_layout(
    title=dict(
      text='Stage Group Partially Invoiced' + '<br>' + 'GBP Excl VAT' )) #+ '<br>' + 'created at ' + datetime.now().strftime('%d %B %Y %H:%M') )) # + '<br>'  + '<b> Total No. of projects =' 
  #  + str(total_no_projects) + '<b>'   ))

  fig4.update_traces(hoverinfo='label+percent', textinfo='value', textfont_size=20,
                     marker=dict(colors=colors4, line=dict(color='#000000', width=2)))

  return dicts_pie, fig,fig1,fig2, fig3, fig4
 
  