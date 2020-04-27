## 1 - Ontology (Vocabulary)
This was implemented in [Protégé](https://protege.stanford.edu/), which create ontologies in *.owl* format. An ontology is a vocabulary defining the concepts and relationships used to describe an area of concern. It's composed of:

* **Classes** (e.g. Department, Movie, Person) to represent a concept.
* **Data Properties** (e.g. average_rating, birth_year,death_year, end_year) to represent relation between concepts.
* **Object Properties - Rules** (e.g. A movie have an actor). Ontologies can be created for every area of concern and by everyone using RDF (Resource Description Framework), RDFS (RDF Schema) and OWL (Web Ontology Language).


## 2 - URI : N-triples RDFs
There are various types of RDFs. But the most frequently used in terms of semantic web is [N-triples RDFs](https://www.w3.org/2001/sw/RDFCore/ntriples/). N-Triples is a line-based, plain text format for representing the correct answers for parsing RDF/XML test cases as part of the RDF Core working group. The conversion of all *data properties * & *object properties* was implemented through the scripts : 
* **Person class** : *name-triples.py*
```
<<Preson>> <<data prop>> <<value>>              (900 MB)
<<Preson>> <<obj prop (is role of)>> <<Movie>>  (3.9 GB)
```

* **Movie class** : *title-triples.py*
```
<<Movie>> <<data prop>> <<value>>               (980 MB)
<<Movie>> <<obj prop (has role of)>> <<Person>> (3.9 GB)
```

## 3 Simple SPARQL Queries
After we properly configured *database/virtuoso.ini* file we correctly loaded the N-triples RDFs into a Semnatic Database through the **Virtuoso**. Now we are ready to execute the **SPARQL queries**. [SPARQL](https://www.wikiwand.com/en/SPARQL) is a rdf query languagef for semantic databases.

## 4 - Expended SPARQL Queries 
### DBPedia
**DBpedia** is a knowledge graph containing informations extracted from wikipedia . In this project **DBpedia** is used to perform 
named entity recognition. In other word, to find class of entities (e.g., Italia is a country/PopulatedPLace.. or B.Obama is a President/Person..)

### WikiData
Loosely, you could describe [Wikidata](https://towardsdatascience.com/a-brief-introduction-to-wikidata-bb4e66395eb1) as Wikipedias database with over 46million data items (April 2018). Like Wikipedia, there are all kinds of data stored in Wikidata. As such, when you are looking for a specific dataset or if you want to answer a curious question, it can be a good start looking for that data at Wikidata first.

