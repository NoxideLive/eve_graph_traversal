# Notes about my sanity

The initial implementation was to build a market tracker for Eve. However, this requires Authentication via their OAuth
system for which you require a Game Account to pull the information. I settled on doing a simple Shortest Path routing
which is the same as provided inside the game.

Given more time I would have expanded on the actual implementation of the system and since their whole nature of data is
graph based there is alot you can do.

The current system runs on an in-memory system since running Cassandra, Elastic Search and Janusgraph seemed too much
for my system to handle. Ideally this would be run one three different vms with their own system resources. Cassandra
gets used as the persistent storage. Elastic search gets used as an indexing store and Janusgraph as the middle man to
run Gremlin queries.

## Short explanation of Graphs

Graphs are essentially an ontology. They use a Vertex and Edge representation of data. Vertices are data points with a
specific label i.e. `movie` or `actor`. Edges define the relationship between to vertices and are directional.
i.e.`plays_in` or `actor_in`.

This allows us to ask the graph system "questions". For instance given a movie name, who are the actors that play in the
movie? this would be written in Gremlin as `g.V().has('movie', 'title', 'Titanic').outE("actor_in").inV().toList()`

Step by step this is addressing the graph traversal for all vertices with the `movie` label and the `title=Titanic`. We
then traverse outwards on an outwards Edge with the Label `actor_in`. We then enter the vertex on the Edge and solve as
a List.

Vertices and Edges both can have properties which can be used for filtering and traversal analysis. Complex graph
queries can be implemented and can answer very complex questions.

The most difficult thing to do with a graph database is deciding how to structure it. Certain structures are more
efficient with answering certain questions. I have paid carefull attention to the building of my graph to facilitate the
answers I want from it.

## Short Explanation of the JanusGraph Stack

Janusgraph is a multi-system graph database system. Originally known as TitanDB it has been a front-runner in Graph DB
tech alongside Neo4Js. What drew my to Janusgraph was 1. that Takealot forced me to use it and 2. The highly compatible
and configurability of the Software

Janusgraph can be run in multiple configurations with almost 6 different databases and quite a few Indexing software and
even with Spark as the Graph Computer for expensive VertexComputing.

## Final Thoughts

Given more time I would definitely clean up the code, make it more generic in some ways. Coming to terms with working in
Python was a challenge at first but the language is but a tool. Sometimes you need more tools in your toolbox. Even if I
do not make the cut I thoroughly enjoyed the task

PS. It is 5am.