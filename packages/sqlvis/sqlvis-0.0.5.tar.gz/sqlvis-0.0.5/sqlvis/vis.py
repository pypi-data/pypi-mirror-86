from IPython.display import display, Javascript, HTML
import json
import os 
import pandas as pd
import time
dir_path = os.path.dirname(os.path.realpath(__file__))



def schema_from_conn(conn):
    schema = {}
    tableQuery= """SELECT name FROM sqlite_master WHERE type ='table' AND name NOT LIKE 'sqlite_%';"""
    tables = pd.read_sql_query(tableQuery, conn)['name']

    for i in tables:
        headerQuery = "select * from "+i+" where 1=2"
        headers = list(pd.read_sql_query(headerQuery, conn))
        schema[i] = headers

    return schema

def visualize(s, schema):
    display(Javascript("""
        require.config({
            paths: {
                d3: 'https://d3js.org/d3.v5.min'
            }
        });
    """))

    display(HTML(filename= dir_path + '/styles.css.html'))
    display(Javascript(filename= dir_path + '/visualize.js'))

    #First, escape all quotation marks.
    query = s.replace("'", "\\'")
    query = query.replace('\n', ' ')
    query = query.replace('\r', ' ')
    query = query.replace('\s+', ' ')
    
    shortSchema = json.dumps(schema)

    command = """
        (function(element) {{
            var query = '{0}';
            var schema = {1};

            require(['viz'], function(viz) {{
                viz(element.get(0), query, schema)
            }});
        }})(element);
        """.format(query, shortSchema)

    return display(Javascript(command))