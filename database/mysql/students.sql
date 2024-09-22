-- Create the 'students' table
CREATE TABLE students (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100),
  exam_score INT,
  scoring_reason VARCHAR(255)
);

-- Insert 15 students with random names, scores, and reasons
INSERT INTO
  students (name, exam_score, scoring_reason)
VALUES
  (
    'Albert Einstein',
    95,
    'Outstanding performance in the exam.'
  ),
  (
    'Marie Curie',
    89,
    'Excellent understanding of the material.'
  ),
  (
    'Isaac Newton',
    76,
    'Good performance, but room for improvement.'
  ),
  (
    'Ada Lovelace',
    82,
    'Strong performance with good analytical skills.'
  ),
  (
    'Galileo Galilei',
    91,
    'Exceptional knowledge and problem-solving skills.'
  ),
  (
    'Charles Darwin',
    87,
    'Very good performance with minor errors.'
  ),
  (
    'Niels Bohr',
    93,
    'High level of understanding and application of concepts.'
  ),
  (
    'Michael Faraday',
    78,
    'Solid performance, but needs more focus on details.'
  ),
  (
    'James Clerk Maxwell',
    85,
    'Good grasp of the material with few mistakes.'
  ),
  (
    'Nikola Tesla',
    90,
    'Excellent performance and innovative approach.'
  ),
  (
    'Alan Turing',
    80,
    'Good performance with some areas for improvement.'
  ),
  (
    'Richard Feynman',
    77,
    'Competent understanding, needs more practice.'
  ),
  (
    'Rosalind Franklin',
    84,
    'Strong performance, but could benefit from review.'
  ),
  (
    'Stephen Hawking',
    92,
    'Exceptional performance with deep understanding.'
  ),
  (
    'John von Neumann',
    0,
    'Missed the exam due to illness.'
  );
