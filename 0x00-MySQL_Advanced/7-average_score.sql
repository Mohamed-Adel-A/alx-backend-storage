-- SQL script to create a stored procedure ComputeAverageScoreForUser

-- Procedure to compute and store the average score for a student
DELIMITER //

CREATE PROCEDURE ComputeAverageScoreForUser(IN user_id INT)
BEGIN
    -- Declare variables to hold total score and total projects
    DECLARE total_score FLOAT;
    DECLARE total_projects INT;
    DECLARE average_score FLOAT;

    -- Calculate total score and total projects for the user
    SELECT SUM(score), COUNT(*) INTO total_score, total_projects
    FROM corrections
    WHERE user_id = user_id;

    -- Check if total projects is greater than 0 to avoid division by zero
    IF total_projects > 0 THEN
        -- Compute average score
        SET average_score = total_score / total_projects;
    ELSE
        SET average_score = 0;
    END IF;

    -- Update the average score for the user
    UPDATE users
    SET average_score = average_score
    WHERE id = user_id;
END //

DELIMITER ;
