# Graphathon_2023-04-14

Repository for material for the graph hackathon facilitated on 14th April 2023.  

For this graphathon was used data from Kaggle https://www.kaggle.com/code/rajesh2609/medicare-provider-fraud-detection and stored in this repository. 

All the preprocessing steps  (no need to re-run them) happens in [DataPreparation notebook](https://github.com/EY-Tech-Consulting-Denmark/Graphathon_2023-04-14/blob/main/Notebooks/DataPreparation.ipynb).   

The preprocessed data are stored in this repository as well.   

End-to-end instructions for Neo4j desktop and Jupyter notebooks:  

1. Install Neo4j desktop (free) from link https://neo4j.com/download/  

2. Create a new database. 
![image](https://user-images.githubusercontent.com/89451887/205630088-83ba01ec-e65c-4cd0-979f-1e1287bc6c86.png)
(Make sure to use versio over 5.0)  
Then install the Graph datascience plug-in. To make it available click on your database first.  
![image](https://user-images.githubusercontent.com/89451887/205834855-7b8a5517-9207-43c3-b77b-ae88fbf86414.png)


After that start the dabase.

If you get an error, press __CTRL+R__ to reset (might be needed to repeat multiple times) ontil the 'Open' button is enabled.  

Open the database.

3. Load the data into the database  
The local database created in Neo4j dekstop can't be reached by google colab and that is why for the next steps you need to clone/fork the repository to be able to run prepared jupyter notebooks.

Open [DataToGraph.ipynb](https://github.com/EY-Tech-Consulting-Denmark/Graphathon_2023-04-14/blob/main/Notebooks/DataToGraph.ipynb) and set up the configuration of your local database.  
![image](https://user-images.githubusercontent.com/89451887/205509513-b5056181-50f5-4479-8ca2-aa386a78bb2e.png)

Provide the same user name and password that you used when you created the database.  
The database URL can be found at the bottom of the Neo4j Desktop browser.  

After setting the right connection, rerun the whole notebook to load the data.  

4. Start with exploring the dataset and practising cypher in Neo4j desktop with [Cypher_exercises.md](https://github.com/EY-Tech-Consulting-Denmark/Graphathon_2023-04-14/blob/main/Cypher_exercises.md). 

5. Continue with practising graph algorithms with [Algorithms.ipynb](https://github.com/EY-Tech-Consulting-Denmark/Graphathon_2023-04-14/blob/main/Notebooks/Algorithms.ipynb). Remember to set up the connection to your database again.  
If you will get stup, look up the exercise in the [Algorithms_answers.md](https://github.com/EY-Tech-Consulting-Denmark/Graphathon_2023-04-14/blob/main/Algorithms_answers.md).  

6. Eventually you can try to improve a machine learning model by enriching it with the graph features. We have prepared a [MachineLearning.ipynb](https://github.com/EY-Tech-Consulting-Denmark/Graphathon_2023-04-14/blob/main/Notebooks/MachineLearning.ipynb) for you, you can build up upon.  
The database connections need to be set up here as well.  

We wish you lot of fun!
