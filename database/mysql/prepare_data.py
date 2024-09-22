import mysql.connector
from mysql.connector import Error

# Configuration for MySQL connection
config = {
    "user": "langchain",
    "password": "langchain",
    "host": "mysql",
    "database": "langchain",
}

# SQL queries to create and populate tables
create_students_table = """
CREATE TABLE IF NOT EXISTS students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    exam_score INT,
    scoring_reason VARCHAR(255)
);
"""

insert_students_data = """
INSERT INTO students (name, exam_score, scoring_reason) VALUES
('Albert Einstein', 95, 'Outstanding performance in the exam.'),
('Marie Curie', 89, 'Excellent understanding of the material.'),
('Isaac Newton', 76, 'Good performance, but room for improvement.'),
('Ada Lovelace', 82, 'Strong performance with good analytical skills.'),
('Galileo Galilei', 91, 'Exceptional knowledge and problem-solving skills.'),
('Charles Darwin', 87, 'Very good performance with minor errors.'),
('Niels Bohr', 93, 'High level of understanding and application of concepts.'),
('Michael Faraday', 78, 'Solid performance, but needs more focus on details.'),
('James Clerk Maxwell', 85, 'Good grasp of the material with few mistakes.'),
('Nikola Tesla', 90, 'Excellent performance and innovative approach.'),
('Alan Turing', 80, 'Good performance with some areas for improvement.'),
('Richard Feynman', 77, 'Competent understanding, needs more practice.'),
('Rosalind Franklin', 84, 'Strong performance, but could benefit from review.'),
('Stephen Hawking', 92, 'Exceptional performance with deep understanding.'),
('John von Neumann', 0, 'Missed the exam due to illness.');
"""

create_parents_table = """
CREATE TABLE IF NOT EXISTS parents (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    student_name VARCHAR(100),
    phone_number VARCHAR(20)
);
"""

insert_parents_data = """
INSERT INTO parents (name, student_name, phone_number) VALUES
('Hermann Einstein', 'Albert Einstein', '555-1234'),
('Pierre Curie', 'Marie Curie', '555-5678'),
('Hannah Newton', 'Isaac Newton', '555-8765'),
('George Lovelace', 'Ada Lovelace', '555-4321'),
('Vincenzo Galilei', 'Galileo Galilei', '555-6789'),
('Robert Darwin', 'Charles Darwin', '555-9876'),
('Catherine Bohr', 'Niels Bohr', '555-5432'),
('Sarah Faraday', 'Michael Faraday', '555-6543'),
('Margaret Maxwell', 'James Clerk Maxwell', '555-3210'),
('Milena Tesla', 'Nikola Tesla', '555-1357'),
('Sara Turing', 'Alan Turing', '555-2468'),
('Arthur Feynman', 'Richard Feynman', '555-3579'),
('Edward Franklin', 'Rosalind Franklin', '555-4680'),
('Jane Hawking', 'Stephen Hawking', '555-5791'),
('Kurt von Neumann', 'John von Neumann', '555-6802');
"""


def execute_query(connection, query):
    """Execute a single query."""
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully.")
    except Error as e:
        print(f"Error: {e}")
    finally:
        cursor.close()


def main():
    try:
        # Establish the connection
        connection = mysql.connector.connect(**config)

        if connection.is_connected():
            print("Connected to MySQL database.")

            # Execute SQL queries
            execute_query(connection, create_students_table)
            execute_query(connection, insert_students_data)
            execute_query(connection, create_parents_table)
            execute_query(connection, insert_parents_data)

    except Error as e:
        print(f"Error: {e}")
    finally:
        if connection.is_connected():
            connection.close()
            print("MySQL connection is closed.")


if __name__ == "__main__":
    main()
