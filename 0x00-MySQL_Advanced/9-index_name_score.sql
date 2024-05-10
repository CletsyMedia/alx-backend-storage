--Creates an idx_name_first_score on a table

CREATE INDEX idx_name_first_score
ON names(name(1), score);
