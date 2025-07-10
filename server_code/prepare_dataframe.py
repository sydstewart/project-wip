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
from datetime import datetime, time, date, timedelta
import numpy as np

def prepare_pandas(dicts, percent_complete,hi_percentage, assigned_to, category, not_completed):

    X = pd.DataFrame.from_dict(dicts)
    print('Made dicts and dataframe')
    X['order_value']= X['order_value'].map(float)
    X['Total Order Value'] =X['order_value'].sum()
    # X['cumulative_orders'] =  X['order_value'].cusum()
    print('Total Order Value from prepare pandas', X['Total Order Value'])
    X['percent_complete'] = X['percent_complete'].fillna(0)
    # print('before',X['percent_complete'])
    X['date_formatted'] = X['order_date'].dt.strftime('%d/%m/%Y')
    X['percent_complete']= X['percent_complete'].astype(int)
    
    X['partially_invoiced_total'] = X['partially_invoiced_total'].fillna(0)
    X['Work Completed'] =X['order_value'] * X['percent_complete']/100
    X['Work To Do'] =X['order_value'] * (100 - X['percent_complete'])/100
    X['Invoiced but NOT completed amount'] = X['partially_invoiced_total'] - X['Work Completed']
    X['Invoiced but NOT completed amount']= X['Invoiced but NOT completed amount'].map(float)

    if  not_completed =='Yes':
           X =  X[X['Invoiced but NOT completed amount'] > 0]
    elif not_completed =='No':
           X =  X[X['Invoiced but NOT completed amount'] <= 0]
    if assigned_to and not category:
       filter = (X['assigned_to'] == assigned_to)
       X =  X[X['percent_complete'] >= int(percent_complete) ]
       X =  X[X['percent_complete'] <= int(hi_percentage) ]
       X =  X[filter]
    elif category and not assigned_to:
          X =  X[X['percent_complete'] >= int(percent_complete)]
          X =  X[X['percent_complete'] <= int(hi_percentage) ]
          X =  X[X['order_category'] == category]
    elif assigned_to and category:
          X =  X[X['percent_complete'] >= int(percent_complete) ]
          X =  X[X['percent_complete'] <= int(hi_percentage) ]
          filter = (X['assigned_to'] == assigned_to)
          X =  X[filter]
          X =  X[X['order_category'] == category]
    elif percent_complete and not category and not assigned_to:
          X =  X[X['percent_complete'] >= int(percent_complete)]
          X =  X[X['percent_complete'] <= int(hi_percentage) ]
    # print('after filter',X['percent_complete'])
    X['percent_complete'] = X['percent_complete'].map(int)
  
    X['order_value_formated'] = X['order_value'].map("£{:,.0f}".format)
    X['partially_invoiced_total_formated'] = X['partially_invoiced_total'].map("£{:,.0f}".format)
    X['Invoiced but NOT completed amount_formated'] = X['Invoiced but NOT completed amount'].map("£{:,.0f}".format)
    X['Value yet to be invoiced'] = X['order_value']-X['partially_invoiced_total']  
    X['Value yet to be invoiced_formated'] = X['Value yet to be invoiced'].map("£{:,.0f}".format)
    today = datetime.today()
    X['days_elapsed'] = (today - X['order_date']).dt.days
    # print(X['days_elapsed']) =  X['days_elapsed'])
    X['Work Completed'] =X['order_value'] * X['percent_complete']/100
    X['Work Completed_formated'] = X['Work Completed'].map("£{:,.0f}".format)
    X['Work To Do'] =X['order_value'] * (100 - X['percent_complete'])/100
    X['Order_Value_Value_Add _per Elapsed_day'] = X['order_value']//X['days_elapsed']
    X['Work_completed_Value_Add _per Elapsed_day'] = X['Work Completed']//X['days_elapsed']
   # X['Value Left to Do'] = (100 - X['percent_complete']) 
    X['Year'] = X['order_date'].dt.year
    X['Month']= X['order_date'].dt.month
    X['Day']= X['order_date'].dt.day
    X['Year'] = X['Year'].map(int)
    X['Month'] = X['Month'].map(int)
    X['Year Num'] =  X['Year'].map(int)
    X['Month Num'] = X['Month'].map(int)
#     def categorize_year( year, month):
#       if month <= 2 :
#           return year - 1
#       elif month > 2:
#           return year

# # Apply the function to the Age column using the apply() function
#     X['Fin Year'] = X['Year  Num'].apply(categorize_year)
    # Define the conditions and corresponding categories
    conditions = [
    X['Month Num'] <= 2 ,
    (X['Month Num'] > 2) & (X['Month Num'] <= 12),
  
]

    categories = [X['Year Num'] -1, X['Year Num']]

# Use np.select() to create the new column
    X['Fin Year'] = np.select(conditions, categories, default='Unknown') 

    conditions = [
    X['Month Num'] <= 2 ,
    (X['Month Num'] > 2) & (X['Month Num'] <= 12),
  
]

    categories = [X['Month Num'] + 10 , X['Month Num'] - 2 ]

# Use np.select() to create the new column
    X['Fin Month'] = np.select(conditions, categories, default='Unknown')

  # Group the stages into categories
    conditions =[X['stage'] == 'On Hold',
                 
                 X['stage'] == 'Awaiting Sign-Off',
                 X['stage'] == 'Work In Progress - 4S', 
                 X['stage'] == 'Pre-requisites in progress' ,
                 X['stage'] == 'Ready for GoLive', 
                 X['stage'] == 'Ready for UAT',
                 X['stage'] == 'Ready to Start',
                 X['stage'] == 'UAT WIP',
                   
                 X['stage'] == 'Order Approved',
                 X['stage'] == 'Order Submitted for Approval',
                 X['stage'] == 'Ordered']

#   Ready for UAT	42,050.00
# UAT WIP              
# Ready for GoLive 
# Ready for UAT 
# Ready to Start 
# UAT WIP
# Order Approved 
# Order Submitted for Approval 
# Ordered
    categories = ['Projects on Hold', 
                  'Project in Progress', 'Project in Progress', 'Project in Progress', 'Project in Progress','Project in Progress', 'Project in Progress','Project in Progress', \
                  'Project waiting to Start', 'Project waiting to Start','Project waiting to Start']
  
    X['Stage Group'] = np.select(conditions, categories, default='Unknown')
  
    pivotsyd = pd.pivot_table(X, values = "order_value", index=['order_category'], aggfunc=('sum'), margins=True, margins_name='Total')
    pivotsyd  = pivotsyd.fillna(0)
    pivotsyd = pivotsyd.sort_values(by=['order_value'], ascending=False)
    # print('pivotsyd',pivotsyd)
    # fig = px.bar(pivotsyd, x='order_category', y='order_value')
    pivotsyd['order_value']=pivotsyd['order_value'].apply('{:,}'.format)
    # print("")
    pivotsyd_to_markdown = pivotsyd.to_markdown()
    # print(pivotsyd_to_markdown)
    pd.set_option('display.max_columns', None)
    # print('pivotsyd',pivotsyd)
    dicts =X.to_dict(orient='records')
  # For projects in progress
    X = X[(X['Stage Group'] =='Project in Progress')] 
    X1 = X[['order_no','project_name', 'percent_complete', 'order_value_formated','partially_invoiced_total_formated','Value yet to be invoiced_formated','days_elapsed','Value yet to be invoiced', 'assigned_to']]
    X1 = X1.sort_values(by='percent_complete',ascending=False)
    # X2 = X1.sort_values(by='Value yet to be invoiced_formated',ascending=False)
    dictspip= X1.to_dict(orient='records')
    
  
    # print('dictspip!!',dictspip)
    X.to_csv('/tmp/X.csv') 
    X_media = anvil.media.from_file('/tmp/X.csv', 'text/csv', 'X')
    # media_object = anvil.pdf.render_form('list_projects')
    return dicts, dictspip, X_media,  pivotsyd_to_markdown