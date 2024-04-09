-- Lists all bands with Glam rock as their main style, ranked by their longevity
SELECT band_name, 
       DATEDIFF('2022-01-01', STR_TO_DATE(SUBSTRING_INDEX(lifespan, '-', 1), '%Y')) AS lifespan
FROM metal_bands
WHERE style = 'Glam rock'
ORDER BY lifespan DESC;
