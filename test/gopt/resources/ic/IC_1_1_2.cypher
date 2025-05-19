MATCH (p1:person)-[:knows]-(:person)-[:person_islocatedin]->(pl:place) WHERE p1.p_personid = 933 
RETURN p1
