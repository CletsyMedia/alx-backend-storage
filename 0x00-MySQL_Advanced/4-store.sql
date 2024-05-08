-- Create a trigger named decrease_quantity
CREATE TRIGGER decrease_quantity

-- Trigger fires after an insertion into the orders table
AFTER INSERT ON orders

-- For each row inserted into the orders table
FOR EACH ROW

-- Update the items table
UPDATE items

-- Subtract the quantity of the item in the orders table from the quantity in the items table
SET quantity = quantity - NEW.number

-- Update only the rows where the item name matches the new item_name inserted in the orders table
WHERE name = NEW.item_name;

