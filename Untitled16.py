#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


df = pd.read_csv(r"C:\Users\naipe\Downloads\8. Netflix Dataset.csv")


# In[3]:


df.head(10)


# In[4]:


df.tail(10)


# In[6]:


df.shape


# In[8]:


df.columns


# In[10]:


df[df.duplicated()]


# In[12]:


df.drop_duplicates(inplace=True)
df.shape


# In[14]:


df.isnull().sum()


# In[16]:


df.dtypes


# In[17]:


df['Date']= pd.to_datetime(df['Release_Date'])


# In[18]:


df['Date'].dt.year.value_counts()


# In[19]:


import seaborn as sns


# In[20]:


df['Date'].dt.year.value_counts().plot(kind='bar')


# In[38]:


df.groupby('Category').Category.count().plot(kind='bar')


# In[65]:


countries= df['Country'].value_counts().sort_values(ascending=False)


# In[63]:


countries.head(10).plot(kind='bar')


# In[64]:


df['Director'].value_counts().head(10)


# In[114]:


genre_list = [i for i in df['Type']]
cleaned_list = [value.strip() for item in genre_list for value in item.split(',')]
unique_list = list(set(cleaned_list))
unique_list


# In[178]:


country_list = [i for i in df['Country']]
cleaned_country = [value.strip() for item in country_list for value in str(item).split(',') if pd.notna(item)]
unique_country = list(set(cleaned_country))
unique_country.sort()
unique_country


# In[94]:


drama_movie= df[(df['Category'] == 'Movie') & df['Type'].str.contains('Drama', case=False)]
drama_movie


# In[120]:


df['Year'] = df['Year'].fillna(0).astype(int)
df.head()


# In[159]:


get_ipython().system('pip install pandas dash')
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
from dash import dash_table
from dash.dash_table.Format import Group


# In[248]:


from IPython.display import IFrame


# In[249]:


app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True


# In[250]:


year_list = [i for i in range(2010, 2020, 1)]

@app.callback(
    Output('table', 'data'),  
    Input('input-country', 'value'),
    Input('input-year', 'value'),
    Input('input-category', 'value'),
    Input('input-genre', 'value'),
)
def update_table(selected_country, selected_year, selected_category, selected_genre):
    filtered_df = df.copy()  
    
    if selected_country:
        filtered_df = filtered_df[filtered_df['Country'] == selected_country]
    if selected_year:
        filtered_df = filtered_df[filtered_df['Year'] == selected_year]
    if selected_category:
        filtered_df = filtered_df[filtered_df['Category'] == selected_category]
    if selected_genre:
        filtered_df = filtered_df[filtered_df['Type'].str.contains(selected_genre, case=False)]

    if filtered_df.empty:
        return []
    else:
        table_data = filtered_df.to_dict('records')
        return table_data

table = dash_table.DataTable(
    id='table',
    columns=[{'name': col, 'id': col} for col in df.columns],  
    data=df.to_dict('records'),  
)

app.layout = html.Div(children=[
        html.Link(href='https://fonts.googleapis.com/css?family=Bebas Neue', rel='stylesheet'),
    html.H1('NETFLIX 2010-2019', style={'textAlign': 'center', 'color': '#D2042D', 'font-size': '20px', 'font-family':'Bebas Neue'}),
    html.Div([
        html.Div([
            html.H2('COUNTRY:', style={'margin-right': '2em', 'font-family':'Bebas Neue', 'color': '#D2042D'}),
        ]),
        dcc.Dropdown(
            id='input-country', 
            options=[{'label': i, 'value': i} for i in unique_country], 
            placeholder='Select a country:', style={'width': '80%', 'padding': '3px', 'font-size': '20px', 'textAlign': 'center'},
        )
    ], style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '10px', 'background-color':'#080808'}),  
    html.Div([
        html.Div([
            html.H2('YEAR:', style={'margin-right': '3em', 'font-family':'Bebas Neue', 'color': '#D2042D'}),
        ]),
        dcc.Dropdown(
            id='input-year',
            options=[{'label': i, 'value': i} for i in year_list],
            placeholder='Select a year',
            style={'width': '80%', 'padding': '4px', 'font-size': '20px', 'textAlign': 'center'},       
        )
    ], style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '10px', 'background-color':'#080808'}),
    html.Div([
        html.Div([
            html.H2('CATEGORY:', style={'margin-right': '2em', 'color': '#D2042D', 'font-family':'Bebas Neue'})
        ]),
        dcc.Dropdown(
            id='input-category',
            options=[{'label': 'Movie', 'value': 'Movie'},
                     {'label':'TV Show', 'value': 'TV Show'}],
            placeholder='Select a category',
            style={'width': '80%', 'padding': '1px', 'font-size': '20px', 'textAlign': 'center'},       
        )
    ], style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '10px', 'background-color':'#080808'}),
    html.Div([
        html.Div([
            html.H2('GENRE:', style={'margin-right': '3em', 'font-family':'Bebas Neue', 'color': '#D2042D'})
        ]),
        dcc.Dropdown(
            id='input-genre',
            options=[{'label': i, 'value': i} for i in df['Type'].unique()],
            placeholder='Select a genre',
            style={'width': '80%', 'padding': '4px', 'font-size': '20px', 'textAlign': 'center'},       
        )
    ], style={'display': 'flex', 'justify-content': 'center', 'margin-bottom': '10px', 'background-color':'#080808'}),
    dash_table.DataTable(
        id='table',
        columns=[{'name': col, 'id': col} for col in df.columns],  
        data=df.to_dict('records'),  
    ),
], style={'background-color':'#080808'})


# In[251]:


if __name__ == '__main__':
    app.run_server(port=8080, mode='inline')


# In[ ]:




