import anvil.email
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server
import pandas as pd
#
@anvil.server.callable
def active_projects():

# Get an iterable object with all the rows in my_table
    all_records = app_tables.projects_stages.search(project_column = q.not_('40. Done',	'90. Completed',	'90. Gone Live - Completed', \
                                                                            'Done',	'Lost/Closed','15. Free of Charge','90. Gone Live - Completed', \
                                                                            'Released','Archive','To Archive','Archived', '10. Order Approved','Ordered',  \
                                                                             '10. Scheduled','To Do', 'To be re-visited','Planning','Planned')
                                                                            , project_board =q.not_('Sales & Marketing') )
    # For each row, pull out only the data we want to put into pandas
    dicts = [{'project_board': r['project_board'],'project_column':r['project_column'], 'new_column':r['new_project_column']['new_column'],'count' : r['count']}
             for r in all_records]

    df = pd.DataFrame.from_dict(dicts)
    print(df['new_column'])
    # options = ['02. Order Approved', '03. Pre-requisites'] 
    # df = df['new_column'].isin(options)
 
    df = df.groupby('project_board')['count'].sum() \
                               .reset_index(name='count') \
                             .sort_values(['count'], ascending=False)
  
    
# selecting rows based on condition 
    
    df['sumsystems'] = df['count'].sum()
    df['%'] =(df['count'] * 100)/df['sumsystems']
    df['%'] = df['%'].map('{:,.0f}'.format)    
    df['%'] = df['%'].astype(int)

    df.loc['Total', 'count']= df['count'].sum()
    df.loc['Total', '%']= df['%'].sum()
    df = df.fillna("")
    
    dicts_boards = df.to_dict(orient='records')
    
    return dicts_boards 
#
