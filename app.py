from dotenv import load_dotenv
load_dotenv() # load all the environment variables

import streamlit as st
import os
import sqlite3

from openai import OpenAI

# Configure API key
api_key = os.getenv('OPENAI_API_KEY')
client = OpenAI(api_key=api_key)

def read_schema(db):
    conn = sqlite3.connect(db)
    cursor = conn.cursor()

    cursor.execute('SELECT name FROM sqlite_master WHERE type = "table";')
    tables = cursor.fetchall()

    schema_info = {}

    for table_name in tables:
        table_name = table_name[0]
        cursor.execute(f'PRAGMA table_info({table_name});')
        columns = cursor.fetchall()

        # Store column details
        # schema_info[table_name] = [{'name': col[1], 'type': col[2], 'notnull': col[3], 'default_value': col[4], 'primary_key': col[5]} for col in columns]
        schema_info[table_name] = [{'name': col[1], 'type': col[2]} for col in columns]
    # Close the connection
    cursor.close()
    conn.close()

    return schema_info


def sum_schema(raw_schema):
    """
    Given a schema, sumamrize and translate the details so that sql_agent would understand
    """

    sum_instruction = """
    You are an agent designed to communicate with users. You job is to understand a given schema, and add details to each column of each table.
    """

    def docstring_parameter(*sub):
        def dec(obj):
            obj.__doc__ = obj.__doc__.format(*sub)
            return obj
        return dec

    @docstring_parameter(raw_schema)
    def sum_question():
        '''I need you to write a detailed summary about the provided schema below. 
        Please add one sentence to each column of each table about what this column means.
        Below is the schema: {0}
        '''
        pass

    sum_follow_up = """
    please summarize your previous response with each column's name and type for a sql query expert assistant, which is a large language model, so that it would understand the schema clearly. Skip all unnecessary words, just return the summary.
    """

    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": sum_instruction},
        {"role": "user", "content": sum_question.__doc__},
        {"role": "user", "content": sum_follow_up}

    ]
    )

    return completion.choices[0].message.content

# Load openai model and provide sql query as response
def get_response(question, instruction):
    """
    Given a question, 
    """
    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": instruction},
        {"role": "user", "content": question}
    ]
    )

    return completion.choices[0].message.content

def read_sql_query(sql, db):
    """
    Use the returned query to retrieve data from database
    """
    conn = sqlite3.connect(db)
    cur = conn.cursor()
    cur.execute(sql)
    rows = cur.fetchall()
    conn.commit()
    conn.close()

    for row in rows:
        print(row)
    return rows

raw_schema = read_schema('data/ecommerce.db')

schema = sum_schema(raw_schema)
#### add schema into prompt


# Streamlit App
st.set_page_config(page_title='Ask me anything about NBA')
st.header('ChatGPT App to Retrieve SQL Data')

question = st.text_input('Input: ', key='input')

submit = st.button('Ask me!')

def docstring_parameter(*sub):
    def dec(obj):
        obj.__doc__ = obj.__doc__.format(*sub)
        return obj
    return dec

@docstring_parameter(schema)
def sql_instruction():
    """You are an expert in converting English questions to SQL query!
    Please familiarize yourself with below schema, and return only a SQL query, and avoid returning any unnecessary words.
    For example: question: "How many leads qualified are there in total?" You should return "SELECT COUNT(DISTINCT mql_id) FROM leads_qualified;"
    also the sql code should not have ``` in beginning or end and 'sql' word in output
    Below is the schema: {0} 
    """
    pass

# if submit is clicked
if submit:
    response = get_response(question, sql_instruction.__doc__)
    print(response)
    data = read_sql_query(response, 'data/ecommerce.db')
    st.subheader(response, 'The response is:')
    for row in data:
        print(row)
        st.header(row)