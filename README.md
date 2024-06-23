# SQL Agent
SQL Agent using ChatGPT-4o

This project is to build a SQL agent which could translate any input questions into SQL queries. Then the queries could retrieve data from a SQLite database, and answer questions by providing the queries and the answers. 

### Installation

To set up and run this application, follow these steps:

1. Clone the repository
```
git clone [repository-url]
cd [repository-directory]
```
2. Install dependencies
```
pip install -r requirements.txt
```
3. Set up environment variables:
```
OPEN_AI_KEY = 'Your-OpenAI-API-Key'
```

### Usage
To run the application:
```
streamlit run app.py
```

### Database
Users could follow the sql.md to build their databases using .sql files. The app.py uses prompts engineering to understand the schema of the dataset, so that the SQL agent understands the schema, hence answering questions regarding the data.

### Future Enhancements
Expand Database Support: Incorporate support for additional database types.
Enhanced Query Optimization: Implement more complex query optimization techniques.
Enhanced Explanation Capability: Implement prompt engineering to further breakdown the thought process.
User Authentication: Add user management and authentication for enhanced security.
