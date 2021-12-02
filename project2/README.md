# NBA Database - Project2

**Database Account**: yh3290

**Web Front-End App URL: http://34.139.184.252:8111/**

**Team Members:** Jiarui Liu (jl6007), Yong Hao (yh3290)

## Description
1. Create composite types.
Add **Full_Name** as a new composite type in player table to replace the old **First_Name** and **Last_Name**. Use one composite type to represent name. So you can either treat them as whole or seperately.
2. Add arrays.
Add **Career_Stats** as array type in player table to replace the old **Career_PTS**, **Career_AST** and **Career_REB**. Use array to represent player's career contribute, which provide more scalability. You can easily add like Block or Steal for every player.
3. Add trigger.
Add trigger function **if_roll_back()** and trigger **check_player_del**. This trigger will make sure every team at least has one player. If you want to delete all players in a team, it will stop. Make sure the at least one player constrain of the team.

## Schema Modification Commands
Please note that we have created a new table called _New_Player_ to replace the old _Player_ table, to show the composite types and arrays features.
```sql
CREATE TYPE Full_Name AS (
First_Name VARCHAR(30),
Last_Name VARCHAR(30)
);
```
```sql
CREATE TABLE New_Player (
	Player_ID INTEGER,
	Name Full_Name,
	Date_Birth DATE,
	Height INTEGER,
	Weight INTEGER,
	Jersey INTEGER,
	Position CHARACTER(30),
	Team_ID INTEGER,
	CAREER_STATS DECIMAL [],
	ALL_STAR_NUM INTEGER,
	PRIMARY KEY (Player_ID),
	FOREIGN KEY (Team_ID) REFERENCES Team
);
```

```sql
CREATE TRIGGER check_player_del
BEFORE DELETE ON new_player
FOR EACH ROW
EXECUTE FUNCTION if_roll_back();

CREATE OR REPLACE FUNCTION if_roll_back() RETURNS TRIGGER AS $example_table$
   BEGIN
      IF (SELECT COUNT(*) FROM new_player WHERE team_id = old.team_id) <= 1 THEN
      RETURN NULL;
      ELSE
      RETURN OLD; 
      END IF;
   END;
$example_table$ LANGUAGE plpgsql;
```
## Interesting Queries
1.
```sql
SELECT COUNT(*) FROM New_Player
WHERE (name).First_Name = 'John';
```
Sometimes, people may want to know how many players in the NBA have the same first name with them. The above query gives such results precisely. Here, it will return the number of players whose first name is John.

2.
```sql
SELECT * FROM New_Player
WHERE Career_Stats[1] >= 20 AND Career_Stats[2] >= 5 AND Career_Stats[3] >= 5;
```
A player who has a 20(PTS)+5(AST)+5(REB) stats is considered all-around. Here, the query returns all all-around players in the history of NBA. In the future, we may add Block and Steal to better form our radar chart function, and we can make the 'all-around' standard as 20+5+5+1(BLK)+1(STL).

3. 
```sql
DELETE FROM New_Player
WHERE team_id = 1610612738;
```
This query tries to delete all players of Celtics. The trigger we set will ensure at least one player for every team. Therefore, there is still going to be one player left in the returned _New_Player_ table.
