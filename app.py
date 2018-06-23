import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd
import pickle

app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

with open('author_num_comments_df.pkl', 'rb') as f:
    df = pickle.load(f)

options = list(set(df['author']))
options.sort()
options = [{'label':option, 'value':option} for option in options]
#Might need to turn above into 'value': value dict

app.layout = html.Div(children=[
    html.H1(children='Number of Marginal Revolution Posts Over Time, by Author'),

    dcc.Dropdown(
        id='author-dropdown',
        options=options
    ),

    dcc.Graph(id='mr_author_comment_graph'),

    dcc.Markdown('''Created by [Mark Nagelberg](http://www.marknagelberg.com/)
    using Dash. See the original blog post corresponding to this dashboard
    [here](http://marknagelberg.com/digging-into-data-science-tools-using-plotlys-dash-to-build-interactive-dashboards).''')

    ])

@app.callback(Output('mr_author_comment_graph', 'figure'), [Input('author-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    author_num_comments_df = df[df['author'] == selected_dropdown_value]
    return {
            'data': [{
                'x': author_num_comments_df['dates_trunc'],
                'y': author_num_comments_df['number_posts']
                }]
            }


if __name__ == '__main__':
    app.run_server(debug=True)
