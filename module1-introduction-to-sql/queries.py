TOTAL_CHARACTERS = "SELECT COUNT(distinct character_id) FROM charactercreator_character;"

TOTAL_ITEMS = "SELECT COUNT(distinct item_id) FROM armory_item;"

WEAPONS = "SELECT COUNT(distinct item_ptr_id) FROM armory_weapon;"

NON_WEAPONS = """
SELECT count(1) - count(w.item_ptr_id)
FROM armory_item i
LEFT JOIN armory_weapon w ON i.item_id = w.item_ptr_id
"""

TOTAL_SUBCLASS = """
select
  CASE
  WHEN cl.character_ptr_id is not null THEN "cleric"
  WHEN f.character_ptr_id is not null THEN "fighter"
  WHEN n.mage_ptr_id is not null THEN "mage-necro"
  WHEN m.character_ptr_id is not null THEN "mage"
  WHEN th.character_ptr_id is not null THEN "thief"
  ELSE "todo"
  END as char_type
  ,count(distinct ch.character_id) as char_count
from charactercreator_character as ch
left join charactercreator_cleric as cl on ch.character_id = cl.character_ptr_id
left join charactercreator_fighter as f on ch.character_id = f.character_ptr_id
left join charactercreator_mage as m on ch.character_id = m.character_ptr_id
left join charactercreator_thief as th on ch.character_id = th.character_ptr_id
left join charactercreator_necromancer as n on m.character_ptr_id = n.mage_ptr_id
group by char_type
"""

CHARACTER_ITEMS = """
SELECT 
  c.character_id
  ,c.name as character_name
  ,count(distinct i.item_id) as item_count
FROM charactercreator_character c
LEFT JOIN charactercreator_character_inventory inv ON c.character_id = inv.character_id
LEFT JOIN armory_item i ON i.item_id = inv.item_id
GROUP BY c.character_id
LIMIT 20
"""

CHARACTER_WEAPONS = """
SELECT 
  c.character_id
  ,c.name as character_name
  -- ,inv.item_id
  -- ,w.item_ptr_id as weapon_id
  ,count(distinct w.item_ptr_id) as weapon_count
FROM charactercreator_character c
LEFT JOIN charactercreator_character_inventory inv ON c.character_id = inv.character_id
LEFT JOIN armory_weapon w ON w.item_ptr_id = inv.item_id
GROUP BY c.character_id
LIMIT 20
"""

AVG_CHARACTER_ITEMS = """
SELECT avg(item_count)
FROM (
	SELECT  c.character_id
	  ,c.name as character_name
	  ,count(distinct i.item_id) as item_count
	FROM charactercreator_character c
	LEFT JOIN charactercreator_character_inventory inv ON c.character_id = inv.character_id
	LEFT JOIN armory_item i ON i.item_id = inv.item_id
	GROUP BY c.character_id
) subq
"""

AVG_CHARACTER_WEAPONS = """
SELECT avg(weapon_count)
FROM (
	SELECT c.character_id
	  ,c.name as character_name
	  -- ,inv.item_id
	  -- ,w.item_ptr_id as weapon_id
	  ,count(distinct w.item_ptr_id) as weapon_count
	FROM charactercreator_character c
	LEFT JOIN charactercreator_character_inventory inv ON c.character_id = inv.character_id
	LEFT JOIN armory_weapon w ON w.item_ptr_id = inv.item_id
	GROUP BY c.character_id
) subq
"""

queries = [
    {"name": "TOTAL_CHARACTERS", "value": TOTAL_CHARACTERS},
    {"name": "TOTAL_ITEMS", "value": TOTAL_ITEMS},
    {"name": "WEAPONS", "value": WEAPONS},
    {"name": "TOTAL_SUBCLASS", "value": TOTAL_SUBCLASS},
    {"name": "CHARACTER_ITEMS", "value": CHARACTER_ITEMS},
    {"name": "CHARACTER_WEAPONS", "value": CHARACTER_WEAPONS},
    {"name": "NON_WEAPONS", "value": NON_WEAPONS},
    {"name": "AVG_CHARACTER_ITEMS", "value": AVG_CHARACTER_ITEMS},
    {"name": "AVG_CHARACTER_WEAPONS", "value": AVG_CHARACTER_WEAPONS},
]
