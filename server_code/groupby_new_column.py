import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server

#
@anvil.server.callable
def groupby_new_column(name):
@anvil.server.callable
def groupareas():
# Get an iterable object with all the rows in my_table
    all_records = app_tables.project_stages.search( )
    # For each row, pull out only the data we want to put into pandas
    dicts = [{'project_board': r['boards'],'project_column':r['stage'], 'new_column':r['new_project_column']['new-column'],'count' : r['count']}] 
            for r in all_records]
    
    df = pd.DataFrame.from_dict(dicts)
#     print(df)
#     group_by_region = df.groupby('Region')['Name'].count()
#     group_by_region = group_by_region.sort_values(['Region'], ascending=False)['Name']
#     print(group_by_region) 


    df = df.groupby('new_column').count() \
                             .reset_index(name='count') \
                             .sort_values(['count'], ascending=False)
    df['sumsystems'] = df['count'].sum()
    df['%'] =(df['count'] * 100)/df['sumsystems']
    df['%'] = df['%'].map('{:,.0f}'.format)    
    df['%'] = df['%'].astype(int)

    df.loc['Total', 'count']= df['count'].sum()
    df.loc['Total', '%']= df['%'].sum()
    df = df.fillna("")
    
    dicts_stages = df.to_dict(orient='records')
    
    return dicts_stages 
#
