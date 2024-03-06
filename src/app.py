#https://www.youtube.com/watch?v=XWJBJoV5yww&ab_channel=CharmingData

import pandas as pd
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

df_1 = pd.read_csv("viz_1.csv")

df_1 = df_1[df_1["Journal"]!= "Total"]
df_2 = pd.read_csv("updated_viz_2.csv")

df_2["yearly_total"] = df_2["DHQ_yearly_total"] + df_2["JCA_yearly_total"] + df_2["JOOCH_yearly_total"]
df_2["proportion of articles with keyword"] = df_2["# of articles keyword DHQ"] + df_2["# of articles keyword JCA"] + df_2["# of articles keyword JOCCH"]

df_3 = pd.read_csv("viz_table.csv")

distinct_colors = [
    '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd',  # Blues, Oranges, Greens, Reds, Purples
    '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',  # Browns, Pinks, Grays, Yellows, Cyans
    '#1a9850', '#66bd63', '#a6d96a', '#d9ef8b', '#fee08b',  # Greens
    '#8dd3c7', '#ffffb3', '#bebada', '#fb8072', '#80b1d3',  # Blues, Yellows, Purples, Reds, Blues
    '#fdb462', '#b3de69', '#fccde5', '#d9d9d9', '#bc80bd',  # Oranges, Greens, Pinks, Grays, Purples
    '#ccebc5', '#ffed6f', '#b15928', '#7cfc00', '#9400d3',  # LawnGreen, DarkViolet
    '#40e0d0', '#da70d6', '#ff634']

df_4 = df_2[["Year","DHQ_yearly_total", "JCA_yearly_total", "JOOCH_yearly_total", "yearly_total"]].drop_duplicates()
df_4.columns = ["Year", "DHQ", "JCA", "JOCCH", "Total"]

final_df_2 = df_2[['Keyword', 'Significance score', 'Rank', 'Year', '# of articles keyword DHQ',
                            '# of articles keyword JCA', '# of articles keyword JOCCH']]

final_df_2.columns = ['Keyword', 'Significance score', 'Rank', 'Year', 'DHQ', 'JCA', 'JOCCH']
final_df_2 = final_df_2.groupby(['Keyword', 'Significance score', 'Rank']).sum().reset_index()
final_df_2 = final_df_2.sort_values(by = 'Rank', ascending = True)


header_style = {
                'textAlign': 'center',
                'color': '#4a90e2',  # Blue color
                'fontSize': '36px',  # Larger font size
                'fontFamily': 'Arial, sans-serif',  # Elegant font family
                'fontWeight': 'bold',  # Bold text
                'textTransform': 'uppercase',  # Uppercase text
                'letterSpacing': '1px',  # Spacing between letters
                'marginBottom': '20px',  # Add bottom margin for spacing
            }

custom_font = {
    'fontFamily': 'Arial, sans-serif'  # You can replace 'Arial, sans-serif' with any other font you prefer
}

drop_down_div = {'textAlign': 'center', 'margin': 'auto', 'color' : '#4a90e2'}

drop_down = {'width': '50%', 'margin': 'auto','backgroundColor': '#1E1E1E', 
                               'color': '#4a90e2', **custom_font}


app = Dash(__name__)
server = app.server

yaxis_range = None


app.layout = html.Div(
    style={'backgroundColor': '#1E1E1E'}, 
    children=[
        
    #Header
    html.Div(className='row',
        style={'background-color': '#282c34', 'padding': '10px'},  # Background color and padding adjusted for a clean look
        children=[
            html.Div(className='twelve columns',
                style = {'textAlign': 'center'},
                children = [
                    html.H2('KEYWORD ANALYSIS ON HUMANITIES JOURNAL ARTICLES',  
                        style = header_style)
                         ]
        )]),
                    html.Div(className='row',
        style={'background-color': '#262c34', 'padding': '10px'},  # Background color and padding adjusted for a clean look
        children=[
            html.Div(className='twelve columns',
                style = {'textAlign': 'center', 'color' : 'white'},
                children = [
        html.P('Text area')
                         ]
        )]),
        
    # Dropdown section 
    html.Div(className = 'row',
        children=[
            #Journal Dropdown
            html.Div(className='four columns',
                style=drop_down_div,  
                children=[
                    dcc.Dropdown(id='journal-dropdown',
                        options=[
                            {'label': 'DHQ', 'value': 'DHQ'},
                            {'label': 'JCA', 'value': 'JCA'},
                            {'label': 'JOCCH', 'value': 'JOCCH'}
                        ], 
                        multi=True, 
                        #value = ["DHQ", "JCA", "JOCCH"],
                        placeholder="Select Humanities Journal",
                        style = drop_down)])
            ,
            html.Div(className='four columns',
                style=drop_down_div,  
                children=[
                    dcc.Dropdown(
                        id='keyword-dropdown',
                        options=[{'label': keyword, 'value': keyword} for keyword in df_2['Keyword'].unique().tolist()],
                        multi=True,
                        #value=df_2['Keyword'].unique().tolist(),  # Set value to include all options
                        placeholder="Select Data Visualization Concept",
                        style= drop_down
                    )])
                    ]
            ),
    
    # Slider
    html.Div(className='row', 
             children=[
                html.Div(className='twelve columns', 
                         children=[
                             html.Div([
                                 html.H3('Choose Year Range',
                                    style={'color': '#FFFFFF', 'font-size': '18px', 'font-weight': 'bold', 'text-align': 'center'}  # Font styles and alignment
                                    ),
                                
                            dcc.RangeSlider(id='year-range-slider',
                                    min=df_2['Year'].min(),
                                    max=df_2['Year'].max(),
                                    value=[df_2['Year'].min(), df_2['Year'].max()],
                                    marks={str(year): str(year) for year in df_2['Year'].unique()})
                                    ], style={'width': '80%', 'margin': 'auto'})
                                    ]
                        )]
            ),
    
    # Cards for displaying number of articles for each journal
    html.Div(className='row', style={'display': 'flex', 'justify-content': 'space-between', 
                                'width': '100%', 'padding-bottom': '10px', }, children=[
    # Card 1: Total no. of articles
    html.Div(className='three columns', style={'paddingLeft': '5px',  'width': '100%'}, children=[
        html.Div(id='total-articles-card', style={'background-color': '#333333', 'color': '#FFFFFF',
                                                'padding' : '20px',
                                                
                                                  'text-align': 'center',
                                              'border': '1px solid #FFFFFF'})
    ]),
    # Card 2: DHQ no. of articles
    html.Div(className='three columns', style={'width': '100%'}, children=[
        html.Div(id='dhq-articles-card', style={'background-color': '#333333', 'color': '#FFFFFF',
                                                'padding' : '20px',
                                                'text-align': 'center',
                                              'border': '1px solid #FFFFFF'})
    ]),
    # Card 3: JCA no. of articles
    html.Div(className='three columns', style={'width': '100%'}, children=[
        html.Div(id='jca-articles-card', style={'background-color': '#333333', 'color': '#FFFFFF',
                                                'padding' : '20px',

                                                'text-align': 'center',
                                              'border': '1px solid #FFFFFF'})
    ]),
    # Card 4: JOCCH no. of articles
    html.Div(className='three columns', style={'paddingRight': '5px', 'width': '100%'}, children=[
        html.Div(id='jocch-articles-card', style={'background-color': '#333333', 'color': '#FFFFFF',
                                                'padding' : '20px',

                                                  'text-align': 'center',
                                              'border': '1px solid #FFFFFF'})
    ])
])
,

    
html.Div(className='row', children=[
        html.Div(className='twelve columns', children=[
        # Graphs
        html.Div(className='row', children=[
            # Graph 1
            html.Div(className='eight columns', style={'display': 'inline-block',
                                                    'padding-left': '2.5px',
                                                    'padding-right': '5px',
                                                      'padding-bottom': '5px'}, children=[
                dcc.Graph(id='histo-chart-final')
            ]),
            # Graph 2
            html.Div(className='four columns', style={'padding-left': '5px', 'padding-right': '2.5px',
                                                      'display': 'inline-block',
                                                      'padding-bottom': '5px'}, children=[
                dcc.Graph(id='second-chart-final')
            ])
        ])
    ])]),
    
    

    
    # Table section
    html.Div(className='row', children=[
        dash_table.DataTable(
            data=[],
            columns=[{'name': col, 'id': col} for col in final_df_2.columns if col!='Year'],
            page_size=11,
            style_table= {
                'overflowX': 'auto',
                'border': '1px solid #FFFFFF',
            },
            style_header={
                'backgroundColor': '#4a90e2',
                'fontWeight': 'bold',
                'border': '1px solid #FFFFFF',
                'color': '#FFFFFF'
            },
            style_data={
                'whiteSpace': 'normal',
                'height': 'auto',
                'border': '1px solid #FFFFFF',
            },
            style_cell={
                'textAlign': 'left',
                'fontSize': '14px',
                'fontFamily': 'Arial, sans-serif',
                'padding': '8px',
                'color': '#FFFFFF',
                'backgroundColor': '#333333',
            },
            id='my-datatable'
        )
    ])
])

@app.callback(
    Output('my-datatable', 'data'),
    [Input('year-range-slider', 'value'),
     Input('journal-dropdown', 'value'),
     Input('keyword-dropdown', 'value')
    ])

def update_table(year_range, selected_journals, selected_keywords):
    
    if selected_keywords is None or len(selected_keywords) == 0:
        selected_keywords = df_2['Keyword'].unique().tolist()
        
    if selected_journals is None or len(selected_journals) == 0:
        selected_journals = ["DHQ", "JCA", "JOCCH"]           



    filtered_df = df_2[(df_2['Year'] >= year_range[0]) & (df_2['Year'] <= year_range[1])]
    filtered_df = filtered_df[filtered_df['Keyword'].isin(selected_keywords)]

    filtered_df = filtered_df[['Keyword', 'Significance score', 'Rank', 'Year', '# of articles keyword DHQ',
                                '# of articles keyword JCA', '# of articles keyword JOCCH']]
    filtered_df.columns = ['Keyword', 'Significance score', 'Rank', 'Year', 'DHQ', 'JCA', 'JOCCH']

    final_df = filtered_df.groupby(['Keyword', 'Significance score', 'Rank']).sum().reset_index()

    if selected_journals: 
        final_df = final_df[['Keyword', 'Significance score', 'Rank'] + selected_journals]
    else:  
        final_df = final_df[['Keyword', 'Significance score', 'Rank']]

    final_df = final_df.sort_values(by = "Rank", ascending = True)
    return final_df.to_dict('records')


# Callback to update the scatter plot based on the selected journal(s)
@app.callback(
    Output(component_id='histo-chart-final', component_property='figure'),
    Input(component_id='journal-dropdown', component_property='value'),
    Input('keyword-dropdown', 'value')

)

def update_graph(selected_journals, selected_keywords):
    if selected_keywords is None or len(selected_keywords) == 0:
        selected_keywords = df_2['Keyword'].unique().tolist()
        
    if selected_journals is None or len(selected_journals) == 0:
        selected_journals = ["DHQ", "JOCCH", "JCA"]
        #return {}  # If no journals are selected, return an empty figure
    
    filtered_df = df_1[df_1['Journal'].isin(selected_journals)]
    filtered_df = filtered_df[filtered_df['Keyword'].isin(selected_keywords)]

    fig = px.scatter(filtered_df, y='Journal', x="% of articles", size="Size", color="Keyword",
                     size_max=20, hover_data={"Keyword": True, "Significance score": True, "# of articles": True,
                                              "% of articles": True, "Rank": True, "Size": False,
                                              "Journal": False}, color_discrete_sequence=distinct_colors)
    fig.update_yaxes(title_text="Digital Humanities Journal", showgrid=False)
    fig.update_xaxes(title_text="% of Articles with keyword", tickformat='.2%', 
                     showgrid=True, gridcolor='#404040', gridwidth=1)
    fig.update_traces(showlegend=True)


    fig.update_layout({
        'plot_bgcolor': '#2b2b2b',  # Dark background color of the plot
        'paper_bgcolor': '#2b2b2b',  # Dark background color of the figure
        'font': {'color': '#FFFFFF'},  # Light text color
        'title': {'text': "Distribution of visualization keywords across journals",  'x': 0.5, 'font': {'size': 15, 'color': '#FFFFFF'}} , # Title of the plot with center alignment
            'margin': dict(l=50, t=50, b=50)  

    })
    
    fig.update_layout(legend=dict(
        traceorder='normal',  # Keep the legend items in the order they are traced
        bordercolor='Black',  # Set border color
        borderwidth=2,  # Set border width
        itemclick=False,  # Disable legend item selection
        itemdoubleclick=False  # Disable legend item double click
    ))
    fig.update_layout(title=dict(
        x=0.1  # Set x position of the title to the left
    ))
    return fig


# Callback to update the second graph with provided plot data
@app.callback(
    Output('second-chart-final', 'figure'),
    [Input('year-range-slider', 'value'),
     Input(component_id='journal-dropdown', component_property='value'),
    Input('keyword-dropdown', 'value')])

def update_second_graph(year_range, selected_journals, selected_keywords):
    
    if selected_keywords is None or len(selected_keywords) == 0:
        selected_keywords = df_2['Keyword'].unique().tolist()
        
    if selected_journals is None or len(selected_journals) == 0:
        selected_journals = ["DHQ", "JOCCH", "JCA"]
        
        
    global yaxis_range  # Access the global variable
    journal_yearly_dict = {'JCA' : 'JCA_yearly_total',
               'DHQ' : 'DHQ_yearly_total', 
               'JOCCH' : 'JOOCH_yearly_total'}

    journal_keyword_dict = {'JCA' : '# of articles keyword DHQ',
               'DHQ' : '# of articles keyword JCA', 
               'JOCCH' : '# of articles keyword JOCCH'}

    if year_range is None or len(year_range) == 0:
        return {}  # If no year range is selected, return an empty figure
    else:
        plot_df_final = df_2[(df_2['Year'] >= year_range[0]) & (df_2['Year'] <= year_range[1])]
        plot_df_final = plot_df_final[plot_df_final['Keyword'].isin(selected_keywords)]
        temp_series_1 = pd.Series(dtype = float)
        temp_series_2 = pd.Series(dtype = float)
                
        for i in selected_journals:
            if(i == "Total"):
                temp_series_1=plot_df_final[journal_yearly_dict['JCA']] + plot_df_final[journal_yearly_dict['DHQ']] + plot_df_final[journal_yearly_dict['JOCCH']]
                temp_series_2=plot_df_final[journal_keyword_dict['JCA']] + plot_df_final[journal_keyword_dict['DHQ']] + plot_df_final[journal_keyword_dict['JOCCH']]
                break
            else:
                temp_series_1 = temp_series_1.add(plot_df_final[journal_yearly_dict[i]], fill_value=0)
                temp_series_2 = temp_series_2.add(plot_df_final[journal_keyword_dict[i]], fill_value=0)
               
        plot_df_final['proportion of articles with keyword'] = temp_series_2 / temp_series_1
        
        fig_2 = px.scatter(plot_df_final, x="Year", y="proportion of articles with keyword",
                           size="Size", color="Keyword", size_max=20, 
                           hover_data = {'Keyword': True, 'dhq_total_keyword_count': False, 
                                         'jca_total_keyword_count': False, 'jooch_total_keyword_count': False, 
                                         'total_keyword_count': False, 'Significance score': True, 
                                         'Rank': True, 'Year': True, '# of articles keyword DHQ': True, 
                                         '# of articles keyword JCA': True, '# of articles keyword JOCCH': True, 
                                         'proportion of articles with keyword': False, 'Size' : False},
                        color_discrete_sequence = distinct_colors )

        fig_2.update_xaxes(title_text="Publication Year", showgrid=False, zeroline=False)
        fig_2.update_yaxes(title_text="% of articles across journals")
        fig_2.update_yaxes(tickformat='.2%', showgrid=False, zeroline=False)
        #fig_2.update_yaxes(range=yaxis_range)
        fig_2.update_traces(showlegend=False)

        fig_2.update_layout(yaxis=dict(side='right'))

        fig_2.update_layout({
            'plot_bgcolor': '#2b2b2b',  # Dark background color of the plot
            'paper_bgcolor': '#2b2b2b',  # Dark background color of the figure
            'font': {'color': '#FFFFFF'},
            'title': {'text': 'Distribution of visualization keywords across years', 'x': 0.5, 'font': {'size': 15, 'color': '#FFFFFF'}},
                'margin': dict(l=0, r=50, t=50, b=50)  
        })
        
        fig_2.update_layout(title=dict(
        x=0.1  # Set x position of the title to the left
        ))
        return fig_2  

# Callback to update the number of articles for each journal based on dropdown and year slider
@app.callback(
    [Output('total-articles-card', 'children'),
     Output('dhq-articles-card', 'children'),
     Output('jca-articles-card', 'children'),
     Output('jocch-articles-card', 'children')],
    [Input('journal-dropdown', 'value'),
     Input('year-range-slider', 'value')]
)
def update_article_counts(selected_journals, selected_years):
    
    if selected_journals is None or len(selected_journals) == 0:
        selected_journals = ["DHQ", "JOCCH", "JCA"]
        
    # Filter data based on selected journal and year range
    filtered_df = df_4[(df_4['Year'] >= selected_years[0]) & 
                       (df_4['Year'] <= selected_years[1])]
    
    
    # Calculate number of articles for each journal
    dhq_articles = 0
    if("DHQ" in selected_journals):
        dhq_articles = int(sum(filtered_df["DHQ"]))
        
    jca_articles = 0
    if("JCA" in selected_journals):
        jca_articles = int(sum(filtered_df["JCA"]))
    
    jocch_articles = 0
    if("JOCCH" in selected_journals):
        jocch_articles = int(sum(filtered_df["JOCCH"]))
    
    total_articles = dhq_articles + jca_articles + jocch_articles
    
    return f'Total Articles: {total_articles}', f'DHQ Articles: {dhq_articles}', f'JCA Articles: {jca_articles}', f'JOCCH Articles: {jocch_articles}'


if __name__ == '__main__':
    app.run(debug=True)
