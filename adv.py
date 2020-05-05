from room import Room
from player import Player
from world import World
from utils import Stack, Queue

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']


graph = {
    0: {"n": "?", "s": "?", "w": "?", "e": "?"}
}

opposite = {
    "n": "s",
    "s": "n",
    "e": "w",
    "w": "e"
}


# *** DEQUEUE METHOD NOW POPS
dft_stack = Stack()
bfs_queue = Queue()
visited = set()


def walk_path(player):
    dft_stack.push(player.current_room)
    final_path = []
    random_dir = None
    # prev_room = None
    while len(graph) < len(room_graph):
        curr_room = dft_stack.pop()
        exit_directions = curr_room.get_exits()
        # if not in graph
        if not curr_room.id in graph:
            # initiate dict entry
            graph[curr_room.id] = {}
            # loop through possible directions
            for d in exit_directions:
                graph[curr_room.id][d] = "?"

        # move in random direction
        # find random direction
        if random_dir is None:
            random_dir = random.choice(exit_directions)

        print("moving in direction", random_dir, len(graph))

        next_room_id = curr_room.get_room_in_direction(random_dir).id
    # TEMPORARY FIX TO INFINITE LOOP
        if next_room_id:
            
            # travel random direction
            player.travel(random_dir)
            # log direction moved
            final_path.append(random_dir)

            # adjust current rooms attributes
        
            graph[curr_room.id][random_dir] = next_room_id

            # adjust next rooms attributes
            graph[next_room_id][opposite[random_dir]] = curr_room.id

            # add the new current room to stack
            dft_stack.push(player.current_room)

    return final_path

# def walk_path(player):
#     dft_stack.push(player.current_room)
#     final_path = []

#     while len(graph) < len(room_graph):
#         curr_room = dft_stack.pop()
#         exit_directions = curr_room.get_exits()
#         # if not a dead end
#         if not curr_room.id in graph:
#             graph[curr_room.id] = {}
#             # check each direction
#             for d in exit_directions:
#                 # update current room's exit in the graph dict
#                 graph[curr_room.id][d] = "?"


#         for d in exit_directions:
#             if graph[curr_room.id][d] == "?":
#                 player.travel(d)
#                 graph[curr_room.id][d] = curr_room.get_room_in_direction(d).id
#                 final_path.append(d)
#                 break
#         # begin BFS for "?" if there's only 1 exit in room
#         # *** Dead End ***
#         if len(exit_directions) == 1:
#             bfs_queue.enqueue([curr_room])
#             path_of_directions = []
#             while bfs_queue.size() > 0:
#                 bfs_path = bfs_queue.dequeue()
#                 bfs_current_room = bfs_path[-1]
#                 # if there's an unexplored room
#                 for d in bfs_current_room.get_exits():
#                     if graph[bfs_current_room.id][d] == "?":
#                         graph[bfs_current_room.id][d] = bfs_current_room.get_room_in_direction(
#                             d).id
#                         player.travel(d)
#                         # convert ids to directions
#                         path_of_directions.append(d)
#                 # CHOOSE RANDOM DIRECTION
#                 for d in bfs_current_room.get_exits():
#                     neighbor = bfs_current_room.get_room_in_direction(d).id
#                     new_path = list(bfs_path)
#                     new_path.append(neighbor)
#                     bfs_queue.enqueue(new_path)
#         # # find random direction
#         # random_direction = random.choice(exit_directions)
#         # # log direction moved
#         # final_path.append(random_direction)
#         # add to loop again
#         dft_stack.push(player.current_room)
#     return final_path
traversal_path = walk_path(player)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
