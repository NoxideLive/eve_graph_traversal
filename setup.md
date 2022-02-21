# Setup

## Steps

1. Docker Compose Up `docker-compose.yml`
2. Wait for JanusGraph to Initialize
    1. Wait for "Channel started at port 8182"
3. Run `http://localhost:8000/loader/graph/load_v`
    1. Wait for it to finish, this might take a while.
    2. This loads all systems and stations from Eve Api and Build the Vertices and Edges
4. Run `http://127.0.0.1:8000/loader/graph/load_e`
    1. Wait for this to finish, this will take longer.
    2. This loads all Star Gates as edges into graph
    3. This needs to run after system vertices are created since it creates edges from to vertices
5. Run `indexing.bat` to add the necessary indexes
## Notes

The way this setup works is to allow reloading and updating running the same functions. This is not the optimal loading
strategy, but it works for Eve Api since the data updates daily.