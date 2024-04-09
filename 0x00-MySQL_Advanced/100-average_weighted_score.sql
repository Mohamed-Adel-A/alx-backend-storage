-- SQL script to create a stored procedure ComputeAverageWeightedScoreForUser

-- Procedure to compute and store the average weighted score for a student
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    -- Declare variables to hold total weighted score and total weight
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight INT;
    DECLARE average_weighted_score FLOAT;

    -- Calculate total weighted score and total weight for the user
    SELECT SUM(score * weight), SUM(weight) INTO total_weighted_score, total_weight
    FROM corrections
    JOIN projects ON corrections.project_id = projects.id
    WHERE corrections.user_id = user_id;

    -- Check if total weight is greater than 0 to avoid division by zero
    IF total_weight > 0 THEN
        -- Compute average weighted score
        SET average_weighted_score = total_weighted_score / total_weight;
    ELSE
        SET average_weighted_score = 0;
    END IF;

    -- Update the average weighted score for the user
    UPDATE users
    SET average_score = average_weighted_score
    WHERE id = user_id;
END //

DELIMITER ;
