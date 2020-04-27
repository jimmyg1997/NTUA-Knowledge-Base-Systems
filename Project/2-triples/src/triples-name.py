import pandas as pd
from functools import reduce

class Person():
	def __init__(self):
		self.prefix = "<https://www.imdb.com/name/>"
		self.infix = "<https://www.example.com/>"
		self.postfix = {"name":'""^^xsd:string', "birth_year":'""^^xsd:string', "death_year":'""^^xsd:string'}

		self.datatypes = { "primaryName" : "name", "birthYear": "birth_year", "deathYear": "death_year"}
		self.data_p = "../rdf/name_data_properties/name_rdf.nt"
	def tokenize_characters(self,c):
		if "[" in c:
			c = c[1:-1]
			c = c.split(",")
			c = [ j[1:-1] for j in c]
			return c
		else: 
			return ["\\N"]

	def data_prop(self):
		chunk = 0

		for name_i in pd.read_csv('../../0-data/csv/name.basics.csv',sep=',',chunksize=10000):

			pd.set_option('display.max_rows', 16)
			
			print(chunk)

			
			with open(self.data_p[:-3] + str(chunk) + self.data_p[-3:], 'w+') as wfile:
				for row in name_i.iterrows():
					row = row[1].to_frame().transpose()

					# Step 1 : Define prefix
					# row in tuple: ( _, row info)
					prefix = self.prefix[:-2] + str(row['nconst'].item()) + self.prefix[-2:]
					
					for column in row.columns[1:]:

						# Step 2 :  Define infix

						# Step 2.1: handle object properties later on
						if(column == "primaryProfession" or column == "knownForTitles"): continue

						# Step 2.2: find the values of the field and tokenize properly
						value = str(row[column].item())


						# Step 2.3 : Check if the fields are nan, if so continue to the next field no need to create a RDF
						nan = True if value == "\\N" else False
						if nan: continue

						# Step 2.4 :  Define the final infix
						infix = self.infix[:-2] + str(self.datatypes[column]) + self.infix[-2:]


						# Step 3 :  Define postfix
						postfix_ =  self.postfix[self.datatypes[column]]

						
						postfix = postfix_[:1] + value + postfix_[1:]
							
						seq = (prefix, infix, postfix)
						line = " ".join(seq) + "\n"
						if line not in wfile:
							wfile.write(line)
			chunk +=1






person = Person()
#movies.data_prop()

