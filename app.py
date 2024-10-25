from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import sqlite3
import random

app = Flask(__name__)
CORS(app)  # Allow Cross-Origin Resource Sharing

# Function to create the agencies table if it doesn't exist
def create_table():
    # Make sure we are using 'agencies_modified.db' as per your project details
    conn = sqlite3.connect('agencies_modified.db')  # Correct database name
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS agencies (
            id INTEGER PRIMARY KEY,
            factory_name TEXT NOT NULL,
            agent_name TEXT NOT NULL,
            workers_name TEXT NOT NULL,
            workers_in_muse INTEGER NOT NULL,
            workers_in_china INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Call the function to create the table when the app starts
create_table()

# Function to fetch agency data from the database by ID
def get_agency_by_id(agency_id):
    conn = sqlite3.connect('agencies_modified.db')  # Use the correct database
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM agencies WHERE id=?', (agency_id,))
    agency = cursor.fetchone()
    conn.close()
    return agency

# Function to generate a unique 6-digit ID
def generate_unique_id():
    while True:
        random_id = random.randint(100000, 999999)  # Generate 6-digit ID
        if not get_agency_by_id(random_id):  # Check if ID is unique
            return random_id

# Route to search for an agency by ID
@app.route('/search', methods=['GET'])
def search_agency():
    agency_id = request.args.get('id')
    if not agency_id:
        return jsonify({'error': 'No agency ID provided'}), 400

    agency = get_agency_by_id(agency_id)

    if agency:
        agency_data = {
            'id': agency[0],
            'factory_name': agency[1],
            'agent_name': agency[2],
            'workers_name': agency[3],
            'workers_in_muse': agency[4],
            'workers_in_china': agency[5],
        }
        return jsonify(agency_data), 200
    else:
        return jsonify({'error': 'Agency not found'}), 404

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# Route to add agency data
@app.route('/add_agency', methods=['POST'])
def add_agency():
    data = request.form
    factory_name = data.get('factory_name')
    agent_name = data.get('agent_name')
    workers_name = data.get('workers_name')
    workers_in_muse = data.get('workers_in_muse')
    workers_in_china = data.get('workers_in_china')

    # Generate a unique 6-digit ID
    agency_id = generate_unique_id()

    # Connect to the correct database
    conn = sqlite3.connect('agencies_modified.db')  # Correct database name
    c = conn.cursor()

    # Insert the new agency data into the database with the generated ID
    c.execute('''
        INSERT INTO agencies (id, factory_name, agent_name, workers_name, workers_in_muse, workers_in_china)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (agency_id, factory_name, agent_name, workers_name, workers_in_muse, workers_in_china))

    # Commit changes and close the connection
    conn.commit()
    conn.close()

    return jsonify({'message': 'Agency added successfully', 'id': agency_id}), 201

if __name__ == "__main__":
    app.run(debug=True)
