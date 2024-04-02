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
  records = cur.fetchall()
  number_of_records =len(records)

# calculate WIP
  with conn.cursor() as cur1:
        cur1.execute(
          "Select Sum(sales_orders.subtotal_usd) As Total_Order_Value,\
            Avg(sales_orders_cstm.workinprogresspercentcomplete_c) As Average_WIP,\
            Sum((sales_orders.subtotal_usd *  sales_orders_cstm.workinprogresspercentcomplete_c) / 100) As Total_WIP_VaLUE \
          From sales_orders \
              INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
              Where sales_orders.date_entered > '2015-09-30' AND \
                  sales_orders_cstm.OrderCategory NOT IN ('Maintenance') AND \
                  sales_orders.so_stage NOT IN ('Closed', 'On Hold', 'Cancelled','Work In Progress - 4S')"
        )
  for r in cur1.fetchall():
        Total_Order_Value =r['Total_Order_Value']
        Total_Order_Value = f"{Total_Order_Value  :.2f}"
        print('Total_Order_Value=',r['Total_Order_Value'])
        Average_WIP = (r['Average_WIP'])
        Average_WIP  = f"{Average_WIP :.2f}"
        print('Average_WIP=',Average_WIP )
        print('Total_WIP_VaLUE',r['Total_WIP_VaLUE'])
        Total_WIP_VaLUE = r['Total_WIP_VaLUE']
        Total_WIP_VaLUE = f"{Total_WIP_VaLUE :.2f}"
        Total_WIP_VaLUE = float(Total_WIP_VaLUE)
  totals = cur1.fetchall()
  today = datetime.today()
  last_row = app_tables.completed_work.search(tables.order_by('Date_entered', ascending=False))[0]
  last_reading = last_row['Order_Value_Completed']
  print('last_reading=', last_reading)
  delta = Total_WIP_VaLUE - float(last_reading)
  app_tables.completed_work.add_row(Order_Value_Completed=Total_WIP_VaLUE,Date_entered = today,delta_work= delta)
  totals = cur.fetchall()
  return records,Total_Order_Value , Total_WIP_VaLUE , Average_WIP, number_of_records


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
              Where sales_orders.date_entered > '2015-09-30' AND \
                  sales_orders_cstm.OrderCategory NOT IN ('Maintenance') AND \
                  sales_orders.so_stage  NOT IN ('Closed', 'On Hold','Cancelled','Work In Progress - 4S')"
                    )  
  records = cur.fetchall()
  number_of_records =len(records)

# calculate WIP
  with conn.cursor() as cur1:
        cur1.execute(
          "Select Sum(sales_orders.subtotal_usd) As Total_Order_Value,\
            Avg(sales_orders_cstm.workinprogresspercentcomplete_c) As Average_WIP,\
            Sum((sales_orders.subtotal_usd *  sales_orders_cstm.workinprogresspercentcomplete_c) / 100) As Total_WIP_VaLUE \
          From sales_orders \
              INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
              Where sales_orders.date_entered > '2015-09-30' AND \
                  sales_orders_cstm.OrderCategory NOT IN ('Maintenance') AND \
                  sales_orders.so_stage NOT IN ('Closed', 'On Hold', 'Cancelled','Work In Progress - 4S')"
        )
  for r in cur1.fetchall():
        Total_Order_Value =r['Total_Order_Value']
        Total_Order_Value = f"{Total_Order_Value  :.2f}"
        print('Total_Order_Value=',r['Total_Order_Value'])
        Average_WIP = (r['Average_WIP'])
        Average_WIP  = f"{Average_WIP :.2f}"
        print('Average_WIP=',Average_WIP )
        print('Total_WIP_VaLUE',r['Total_WIP_VaLUE'])
        Total_WIP_VaLUE = r['Total_WIP_VaLUE']
        Total_WIP_VaLUE = f"{Total_WIP_VaLUE :.2f}"
        Total_WIP_VaLUE = float(Total_WIP_VaLUE)
  totals = cur1.fetchall()
  today = datetime.today()
  last_row = app_tables.completed_work.search(tables.order_by('Date_entered', ascending=False))[0]
  last_reading = last_row['Order_Value_Completed']
  print('last_reading=', last_reading)
  delta = Total_WIP_VaLUE - float(last_reading)
  app_tables.completed_work.add_row(Order_Value_Completed=Total_WIP_VaLUE,Date_entered = today,delta_work= delta)
  totals = cur.fetchall()
  return records,Total_Order_Value , Total_WIP_VaLUE , Average_WIP, number_of_records


import anvil.pdf

@anvil.server.callable
def create_zaphod_pdf():
  media_object = anvil.pdf.render_form('chart_form')
  return media_object

@anvil.server.callable
def send_pdf_email():
  anvil.email.send(
    from_name="Test Project Work Flow Run Chart", 
    to="sydney.w.stewart@gmail.com,alistair@4s-dawn.com",
    subject="An auto-generated Project Flow Run Chart",
    text="Your auto-generated Project Flow Run Chart is attached to this email as a PDF.",
    attachments=anvil.pdf.render_form('Email_chart')
  )

# syd@4s-dawn.com, 4salistair@gmail.com,

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
               sales_orders.date_modified AS date_modified \
               From sales_orders\
               INNER JOIN `sales_orders_cstm` ON (`sales_orders`.`id` = `sales_orders_cstm`.`id_c`)\
               LEFT JOIN `users` ON (`sales_orders`.`assigned_user_id` = `users`.`id`) \
              Where sales_orders.date_entered > '2015-09-30' AND \
                  sales_orders_cstm.OrderCategory NOT IN ('Maintenance') AND \
                  sales_orders.so_stage  NOT IN ('Closed', 'On Hold','Cancelled','Work In Progress - 4S')"
                    )  
  records = cur2.fetchall()
  number_of_records =len(records)
  print('Number of timeline records loaded = ',number_of_records)
  for r in records:
        projrec = app_tables.projects_master.get(order_no = r['so_number'])
        print('Order No', r['so_number'] )
        today = date.today()
        date_entered = (r['date_entered']).date()
        date_modified = (r['date_modified']).date()
        days_elapsed = abs(today - date_entered).days
        days_since_updated =  abs(today - date_modified).days
        print('days elapsed=', days_elapsed)
        print('days since updated=', days_since_updated )
        if projrec:
          app_tables.burndown.add_row(order_no = r['so_number'],timeline_date = datetime.today(), percent_complete =r['workinprogresspercentcomplete_c'], order_no_link= projrec, elapsed_days= days_elapsed)
          update_row = app_tables.projects_master.get(order_no =  r['so_number'])
          update_row['latest_percent_complete'] = r['workinprogresspercentcomplete_c']
          update_row['elapsed_time'] = days_elapsed
          update_row['days_since_updated'] = days_since_updated
        else: # add new project master then burndown
          app_tables.projects_master.add_row(order_no = r['so_number'],project_name =r['name'], order_value = r['Order_Value'],order_date = r['date_entered'],
                                             order_category = r['OrderCategory'], user = r['first_name'], latest_percent_complete =r['workinprogresspercentcomplete_c'],                            
                                             elapsed_time  = days_elapsed)
          order_link =  app_tables.projects_master.get(order_no=r['so_number'])
          app_tables.burndown.add_row(order_no = r['so_number'],timeline_date = datetime.today(), percent_complete =r['workinprogresspercentcomplete_c'], order_no_link=order_link,elapsed_days= days_elapsed)
 
@anvil.server.callable
def show_progress(project):
      order_no = app_tables.projects_master.get(project_name=project)
      project_burndown = app_tables.burndown.search(order_no_link  = order_no)
      dicts = [{'order_no': r['order_no'], 'order_date':r['order_no_link']['order_date'],'user':r['order_no_link']['user'],'percent_complete': r['percent_complete'], 'project_name':r['order_no_link']['project_name'], 'order_value':r['order_no_link']['order_value'], 'timeline_date':r['timeline_date'],'elapsed_time':r['elapsed_days']} for r in project_burndown ]
      print(dicts)
      return dicts 

@anvil.server.callable
def show_progress_managers(user):
      order_no = app_tables.projects_master.search(tables.order_by('latest_percent_complete', ascending=False), user=user)
      dicts = [{'order_no': r['order_no'], 'order_date':r['order_date'],'user':r['user'],'latest_percent_complete': r['latest_percent_complete'], 'project_name':r['project_name'], 'order_value':r['order_value'],'elapsed_time':r['elapsed_time'],'days_since_updated': r['days_since_updated']} for r in order_no]
      print(dicts)
      df = pd.DataFrame.from_dict(dicts)
      print('df',df)
      line_plots = go.Scatter(x=df['elapsed_time'], y=df['latest_percent_complete'], name='Project Progress', marker=dict(color='#e50000', size=df['order_value']/3000 +4), mode="markers", text=df['project_name'] + "<br>Order Value: £" + df['order_value'].astype(str) )
      return dicts, line_plots 


@anvil.server.callable
def project_list():
   projects =list({(r['project_name']) for r in app_tables.projects_master.search(tables.order_by('project_name'))})
   return projects

@anvil.server.callable
def managers_list():
   managers =list({(r['user']) for r in app_tables.projects_master.search(tables.order_by('user',ascending=True ))})
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
      order_no = app_tables.projects_master.search()
      dicts = [{'order_no': r['order_no'], 'order_date':r['order_date'],'percent_complete': r['latest_percent_complete'], 'project_name':r['project_name'], 'order_value':r['order_value'], 'elapsed_days':r['elapsed_time']} for r in order_no]
      df = pd.DataFrame.from_dict(dicts)
      dfelapsed = df['elapsed_days']
      project_count = len(df)
      average_elapsed = df['elapsed_days'].mean()
      print('dfelapsed',dfelapsed)
      # fig = go.Figure()
      # fig.add_trace(go.Histogram(x= dfelapsed, xbins =dict(start=0, end=3500, size=365), histnorm = 'percent', cumulative_enabled=True))
         
      print(df)
      # fig = px.histogram(df,
      #   x='dfelapsed',
      #   y='count',
      #   xbins =dict(start=0, end=3500, size=365),
      #   cumulative =True
      #   # marginal='box'
      #   )
       
      # fig.add_vline(x=average_elapsed, line_width=2, line_dash='dash', line_color='red', col=1)
      # # fig.add_vline(x=3.4, line_width=1, line_dash='dash', line_color='gray', col=2)
      # # fig.add_vline(x=4.1, line_width=1, line_dash='dash', line_color='gray', col=3)
      
      # return project_count, fig, average_elapsed
      line_plots = go.Histogram(x= dfelapsed, xbins =dict(start=0, end=3500, size=365), histnorm = 'percent', cumulative_enabled=True)
      #   # # # line_plots.add_vline(x =average_elapsed)
      #   # # # fig.add_hline(y=0.9)
      #   # return project_count, line_plots, average_elapsed
      # line_plots = go.Histogram(x= dfelapsed, xbins =dict(start=0, end=3500, size=365), histnorm = 'percent', cumulative_enabled=True)
      # # line_plots.add_vline(x =average_elapsed)
      # # fig.add_hline(y=0.9)
      return project_count, line_plots, average_elapsed

@anvil.server.callable
def show_histograms_px():
      order_no = app_tables.projects_master.search()
      dicts = [{'order_no': r['order_no'], 'order_date':r['order_date'],'percent_complete': r['latest_percent_complete'], 'project_name':r['project_name'], 'order_value':r['order_value'], 'elapsed_days':r['elapsed_time']} for r in order_no]
      df = pd.DataFrame.from_dict(dicts)
      fig = px.histogram(df, x="elapsed_days",cumulative=True,histnorm = 'percent', nbins =35, marginal ='violin' )
      # dfelapsed = df['elapsed_days']
      project_count = len(df)
      average_elapsed = df['elapsed_days'].mean()
      # print('dfelapsed',dfelapsed)
      # # fig = go.Figure()
      # # fig.add_trace(go.Histogram(x= dfelapsed, xbins =dict(start=0, end=3500, size=365), histnorm = 'percent', cumulative_enabled=True))
         
      # print(df)
      # # fig = px.histogram(df,
      # #   x='dfelapsed',
      # #   y='count',
      # #   xbins =dict(start=0, end=3500, size=365),
      # #   cumulative =True
      # #   # marginal='box'
      # #   )
       
      fig.add_vline(x=average_elapsed, line_width=2, line_dash='dash', line_color='red', col=1,  annotation_text="Average Days in Progress= " + str(int(average_elapsed)), annotation_position="top right" )
      # # # fig.add_vline(x=3.4, line_width=1, line_dash='dash', line_color='gray', col=2)
      # # # fig.add_vline(x=4.1, line_width=1, line_dash='dash', line_color='gray', col=3)
      
      # # return project_count, fig, average_elapsed
      # line_plots = go.Histogram(x= dfelapsed, xbins =dict(start=0, end=3500, size=365), histnorm = 'percent', cumulative_enabled=True)
      # #   # # # line_plots.add_vline(x =average_elapsed)
      # #   # # # fig.add_hline(y=0.9)
      # #   # return project_count, line_plots, average_elapsed
      # # line_plots = go.Histogram(x= dfelapsed, xbins =dict(start=0, end=3500, size=365), histnorm = 'percent', cumulative_enabled=True)
      # # # line_plots.add_vline(x =average_elapsed)
      # # # fig.add_hline(y=0.9)
      return project_count, fig, average_elapsed