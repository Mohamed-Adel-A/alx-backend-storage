-- Creates a stored procedure ComputeAverageWeightedScoreForUsers that
-- computes and stores the average weighted score for all students.
DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUsers;
DELIMITER $$
CREATE PROCEDURE ComputeAverageWeightedScoreForUsers ()
BEGIN
    ALTER TABLE users ADD total_weighted_score FLOAT;
    ALTER TABLE users ADD total_weight FLOAT;

    UPDATE users
        SET total_weighted_score = (
            SELECT SUM(corrections.score * projects.weight)
            FROM corrections
                INNER JOIN projects ON corrections.project_id = projects.id
            WHERE corrections.user_id = users.id
        );

    UPDATE users
        SET total_weight = (
            SELECT SUM(projects.weight)
            FROM corrections
                INNER JOIN projects ON corrections.project_id = projects.id
            WHERE corrections.user_id = users.id
        );

    UPDATE users
        SET users.average_score = IF(total_weight = 0, 0, total_weighted_score / total_weight);

    ALTER TABLE users DROP COLUMN total_weighted_score;
    ALTER TABLE users DROP COLUMN total_weight;
END $$
DELIMITER ;
