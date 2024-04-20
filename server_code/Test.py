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
import math
from anvil.tables import app_tables
from anvil.pdf import PDFRenderer

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
     
   df['mean'] = df['delta_work'].mean()
   Mean = df['delta_work'].mean()
   print('Mean=', df['delta_work'].mean())
   df['Range']= abs(df['delta_work'] - df['delta_work'].shift(1))
   df['Range'].dropna()
   print('Ranges', df['Range'])
   df['rangemean']  = df['Range'].mean()
   RangeMean =  df['Range'].mean() 
   print('rangemean=', df['Range'].mean())
   df['median'] = df['Range'].median()
   RangeMedian= df['Range'].median()
   print('median of Range=', RangeMedian)
  
  #== Calcuate UCLs ========================================================
   UCLMedian = (RangeMedian  * 3.14) + Mean
   print(' UCL using Range Median =', UCLMedian)
   UCLMean = RangeMean *2.66 + Mean
   print(' UCL using Range Mean =', UCLMean)
   UCLcChart = (math.sqrt(Mean) * 3) + Mean
   LCL = Mean - (RangeMedian  * 3.14) 
   print(' LCL using Range Medeian =', LCL)
  
   line_plots = [
          
           go.Scatter(x=df['Date_entered'], y=df['delta_work'], name='Delta Work Completed', marker=dict(color='#e50000')),
        
           go.Scatter(x=df['Date_entered'], y=df['mean'],  name='Mean of Delta Work per week='  + str(round(Mean,1))),
    
          # go.Scatter(x=res['ym-date'], 
          #           y=(res['rangemean'] * 2.66) + res['mean'], 
          #           name='UCL based on range mean = ' + str(round(UCLMean,1))),
    
          go.Scatter(x= df['Date_entered'], 
                    y=(df['median'] * 3.14) + df['mean'], 
                    name='UCL based on range median  =' + str(round(UCLMedian,1)) ),
          
          # go.Scatter(x=res['ym-date'], 
          #           y= ((res['sqmean'])) * 3 + res['mean'], 
          #           name='UCL based on c-Chart  =' + str(round(UCLcChart,1)) )
                    
                    ]





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
    to="sydney.w.stewart@gmail.com", # ,alistair@4s-dawn.com",
    subject="An auto-generated Project Flow Run Chart",
    text="Your auto-generated Project Flow Run Chart is attached to this email as a PDF.",
    attachments=anvil.PDFRenderer(page_size='A4'. landscape = True).render_form('run_chart')   #     pdf.render_form(page_size='A4')('run_chart')
  
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
               users.`email1` AS users_email1, \
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
        
        # print('Last percent change= ',last_percent_complete) 
        email = (r['users_email1'].lower())  # emails in CRM different with some capitalised first letter
    
        print('days elapsed=', days_elapsed)
        print('days since updated=', days_since_updated )
        if projrec:
          app_tables.burndown.add_row(order_no = r['so_number'],timeline_date = datetime.today(), percent_complete =r['workinprogresspercentcomplete_c'], order_no_link= projrec, elapsed_days= days_elapsed)
          projreclast = app_tables.projects_master.get(order_no = r['so_number'])   
          order_value = projreclast['order_value']
          update_row = app_tables.projects_master.get(order_no =  r['so_number'])
          update_row['latest_percent_complete'] = r['workinprogresspercentcomplete_c']
          update_row['percent_change']= r['workinprogresspercentcomplete_c'] - last_percent_complete
          update_row['elapsed_time'] = days_elapsed
          update_row['days_since_updated'] = days_since_updated
          update_row['value_change'] = update_row['order_value'] * update_row['percent_change']/100
        else: # add new project master then burndown
          app_tables.projects_master.add_row(order_no = r['so_number'],project_name =r['name'], order_value = r['Order_Value'],order_date = r['date_entered'],
                                             order_category = r['OrderCategory'], user = r['first_name'], latest_percent_complete =r['workinprogresspercentcomplete_c'],                            
                                             elapsed_time  = days_elapsed, user_email = email, days_since_updated= days_since_updated, percent_change=  r['workinprogresspercentcomplete_c'] , value_change= order_value*percent_change/100 )
          order_link =  app_tables.projects_master.get(order_no=r['so_number'])
          app_tables.burndown.add_row(order_no = r['so_number'],timeline_date = datetime.today(), percent_complete =r['workinprogresspercentcomplete_c'], order_no_link=order_link,elapsed_days= days_elapsed)
 
@anvil.server.callable
def show_progress(project):
      order_no = app_tables.projects_master.get(project_name=project)
      project_burndown = app_tables.burndown.search(order_no_link  = order_no)
      dicts = [{'order_no': r['order_no'], 'order_date':r['order_no_link']['order_date'],'user':r['order_no_link']['user'],'percent_complete': r['percent_complete'], 'project_name':r['order_no_link']['project_name'], 'order_value':r['order_no_link']['order_value'], 'timeline_date':r['timeline_date'],'elapsed_time':r['elapsed_days', 'percent_change':r['percent_change']]} for r in project_burndown ]
      print(dicts)
      return dicts 

@anvil.server.callable
def show_progress_managers(user):
      print('past user',user)
      
     
      if user and user != 'All':
          order_no = app_tables.projects_master.search(tables.order_by('latest_percent_complete', ascending=False), user_email= user)
          titledesc = 'Heat Map of Projects created at ' + datetime.now().strftime('%d %B %Y %H:%M') + ' for ' + (user)
      if user == 'All':
          order_no = app_tables.projects_master.search(tables.order_by('latest_percent_complete', ascending=False))
          titledesc = 'Heat Map of Projects created at ' + datetime.now().strftime('%d %B %Y %H:%M')
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
                             title = titledesc
                            )

            fig.add_shape(type="line",  x0=1, y0=0, x1=200, y1=100, line=dict(color="green",width=2) )
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
      order_no = app_tables.projects_master.search()
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