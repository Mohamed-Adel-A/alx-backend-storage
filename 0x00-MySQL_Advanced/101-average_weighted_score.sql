-- SQL script to create a stored procedure ComputeAverageWeightedScoreForUsers

-- Procedure to compute and store the average weighted score for all students
DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    -- Declare variables for cursor and user id
    DECLARE done INT DEFAULT FALSE;
    DECLARE user_id INT;

    -- Declare cursor for selecting all user ids
    DECLARE users_cursor CURSOR FOR
    SELECT id FROM users;

    -- Declare continue handler for cursor
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    -- Open cursor
    OPEN users_cursor;

    -- Loop through all user ids
    users_loop: LOOP
        -- Fetch user id from cursor
        FETCH users_cursor INTO user_id;

        -- Check if done
        IF done THEN
            LEAVE users_loop;
        END IF;

        -- Call procedure to compute average weighted score for the user
        CALL ComputeAverageWeightedScoreForUser(user_id);
    END LOOP;

    -- Close cursor
    CLOSE users_cursor;
END //

DELIMITER ;
