# Santa needs your help!


It's Christmas time, and Santa has a long list of children waiting for their gifts. Due to striking Elves, he has no route planned and no one else to help him deliver. 
**Can you help him, and plan the optimal route for him?**

You will be given graphs, telling you travel times between households as well as the number of presents expected in each. Each graph has weighted symmetrical edges, indicating travel times, as well as node values for the number of presents each household expects.  
The graphs will be presented as .json files in the **graphs/** folder.
Each graph presents a new and more difficult challenge!  
The files contain a list of nodes, which will always have your base as the starting point (hence, the entry of 0), as well as an adjacency matrix for the edges.
The adacency matrix lets you look up the travel times (in minutes) from house to house - so the entry edges[i][j] will tell you how many minutes it takes to go from house i to house j (and vice versa. Wind doesn't seem to affect you!).

Given this information, find the route that lets you deliver the most presents possible. Santa can only start at 8pm, and has until midnight to deliver! For simplicity's sake, you can assume that all households are in the same timezone.

Write all your results into the file **result.json**, using the structure indicated in that file.

**Good luck, and merry Christmas!**


**Example:**
Input:
graph_01.json
```json
{
    "Nodes": [0, 11, 18, 14], 
    "Edges": {
        "0": [0, 89.6, 31.3, 44.6], 
        "1": [89.6, 0, 77.6, 90.6], 
        "2": [31.3, 77.6, 0, 78.0], 
        "3": [44.6, 90.6, 78.0, 0]
    }
}
```

Expected result:
```json
{
    "graph_01": {
        "Gifts": 32,
        "Path": [
            0,
            2,
            3
        ]
    }
}
```

![Oh no! Seems like this reference broke.](resources/santa-pulled-by-reindeer.gif "Merry Christmas!")
