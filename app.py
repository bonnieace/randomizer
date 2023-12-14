from flask import Flask, request, render_template, jsonify
import random
import string
import sqlite3
from faker import Faker

app = Flask(__name__)

# Function to create a Faker object
def create_faker():
    return Faker()

# Function to generate a random name using Faker
def generate_random_name(faker):
    return faker.first_name().lower()

# Function to generate a random ID number
def generate_random_id():
    return ''.join(random.choice(string.digits) for i in range(8))

# Function to generate a random sub-county
def generate_random_sub_county():
    sub_counties = ['kiambu', 'nairobi', 'mombasa', 'kisumu', 'eldoret']
    return random.choice(sub_counties)

# Function to create the 'people' table if it doesn't exist
def create_people_table():
    conn = sqlite3.connect('weekend_event.db')
    c = conn.cursor()

    c.execute('''
        CREATE TABLE IF NOT EXISTS people (
            id INTEGER PRIMARY KEY,
            name TEXT,
            id_number TEXT,
            sub_county TEXT,
            is_selected INTEGER,
            weekend_num INTEGER
        )
    ''')

    conn.commit()
    conn.close()

# Function to fill the database with dummy data
def fill_database_with_dummy_data(num_entries):
    conn = sqlite3.connect('weekend_event.db')
    c = conn.cursor()

    for i in range(num_entries):
        # Create a Faker object
        faker = create_faker()

        # Generate a random name
        name = generate_random_name(faker)
        id_number = generate_random_id()
        sub_county = generate_random_sub_county()

        # Insert the data into the database and set is_selected and weekend_num to 0
        c.execute('INSERT INTO people (name, id_number, sub_county, is_selected, weekend_num) VALUES (?, ?, ?, ?, ?)',
                  (name, id_number, sub_county, 0, 0))

    conn.commit()
    conn.close()


# Check if the 'people' table exists, and create it if not
create_people_table()

# Fill the database with 20 dummy entries
fill_database_with_dummy_data(20)



# Route to handle form submission
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data['name']
    id_number = data['id_number']
    sub_county = data['sub_county']

    # Connect to the SQLite database
    conn = sqlite3.connect('weekend_event.db')
    c = conn.cursor()

    # Insert the user input into the database
    c.execute('INSERT INTO people (name, id_number, sub_county, is_selected, weekend_num) VALUES (?, ?, ?, ?, ?)',
              (name, id_number, sub_county, 0, 0))

    # Commit the changes
    conn.commit()
    conn.close()

    return jsonify({'message': 'Registration successful'}), 200





# Route to serve the index.html file
@app.route('/')
def index():
    return render_template('index.html')
selected_referees_by_weekend={}
# ... (Existing code as before)

# Route to display the weekend selection page
@app.route('/weekend_selection', methods=['GET'])
def weekend_selection():
    return render_template('weekend_selection.html')

# Route to handle weekend selection form submissions
@app.route('/weekend_selection', methods=['POST'])
def handle_weekend_selection():
    data = request.form
    weekend_num = int(data['weekend_num'])

    # Connect to the SQLite database
    conn = sqlite3.connect('weekend_event.db')
    c = conn.cursor()

    # Fetch all the names from the database
    c.execute('SELECT name FROM people')
    all_names = [row[0] for row in c.fetchall()]

    # Check if there are still unselected referees for the current weekend
    if weekend_num in selected_referees_by_weekend and len(selected_referees_by_weekend[weekend_num]) >= len(all_names):
        conn.close()
        return jsonify({'message': 'All referees for this weekend have been selected'}), 400

    # Fetch the names of referees already selected for the current weekend
    selected_referees = set(selected_referees_by_weekend.get(weekend_num, []))

    # Calculate the list of remaining unselected referees for the current weekend
    remaining_referees = list(set(all_names) - selected_referees)

    # If all referees have been selected for this weekend, return an error response
    if not remaining_referees:
        conn.close()
        return jsonify({'message': 'All referees for this weekend have been selected'}), 400

    # Randomly select one referee from the remaining unselected referees
    selected_referee = random.choice(remaining_referees)

    # Update the 'weekend_num' for the selected referee in the database
    c.execute('UPDATE people SET weekend_num = ? WHERE name = ?', (weekend_num, selected_referee))

    # Commit the changes
    conn.commit()
    conn.close()

    # Update the selected_referees_by_weekend dictionary
    if weekend_num not in selected_referees_by_weekend:
        selected_referees_by_weekend[weekend_num] = []
    selected_referees_by_weekend[weekend_num].append(selected_referee)

    return jsonify({'message': f'Weekend {weekend_num} selection successful', 'selected_referee': selected_referee}), 200
if __name__ == '__main__':
    app.run(debug=True)