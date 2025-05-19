MATCH (p1:person)-[:knows]-(p2:person)-[:person_islocatedin]->(pl:place) WHERE p1.p_personid = 933 
RETURN p2
