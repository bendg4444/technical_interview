import dash
import dash_bootstrap_components as dbc
import pandas as pd
import psycopg2
import psycopg2.extras
import warnings
import plotly.express as px
from dotenv import load_dotenv
from dash import html, dcc, Dash,  Output, Input
from utils import get_db_connection, get_artists_gender_demographics, \
    get_artists_nationality_demographics, get_the_number_of_artworks, \
    drop_untitled_artwork, filter_by_department, filter_completed_work_by_date_range \
   
warnings.filterwarnings('ignore')

# Create database connection, get get data
# conn = get_db_connection()
# sql = """SELECT * FROM artwork 
#             JOIN artist 
#                 ON artwork.artist_id = artist.artist_id"""

# data = pd.read_sql(sql, conn)


def create_gender_graph(data: pd.DataFrame) -> px.bar:
    """Creates a graph for the gender aggregates for data"""
    plot_data = {"gender": list(data['gender']), "count":list(data['count'])}
    fig = px.bar(plot_data, title="Artists Gender Distribution",
                 x="gender", y="count", color = "gender", 
                 labels ={
                    "gender":"Gender",
                    "count":"Count"
                 })
    fig.update_layout(
        font=dict(
            size=18
        ),
        title_x=0.5
    )
    return fig

def create_nationality_graph(data: pd.DataFrame) -> px.bar:
    """Creates a graph for nationalities count for given data set"""
    plot_data = {"nationality": list(data['nationality']), "count":list(data['count'])}
    fig = px.bar(plot_data, title="Artists Nationality Distribution",
                 x="nationality", y="count", color = "nationality", 
                 labels ={
                    "nationality":"Nationality",
                    "count":"Count"
                 })
    fig.update_layout(
        font=dict(
            size=18
        ),
        title_x=0.5
    )
    
    return fig


data = pd.read_csv('./art_data.csv')

#removes duplicates
data = data[data.duplicated() == False ]

app = Dash(__name__, external_stylesheets=[
           dbc.themes.ZEPHYR], use_pages=True)
app.layout = html.Div(dash.page_container)


@app.callback(
    [  
        Output(component_id="num-of-artworks", component_property="children"),
        Output(component_id="gender-graph", component_property="figure"),
        Output(component_id="nationality-graph", component_property="figure"),
        Output(component_id="descriptive-string", component_property="children"),
        Output(component_id="error-warning", component_property="children")
    ],
    [
        Input(component_id="department-dropdown", component_property="value"),
        Input(component_id="year-start", component_property="value"),
        Input(component_id="year-end", component_property="value"),

    ]
)
def output_data(department: str, start_year: int, end_year: int):
    """Function to take in the inputs from the user and update the dashboard"""
    
    processed_data = drop_untitled_artwork(data)

    error_warning = ""
    if end_year < start_year:
        error_warning = "Error: end year should not be greater than start"

    if department != "All":

        filtered_data = filter_by_department(processed_data, department)
        filtered_data = filter_completed_work_by_date_range(filtered_data, start_year, end_year)

        num_of_artworks = get_the_number_of_artworks(filtered_data)
        description_string =  f"""The results are for: {department} from {start_year} - {end_year}"""

    else:
        filtered_data = filter_completed_work_by_date_range(processed_data, start_year, end_year)
        num_of_artworks = get_the_number_of_artworks(filtered_data)
        description_string =  f"""The results are for: All departments from {start_year} - {end_year}"""
    
    num_artworks_string = f"Number of artworks for given constraints: {num_of_artworks}" 

    # create gender graph 
    artist_gender_demographics = get_artists_gender_demographics(filtered_data)
    gender_fig = create_gender_graph(artist_gender_demographics)

    # create nationality graph
    artist_nationality_demographics = get_artists_nationality_demographics(filtered_data)
    nationality_fig = create_nationality_graph(artist_nationality_demographics)

    return num_artworks_string , gender_fig, nationality_fig, description_string, error_warning


if __name__ == "__main__":
    app.run_server(host="0.0.0.0", debug=True, port=8080)