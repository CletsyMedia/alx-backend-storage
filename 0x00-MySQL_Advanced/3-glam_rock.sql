-- List all bands with Glam rock as their main style, ranked by their longevity

-- Select band_name and calculate lifespan
SELECT band_name, 
       (IFNULL(split, '2022') - formed) AS lifespan
       
-- From the metal_bands table
FROM metal_bands

-- Filter bands with Glam rock as their main style
WHERE style LIKE '%Glam rock%'

-- Order the results by lifespan in descending order
ORDER BY lifespan DESC;

