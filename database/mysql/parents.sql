-- Create the 'parents' table
CREATE TABLE parents (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  student_name VARCHAR(100),
  phone_number VARCHAR(20)
);

-- Insert data into the 'parents' table
INSERT INTO
  parents (name, student_name, phone_number)
VALUES
  ('Hermann Einstein', 'Albert Einstein', '555-1234'),
  ('Pierre Curie', 'Marie Curie', '555-5678'),
  ('Hannah Newton', 'Isaac Newton', '555-8765'),
  ('George Lovelace', 'Ada Lovelace', '555-4321'),
  ('Vincenzo Galilei', 'Galileo Galilei', '555-6789'),
  ('Robert Darwin', 'Charles Darwin', '555-9876'),
  ('Catherine Bohr', 'Niels Bohr', '555-5432'),
  ('Sarah Faraday', 'Michael Faraday', '555-6543'),
  (
    'Margaret Maxwell',
    'James Clerk Maxwell',
    '555-3210'
  ),
  ('Milena Tesla', 'Nikola Tesla', '555-1357'),
  ('Sara Turing', 'Alan Turing', '555-2468'),
  ('Arthur Feynman', 'Richard Feynman', '555-3579'),
  (
    'Edward Franklin',
    'Rosalind Franklin',
    '555-4680'
  ),
  ('Jane Hawking', 'Stephen Hawking', '555-5791'),
  (
    'Kurt von Neumann',
    'John von Neumann',
    '555-6802'
  );
