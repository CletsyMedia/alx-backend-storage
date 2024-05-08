-- Drop the users table if it already exists
DROP TABLE IF EXISTS users;

-- Create the users table if it doesn't exist
CREATE TABLE IF NOT EXISTS users (
    -- Define the id column as an integer, auto-incremented, and not nullable
    id INT NOT NULL AUTO_INCREMENT,
    -- Define the email column as a string with a maximum length of 255 characters, not nullable
    email VARCHAR(255) NOT NULL,
    -- Define the name column as a string with a maximum length of 255 characters
    name VARCHAR(255),
    -- Define the valid_email column as a boolean (0 or 1) and not nullable with a default value of 0
    valid_email BOOLEAN NOT NULL DEFAULT 0,
    -- Define the primary key constraint for the id column
    PRIMARY KEY (id)
);

-- Insert sample data into the users table
INSERT INTO users (email, name) VALUES ("bob@dylan.com", "Bob");
INSERT INTO users (email, name, valid_email) VALUES ("sylvie@dylan.com", "Sylvie", 1);
INSERT INTO users (email, name, valid_email) VALUES ("jeanne@dylan.com", "Jeanne", 1);

