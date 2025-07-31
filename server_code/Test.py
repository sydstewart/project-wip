import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server
import pymysql
import anvil.tables.query as q
import anvil.media
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import statistics

from anvil.tables import app_tables

from datetime import datetime, time , date , timedelta



def connect():
  connection = pymysql.connect(host='51.141.236.29',
                               port=3306,
                               user='CRMReadOnly',
                               password=anvil.secrets.get_secret('Teamwork Pass'),
                               database = 'infoathand',
                               cursorclass=pymysql.cursors.DictCursor)
  if not connection:
     alert(' Connection down')
  return connection
  
@anvil.server.background_task
def testprojects():
  # ++++++++++++++++++++++++++++++++++++++
  dayofweek = datetime.today().weekday()
  print('Day of Week', datetime.today().weekday())
  # dayofweek = 5
  if dayofweek < 5:
    
          conn = connect()
        #=============================================================================  
          # Load Orders 
          with conn.cursor() as cur:
                cur.execute(
                      "Select sales_orders.name As name, sales_orders.date_entered As date_entered, \
                        CONCAT(sales_orders.prefix,sales_orders.so_number) As so_number, sales_orders.so_stage As so_stage, \
                        sales_orders.subtotal_usd AS Order_Value, \
                      sales_orders_cstm.workinprogresspercentcomplete_c AS workinprogresspercentcomplete_c,\
                      sales_orders_cstm.OrderCategory AS OrderCategory,\
                      sales_orders.so_number AS so_number,\
                      users.user_name AS user_name\
                      From sales_orders\
                      INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
                      LEFT JOIN `users` ON (`sales_orders`.`assigned_user_id` = `users`.`id`) \
                      Where sales_orders.date_entered > '2020-01-01' AND \
                          sales_orders_cstm.OrderCategory NOT IN ('Maintenance') AND \
                          sales_orders.so_stage  NOT IN ('Closed', 'Cancelled','Complete')"
                            )  
          records = cur.fetchall()
          number_of_records =len(records)
          print('No of projects',number_of_records)
        
        # calculate WIP
          with conn.cursor() as cur1:
                cur1.execute(
                   "Select Sum(sales_orders.subtotal_usd) As Total_Order_Value,\
                   Avg(sales_orders_cstm.workinprogresspercentcomplete_c) As Average_Percent_Work_Complete,\
                   Sum((sales_orders.subtotal_usd *  (sales_orders_cstm.workinprogresspercentcomplete_c) / 100)) As Total_Completed_VaLUE \
                   From sales_orders \
                      INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
                      Where sales_orders.date_entered > '2020-01-01' AND \
                          sales_orders_cstm.OrderCategory NOT IN ('Maintenance') AND \
                          sales_orders.so_stage NOT IN ('Closed', 'Cancelled','Complete')"
                )
        
          for r in cur1.fetchall():
        
                Total_Order_Value =r['Total_Order_Value']
                Total_Order_Value = float(Total_Order_Value)
                # Total_Order_Value = f"{Total_Order_Value  :.2f}"
                print('Total_Order_Value=',Total_Order_Value)
            
                Average_Percent_Work_Complete = (r['Average_Percent_Work_Complete'])
                # Average_Percent_Work_Complete  = f"{Average_Percent_Work_Complete :.2f}"
                print('Average_Percent_Work_Complete=',Average_Percent_Work_Complete )
            
                Total_Work_Completed_VaLUE = r['Total_Completed_VaLUE']
                Total_Work_Completed_VaLUE = float(Total_Work_Completed_VaLUE)
                # Total_Work_Completed_VaLUE = f"{Total_Work_Completed_VaLUE :.2f}"
                print('Total_Work_Completed_VaLUE',Total_Work_Completed_VaLUE)
        
                Total_Work_Left = float(Total_Order_Value) - float(Total_Work_Completed_VaLUE)
                print('Total_Work_Left_VaLUE',Total_Work_Left)

        # # calculate WIP by order category
        #   with conn.cursor() as cur2:
        #         cur2.execute(
        #   "Select Sum(sales_orders.subtotal_usd) As Total_Order_Value,\
        #     Avg(sales_orders_cstm.workinprogresspercentcomplete_c) As Average_Percent_Work_Complete,\
        #     Sum((sales_orders.subtotal_usd *  (sales_orders_cstm.workinprogresspercentcomplete_c) / 100)) As Total_Completed_VaLUE \
        #     From sales_orders \
        #       INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
        #       Where sales_orders.date_entered > '2020-01-01' AND \
        #           sales_orders_cstm.OrderCategory NOT IN ('Maintenance') AND \
        #           sales_orders.so_stage NOT IN ('Closed', 'On Hold', 'Cancelled','Complete')"
        # )
                # "Select Sum(sales_orders.subtotal_usd) As Total_Order_Value,\
#                Avg(sales_orders_cstm.workinprogresspercentcomplete_c) As Average_WIP,\
#               Sum((sales_orders.subtotal_usd *  Avg(sales_orders_cstm.workinprogresspercentcomplete_c) / 100) As Total_WIP_VaLUE \
#               From sales_orders \
#               INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
#               Where sales_orders.date_entered > '2015-09-30' AND \
#                   sales_orders_cstm.OrderCategory NOT IN ('Maintenance') AND \
#                   sales_orders.so_stage NOT IN ('Closed', 'On Hold', 'Cancelled','Work In Progress - 4S')" )
                   # "Select Sum(sales_orders.subtotal_usd) As Total_Order_Value,\
                   # Avg(sales_orders_cstm.workinprogresspercentcomplete_c) As Average_Percent_Work_Complete,\
                   # Sum((sales_orders.subtotal_usd *  (sales_orders_cstm.workinprogresspercentcomplete_c) / 100)) As Total_Completed_VaLUE \
                   # count(sales_orders.id) as No_of_projects \
                   # From sales_orders \
                   #    INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
                   #    Where sales_orders.date_entered > '2020-01-01' AND \
                   #        sales_orders_cstm.OrderCategory NOT IN ('Maintenance') AND \
                   #        sales_orders.so_stage NOT IN ('Closed', 'On Hold', 'Cancelled','Complete'), \
                   #    Group By sales_orders_cstm.OrderCategory, \
                   #    Having sales_orders_cstm.OrderCategory Not In ('Maintenance')"
                
          print('Syd SQL')
          for r in cur1.fetchall():
        
                Total_Order_Value =r['Total_Order_Value']
                Total_Order_Value = float(Total_Order_Value)
                # Total_Order_Value = f"{Total_Order_Value  :.2f}"
                print('Total_Order_Value=',Total_Order_Value)
            
                Average_Percent_Work_Complete = (r['Average_Percent_Work_Complete'])
                # Average_Percent_Work_Complete  = f"{Average_Percent_Work_Complete :.2f}"
                print('Average_Percent_Work_Complete=',Average_Percent_Work_Complete )
            
                Total_Work_Completed_VaLUE = r['Total_Completed_VaLUE']
                Total_Work_Completed_VaLUE = float(Total_Work_Completed_VaLUE)
                # Total_Work_Completed_VaLUE = f"{Total_Work_Completed_VaLUE :.2f}"
                print('Total_Work_Completed_VaLUE',Total_Work_Completed_VaLUE)
        
                Total_Work_Left = float(Total_Order_Value) - float(Total_Work_Completed_VaLUE)
                print('Total_Work_Left_VaLUE',Total_Work_Left)                
        
        
          # totals = cur1.fetchall()
          today = datetime.today()
          # last_row = app_tables.completed_work.search(tables.order_by('Date_entered', ascending=False))[0]
          # last_reading = last_row['Order_Value_Completed']
          # print('last_reading=', last_reading)
          # delta = Total_WIP_VaLUE - float(last_reading)
          app_tables.daily_wip.add_row(Date_of_WIP = (today),  Total_Order_Value = round(float(Total_Order_Value),0) , Average_Percent_Work_Complete = int(Average_Percent_Work_Complete), Total_Work_Completed = int(Total_Work_Completed_VaLUE), Total_Work_To_Do_Value = int(Total_Work_Left), No_of_projects = number_of_records)
          print('Produced from background and Daily WIP updated at ', today)
  else:
          print('Not a week day - no update of Daily WIP table', datetime.today().weekday())
    
#   conn = connect()
# #=============================================================================  
#   # Load Orders 
#   with conn.cursor() as cur:
#         cur.execute(
#               "Select sales_orders.name As name, sales_orders.date_entered As date_entered, \
#                 CONCAT(sales_orders.prefix,sales_orders.so_number) As so_number, sales_orders.so_stage As so_stage, \
#                 sales_orders.subtotal_usd AS Order_Value, \
#                sales_orders_cstm.workinprogresspercentcomplete_c AS workinprogresspercentcomplete_c,\
#                sales_orders_cstm.OrderCategory AS OrderCategory,\
#                sales_orders.so_number AS so_number,\
#                users.user_name AS user_name\
#               From sales_orders\
#                INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
#                LEFT JOIN `users` ON (`sales_orders`.`assigned_user_id` = `users`.`id`) \
#               Where sales_orders.date_entered > '2020-01-01' AND \
#                   sales_orders_cstm.OrderCategory NOT IN ('Maintenance') AND \
#                   sales_orders.so_stage  NOT IN ('Closed', 'On Hold','Cancelled','Complete')"
#                     )  
#   records = cur.fetchall()
#   number_of_records =len(records)
#   print('No of projects',number_of_records)

# # calculate WIP
#   with conn.cursor() as cur1:
#         cur1.execute(
#           "Select Sum(sales_orders.subtotal_usd) As Total_Order_Value,\
#             Avg(sales_orders_cstm.workinprogresspercentcomplete_c) As Average_Percent_Work_Complete,\
#             Sum((sales_orders.subtotal_usd *  (sales_orders_cstm.workinprogresspercentcomplete_c) / 100)) As Total_Completed_VaLUE \
#           From sales_orders \
#               INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
#               Where sales_orders.date_entered > '2020-01-01' AND \
#                   sales_orders_cstm.OrderCategory NOT IN ('Maintenance') AND \
#                   sales_orders.so_stage NOT IN ('Closed', 'On Hold', 'Cancelled','Complete')"
#         )

#   for r in cur1.fetchall():

#         Total_Order_Value =r['Total_Order_Value']
#         Total_Order_Value = float(Total_Order_Value)
#         # Total_Order_Value = f"{Total_Order_Value  :.2f}"
#         print('Total_Order_Value=',Total_Order_Value)
    
#         Average_Percent_Work_Complete = (r['Average_Percent_Work_Complete'])
#         # Average_Percent_Work_Complete  = f"{Average_Percent_Work_Complete :.2f}"
#         print('Average_Percent_Work_Complete=',Average_Percent_Work_Complete )
    
#         Total_Work_Completed_VaLUE = r['Total_Completed_VaLUE']
#         Total_Work_Completed_VaLUE = float(Total_Work_Completed_VaLUE)
#         # Total_Work_Completed_VaLUE = f"{Total_Work_Completed_VaLUE :.2f}"
#         print('Total_Work_Completed_VaLUE',Total_Work_Completed_VaLUE)

#         Total_Work_Left = float(Total_Order_Value) - float(Total_Work_Completed_VaLUE)
#         print('Total_Work_Left_VaLUE',Total_Work_Left)


#   # totals = cur1.fetchall()
#   today = datetime.today()
#   # last_row = app_tables.completed_work.search(tables.order_by('Date_entered', ascending=False))[0]
#   # last_reading = last_row['Order_Value_Completed']
#   # print('last_reading=', last_reading)
#   # delta = Total_WIP_VaLUE - float(last_reading)
#   app_tables.daily_wip.add_row(Date_of_WIP = (today),  Total_Order_Value = round(float(Total_Order_Value),2) , Average_Percent_Work_Complete = int(Average_Percent_Work_Complete), Total_Work_Completed = int(Total_Work_Completed_VaLUE), Total_Work_To_Do_Value = int(Total_Work_Left))
#   # totals = cur.fetchall()
#   # return records,Total_Order_Value , Total_WIP_VaLUE , Average_WIP, number_of_records


  # totals = cur.fetchall()
  # return records,Total_Order_Value , Total_WIP_VaLUE , Average_WIP, number_of_records



#++++++++++++++++++++++++++++++++++++++++++
#   conn = connect()
# #=============================================================================  
#   # Load Orders 
#   with conn.cursor() as cur:
#         cur.execute(
#               "Select sales_orders.name As name, sales_orders.date_entered As date_entered, \
#                 CONCAT(sales_orders.prefix,sales_orders.so_number) As so_number, sales_orders.so_stage As so_stage, \
#                 sales_orders.subtotal_usd AS Order_Value, \
#                sales_orders_cstm.workinprogresspercentcomplete_c AS workinprogresspercentcomplete_c,\
#                sales_orders_cstm.OrderCategory AS OrderCategory,\
#                sales_orders.so_number AS so_number\
#               From sales_orders\
#                INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
#               Where sales_orders.date_entered > '2015-09-30' AND \
#                   sales_orders_cstm.OrderCategory NOT IN ('Maintenance') AND \
#                   sales_orders.so_stage  NOT IN ('Closed', 'On Hold','Cancelled','Work In Progress - 4S')"
#                     )  
#   records = cur.fetchall()
#   number_of_records =len(records)

# # calculate WIP
#   with conn.cursor() as cur1:
#         cur1.execute(
#           "Select Sum(sales_orders.subtotal_usd) As Total_Order_Value,\
#             Avg(sales_orders_cstm.workinprogresspercentcomplete_c) As Average_WIP,\
#             Sum((sales_orders.subtotal_usd *  Avg(sales_orders_cstm.workinprogresspercentcomplete_c) / 100) As Total_WIP_VaLUE \
#           From sales_orders \
#               INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
#               Where sales_orders.date_entered > '2015-09-30' AND \
#                   sales_orders_cstm.OrderCategory NOT IN ('Maintenance') AND \
#                   sales_orders.so_stage NOT IN ('Closed', 'On Hold', 'Cancelled','Work In Progress - 4S')"
#         )
#   for r in cur1.fetchall():
#         Total_Order_Value =r['Total_Order_Value']
#         Total_Order_Value = f"{Total_Order_Value  :.2f}"
#         print('Total_Order_Value=',r['Total_Order_Value'])
#         Average_WIP = (r['Average_WIP'])
#         Average_WIP  = f"{Average_WIP :.2f}"
#         print('Average_WIP=',Average_WIP )
#         print('Total_WIP_VaLUE',r['Total_WIP_VaLUE'])
#         Total_WIP_VaLUE = r['Total_WIP_VaLUE']
#         Total_WIP_VaLUE = f"{Total_WIP_VaLUE :.2f}"
#         Total_WIP_VaLUE = float(Total_WIP_VaLUE)
#   totals = cur1.fetchall()
#   today = datetime.today()
#   last_row = app_tables.completed_work.search(tables.order_by('Date_entered', ascending=False))[0]
#   last_reading = last_row['Order_Value_Completed']
#   print('last_reading=', last_reading)
#   delta = Total_WIP_VaLUE - float(last_reading)
#   app_tables.completed_work.add_row(Order_Value_Completed=Total_WIP_VaLUE,Date_entered = today,delta_work= delta)
#   totals = cur.fetchall()
#   return records,Total_Order_Value , Total_WIP_VaLUE , Average_WIP, number_of_records
# Syd

@anvil.server.callable
def get_run_chart():
   import plotly.graph_objects as go
   chart_data = app_tables.completed_work.search(Date_entered = q.greater_than(date(year=2024, month=3, day=9)))
   dicts = [{'Date_entered': r['Date_entered'], 'delta_work': r['delta_work']}
         for r in chart_data]
   df = pd.DataFrame.from_dict(dicts)
   print('df',df)
   line_plots = go.Scatter(x=df['Date_entered'], y=df['delta_work'], name='Delta Work Completed', marker=dict(color='#e50000'))
   
   return line_plots

@anvil.server.callable
def wip_run_chart():
   import plotly.graph_objects as go
   import plotly.express as px 
   chart_data = app_tables.daily_wip.search(tables.order_by("Date_of_WIP", ascending=False) ,Date_of_WIP= q.greater_than(date(year=2024, month=7, day=17)))
   dicts = [{'Date_entered': r['Date_of_WIP'], 'Total Order Value': r['Total_Order_Value'], 'Total Work To Do Value': r['Total_Work_To_Do_Value']} for r in chart_data]
   df = pd.DataFrame.from_dict(dicts)
   print('df',df)
 
 
   fig = go.Figure([
    go.Scatter(
        name='Total Order Value',
        x=df['Date_entered'],
        y=df['Total Order Value'],
        mode='lines+markers',
        marker=dict(color='red', size=4),
        line=dict(width=1),
        showlegend=True)
    ,
    go.Scatter(
        name='Total Work To Do Value',
        x=df['Date_entered'],
        y=df['Total Work To Do Value'],
        mode='lines+markers',
        marker=dict(color='blue', size=4),
        line=dict(width=1),
        showlegend=True)
   ])
   fig.update_layout(
    title=dict(
      text='Total Order Value and Value of Total Work to be Done' + '<br>' + 'created at ' + datetime.now().strftime('%d %B %Y %H:%M')
    ),
    yaxis=dict(
      title=dict(
        text="Value"
      )
    ),
    xaxis=dict(
      title=dict(
        text="Date Entered"
      )  
    ))
   fig.update_layout(legend=dict(
      yanchor="top",
      y=0.99,
      xanchor="left",
      x=0.10
    ))
   return fig

@anvil.server.callable
def work_to_do_chart(start_date):
   import plotly.graph_objects as go
   import plotly.express as px 
   print('start_date=', start_date)
   start_date= str(start_date)
   start_year = int(start_date[0:4])
   print('start_year', start_year)
   start_month = int(start_date[5:7])
   print('start_month', start_month)
   start_day = int(start_date[8:10])
   print('start_day', start_day)
 

   chart_data = app_tables.daily_wip.search(tables.order_by("Date_of_WIP", ascending=False) , Date_of_WIP= q.greater_than(date(year=start_year, month=start_month, day=10) ))
   dicts = [{'Date_entered': r['Date_of_WIP'], 'Total Order Value': r['Total_Order_Value'], 'Total Work To Do Value': r['Total_Work_To_Do_Value']} for r in chart_data]
   df = pd.DataFrame.from_dict(dicts)
   df['Median'] = df['Total Work To Do Value'].median()
   print('df for daily WIP',df)
   
   
   fig = go.Figure([

    go.Scatter(
        name='Total Work To Do Value',
        x=df['Date_entered'],
        y=df['Total Work To Do Value'],
        mode='lines+markers',
        marker=dict(color='blue', size=4),
        line=dict(width=1),
        showlegend=True)
   ])
   fig.add_scatter(x=df['Date_entered'], y=df['Median'], mode='lines', name= 'Median Total Work To Do Value')
   fig.update_layout(
    title=dict(
      text='Run Chart of Value of Total Work to be Done' + '<br>' + 'created at ' + datetime.now().strftime('%d %B %Y %H:%M')
    ),
    yaxis=dict(
      title=dict(
        text="Value"
      )
    ),
    xaxis=dict(
      title=dict(
        text="Date Entered"
      )  
    ))
   # fig = px.line(df, x= 'Date_entered', y='Total Order Value', markers=True)
   # fig['data'][0]['name']='Total Order Value'
   # # line_plots = go.Scatter(x=df['Date_entered'], y=df['Total Order Value'], name='Total Order Value', marker=dict(color='#e50000'))
   # fig.add_scatter(x=df['Date_entered'], y=df['Total Work To Do Value'], mode='markers+lines', name= 'Total Work To Do Value'), fig
   print('fig',fig)
   return fig

@anvil.server.callable
def orders_chart():
   import plotly.graph_objects as go
   import plotly.express as px 
   chart_data = app_tables.daily_wip.search(tables.order_by("Date_of_WIP", ascending=False) ,Date_of_WIP= q.greater_than(date(year=2024, month=7, day=17)))
   dicts = [{'Date_entered': r['Date_of_WIP'], 'Total Order Value': r['Total_Order_Value'], 'Total Work To Do Value': r['Total_Work_To_Do_Value']} for r in chart_data]
   df = pd.DataFrame.from_dict(dicts)
   print('df',df)
   df['Median'] = df['Total Order Value'].median()
 
   fig = go.Figure([

    go.Scatter(
        name='Total Order Value',
        x=df['Date_entered'],
        y=df['Total Order Value'],
        mode='lines+markers',
        marker=dict(color='red', size=4),
        line=dict(width=1),
        showlegend=True)
     ])
   return fig
  
@anvil.server.callable
def testprojects():
  
  conn = connect()
#=============================================================================  
  # Load Orders 
  with conn.cursor() as cur:
        cur.execute(
              "Select sales_orders.name As name, sales_orders.date_entered As date_entered, \
                CONCAT(sales_orders.prefix,sales_orders.so_number) As so_number, sales_orders.so_stage As so_stage, \
                sales_orders.subtotal_usd AS Order_Value, \
               sales_orders_cstm.workinprogresspercentcomplete_c AS workinprogresspercentcomplete_c,\
               sales_orders_cstm.OrderCategory AS OrderCategory,\
               sales_orders.so_number AS so_number,\
               users.user_name AS user_name\
              From sales_orders\
               INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
               LEFT JOIN `users` ON (`sales_orders`.`assigned_user_id` = `users`.`id`) \
              Where sales_orders.date_entered > '2020-01-01' AND \
                  sales_orders_cstm.OrderCategory NOT IN ('Maintenance') AND \
                  sales_orders.so_stage  NOT IN ('Closed', 'On Hold','Cancelled','Complete')"
                    )  
  records = cur.fetchall()
  number_of_records =len(records)
  print('No of projects',number_of_records)

# calculate WIP
  with conn.cursor() as cur1:
        cur1.execute(
          "Select Sum(sales_orders.subtotal_usd) As Total_Order_Value,\
            Avg(sales_orders_cstm.workinprogresspercentcomplete_c) As Average_Percent_Work_Complete,\
            Sum((sales_orders.subtotal_usd *  (sales_orders_cstm.workinprogresspercentcomplete_c) / 100)) As Total_Completed_VaLUE \
          From sales_orders \
              INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
              Where sales_orders.date_entered > '2020-01-01' AND \
                  sales_orders_cstm.OrderCategory NOT IN ('Maintenance') AND \
                  sales_orders.so_stage NOT IN ('Closed', 'On Hold', 'Cancelled','Complete')"
        )

  for r in cur1.fetchall():

        Total_Order_Value =r['Total_Order_Value']
        Total_Order_Value = float(Total_Order_Value)
        # Total_Order_Value = f"{Total_Order_Value  :.2f}"
        print('Total_Order_Value=',Total_Order_Value)
    
        Average_Percent_Work_Complete = (r['Average_Percent_Work_Complete'])
        # Average_Percent_Work_Complete  = f"{Average_Percent_Work_Complete :.2f}"
        print('Average_Percent_Work_Complete=',Average_Percent_Work_Complete )
    
        Total_Work_Completed_VaLUE = r['Total_Completed_VaLUE']
        Total_Work_Completed_VaLUE = float(Total_Work_Completed_VaLUE)
        # Total_Work_Completed_VaLUE = f"{Total_Work_Completed_VaLUE :.2f}"
        print('Total_Work_Completed_VaLUE',Total_Work_Completed_VaLUE)

        Total_Work_Left = float(Total_Order_Value) - float(Total_Work_Completed_VaLUE)
        print('Total_Work_Left_VaLUE',Total_Work_Left)


  # totals = cur1.fetchall()
  today = datetime.today()
  # last_row = app_tables.completed_work.search(tables.order_by('Date_entered', ascending=False))[0]
  # last_reading = last_row['Order_Value_Completed']
  # print('last_reading=', last_reading)
  # delta = Total_WIP_VaLUE - float(last_reading)
  app_tables.daily_wip.add_row(Date_of_WIP = (today),  Total_Order_Value = round(float(Total_Order_Value),0) , Average_Percent_Work_Complete = int(Average_Percent_Work_Complete), Total_Work_Completed = int(Total_Work_Completed_VaLUE), Total_Work_To_Do_Value = int(Total_Work_Left), No_of_projects = number_of_records)
  # totals = cur.fetchall()
  # return records,Total_Order_Value , Total_WIP_VaLUE , Average_WIP, number_of_records
  print('Produced from Stand alone version')



@anvil.server.callable
def create_zaphod_pdf(formname):
  import anvil.pdf
  media_object = anvil.pdf.render_form(formname, 42, name=formname)
  return media_object

@anvil.server.callable
def send_pdf_email():
  anvil.email.send(
    from_name="Test Project Work Flow Run Chart", 
    to="sydney.w.stewart@gmail.com,alistair@4s-dawn.com",
    subject="An auto-generated Project Flow Run Chart",
    text="Your auto-generated Project Flow Run Chart is attached to this email as a PDF.",
    attachments=anvil.pdf.render_form('run_chart')
  )


# syd@4s-dawn.com, 4salistair@gmail.com,
# @anvil.server.background_task
@anvil.server.callable
@anvil.tables.in_transaction
def burndown():
  
  conn = connect()
#=============================================================================  
  # Load Orders 
  with conn.cursor() as cur2:
        cur2.execute(
              "Select sales_orders.name As name, sales_orders.date_entered As date_entered,\
                CONCAT(sales_orders.prefix,sales_orders.so_number) As so_number, sales_orders.so_stage As so_stage, \
                sales_orders.subtotal_usd AS Order_Value, \
               sales_orders_cstm.workinprogresspercentcomplete_c AS workinprogresspercentcomplete_c,\
               sales_orders_cstm.OrderCategory AS OrderCategory,\
               sales_orders.so_number AS so_number,\
               users.first_name AS first_name,\
               users.`email1` AS users_email1, \
               sales_orders.date_modified AS date_modified \
               From sales_orders\
               INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
               LEFT JOIN `users` ON (`sales_orders`.`assigned_user_id` = `users`.`id`) \
              Where sales_orders.date_entered > '2015-09-30' AND \
                  sales_orders_cstm.OrderCategory NOT IN ('Maintenance') AND \
                  sales_orders.so_stage  NOT IN ('Closed', 'On Hold','Cancelled')"
                    )  
  records = cur2.fetchall()
  number_of_records =len(records)
  print('Number of timeline records loaded = ',number_of_records)
  max_date = app_tables.projects_master.search(tables.order_by("order_date", ascending=False))[0]['order_date']
  print('Max_Date', max_date)
  for r in records:
        projrec = app_tables.projects_master.get(order_no = r['so_number'])
        if projrec:
              print('Order No', r['so_number'] ) 
              print('Name', r['name'])
              
              projectname = r['name']
              # if projrec['latest_percent_complete'] >=0:
              percent_completed = projrec['latest_percent_complete']
              # print('Project Name',projrec['project_name'])
              today = date.today()
              date_entered = (r['date_entered']).date()
              date_modified = (r['date_modified']).date()
              days_elapsed = abs(today - date_entered).days
              days_since_updated =  abs(today - date_modified).days
              
              # print('Last percent change= ',last_percent_complete) 
              email = (r['users_email1'].lower())  # emails in CRM different with some capitalised first letter
          
              print('days elapsed=', days_elapsed)
              print('days since updated=', days_since_updated )
              order_link =  app_tables.projects_master.get(order_no=r['so_number'])
              # projectname = order_link['project_name']
              percent_completed = 0
        
             
              # app_tables.burndown.add_row(order_no = r['so_number'],timeline_date = datetime.today(), percent_complete =r['workinprogresspercentcomplete_c'], projectname = projectname, elapsed_days= days_elapsed)
              # projreclast = app_tables.projects_master.get(order_no = r['so_number'])  
              # order_value = projreclast['order_value']
              update_row = app_tables.projects_master.get(order_no =  r['so_number'])
              
              print(r['so_number'], 'has', r['workinprogresspercentcomplete_c'], ' percent complete')
            
              update_row['latest_percent_complete'] = percent_completed
              update_row['percent_change']= r['workinprogresspercentcomplete_c'] - percent_completed
              update_row['elapsed_time'] = days_elapsed
              update_row['days_since_updated'] = days_since_updated
              
              if update_row['order_value'] and update_row['percent_change']:
                  update_row['value_change'] = update_row['order_value'] * update_row['percent_change']/100
              else:
                  update_row['value_change']= 0
        else:
            # add new project master then burndown
            percent_change = 0
            if r['Order_Value']:
              order_value = r['Order_Value']
            else:
              order_value = 0
              
            app_tables.projects_master.add_row(order_no = r['so_number'],project_name =r['name'], order_value = order_value,order_date = r['date_entered'],
                                                order_category = r['OrderCategory'], user = r['first_name'], latest_percent_complete =r['workinprogresspercentcomplete_c'],                            
                                                elapsed_time  = days_elapsed, user_email = email, days_since_updated= days_since_updated, percent_change=  r['workinprogresspercentcomplete_c'] , value_change= order_value*percent_change/100 )
              # order_link =  app_tables.projects_master.get(order_no=r['so_number'])
              # app_tables.burndown.add_row(order_no = r['so_number'],timeline_date = datetime.today(), percent_complete =r['workinprogresspercentcomplete_c'], projectname=projectname,elapsed_days= days_elapsed)
    
@anvil.server.callable
def show_progress(project):
      order_no = app_tables.projects_master.get(project_name=project)
      project_burndown = app_tables.burndown.search(order_no_link  = order_no)
      dicts = [{'order_no': r['order_no'], 'order_date':r['order_no_link']['order_date'],'user':r['order_no_link']['user'],'percent_complete': r['percent_complete'], 'project_name':r['order_no_link']['project_name'], 'order_value':r['order_no_link']['order_value'], 'timeline_date':r['timeline_date'],'elapsed_time':r['elapsed_days', 'percent_change':r['percent_change']]} for r in project_burndown ]
      print(dicts)
      return dicts 

@anvil.server.callable
def show_new_orders():
      # Get today's date
      today = date.today()
      print("Today is: ", today)
     
      # Yesterday date
      # yesterday = today - timedelta(days = 1)
      # day= day(yesterday)
      # month = month(yesterday)
      # year= year(yesterday)
      
      # print("Yesterday was: ", yesterday)
      order_no = app_tables.projects_master.search(order_date = datetime(day= 20, month=8, year=2024))
      count_found = len(order_no)
      print('Count Found',count_found)
      # if not num_displayed:
      #       num_displayed= 10
      if count_found != 0:
            dicts = [{'order_no': r['order_no'], 'order_date':r['order_date'],'user':r['user'],'latest_percent_complete': r['latest_percent_complete'], 'project_name':r['project_name'], 'order_value':r['order_value'],'elapsed_time':r['elapsed_time'],'days_since_updated': r['days_since_updated'], 'order_category': r['order_category']} for r in order_no]
            print(dicts)
            df = pd.DataFrame.from_dict(dicts)
            dicts = df.to_dict(orient='records')  
            return dictsd
      else:
          dicts =[]
          fig = []
          return dicts


@anvil.server.callable
def show_progress_managers(user):
      print(user)
      order_no = app_tables.projects_master.search(tables.order_by('latest_percent_complete', ascending=False), user_email= user)
      count_found = len(order_no)
      print('Count Found',count_found)
      print('user', user)

      if count_found != 0:
            dicts = [{'order_no': r['order_no'], 'order_date':r['order_date'],'user':r['user'],'latest_percent_complete': r['latest_percent_complete'], 'project_name':r['project_name'], 'order_value':r['order_value'],'elapsed_time':r['elapsed_time'],'days_since_updated': r['days_since_updated'], 'order_category': r['order_category']} for r in order_no]
            print(dicts)
            df = pd.DataFrame.from_dict(dicts)
            print('df',df)
            color_map = {'Implementation':'yellow', 'Interface(s)':'blue', 'Questionnaire(s)':'orange','Configuration/Dev':'pink','Server Mover with Interfaces': 'brown','Server Mover with NO Interfaces':'green','Re-installation':'purple' }
            cat_color = df['order_category'].map(color_map)
            fig = px.scatter(df, x= 'elapsed_time',
                             y='latest_percent_complete', 
                             color = 'order_category',  
                             size ='order_value', 
                             hover_name  = 'project_name', 
                             title = 'Heat Map of Projects created at ' + datetime.now().strftime('%d %B %Y %H:%M') + ' for ' + user,
                            )
            fig.update_layout(showlegend=True)
            fig.update_layout(hoverlabel=dict(bgcolor="white", ))
            return dicts, fig, count_found
      else:
          dicts =[]
          fig = []
          return dicts, fig, count_found
@anvil.server.callable
def show_changes():

     # burndown =  app_tables.burndown.search(tables.order_by('latest_percent_complete', ascending=False), days_since_updated =q.less_than_or_equal_to(7))
      order_no = app_tables.projects_master.search(tables.order_by('latest_percent_complete', ascending=False), days_since_updated =q.less_than_or_equal_to(7))
      count_found = len(order_no)
      print('Count Found',count_found)
    
      if count_found != 0:
            dicts = [{'order_no': r['order_no'], 'order_date':r['order_date'],'user':r['user'],'latest_percent_complete': r['latest_percent_complete'], 'project_name':r['project_name'], 'order_value':r['order_value'],'elapsed_time':r['elapsed_time'],'days_since_updated': r['days_since_updated'], 'order_category': r['order_category'],'percent_change': r['percent_change']} for r in order_no]
            print(dicts)
            # df = pd.DataFrame.from_dict(dicts)
            return dicts, count_found
      else:
          dicts =[]
          return dicts, count_found

@anvil.server.callable
def project_list():
   projects =list({(r['project_name']) for r in app_tables.projects_master.search(tables.order_by('project_name'))})
   return projects

@anvil.server.callable
def managers_list():
   # managers =list({(r['firstname'], r) for r in app_tables.users.search(tables.order_by('firstname',ascending=True ))})
   # managers.sort()
   managers = [(cat['email'], cat) for cat in app_tables.users.search(tables.order_by('email',ascending=True ))]
   return managers
   # [(row['Year'], row) for row in app_tables.testcars.search()]

@anvil.server.callable
def individual_chart(project):
      order_no = app_tables.projects_master.get(project_name=project)
      project_burndown = app_tables.burndown.search(order_no_link  = order_no)
      dicts = [{'order_no': r['order_no'], 'order_date':r['order_no_link']['order_date'],'percent_complete': r['percent_complete'], 'project_name':r['order_no_link']['project_name'], 'order_value':r['order_no_link']['order_value'], 'timeline_date':r['timeline_date'],'elapsed_days':r['elapsed_days']} for r in project_burndown ]
      df = pd.DataFrame.from_dict(dicts)
      print('df',df)
      line_plots = go.Scatter(x=df['elapsed_days'], y=df['percent_complete'], name='Project Progress', marker=dict(color='#e50000'))
   
      return line_plots



@anvil.server.callable
def show_histograms():
  # get data for chart into a dataframe
      order_no = app_tables.projects_master.search(latest_percent_complete=q.less_than(100))
      dicts = [{'order_no': r['order_no'], 'order_date':r['order_date'],'percent_complete': r['latest_percent_complete'], 'project_name':r['project_name'], 'order_value':r['order_value'], 'elapsed_days':r['elapsed_time']} for r in order_no]
      df = pd.DataFrame.from_dict(dicts)
  # calculate number of projects and average running time
      dfelapsed = df['elapsed_days']
      project_count = len(df)
      average_elapsed = df['elapsed_days'].mean()
      print('dfelapsed',dfelapsed)
   # prepare histogram using plotly go  
      line_plots = go.Histogram(x= dfelapsed, xbins =dict(start=0, end=3500, size=365), histnorm = 'percent', cumulative_enabled=True)
  
      # return project_count, fig, average_elapsed
      return project_count, line_plots, average_elapsed

@anvil.server.callable
def show_histograms_px():  #using plotly express
  # get data into a dataframe
      order_no = app_tables.projects_master.search()
      dicts = [{'order_no': r['order_no'], 'order_date':r['order_date'],'percent_complete': r['latest_percent_complete'], 'project_name':r['project_name'], 'order_value':r['order_value'], 'elapsed_days':r['elapsed_time']} for r in order_no]
      df = pd.DataFrame.from_dict(dicts)
  # prepare histogram  in plotly using express (px)
      fig = px.histogram(df, x="elapsed_days",cumulative=True,histnorm = 'percent', nbins =35 )
      # dfelapsed = df['elapsed_days']
      project_count = len(df)
      average_elapsed = df['elapsed_days'].mean()
  # add an average line        
      fig.add_vline(x=average_elapsed, line_width=2, line_dash='dash', line_color='red', col=1,  annotation_text="Average Days in Progress= " + str(int(average_elapsed)), annotation_position="top right" )
      return project_count, fig, average_elapsed

@anvil.server.background_task
def burndownprojects():
  
  conn = connect()
#=============================================================================  
  # Load Orders 
  with conn.cursor() as cur:
        cur.execute(
              "Select sales_orders.name As name, sales_orders.date_entered As date_entered, \
                CONCAT(sales_orders.prefix,sales_orders.so_number) As so_number, sales_orders.so_stage As so_stage, \
                sales_orders.subtotal_usd AS Order_Value, \
               sales_orders_cstm.workinprogresspercentcomplete_c AS workinprogresspercentcomplete_c,\
               sales_orders_cstm.OrderCategory AS OrderCategory,\
               sales_orders.so_number AS so_number\
              From sales_orders\
               INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
              Where sales_orders.date_entered > '2015-09-30' AND \
                  sales_orders_cstm.OrderCategory NOT IN ('Maintenance') AND \
                  sales_orders.so_stage  NOT IN ('Closed', 'On Hold','Cancelled','Work In Progress - 4S')"
                    )  
  # records = cur.fetchall()
  today = datetime.today()
  for r in cur.fetchall():
     year= r['date_entered'].year
     month = r['date_entered'].month
     day = r['date_entered'].day
     f_date = date(year, month, day)
     today_d = date(today.year, today.month, today.day)
     datediff = (today_d - f_date)
     app_tables.burndown.add_row(order_no = r['so_number'],  timeline_date = today, percent_complete = r['workinprogresspercentcomplete_c'], elapsed_days=datediff )
     print(r['so_number'],r['workinprogresspercentcomplete_c'], datediff)


@anvil.server.callable
def burndownproj():
 
  conn = connect()
#=============================================================================  
  # Load Orders 
  with conn.cursor() as cur:
        cur.execute(
              "Select sales_orders.name As name, sales_orders.date_entered As date_entered, \
                CONCAT(sales_orders.prefix,sales_orders.so_number) As so_number, sales_orders.so_stage As so_stage, \
                sales_orders.subtotal_usd AS Order_Value, \
               sales_orders_cstm.workinprogresspercentcomplete_c AS workinprogresspercentcomplete_c,\
               sales_orders_cstm.OrderCategory AS OrderCategory,\
               sales_orders.so_number AS so_number\
              From sales_orders\
               INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
              Where sales_orders.date_entered > '2015-09-30' AND \
                  sales_orders_cstm.OrderCategory NOT IN ('Maintenance') AND \
                  sales_orders.so_stage  NOT IN ('Closed', 'On Hold','Cancelled','Work In Progress - 4S')"
                    )  
  # records = cur.fetchall()
  today = datetime.today()
  for r in cur.fetchall():
     year= r['date_entered'].year
     month = r['date_entered'].month
     day = r['date_entered'].day
     f_date = date(year, month, day)
     today_d = date(today.year, today.month, today.day)
     datediff = (today_d - f_date).days
     print('datedif',datediff)
     app_tables.burndown.add_row(order_no = r['so_number'],  timeline_date = today, percent_complete = r['workinprogresspercentcomplete_c'], elapsed_days=datediff )
     print(r['so_number'],r['workinprogresspercentcomplete_c'])


@anvil.server.callable
def show_all_projects(num_displayed, user):
      order_no = app_tables.projects_master.search(tables.order_by('latest_percent_complete', ascending=False))
      print('num_displayed', num_displayed)
      count_found = len(order_no)
      print('Count Found',count_found)
      # if not num_displayed:
      #       num_displayed= 10
      if count_found != 0:
            dicts = [{'order_no': r['order_no'], 'order_date':r['order_date'],'user':r['user'],'latest_percent_complete': r['latest_percent_complete'], 'project_name':r['project_name'], 'order_value':r['order_value'],'elapsed_time':r['elapsed_time'],'days_since_updated': r['days_since_updated'], 'order_category': r['order_category']} for r in order_no]
            print(dicts)
            df = pd.DataFrame.from_dict(dicts)
            if user:
                df =  df[df['user'] == user] 
            df= df.nlargest(num_displayed, 'order_value')
            print('df',df)
            color_map = {'Implementation':'yellow', 'Interface(s)':'blue', 'Questionnaire(s)':'orange','Configuration/Dev':'pink','Server Mover with Interfaces': 'brown','Server Mover with NO Interfaces':'green','Re-installation':'purple' }
            cat_color = df['order_category'].map(color_map)
            fig = px.scatter(df, x= 'elapsed_time',
                             y='latest_percent_complete', 
                             color = 'order_category',  
                             size ='order_value', 
                             hover_name  = 'project_name', 
                             title = 'Heat Map of Projects created at ' + datetime.now().strftime('%d %B %Y %H:%M') 
                            )
            fig.update_layout(showlegend=True)
            fig.update_layout(hoverlabel=dict(bgcolor="white", ))
            dicts = df.to_dict(orient='records')  
            return dicts, fig, count_found
      else:
          dicts =[]
          fig = []
          return dicts, fig, count_found

@anvil.server.callable  
def get_changes():

  conn = connect()
#=============================================================================  
  # Load order changes 
  with conn.cursor() as curaudit:
        curaudit.execute(
            "Select Concat(sales_orders.prefix, sales_orders.so_number) As Order_No, \
              sales_orders.name, sales_orders_cstm.neworexistingsystem_c, users1.first_name  \
              As Assigned_to, sales_orders.date_entered as date_entered, sales_orders_audit.date_created As Update_date, users.first_name \
              As Updated_by, \
              sales_orders_cstm.OrderCategory as order_category, \
              sales_orders_audit.field_name, \
              sales_orders_audit.before_value_string as BeforePercent, sales_orders_audit.after_value_string as AfterPercent, \
              sales_orders.subtotal_usd As GBP_Excl_Vat, sales_orders.amount_usdollar As \
              GBP_Incl_VAT \
            From sales_orders Inner Join \
              sales_orders_audit On sales_orders.id = sales_orders_audit.parent_id \
              Inner Join \
              sales_orders_cstm On sales_orders_cstm.id_c = sales_orders.id Inner Join \
              users On sales_orders_audit.created_by = users.id Inner Join \
              users users1 On sales_orders.created_by = users1.id \
            Where sales_orders_cstm.neworexistingsystem_c In ('New', 'Existing') And \
              sales_orders_audit.field_name = 'workinprogresspercentcomplete_c' And \
              sales_orders.date_entered  > '2020-01-01' \
            Order By  Concat(sales_orders.prefix, sales_orders.so_number) Desc   , sales_orders_audit.date_created Desc "  
            )
  records = curaudit.fetchall()
  number_of_records =len(records)
  print('No of changes',number_of_records)
  if number_of_records:
            dicts = [{'order_no': r['Order_No'], 'project_name':r['name'] ,'order_date':r['date_entered'], 'order_category':r['order_category'],'Assigned_to':r['Assigned_to'] , 'order_value':r['GBP_Excl_Vat'] , 'Update_Date':r['Update_date'], \
                     'Updated_by':r['Updated_by'],'Percent_Completion_Before':r['BeforePercent'],'Percent_Completion_After':r['AfterPercent']} for r in records]
            # print(dicts)
  X = pd.DataFrame.from_dict(dicts)
  X['order_value_formated'] = X['order_value'].map("£{:,.0f}".format) 
  # X['Percent_Completion_Before'] = X['Percent_Completion_Before'].fillna(0)
  # print('before',X['Percent_Completion_Before'])
  
  # X['Percent_Completion_Before']= X['Percent_Completion_Before'].astype(int)
  # X =  X[X['Percent_Completion_Before'] > limit]
  # print('after filter',X['Percent_Completion_Before'])
  # X['Percent_Completion_Before'] = X['Percent_Completion_Before'].map(str)
  dicts =X.to_dict(orient='records')
  print(dicts)
  X.to_csv('/tmp/X.csv') 
  X_media = anvil.media.from_file('/tmp/X.csv', 'text/csv', 'X')
  
  return dicts, X_media

@anvil.server.callable
def stats():
  """Launch a single stats background task."""
  task = anvil.server.launch_background_task('testprojects')
  return task
  
@anvil.server.callable
def daily_stats():
  """Launch a single stats background task."""
  task = anvil.server.launch_background_task('daily_by_stats')
  return task  
  
# @anvil.server.callable
# def test_chart():

#   conn = connect()
#   #=============================================================================  
#   # Load Orders 
#   with conn.cursor() as cur:
#     cur.execute(
#       "Select sales_orders.name As name, sales_orders.date_entered As date_entered, \
#                         CONCAT(sales_orders.prefix,sales_orders.so_number) As so_number, sales_orders.so_stage As so_stage, \
#                         sales_orders.subtotal_usd AS Order_Value, \
#                       sales_orders_cstm.workinprogresspercentcomplete_c AS workinprogresspercentcomplete_c,\
#                       sales_orders_cstm.OrderCategory AS OrderCategory,\
#                       sales_orders_cstm.applicationarea_c AS AppArea, \
#                       sales_orders_cstm.partialinvoicedtotal_c AS partially_invoiced_total, \
#                       If(sales_orders_cstm.applicationarea_c = 'Anticoagulation', 'Anticoagulation', 'Safety Monitoring and Misc') As AppGroup ,\
#                       sales_orders.so_number AS so_number,\
#                       sales_orders.so_stage AS stage, \
#                       users.user_name AS user_name, \
#                       sales_orders_cstm.workinprogresspercentcomplete_c AS workinprogresspercentcomplete_c \
#                       From sales_orders\
#                       INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
#                       LEFT JOIN `users` ON (`sales_orders`.`assigned_user_id` = `users`.`id`) \
#                       Where sales_orders.date_entered > '2020-03-01' AND \
#                       sales_orders_cstm.OrderCategory NOT IN ('Maintenance')     ")    #AND \
#     # sales_orders.so_stage  NOT IN ('Closed', 'On Hold','Cancelled', 'Complete')")  # ,'Complete'
#     records = cur.fetchall()
# number_of_records =len(records)
# print('No of projects',number_of_records)

# if number_of_records:
#   dicts = [{'order_no': r['so_number'], 'project_name':r['name'] ,'order_date':r['date_entered'], 'order_category':r['OrderCategory'],'assigned_to':r['user_name'] , \
#             'order_value':r['Order_Value'], 'percent_complete':r['workinprogresspercentcomplete_c'],'app_area':r['AppArea'] , 'stage':r['stage'], 'Appgroup':r['AppGroup'], \
#             'partially_invoiced_total':r['partially_invoiced_total']} \
#            for r in records]
#   print(dicts)

#   X = pd.DataFrame.from_dict(dicts)

  
# print('Made dicts and dataframe')
# X['order_value']= X['order_value'].map(float)
# # X['cumulative_orders'] =  X['order_value'].cusum()
# print('Cusum =', X['order_value'])
# X['percent_complete'] = X['percent_complete'].fillna(0)
# # print('before',X['percent_complete'])
# X['date_formatted'] = X['order_date'].dt.strftime('%d/%m/%Y')
# X['percent_complete']= X['percent_complete'].astype(int)

# X['partially_invoiced_total'] = X['partially_invoiced_total'].fillna(0)
# X['Work Completed'] =X['order_value'] * X['percent_complete']/100
# X['Work To Do'] =X['order_value'] * (100 - X['percent_complete'])/100
# X['Invoiced but NOT completed amount'] = X['partially_invoiced_total'] - X['Work Completed']
# X['Invoiced but NOT completed amount']= X['Invoiced but NOT completed amount'].map(float)

# if  not_completed =='Yes':
#   X =  X[X['Invoiced but NOT completed amount'] > 0]
# elif not_completed =='No':
#   X =  X[X['Invoiced but NOT completed amount'] <= 0]
#   if assigned_to and not category:
#     filter = (X['assigned_to'] == assigned_to)
#     X =  X[X['percent_complete'] >= int(percent_complete) ]
#     X =  X[X['percent_complete'] <= int(hi_percentage) ]
#     X =  X[filter]
#   elif category and not assigned_to:
#     X =  X[X['percent_complete'] >= int(percent_complete)]
#     X =  X[X['percent_complete'] <= int(hi_percentage) ]
#     X =  X[X['order_category'] == category]
#   elif assigned_to and category:
#     X =  X[X['percent_complete'] >= int(percent_complete) ]
#     X =  X[X['percent_complete'] <= int(hi_percentage) ]
#     filter = (X['assigned_to'] == assigned_to)
#     X =  X[filter]
#     X =  X[X['order_category'] == category]
#   elif percent_complete and not category and not assigned_to:
#     X =  X[X['percent_complete'] >= int(percent_complete)]
#     X =  X[X['percent_complete'] <= int(hi_percentage) ]
#     # print('after filter',X['percent_complete'])
#     X['percent_complete'] = X['percent_complete'].map(int)

# X['order_value_formated'] = X['order_value'].map("£{:,.0f}".format)
# X['partially_invoiced_total_formated'] = X['partially_invoiced_total'].map("£{:,.0f}".format)
# X['Invoiced but NOT completed amount_formated'] = X['Invoiced but NOT completed amount'].map("£{:,.0f}".format)
# X['Value yet to be invoiced'] = X['order_value']-X['partially_invoiced_total']  
# X['Value yet to be invoiced_formated'] = X['Value yet to be invoiced'].map("£{:,.0f}".format)
# today = datetime.today()
# X['days_elapsed'] = (today - X['order_date']).dt.days
# # print(X['days_elapsed']) =  X['days_elapsed'])
# X['Work Completed'] =X['order_value'] * X['percent_complete']/100
# X['Work Completed_formated'] = X['Work Completed'].map("£{:,.0f}".format)
# X['Work To Do'] =X['order_value'] * (100 - X['percent_complete'])/100
# X['Order_Value_Value_Add _per Elapsed_day'] = X['order_value']//X['days_elapsed']
# X['Work_completed_Value_Add _per Elapsed_day'] = X['Work Completed']//X['days_elapsed']
# # X['Value Left to Do'] = (100 - X['percent_complete']) 
# X['Year'] = X['order_date'].dt.year
# X['Month']= X['order_date'].dt.month
# X['Day']= X['order_date'].dt.day
# X['Year'] = X['Year'].map(int)
# X['Month'] = X['Month'].map(int)
# X['Year Num'] =  X['Year'].map(int)
# X['Month Num'] = X['Month'].map(int)
# #     def categorize_year( year, month):
# #       if month <= 2 :
# #           return year - 1
# #       elif month > 2:
# #           return year

# # # Apply the function to the Age column using the apply() function
# #     X['Fin Year'] = X['Year  Num'].apply(categorize_year)
# # Define the conditions and corresponding categories
# conditions = [
#   X['Month Num'] <= 2 ,
#   (X['Month Num'] > 2) & (X['Month Num'] <= 12),

# ]

# categories = [X['Year Num'] -1, X['Year Num']]

# # Use np.select() to create the new column
# X['Fin Year'] = np.select(conditions, categories, default='Unknown') 

# conditions = [
#   X['Month Num'] <= 2 ,
#   (X['Month Num'] > 2) & (X['Month Num'] <= 12),

# ]

# categories = [X['Month Num'] + 10 , X['Month Num'] - 2 ]

# # Use np.select() to create the new column
# X['Fin Month'] = np.select(conditions, categories, default='Unknown')

# # Group the stages into categories
# conditions =[X['stage'] == 'On Hold',

#              X['stage'] == 'Work In Progress - 4S', 
#              X['stage'] == 'Pre-requisites in progress' ,
#              X['stage'] == 'Ready for GoLive', 
#              X['stage'] == 'Ready for UAT',
#              X['stage'] == 'Ready to Start',
#              X['stage'] == 'UAT WIP',

#              X['stage'] == 'Order Approved',
#              X['stage'] == 'Order Submitted for Approval',
#              X['stage'] == 'Ordered']

# categories = ['Projects on Hold', \
#               'Project in Progress', 'Project in Progress', 'Project in Progress','Project in Progress', 'Project in Progress','Project in Progress', \
#               'Project waiting to Start', 'Project waiting to Start','Project waiting to Start']

# X['Stage Group'] = np.select(conditions, categories, default='Unknown')

# pivotsyd = pd.pivot_table(X, values = "order_value", index=['order_category'], aggfunc=('sum'), margins=True, margins_name='Total')
# pivotsyd  = pivotsyd.fillna(0)
# pivotsyd = pivotsyd.sort_values(by=['order_value'], ascending=False)
# print(pivotsyd)
# # fig = px.bar(pivotsyd, x='order_category', y='order_value')
# pivotsyd['order_value']=pivotsyd['order_value'].apply('{:,}'.format)
# print("")
# pivotsyd_to_markdown = pivotsyd.to_markdown()
# print(pivotsyd_to_markdown)
# pd.set_option('display.max_columns', None)
# print('pivotsyd',pivotsyd)

# X = X[(X['Stage Group'] =='Project in Progress')] 
 # X1 = X[['order_no','project_name', 'percent_complete', 'order_value,'partially_invoiced_total_formated','Value yet to be invoiced_formated','days_elapsed','Value yet to be invoiced', 'assigned_to']]
# X1 = X1.sort_values(by='percent_complete',ascending=False)
# X2 = X1.sort_values(by='Value yet to be invoiced_formated',ascending=False)

# dicts =X.to_dict(orient='records')
# dictspip= X1.to_dict(orient='records')

@anvil.server.callable
def stage_groups_chart():
  import plotly.graph_objects as go
  import plotly.express as px 
  chart_data = app_tables.stage_summary.search(tables.order_by("Date_of_WIP", ascending=False) ,Date_of_WIP= q.greater_than(date(year=2024, month=7, day=17)))
  dicts = [{'Date_entered': r['Date_of_WIP'], 
            'Sum_on_hold': r['Sum_on_hold'],
            'Sum_in_Progress': r['Sum_in_Progress'],
            'Sum_in_Waiting_to_Start': r['Sum_in_Waiting_to_Start']
             } 
           for r in chart_data]
  df = pd.DataFrame.from_dict(dicts)
  print('df',df)


  fig = go.Figure([
    go.Scatter(
      name='Total Order Value on Hold',
      x=df['Date_entered'],
      y=df['Sum_on_hold'],
      stackgroup='one',
      mode='lines+markers',
      marker=dict(color='gold', size=6),
      line=dict(width=1),
      showlegend=True)
    ,
    go.Scatter(
      name='Total Order Value in Progress',
      x=df['Date_entered'],
      y=df['Sum_in_Progress'],
      stackgroup='one',
      mode='lines+markers',
      marker=dict(color='mediumturquoise', size=6),
      line=dict(width=1),
      showlegend=True)
    ,
    go.Scatter(
      name='Total Order Value in Waiting to Start',
      x=df['Date_entered'],
      y=df['Sum_in_Waiting_to_Start'],
      stackgroup='one',
      mode='lines+markers',
      marker=dict(color='lightgreen', size=6),
      line=dict(width=1),
      showlegend=True)
  ])
  fig.update_layout(
    title=dict(
      text='Total Order Value of Stage Groups' + '<br>' + 'created at ' + datetime.now().strftime('%d %B %Y %H:%M')
    ),
    yaxis=dict(
      title=dict(
        text="Value"
      )
    ),
    xaxis=dict(
      title=dict(
        text="Date Entered"
      )  
    ))
  fig.update_layout(legend=dict(
    yanchor="top",
    y=0.99,
    xanchor="right",
    x=0.90
  ))
  fig.update_layout(yaxis_range=[0,1000000])
  return fig

 