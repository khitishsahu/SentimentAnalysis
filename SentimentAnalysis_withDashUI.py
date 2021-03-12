# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 20:29:22 2021

@author: khsahu
"""
#importing libraries
import pickle
import pandas as pd
import numpy as np
import webbrowser
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import plotly.graph_objects as go

import os
os.environ['CURL_CA_BUNDLE'] = ""

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
project_name = "Sentiment Analysis with Insights"

def open_browser():
 #   return webbrowser.open_new("http://127.0.0.1:8050/")
     chrome_path = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
     return webbrowser.get(chrome_path).open_new('http://127.0.0.1:8050/')

def load_model():
    global pickle_model
    global vocab
    global df, dfs
    
    df = pd.read_csv("balanced_reviews.csv") # this dataset is used for model building but not in this file   
    dfs = pd.read_csv("scrappedReviews.csv")   
       
    
    with open("pickle_model.pkl", 'rb') as file:
        pickle_model = pickle.load(file)
    with open("feature.pkl", 'rb') as voc:
        vocab = pickle.load(voc)
        
def check_review(reviewText):
    transformer = TfidfTransformer()
    loaded_vec = CountVectorizer(decode_error="replace",vocabulary=vocab)
    reviewText = transformer.fit_transform(loaded_vec.fit_transform([reviewText]))
    return pickle_model.predict(reviewText)

def create_app_ui():
    global project_name
    global df
    global dfs
    df = df.dropna()
    df = df[df['overall'] != 3]
    df['Positivity'] = np.where(df['overall'] > 3, 1, 0)
    
    bd=[]
    for i in range (0,len(dfs)):
        bd.append(check_review(dfs["reviews"].values[i])[0])
    #values = [len(df[df.Positivity == 1]), len(df[df.Positivity == 0])]
    dfs["positivity"] = bd
    values = [len(dfs[dfs.positivity == 1]), len(dfs[dfs.positivity == 0])]
    labels = ['Positive Reviews', 'Negative Reviews']
    main_layout = dbc.Container(
        dbc.Jumbotron(
                [
                    html.H1(id = 'heading', children = project_name, className = 'display-3 mb-4'),
                    dbc.Container(
                        dcc.Loading(
                        dcc.Graph(
                            figure = {'data' : [go.Pie(labels=labels, values=values)],
                                      'layout': go.Layout(height = 600, width = 1000, autosize = False)
                                      }
                            )
                        ),
                        className = 'd-flex justify-content-center'
                    ),
                    
                    html.Hr(),
                    dbc.Textarea(id = 'textarea', className="mb-3", placeholder="Enter the Review", value = 'I do not like the product', style = {'height': '150px'}),
                    html.Div(id = 'result'),
                    html.Hr(),
                    dbc.Container([
                        dcc.Dropdown(
                    id='dropdown',
                    placeholder = 'Select a Review',
                    options=[{'label': i[:100] + "...", 'value': i} for i in dfs.reviews],
                    value = dfs.reviews[0],
                    style = {'margin-bottom': '30px'}
                    
                )
                       ],
                        style = {'padding-left': '50px', 'padding-right': '50px'}
                        ),
                    html.Div(id = 'result1'),
                    dbc.Button("Submit", color="dark", className="mt-2 mb-3", id = 'button', style = {'width': '100px'})
                    ],
                className = 'text-center'
                ),
        className = 'mt-4'
        )
    return main_layout

@app.callback(
    Output('result', 'children'),
    [
    Input('button', 'n_clicks')
    ],
    [
    State('textarea', 'value')
    ]
    )    
def update_app_ui(n_clicks, textarea):
    result_list = check_review(textarea)
    
    if (result_list[0] == 0 ):
        return dbc.Alert("Negative", color="danger")
    elif (result_list[0] == 1 ):
        return dbc.Alert("Positive", color="success")
    else:
        return dbc.Alert("Unknown", color="dark")

@app.callback(
    Output('result1', 'children'),
    [
    Input('button', 'n_clicks')
    ],
    [
     State('dropdown', 'value')
     ]
    )
def update_dropdown(n_clicks, value):
    result_list = check_review(value)
    
    if (result_list[0] == 0 ):
        return dbc.Alert("Negative", color="danger")
    elif (result_list[0] == 1 ):
        return dbc.Alert("Positive", color="success")
    else:
        return dbc.Alert("Unknown", color="dark")
    
def main():
    global app
    global project_name
    load_model()
    app.layout = create_app_ui()
    app.title = project_name
    open_browser()
    app.run_server()
    app = None
    project_name = None
if __name__ == '__main__':
    main()
