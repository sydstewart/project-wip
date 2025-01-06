import anvil.email
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.secrets
import anvil.server
import pandas as pd
import plotly.graph_objs as go

# def outofcontrolofall(df,'Date',meascol): #, 'Date', meascol, total_rows, pointmean, sd, showmeans, tablename, chartid):

    
#     # title = ('Find six points falling in succession')
#     # 'Date'_title = 'Date'
#     # meascol_title = meascol
#     # return title, 'Date'_title, meascol_title
#     total_rows = df.shape[0]
#     # st.write(total_rows)
#     outofcontrol6fall = pd.DataFrame()
#     for i in range(6, total_rows):
#         countx = 0
#         if (df[meascol].iloc[i] < df[meascol].iloc[i - 1]):
#             countx = 1
#             # st.write(df['Date'].iloc[i], df[meascol].iloc[i], i, countx)
#         if (df[meascol].iloc[i - 1] < df[meascol].iloc[i - 2]):
#             countx = countx + 1
#             # st.write(df['Date'].iloc[i], df[meascol].iloc[i], i, countx)
#         if (df[meascol].iloc[i - 2] < df[meascol].iloc[i - 3]):
#             countx = countx + 1
#         #               print(df[meascol].iloc[i-2],i-2, countx)
#         if (df[meascol].iloc[i - 3] < df[meascol].iloc[i - 4]):
#             countx = countx + 1
#         #               print(df[meascol].iloc[i-3], i-3, countx)
#         if (df[meascol].iloc[i - 4] < df[meascol].iloc[i - 5]):
#             countx = countx + 1
#         #               print(df[meascol].iloc[i-4], i-4, countx)
#         if (df[meascol].iloc[i - 5] < df[meascol].iloc[i - 6]):
#             countx = countx + 1
#             # st.write(df['Date'].iloc[i], df[meascol].iloc[i], i, countx)
#         #       if (df[meascol].iloc[i - 6]  < df[meascol].iloc[i-7] ):
#         #                        countx = countx + 1

#         if countx == 6:
#             outofcontrol6fall = outofcontrol6fall._append(
#                 {'Date': df['Date'].iloc[i - 5], meascol: df[meascol].iloc[i - 5]}, ignore_index=True)
#             outofcontrol6fall = outofcontrol6fall._append(
#                 {'Date': df['Date'].iloc[i - 4], meascol: df[meascol].iloc[i - 4]}, ignore_index=True)
#             outofcontrol6fall = outofcontrol6fall._append(
#                 {'Date': df[datecol].iloc[i - 3], meascol: df[meascol].iloc[i - 3]}, ignore_index=True)
#             outofcontrol6fall = outofcontrol6fall._append(
#                 {datecol: df[datecol].iloc[i - 2], meascol: df[meascol].iloc[i - 2]}, ignore_index=True)
#             outofcontrol6fall = outofcontrol6fall._append(
#                 {datecol: df[datecol].iloc[i - 1], meascol: df[meascol].iloc[i - 1]}, ignore_index=True)
#             outofcontrol6fall = outofcontrol6fall._append(
#                 {datecol: df[datecol].iloc[i], meascol: df[meascol].iloc[i]}, ignore_index=True)

#     if outofcontrol6fall.empty:
#         down6 = go.Scatter(
#             visible='legendonly')
#         mean6fallline = go.Scatter(
#             visible='legendonly',
#             name='New Mean')

#     else:
#         down6 = go.Scatter(  # x=df[datecol],
#             # y=df[meascol],
#             x=outofcontrol6fall[datecol],
#             y=outofcontrol6fall[meascol],
#             mode='markers',
#             name='6 falling in sucession',
#             marker=dict(
#                 color='red',
#                 size=2,
#                 line=dict(
#                     color='green',
#                     width=8
#                 ))
#         )

#     return outofcontrol6fall
# def outofcontrol9below(df, pointdate, pointname, total_rows, pointmean, sd, showmeans , tablename, chartid):

#             import pandas as pd
#             print('pointmean',pointmean) 
#             print()
#             print ('Nine or more Points on low side of the mean')
#             print ('-------------------------------------------')
#             print()
# #             print(df)
# #             print('pointmean=',pointmean)
# #             print('total_rows=', total_rows)
#             t = app_tables.charts.get(chartid = chartid)
            
#             chartname = t['Chart_Name']
#             outofcontrol9below = pd.DataFrame()
#             stagemeandict9low = pd.DataFrame() 
#           # remember ranges start at 0 index
# #             countx = 0  error? spotted 01022023
#             for i in range(8,total_rows + 1):
#                 countx = 0
# #                 print(df[pointname].iloc[i],i)
#                 if (df[pointname].iloc[i]  < (pointmean)):
#                     countx = 1
                   
#                 if (df[pointname].iloc[i-1]  < (pointmean)):
#                         countx = countx + 1
                       
#                 if (df[pointname].iloc[i-2]  < (pointmean)):
#                         countx = countx + 1
                       
#                 if (df[pointname].iloc[i-3]  < (pointmean)):
#                         countx = countx + 1
                        
#                 if (df[pointname].iloc[i-4]  < (pointmean)):
#                         countx = countx + 1

#                 if (df[pointname].iloc[i - 5]  < (pointmean)):
#                         countx = countx + 1
                   
#                 if (df[pointname].iloc[i-6]  < (pointmean)):
#                         countx = countx + 1
                        
#                 if (df[pointname].iloc[i-7]  < (pointmean)):
#                         countx = countx + 1
                        
#                 if (df[pointname].iloc[i-8]  < (pointmean)):
#                         countx = countx + 1
#                 print ('countx=',countx)
               
                
#                 if countx == 9:
                        
#                         outofcontrol9below = outofcontrol9below.append({pointdate: df[pointdate].iloc[i-8],pointname:df[pointname].iloc[i-8]}, ignore_index=True)
#                         outofcontrol9below = outofcontrol9below.append({pointdate: df[pointdate].iloc[i-7],pointname:df[pointname].iloc[i-7]}, ignore_index=True)
#                         outofcontrol9below = outofcontrol9below.append({pointdate: df[pointdate].iloc[i-6],pointname:df[pointname].iloc[i-6]}, ignore_index=True)
#                         outofcontrol9below = outofcontrol9below.append({pointdate: df[pointdate].iloc[i-5],pointname:df[pointname].iloc[i-5]}, ignore_index=True)
#                         outofcontrol9below = outofcontrol9below.append({pointdate: df[pointdate].iloc[i-4],pointname:df[pointname].iloc[i-4]}, ignore_index=True)
#                         outofcontrol9below = outofcontrol9below.append({pointdate: df[pointdate].iloc[i-3],pointname:df[pointname].iloc[i-3]}, ignore_index=True)
#                         outofcontrol9below = outofcontrol9below.append({pointdate: df[pointdate].iloc[i-2],pointname:df[pointname].iloc[i-2]}, ignore_index=True)
#                         outofcontrol9below = outofcontrol9below.append({pointdate: df[pointdate].iloc[i-1],pointname:df[pointname].iloc[i-1]}, ignore_index=True)
#                         outofcontrol9below = outofcontrol9below.append({pointdate: df[pointdate].iloc[i],pointname:df[pointname].iloc[i]}, ignore_index=True)
#                         Mean9below =outofcontrol9below[pointname].mean()
# #                         print('Mean9below',Mean9below)
#                         outofcontrol9below['Mean9below'] = Mean9below
#                         print ('outofcontrol9below', outofcontrol9below)                                              
#                         print(' 9 below Mean for:' ,tablename,' at', (df[pointdate].iloc[i].strftime("%b %d, %Y")), 'with New Mean=',round(Mean9below,0))
                        
#                         row = app_tables.changes.get(
#                                   change_type="9 below mean",
#                                   chartid = chartid,
#                                   change_date= df[pointdate].iloc[i])
      
#                         if not row:
#                                 row = app_tables.changes.add_row(
#                                       change_type="9 below mean",
#                                       chartid = chartid,
#                                       change_date= df[pointdate].iloc[i],
#                                       new_mean=df[pointname].iloc[i],
#                                       short_date = df[pointdate].iloc[i].date(),
#                                       chartname=chartname
#                                 )
  
# #                         stagemean = (df[pointname].iloc[i-8] + df[pointname].iloc[i-7] + df[pointname].iloc[i-1] +
# #                                      df[pointname].iloc[i-6] + df[pointname].iloc[i-5] + df[pointname].iloc[i -4] + 
# #                                      df[pointname].iloc[i-3] + df[pointname].iloc[i-2] + df[pointname].iloc[i])/9
# #                         print('Stagemean 9low', stagemean) 
# # #                         stagemeandict9low = pd.DataFrame() 
# #                         stagemeandict9low = stagemeandict9low.append({pointdate: df[pointdate].iloc[i-5],pointmean:stagemean}, ignore_index=True)
# #                         stagemeandict9low = stagemeandict9low.append({pointdate: df[pointdate].iloc[i-4],pointmean:stagemean}, ignore_index=True)
# #                         stagemeandict9low = stagemeandict9low.append({pointdate: df[pointdate].iloc[i-3],pointmean:stagemean}, ignore_index=True)
# #                         stagemeandict9low = stagemeandict9low.append({pointdate: df[pointdate].iloc[i-2],pointmean:stagemean}, ignore_index=True)
# #                         stagemeandict9low = stagemeandict9low.append({pointdate: df[pointdate].iloc[i-1],pointmean:stagemean}, ignore_index=True)
# #                         stagemeandict9low = stagemeandict9low.append({pointdate: df[pointdate].iloc[i],pointmean:stagemean}, ignore_index=True)
# #                         stagemeandict9low = stagemeandict9low.append({pointdate: df[pointdate].iloc[i-8],pointmean:stagemean}, ignore_index=True)
# #                         stagemeandict9low = stagemeandict9low.append({pointdate: df[pointdate].iloc[i-7],pointmean:stagemean}, ignore_index=True)
# #                         stagemeandict9low = stagemeandict9low.append({pointdate: df[pointdate].iloc[i-6],pointmean:stagemean}, ignore_index=True)
# #                         print ('stagemeandict9low 9 low',stagemeandict9low)
# #                         countx = 0
#             if not outofcontrol9below.empty: 
#                 #Filter out  below (9 below mean)
# #                 outofcontrol9belowfilter =  outofcontrol9below[pointname] < (pointmean)
# #                 outofcontrol9below =  outofcontrol9below[outofcontrol9belowfilter] 
# #                 print('outofcontrol9below with 9 consequtive measures below mean')
#                 Mean9below =outofcontrol9below[pointname].mean()
#                 outofcontrol9below['Mean9below'] = Mean9below
# #                 print ('outofcontrol9below', outofcontrol9below)      
            
# #             print('outofcontrol9below',outofcontrol9below)
            
            
            
#             if outofcontrol9below.empty:  
#                     ninebelow = go.Scatter(
#                     visible='legendonly',
#                     name='9 consecutively below mean')
# #                     i\f showmeans == False:
#                     mean9belowline = go.Scatter(
#                     visible='legendonly',
#                     name='New Mean')
#             else:
#                 ninebelow = go.Scatter(
#                     x=outofcontrol9below[pointdate],
#                     y=outofcontrol9below[pointname],
#                     mode='markers',
#                     name='9 below mean',
#                     marker=dict(
#                         color='red',
#                         size=5,
#                         line=dict(
#                             color='pink',
#                             width=8
#                         ))
#                           ) 
# #                 if showmeans == False:
# #                 mean9belowline = go.Scatter(  # x=df[pointdate],
# #                         # y=df[pointname],
# #                         x=stagemeandict9low[pointdate],
# #                         y=stagemeandict9low[Mean9below],
# #                         mode='markers',
# # #                         marker_symbol = 'line-ew',
# #                         name='New Mean 9 below',
# #                         marker=dict(
# #                             color='pink',
# #                             size=7,
# #                             line=dict(
# #                                 color='black',
# #                                 width=2
# #                             )) )
                
#                 mean9belowline = go.Scatter(  # x=df[pointdate],
#                           # y=df[pointname],
#                           x=outofcontrol9below[pointdate],
#                           y=outofcontrol9below['Mean9below'],
#                           mode='markers',
#                           marker_symbol = 'line-ew',
#                           name='New Mean 9 below',
                          
#                            marker=dict(
#                               color='pink',
#                               size=7,
#                               line=dict(
#                                   color='pink',
#                                   width=2
#                               )) )
  
  
  
  
# #                    stagemeandictline9low = go.Scatter(  # x=df[pointdate],
# #                       # y=df[pointname],
# #                       x=stagemeandict9low[pointdate],
# #                       y=stagemeandict9low[pointmean],
# #                       mode='markers',
# #                       name='9 in succession below mean',
# #                       marker_symbol = 'line-ew',
                      
# #           #             text= str(round(pointmean,1)),
# #           #             textposition='top left',
# #           #             textfont=dict(
# #           #                       family="sans serif",
# #           #                       size=11,
# #           #                       color="black"),
# #                       marker=dict(
# #                           color='green',
# #                           size=7,
# #                           line=dict(
# #                               color='pink',
# #                               width=3
# #                           )) )
#             return  ninebelow,  mean9belowline