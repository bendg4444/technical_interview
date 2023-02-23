import pandas as pd
import psycopg2
import psycopg2.extras


def get_db_connection() -> psycopg2.extensions.connection:
    """Create a connection for database postgres"""
    DB_USER = 'vxygirtn'
    DB_PASSWORD = 'RguWG24fx16sgqY-h2YwD1zMdegyjWkf'
    DB_HOST = 'trumpet.db.elephantsql.com'
    DB_NAME = 'vxygirtn'

    try:
        conn = psycopg2.connect(f"""
        dbname={DB_NAME}
        user={DB_USER} 
        password={DB_PASSWORD}
        host={DB_HOST}""")
        return conn
    except:
        print("Error connecting to database.")


def query_executer(
    conn: psycopg2.extensions.connection, query: str, params: tuple = ()
) -> list:
    """An executor function for executing sql statements"""
    if conn != None:
        with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
            cur.execute(query, params)
            conn.commit()
            try:
                returned_data = cur.fetchall()
                return returned_data
            except:
                pass
    else:
        return "No connection"


def drop_untitled_artwork(data: pd.DataFrame) -> pd.DataFrame:
    """Function to drop the titles with 'Untitled' in the title"""
    return data[~(data['title'].str.contains('Untitled'))]


def filter_by_department(data: pd.DataFrame, department: str) -> pd.DataFrame:
    """Given a department, filter the dataframe to return results only from that department"""
    filtered_data = data[data['department'] == department]

    return filtered_data


def filter_completed_work_by_date_range(data: pd.DataFrame, start_year: int, end_year: int) -> pd.DataFrame:
    """Given a start and end year, filter the data for completed work using these ranges"""
    filtered_data = data[(data['year_completed'] >= start_year) & (
        data['year_completed'] <= end_year)]

    return filtered_data


def get_the_number_of_artworks(data: pd.DataFrame) -> int:
    """Function to make return number of artworks available"""
    return len(data)


def get_artists_gender_demographics(data: pd.DataFrame) -> pd.DataFrame:
    """Get the breakdown of artists gender demographics for given data"""
    # drop duplicate values for artists
    processed = data.drop_duplicates(subset=['artist_id'])
    gender_demographics = processed.groupby('gender').count().reset_index()
    gender_demographics['count'] = gender_demographics['artwork_id']

    return gender_demographics[['gender', 'count']]


def get_artists_nationality_demographics(data: pd.DataFrame) -> pd.DataFrame:
    """Returns a data frame with artists nationality distribution"""
    # drop duplicate artists values
    processed = data.drop_duplicates(subset=['artist_id'])
    nationality_demographics = processed.groupby(
        'nationality').count().reset_index()
    nationality_demographics['count'] = nationality_demographics['artwork_id']

    return nationality_demographics[['nationality', 'count']]
