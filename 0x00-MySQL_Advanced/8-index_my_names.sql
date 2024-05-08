-- Create an index named idx_name_first
CREATE INDEX idx_name_first
-- On the names table, indexing the first character of the name column
ON names(name(1));

