
import pandas as pd
from functools import reduce
class Movie():
	def __init__(self):
		self.prefix = "<https://www.imdb.com/title/>"
		self.infix = "<https://www.example.com/>"
		self.postfix1 = {"type":'""^^xsd:string',"prim_title":'""^^xsd:string',"orig_title":'""^^xsd:string',
					    "adult" : '""^^xsd:boolean', "start_year":'""^^xsd:string', "end_year":'""^^xsd:string',"duration":'""^^xsd:int',
					    "ordering":'""^^xsd:int', "category":'""^^xsd:string', "job":'""^^xsd:string',"rating":'""^^xsd:double',
					    "voting":'""^^xsd:int', "genre":'""^^xsd:string', "character":'""^^xsd:string'}


		self.postfix2 = "<https://www.imdb.com/name/>"

		self.datatypes = { "titleType" : "type", "primaryTitle" : "prim_title", "originalTitle" : "orig_title", 
						   "isAdult": "adult", "startYear": "start_year", "endYear": "end_year", 
						   "runtimeMinutes": "duration", "ordering": "ordering", "category": "category", "job": "job", 
						   "averageRating": "rating", "numVotes": "voting", "genres": "genre", "characters":"character"}


		self.objectypes1 = { "director":"has_director", "actor": "has_actor","actress": "has_actress", "composer" :"has_composer", "editor" : "has_editor", 
							"cinematographer": "has_cinematographer",  "producer": "has_producer", "writer":"has_writer", "self" : "has_self"}
		self.objectypes2 = { "director":"is_director_of", "actor": "is_actor_of","actress": "is_actress_of", "composer" :"is_composer_of", 
							 "editor" : "is_editor_of", "cinematographer": "is_cinematographer_of",  "producer": "is_producer_of", "writer":"is_writer_of", "self": "is_self_of"}

		self.data_p = "../rdf/movie_data_properties/title_rdf.nt"
		self.object_p1 = "../rdf/movie_object_properties/title_rdf.nt"
		self.object_p2 = "../rdf/name_object_properties/name_rdf.nt"

		
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
		ratings = pd.read_csv('../../0-data/csv/title.ratings.csv',sep=',')
		for movie_i in pd.read_csv('../../0-data/csv/title.basics.csv',sep=',',chunksize=10000):
			dfs = [movie_i, ratings]

			movies = reduce(lambda left,right: pd.merge(left,right,how = 'inner', on='tconst'), dfs)
			pd.set_option('display.max_rows', 16)
			
			print(chunk)

			
			with open(self.data_p[:-3] + str(chunk) + self.data_p[-3:], 'w+') as wfile:
				for row in movies.iterrows():
					row = row[1].to_frame().transpose()

					# Step 1 : Define prefix
					# row in tuple: ( _, row info
					prefix = self.prefix[:-2] + str(row['tconst'].item()) + self.prefix[-2:]
					print(row)
					
					for column in row.columns[1:]:

						# Step 2 :  Define infix

						# Step 2.1: handle object properties later on
						if(column == "nconst"): continue

						# Step 2.2: find the values of the field and tokenize properly
						values = str(row[column].item()).split(',')

						
						# Step 2.3 : Check if the fields are nan, if so continue to the next field no need to create a RDF
						nan = True if values[0] == "\\N" else False
						if nan: continue

						# Step 2.4 :  Define the final infix
						infix = self.infix[:-2] + str(self.datatypes[column]) + self.infix[-2:]
						#print(infix)
						#print(values)

						# Step 3 :  Define postfix
						postfix_ = tmp = self.postfix1[self.datatypes[column]]

						for v in values:
							postfix = postfix_[:1] + v + postfix_[1:]
							
							seq = (prefix, infix, postfix)
							line = " ".join(seq) + "\n"
							if line not in wfile:
								wfile.write(line)
			chunk +=1



	def object_prop(self):
		chunk = -1
		for movie_i in pd.read_csv('../../0-data/csv/title.principals.csv',sep=',',chunksize=10000):
			chunk += 1
			if(chunk <= 820): continue

			pd.set_option('display.max_rows', 16)
			
			print(chunk)


			wfile1 = open(self.object_p1[:-3] + str(chunk) + self.object_p1[-3:], 'w+')
			wfile2 = open(self.object_p2[:-3] + str(chunk) + self.object_p2[-3:], 'w+')

			for row in movie_i.iterrows():
				# Step 1 : Keep only the columns necessary and row in tuple: ( _, row info)
				row = row[1].to_frame().transpose()
				row = row[['tconst','nconst', 'category']]

				# Step 2 : Define prefix
				prefix = self.prefix[:-1] + str(row['tconst'].item()) + self.prefix[-1:]

				# Step 3 : Define infix
				if row['category'].item() not in self.objectypes1 : continue
				infix1 = self.infix[:-1] + str(self.objectypes1[row['category'].item()]) + self.infix[-1:]
				infix2 = self.infix[:-1] + str(self.objectypes2[row['category'].item()]) + self.infix[-1:]

				# Step 4 : Define the postfix
				postfix = self.postfix2[:-1] + str(row['nconst'].item()) + self.postfix2[-1:]

				# Step 5 : Write the line in the corresponding file
				seq = (prefix, infix1, postfix)
				line = " ".join(seq) + ".\n"
				if line not in wfile1: wfile1.write(line)

				seq = (postfix, infix2, prefix)
				line = " ".join(seq) + ".\n"
				if line not in wfile2: wfile2.write(line)




movies = Movie()
#movies.data_prop()
#movies.object_prop()


