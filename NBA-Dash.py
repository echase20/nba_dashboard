
import dash
from dash import dcc,html
import dash_bootstrap_components as dbc
import pandas as pd
from dash.dependencies import Input, Output, State
from dash import dash_table
from redis_api import NBAAPI
from nba_api.stats.static import players,teams
import plotly.express as px


api = NBAAPI(6379, 0)
playerdf = api.get('StevenAdamsCareer')
print(playerdf.columns)


player_options = pd.DataFrame(players.get_active_players()).full_name
player_columns = ['PLAYER_NAME','PLAYER_ID', 'SEASON_ID', 'LEAGUE_ID', 'TEAM_ID', 'TEAM_ABBREVIATION',
       'PLAYER_AGE', 'GP', 'GS', 'MIN', 'FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A',
       'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL',
       'BLK', 'TOV', 'PF', 'PTS',]
team_options = pd.DataFrame(teams.get_teams()).full_name
team_columns = ['TEAM_ID', 'TEAM_CITY', 'TEAM_NAME', 'YEAR', 'GP', 'WINS', 'LOSSES',
       'WIN_PCT', 'CONF_RANK', 'DIV_RANK', 'PO_WINS', 'PO_LOSSES',
       'CONF_COUNT', 'DIV_COUNT', 'NBA_FINALS_APPEARANCE', 'FGM', 'FGA',
       'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA', 'FT_PCT', 'OREB',
       'DREB', 'REB', 'AST', 'PF', 'STL', 'TOV', 'BLK', 'PTS', 'PTS_RANK']
# print(team_options)

teamsdf = api.get('BostonCelticsStats')
print(teamsdf.columns)
# print(x)

# career = api.get('Career')


# START REDIS WITH redis-server

app = dash.Dash(external_stylesheets=[dbc.themes.CERULEAN])

app.layout = dbc.Col(children=[
    html.Hr(),
    html.H1(children= 'NBA DASH'),
    
    html.Hr(),
    dcc.Tabs(id="NBA-DataTabs", value='players', children=[
        dcc.Tab(label='Players', value='players', children = [
            dbc.Row([
                dbc.Col([
                    html.Hr(),
                    html.Label('Choose Players'),
                    dcc.Dropdown(id = 'player_input',value = 'Bam Adebayo',options = player_options,multi=True),
                    html.Label('X Axis'),
                    dcc.Dropdown(id = 'x_axis_input',value = 'SEASON_ID',options = player_columns,multi=False),
                    html.Label('Y Axis'),
                    dcc.Dropdown(id = 'y_axis_input',value = 'REB',options = player_columns, multi=False),
                    html.Label('Color By'),
                    dcc.Dropdown(id = 'colorby_input',value = 'PLAYER_AGE',options = player_columns, multi=False),
                    html.Hr(),

                ],width=2),
                html.Hr(),
                dbc.Col([
                    dcc.Graph(id='config_plot'),
                    html.Hr(),
                    dcc.Graph(id = 'Players_bar_plot')
                    ],width = 10)
            ]),
        ]),
        dcc.Tab(label='Teams', value='teams',children=[
            dbc.Row([
                dbc.Col([
                    html.Hr(),
                    html.Label('Choose Teams'),
                    dcc.Dropdown(id = 'team_input',value = 'Boston Celtics',options = team_options,multi=True),
                    html.Hr(),
                    html.Label('Bar X Axis'),
                    dcc.Dropdown(id = 'x_axis_team',value = 'TEAM_NAME',options = team_columns, multi=False),
                    html.Label('Bar Y Axis'),
                    dcc.Dropdown(id = 'y_axis_team',value = 'WINS',options = team_columns, multi=False),
                    html.Label('Bar Color By'),
                    dcc.Dropdown(id = 'colorby_team',value = 'LOSSES',options = team_columns, multi=False),
                    html.Hr(),
                    html.Label('Line X Axis'),
                    dcc.Dropdown(id = 'x_axis_team_Line',value = 'YEAR',options = team_columns, multi=False),
                    html.Label('Line Y Axis'),
                    dcc.Dropdown(id = 'y_axis_team_Line',value = 'WINS',options = team_columns, multi=False),
                    html.Label('Line Color By'),
                    dcc.Dropdown(id = 'colorby_team_Line',value = 'TEAM_NAME',options = team_columns, multi=False),
                    html.Hr()
                ]),
                dbc.Col([
                    dcc.Graph(id='teams_plot'),
                    html.Hr(),
                    dcc.Graph(id = 'teams_line_plot')
                    ],width = 10)
            ])
        ]),
        # dcc.Tab(label='Games', value='games'),
        dcc.Tab(label='Data', value='data',children = [
            html.Hr(),
            html.Label('Selected Players Data'),
            html.Div(id = 'data_table'),
            html.Hr(),
            html.Label('Selected Teams Data'),
            html.Div(id = 'data_table_teams')
        ]),
    ]),
    
    
    html.Hr(),
    dbc.Row([
        
        
    ]),
    dcc.Store(id = 'players_career_data',storage_type='session'),
    dcc.Store(id = 'teams_data',storage_type='session'),
    

])

@app.callback(
    Output('data_table', 'children'),
    Input('players_career_data','data')
)
def get_data_table(data):
    df = pd.DataFrame(data)
    return dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns],
            style_table={'overflowX': 'scroll','height': 'auto','width': 'auto',},
        )

@app.callback(
    Output('data_table_teams', 'children'),
    Input('teams_data','data')
)
def get_data_table(data):
    df = pd.DataFrame(data)
    return dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns],
            style_table={'overflowX': 'scroll','height': 'auto','width': 'auto',},
        )

@app.callback(
    Output('players_career_data','data'),
    Input('player_input', 'value')
)
def get_season_data(players):
    if players is None:
        raise dash.exceptions.PreventUpdate
    if isinstance(players, list): 
        df_list = []
        for player in players:
            string = player.replace(" ", "") 
            df = api.get(f'{string}Career')
            if df is not None:
                df['PLAYER_NAME'] = player
                print(len(df),player)
                df_list.append(df)
            else:
                print('no data for ',player)
        print(pd.concat(df_list))
        return pd.concat(df_list).to_dict('records')
    else:
        string = players.replace(" ", "") 
        df = api.get(f'{string}Career')
        df['PLAYER_NAME'] = players

        # print(df)
        return df.to_dict('records')

@app.callback(
    Output('teams_data','data'),
    Input('team_input', 'value')
)
def get_teams_data(teams):
    if teams is None:
        raise dash.exceptions.PreventUpdate
    if isinstance(teams, list): 
        df_list = []
        for team in teams:
            string = team.replace(" ", "") 
            df = api.get(f'{string}Stats')
            if df is not None:
                df['TEAM_NAME'] = team
                print(len(df),team)
                df_list.append(df)
            else:
                print('no data for ',team)
        print(pd.concat(df_list))
        return pd.concat(df_list).to_dict('records')
    else:
        string = teams.replace(" ", "") 
        df = api.get(f'{string}Stats')
        df['TEAM_NAME'] = teams

        # print(df)
        return df.to_dict('records')

    


@app.callback(
    Output('config_plot','figure'),
    Input('x_axis_input','value'),
    Input('y_axis_input','value'),
    Input('colorby_input','value'),
    Input('players_career_data','data')
)
def plot_scatter(x_axis,y_axis,color_input,data):
    df = pd.DataFrame(data)
    df = df.sort_values(by=[x_axis, y_axis])
    # print(df)
    if x_axis is None or y_axis is None or color_input is None:
        raise dash.exceptions.PreventUpdate
    fig = px.scatter(df,
        x = x_axis,
        y = y_axis,
        color = color_input,
        title = f'{x_axis} by {y_axis}',
        hover_data = ['PLAYER_NAME']
    )
    return fig


@app.callback(
    Output('Players_bar_plot','figure'),
    Input('x_axis_input','value'),
    Input('y_axis_input','value'),
    Input('colorby_input','value'),
    Input('players_career_data','data')
)
def plot_bar(x_axis,y_axis,color_input,data):
    df = pd.DataFrame(data)
    df = df.sort_values(by=[x_axis, y_axis])
    # print(df)
    if x_axis is None or y_axis is None or color_input is None:
        raise dash.exceptions.PreventUpdate
    fig = px.bar(df,
        x = x_axis,
        y = y_axis,
        color = color_input,
        title = f'{x_axis} by {y_axis}',
        hover_data = ['PLAYER_NAME'],
        barmode='group'
    )
    return fig



@app.callback(
    Output('teams_plot','figure'),
    Input('x_axis_team','value'),
    Input('y_axis_team','value'),
    Input('colorby_team','value'),
    Input('teams_data','data')
)
def plot_scatter(x_axis,y_axis,color_input,data):
    df = pd.DataFrame(data)
    df = df.sort_values(by=[x_axis, y_axis])
    # print(df)
    if x_axis is None or y_axis is None or color_input is None:
        raise dash.exceptions.PreventUpdate
    fig = px.bar(df,
        x = x_axis,
        y = y_axis,
        color = color_input,
        title = f'{x_axis} by {y_axis}',
    )
    return fig

@app.callback(
    Output('teams_line_plot','figure'),
    Input('x_axis_team_Line','value'),
    Input('y_axis_team_Line','value'),
    Input('colorby_team_Line','value'),
    Input('teams_data','data')
)
def plot_scatter(x_axis,y_axis,color_input,data):
    df = pd.DataFrame(data)
    df = df.sort_values(by=[x_axis, y_axis])
    # print(df)
    if x_axis is None or y_axis is None or color_input is None:
        raise dash.exceptions.PreventUpdate
    fig = px.line(df,
        x = x_axis,
        y = y_axis,
        color = color_input,
        title = f'{x_axis} by {y_axis}',
    )
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)