-- Spatial
SELECT 
	DISTINCT ON (regbl."EGID")
	CONCAT(regbl."GDEKT", regbl."EGID") AS fid,
	footprint.geom AS geometry,
	1 AS ds_id,
	ST_Area(footprint.geom) AS surface,
	regbl."EGID" AS egid, 
	regbl."GDEKT" AS canton, 
	regbl."GGDENAME" AS commune,
	footprint."UUID" AS uuid
FROM 
	public.all_buildings as footprint
JOIN
	public.all_regbl as regbl
ON
	ST_Intersects(regbl.geom, footprint.geom)
WHERE
	ST_Area(footprint.geom) > 20
LIMIT 10


-- REGBL
CREATE TABLE only_regbl AS
SELECT *
FROM 
	public.all_regbl AS regbl
WHERE regbl."GDEKT"='BE' 
	OR regbl."GDEKT"='GE'
	OR regbl."GDEKT"='GE' 
	OR regbl."GDEKT"='JU' 
	OR regbl."GDEKT"='NE' 
	OR regbl."GDEKT"='FR' 
	OR regbl."GDEKT"='VD' 
	OR regbl."GDEKT"='VS' 
	
-- FOOTPRINT
CREATE TABLE only_buildings AS
SELECT *
FROM 
	public.all_buildings as footprint
WHERE ST_Area(footprint.geom) > 20

-- CANTON
SELECT * 
FROM public.canton
WHERE
	"NAME" = 'Berne'
	OR "NAME" = 'Genève'
	OR "NAME" = 'Jura'
	OR "NAME" = 'Neuchatel'
	OR "NAME" = 'Fribourg'
	OR "NAME" = 'Vaud'
	OR "NAME" = 'Valais'
ORDER BY "NAME"


-- MERGED
CREATE TABLE merged_data AS
SELECT 
	DISTINCT ON (footprint."UUID")
	footprint.geom AS geometry,
	regbl."EGID" AS egid,
	regbl."GDEKT" AS canton,
	regbl."GGDENAME" AS commune,
	regbl."LTYP" AS building_type,
	regbl."GKSCE" AS regbl_soruce,
	regbl."GKAT" AS category,
	regbl."GKLAS" AS class,
	regbl."GBAUJ" AS construction_year,
	regbl."GAREA" AS regbl_surface,
	regbl."GVOL" AS regbl_volume,
	regbl."GASTW" AS regbl_levels,
	regbl."GEBF" AS regbl_sre,
	-- PRODUCTION DE CHALEUR
	regbl."GWAERZH1" AS regbl_heat_generator1,
	regbl."GENH1" AS regbl_heat_source1,
	regbl."GWAERZH2" AS regbl_heat_generator2,
	regbl."GENH2" AS regbl_heat_source2,
	-- PRODUCTION D'ECS
	regbl."GWAERZW1" AS regbl_hot_water_generator1,
	regbl."GENW1" AS regbl_hot_water_source1,
	regbl."GWAERZW2" AS regbl_hot_water_generator2,
	regbl."GENW2" AS regbl_hot_water_source2
FROM 
	public.all_regbl AS regbl
JOIN
	public.all_buildings as footprint
ON
	ST_Intersects(regbl.geom, footprint.geom)
WHERE ST_Area(footprint.geom) > 20
--LIMIT 100


