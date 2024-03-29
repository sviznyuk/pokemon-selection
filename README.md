# pokemon-selection

## Objective:
Sort pokemon by their likelihood to win battles

## Preamble:
Do analysis on a subset of data available at https://pokeapi.co/ to come up with a team of 6 Pokemon
that has the highest chance of winning battles.

Do analysis initially based solely on the Pokemon “type” system - a system
somewhat like “rock, paper, scissors”. For example, Fire type moves do double damage against
Grass type Pokemon, but only do half damage to Water type Pokemon, etc.

The full list of types (including links to their full half/double damage information) is available at
https://pokeapi.co/api/v2/type

Consider the typing of the Pokemon in relation to the total population of other
Pokemon with types that are beneficial/detrimental to each Pokemon.

Build a team of 6 Pokemon with the widest range of type coverage for all potential opponents.

The list of eligible Pokemon for this team is all Pokemon in the National Dex https://pokeapi.co/api/v2/pokedex/1/

## Deliverables:

### 1. Storage schema for storing the relevant data retrieved from the PokéAPI.

   **The storage schema consists of 5 tables:**

| table name | data elements in the table| description |
| --- | --- | --- |
| eligible_pokemon | pokemon_name | **the list of eligible pokemon** |
| pokemon_types | pokemon_name, pokemon_type | **pokemon names with their types** |
| damage_relations | damage, from_type, to_type | **pokemon types with damage they can do to other types and sustain from other types** |
| pokemon_damage_levels_to | pokemon_name, pokemon_type, damage_to, to_type | **the main fact table** |
| pokemon_damage_levels_from | pokemon_name, pokemon_type, damage_from, from_type | **the main fact table** |
| pokemon_ranking | pokemon_name, damage_to, damage_from, damage_diff | **the pokemon sorted by their damage abilities** |

   The schema is physicalized and loaded with data, as CSV files:

   eligible_pokemon.csv  
   damage_relations.csv  
   pokemon_types.csv  
   pokemon_damage_levels_to.csv  
   pokemon_damage_levels_from.csv  
   pokemon_ranking.csv

### 2. Develop an integration with the PokéAPI to extract the relevant information and store it in defined storage schema.

   **select_pokemon.py** Python3 script
   
   The script requires the following Python modules:  
   requests  
   pandas  
   json  
   time  
   
   The script pulls data from PokeAPI and populates 5 schema tables listed above.  
   The example of script run from command line on Linux:

/src/pokemon-selection> ./select_pokemon.py  

Retrieving list of eligible pokemon in 1.359 s  
Retrieving pokemon types in 0.155 s  
Retrieving damage relations for normal in 0.478 s  
Retrieving damage relations for fighting in 0.36 s  
Retrieving damage relations for flying in 0.493 s  
Retrieving damage relations for poison in 0.402 s  
Retrieving damage relations for ground in 0.409 s  
Retrieving damage relations for rock in 0.377 s  
Retrieving damage relations for bug in 0.418 s  
Retrieving damage relations for ghost in 0.33 s  
Retrieving damage relations for steel in 0.378 s  
Retrieving damage relations for fire in 0.395 s  
Retrieving damage relations for water in 0.574 s  
Retrieving damage relations for grass in 0.491 s  
Retrieving damage relations for electric in 0.38 s  
Retrieving damage relations for psychic in 0.451 s  
Retrieving damage relations for ice in 0.309 s  
Retrieving damage relations for dragon in 0.344 s  
Retrieving damage relations for dark in 0.361 s  
Retrieving damage relations for fairy in 0.316 s  
Retrieving damage relations for unknown in 0.216 s  
Retrieving damage relations for shadow in 0.155 s  
Reformating and writing data in 0.391 s  
Total runtime 9.5 s

### 3. Final result:  
   From pokemon_ranking.csv file, it follows:  
   the 6 pokemon with max difference between ability to do damage to others and sustain damage from others are:  

| pokemon_name | sum_damage_to | sum_damage_from | sum_damage_diff |
| --- | --- | --- | --- |
|dialga |	26 |	13 |	13
|tyrantrum | 24	| 14 |	10
|tyrunt	| 24 | 14	| 10
|aggron	| 30 |	21 |	9
|aron	| 30 |	21	| 9
|bastiodon	| 30 |	21 |	9

### 4. Followup Questions:

   **4.1 How would you work with stakeholders to make sure the storage schema meets their requirements?**  
       The schema maps between pokemon, their types, and damage abilities which allows analysts to  
       run various queries to sort pokemon by their abilities using different criteria  

   **4.2 What conveniences could you add to the schema to improve their workflow?**  
       Multiple views can be created on top of 5 tables to present data in different prospectives.  
       Data can be loaded into relational database in AWS cloud and made available via web interface.
  
   **4.3 What changes would you need to make to this storage schema (if any) to handle arbitrary additional  
       data the Data Science team would like to consider from the API in their analysis?**  
       The intermediate steps to load schema tables allows adding additional attributes to consideration,  
       in addition to pokemon types. More tables may be added in addition to pokemon_types to contain  
       mapping of pokemon to other attributes
       
   **4.4 What changes would we need to make to the schema to support different versions of Pokemon across game generations that may have new/updated types?**  
       The current schema already supports different version of Pokemon, e.g. steelix and steelix-mega,  
       landorus-incarnate and landorus-therian, diglett and diglett-alola, etc
       
   **4.5 What concepts should we utilize if we needed to make sure our Pokemon types are kept up-to-date on a daily basis?**  
       A batch job needs to be setup to execute select_pokemon.py script on a daily basis
   
   **4.6 What other considerations do we need to take into account while trying to keep our data up-to-date?**  
       One has to monitor changes to PokeAPI interface and specs
  
   **4.7 How can we verify the continued accuracy of our data and/or correct for invalid or incomplete data in our pipeline?**  
       A separate and independent reconciliation batch job has to be set up to reconcile data in the schema back to PokeAPI
