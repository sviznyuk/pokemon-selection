#!/bin/env python3
#	build pokemon team from type damage info
#
#	Copyright (C) Nov,2019 Sergei Viznyuk <phystech@hotmail.com>
#
#	This program is distributed in the hope that it will be useful, but
#	without any warranty; without even the implied warranty of
#	merchantability or fitness for a particular purpose

import requests
import pandas
import json
import time

start_time=time.perf_counter()
time0=start_time

# Retrive the list of eligible pokemon and their types into pandas dataframe

print('Retrieving list of eligible pokemon in ',end='')
pokemon_url = 'https://pokeapi.co/api/v2/pokedex/1/'
pokemon_resp=requests.get(url=pokemon_url,headers={'User-Agent': 'Chrome/77.0.3865.120', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'Keep-Alive'})

pokemon_entries_dict=json.loads(pokemon_resp.text)
pokemon_entries=pokemon_entries_dict['pokemon_entries']
pokemon_df=pandas.DataFrame(columns=['pokemon_name'])

i=0
for pokemon_entry in pokemon_entries:
	pokemon_df.loc[i]=pokemon_entry['pokemon_species']['name']
	i=i+1
pokemon_df.drop_duplicates(inplace=True)
end_time=time.perf_counter()
print(round(end_time-start_time,3),'s')
start_time=end_time

# Retrieve the list of types

print('Retrieving pokemon types in ',end='')
types_url='https://pokeapi.co/api/v2/type'
types_resp=requests.get(url=types_url,headers={'User-Agent': 'Chrome/77.0.3865.120', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'Keep-Alive'})

types_dict=json.loads(types_resp.text)
type_entries_list=types_dict['results']

end_time=time.perf_counter()
print(round(end_time-start_time,3),'s')
start_time=end_time

# Retrieve damage relations for each type

damage_relations_df=pandas.DataFrame(columns=['damage','from_type','to_type'])
pokemon_type_df=pandas.DataFrame(columns=['pokemon_name','pokemon_type'])

j=0
k=0
for type_entry in type_entries_list:
	type_name=type_entry["name"]
	print('Retrieving damage relations for ' + type_name + ' in ', end="")
	damage_relation_resp=requests.get(url=type_entry['url'],headers={'User-Agent': 'Chrome/77.0.3865.120', 'Accept-Encoding': 'gzip, deflate', 'Accept': '*/*', 'Connection': 'Keep-Alive'})
	damage_relation_dict=json.loads(damage_relation_resp.text);
	damage_relation=damage_relation_dict['damage_relations']
	for key in damage_relation.keys():
		damage_relation_names=damage_relation[key]
		for other_name in damage_relation_names:
			other_name_name=other_name['name']
			if key == 'double_damage_from':
				damage_relations_df.loc[j]=[2,other_name_name,type_name]
			elif  key == 'double_damage_to':
				damage_relations_df.loc[j]=[2,type_name,other_name_name]
			elif  key == 'half_damage_from':
				damage_relations_df.loc[j]=[1,other_name_name,type_name]
			elif  key == 'half_damage_to':
				damage_relations_df.loc[j]=[1,type_name,other_name_name]
			elif  key == 'no_damage_from':
				damage_relations_df.loc[j]=[0,other_name_name,type_name]
			elif  key == 'no_damage_to':
				damage_relations_df.loc[j]=[0,type_name,other_name_name]
			else:
				print('WARNING: unexpected damage relation: ' + key)
			j=j+1
	pokemon_list=damage_relation_dict['pokemon']
	for pokemon_entry in pokemon_list:
		pokemon_name=pokemon_entry['pokemon']['name']
# Check if the pokemon is in eligible pokemon list
		ff=pokemon_name.find('-')
		if ( ff == -1 ):
			pokemon_short=pokemon_name
		else:
			pokemon_short=pokemon_name[0:ff]
		if pokemon_df['pokemon_name'].str.contains(pokemon_short).any():
			pokemon_type_df.loc[k]=[pokemon_name,type_name]
			k=k+1
	end_time=time.perf_counter()
	print(round(end_time-start_time,3),'s')
	start_time=end_time

print('Reformating and writing data in ',end='')

damage_relations_df.drop_duplicates().to_csv('damage_relations.csv',index=False,header=True)
pokemon_df.to_csv('eligible_pokemon.csv',index=False,header=True)
pokemon_type_df.to_csv('pokemon_types.csv',index=False,header=True)

pokemon_type_df.drop_duplicates(inplace=True)
df1=pokemon_type_df.merge(damage_relations_df,how='left',left_on='pokemon_type',right_on='from_type').drop(columns=['from_type']).rename(columns={'damage':'damage_to'}).sort_values(by=['pokemon_name','pokemon_type','to_type']).drop_duplicates()
df2=pokemon_type_df.merge(damage_relations_df,how='left',left_on='pokemon_type',right_on='to_type').drop(columns=['to_type']).rename(columns={'damage':'damage_from'}).sort_values(by=['pokemon_name','pokemon_type','from_type']).drop_duplicates()
df1.to_csv('pokemon_damage_levels_to.csv',index=False,header=True)
df2.to_csv('pokemon_damage_levels_from.csv',index=False,header=True)
df3=df1.groupby('pokemon_name')['damage_to'].sum().reset_index()
df4=df2.groupby('pokemon_name')['damage_from'].sum().reset_index()
df5=df4.merge(df3,how='left',left_on='pokemon_name',right_on='pokemon_name')
df5['damage_diff']=df5['damage_from']-df5['damage_to']
df5.sort_values(by=['damage_diff','damage_to'],ascending=False).to_csv('pokemon_ranking.csv',index=False,header=True)

end_time=time.perf_counter()
print(round(end_time-start_time,3),'s')
print('Total runtime',round(end_time-time0,1),'s')
