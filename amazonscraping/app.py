from flask import Flask, render_template
import psycopg2
import psycopg2.extras

app = Flask(__name__)

app.config['DEBUG'] = True

#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://testuser:postgres@localhost/booksdb'

@app.route('/')
def display_books():
    # Connect to the database
    conn = psycopg2.connect(
        host="localhost",
        user="testuser",
        password="postgres",
        dbname="booksdb"
    )

    # Create a cursor
    curr = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # Execute a SELECT query to retrieve the data from the books_tb table
    curr.execute("SELECT * FROM books_tb")

    # Fetch the results of the query
    results = curr.fetchall()

    # Close the cursor and connection
    curr.close()
    conn.close()

    # Render the template and pass the data as a variable
    return render_template('books.html', books=results)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)