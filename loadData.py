import mysql.connector
import random

# Create random data to input into healthcare table
first_names_boy = ["Austin", "Seth", "David", "Liam", "Noah", "Oliver", "Theodore", "James", "Henry", "Matthew", "Elijah", "Lucas", "William"]
first_names_girl = ["Olivia", "Emma", "Amelia", "Charlotte", "Mia", "Sophia", "Isabella", "Evelyn", "Ava", "Mary", "Linda", "Jennifer"]
last_names = ["Joseph", "Opatz", "Tinley", "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Lopez", "Wilson", 
              "Anderson", "Thomas", "Moore", "Jackson", "Martin", "Lee", "Thompson", "White", "Harris", "Clark", "Lewis"]
health_issues = [
    "No significant medical history",
    "Asthma",
    "Diabetes",
    "High blood pressure",
    "Allergies",
    "Migraines",
    "Heart murmur",
    "Recent surgery",
    "Anxiety",
    "Depression",
    "Arrhythmia"
]

# Connect to DB
conn = mysql.connector.connect(
    host="dsp-mysqldatabase.chogg206kt6s.us-east-2.rds.amazonaws.com",
    user="admin",
    password="Kent2025",
    database="DSP_Database",
    port=3306
)

cur = conn.cursor()

# Create query string that creates the healthcare table
create_table_query = """
CREATE TABLE IF NOT EXISTS healthcare (
    id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    gender BOOLEAN,
    age INT,
    weight FLOAT,
    height FLOAT,
    health_history TEXT
);
"""
# Run the query for table creation to create the healthcare table
cur.execute(create_table_query)
conn.commit()

print("Table 'healthcare' created successfully.")


# Create query string for loading the table with no values in it yet
insert_query = """
INSERT INTO healthcare (first_name, last_name, gender, age, weight, height, health_history)
VALUES (%s, %s, %s, %s, %s, %s, %s)
"""

for i in range(100):
    # Create random data for each field
    gender = random.choice([0, 1])  # 0 = female, 1 = male
    if gender == 0:
        first = random.choice(first_names_girl)
    else:
        first = random.choice(first_names_boy)
    last = random.choice(last_names)
    age = random.randint(1, 100)
    weight = round(random.uniform(90, 250), 1)   # random weight in lbs
    height = round(random.uniform(4.0, 7.0), 2)  # random height in feet
    history = random.choice(health_issues)
    # Add random data to table row
    cur.execute(insert_query, (first, last, gender, age, weight, height, history))

conn.commit()
print("Inserted 100 random healthcare records.")

cur.close()
conn.close()
