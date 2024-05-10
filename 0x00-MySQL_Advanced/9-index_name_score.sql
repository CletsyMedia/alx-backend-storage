--Creates an idx name first score on a table
CREATE INDEX idx_name_first_score
--Target the first letter of name and the score
ON names(name(1), score);

