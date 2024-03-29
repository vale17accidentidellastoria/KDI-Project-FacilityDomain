# KDI Project 2019 - FacilityDomain

This repository contains all the output files of the project "Facilities and Events" for the Knowledge and Data Integration Course 2019/2020 at University of Trento.

Brief description/introduction

## Explanation of this repository content

Our Github project is structured in this directory tree

* informal-model/
* formal-model/
* data/
* models/
  * /rapidminer
  * /r2rml
  * /script
  
The *informal-model/* folder contains:
 * *Final_informal_model.graphml.xml* : yEd file containing the EER diagram
 * *Final_informal_model.png* : a picture of the EER diagram
 
The *formal-model/* folder contains:
 * *CSK_grounding.graphml.xml* : yEd file containing the diagram of the Top Level Grounding Ontology
 * *CSK_grounding.png* : a picture of the Top Level Grounding Diagram
 * *facilities_ontology.owl* : the OWL file containing the ontology about facilities and events
 * *ontology_img.png* : a picture that visualizes completely our ontology exported in png format
 * *final_ontology.png* : a picture that visualizes the class hierarchy of the ontology (OWLViz)
 * *oops_evaluation.png* : the results about the ontology evaluated using OOPS! tool
 * *schemaorg_complete_ontology.owl* : Schema.org's complete ontology
 * *schemaorg_selected_classes.owl* : Schema.org's ontology containing only the classes needed to us for the top level grounding
 * *toplevel_grounding_facilities_ontology.owl* : the OWL file about the final top level grounding ontology 
 * *final_top_level_grounding_picture.png* : a picture that visualizes the final top level grounding ontology (OWLViz)
 * *webvowl_ontology.svg* : a picture that visualizes completely our ontology exported in svg format (realized using WebVOWL)

The *data/* folder contains:
* *cinemaRovereto.json* : output JSON file generated by webscraping using ParseHub from Cinema Rovereto  
* *cineworldTrento.json* : output JSON file generated by webscraping using ParseHub from Cineworld Trento  
* *cultura.json* : output JSON file generated by webscraping using ParseHub from Cultura  
* *mart.json* : output JSON file generated by webscraping using ParseHub from Mart  
* *muse.json* : output JSON file generated by webscraping using ParseHub from Muse  
* *trentoTodayE.json* : output JSON file generated by webscraping using ParseHub from Trento Today  
* *visitTrentino.json* : output JSON file generated by webscraping using ParseHub from Visit Trentino  

the *models/* folder contains:
* *script/*:
    * *extract/*: python files for extracting data from description 
    * *format/*: python files for uniforming date and time
    * *structure/*: python files for converting the datasources' structure to desired structure
    * *movieDetails/*: python files for fetching Movie details 
    * *locations/*: python file for adding geolocation data
    * *merge/*:
        * *merge.py*: python file for merge datasources to a single table
        * *split_save.py*: python file to split the final dataset. seperated datasets for different categories.
* *rapidminer/*:
    * *output/*: csv output files of RapidMiner. one file for each seven categories, one for facilities, one for movie details.
    * *Process.rmp*: RapidMiner Project file

## Procedure
* load *Process.rmp* in RapidMiner and run it. The output CSV files will appear on output folder.
* load each csv file in Karma and apply the relative r2rml found in /models/r2rml
* export RDFs from Karma

## Team Members

#### Model Subgroup

* Cappellaro Davide
* Conti Alessandro (Whole Group PM)
* Diaconu Andrei
* Pigato Valentina Sofia (Model Subgroup PM)

#### Integration Subgroup

* Hassanli Seyyed Arya (Integration Subgroup PM)
* Iossa Andrea
* Mattè Andrea
