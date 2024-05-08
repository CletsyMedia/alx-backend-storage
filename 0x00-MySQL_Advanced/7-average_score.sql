-- Define the delimiter to $$
DELIMITER $$

-- Drop the procedure if it already exists
DROP PROCEDURE IF EXISTS ComputeAverageScoreForUser;

-- Create the procedure ComputeAverageScoreForUser
CREATE PROCEDURE ComputeAverageScoreForUser(IN `user_id` INT)
BEGIN
    -- Update the users table to set the average_score column
    UPDATE users
    -- Set the average_score to the average score calculated from the corrections table for the given user_id
    SET average_score = (SELECT AVG(score)
                         FROM corrections
                         WHERE corrections.user_id = user_id)
    -- Where the id matches the given user_id
    WHERE id = user_id;
END $$

-- Reset the delimiter to ;
DELIMITER ;

