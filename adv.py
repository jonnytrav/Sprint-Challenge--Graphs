from room import Room
from player import Player
from world import World
from utils import Stack, Queue

import random
import copy
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

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
# dft_stack = Stack()
# bfs_queue = Queue()

visited = {}
visited[player.current_room.id] = player.current_room.get_exits()
reverse_path = []
final_path = []


def walk_path(player):
    while len(visited) < len(room_graph) - 1:
        if player.current_room.id not in visited:
            visited[player.current_room.id] = player.current_room.get_exits()
            # we do not want to travel the way we just came when we .pop() for a direction
            visited[player.current_room.id].remove(reverse_path[-1])
        else:
            if len(visited) > 1:
                visited[player.current_room.id].remove(reverse_path[-1])

        # if there are no directions to .pop()
        while len(visited[player.current_room.id]) == 0:
            # walks backwards one step using reverse list
            opposite_dir = reverse_path.pop()
            print("walking opposite direction", opposite_dir)
            final_path.append(opposite_dir)
            player.travel(opposite_dir)
            # log step we took

        # get valid direction
        direction = visited[player.current_room.id].pop()
        print(f"in {player.current_room.id}, going {direction}")
        # move player that direction
        player.travel(direction)
        # log actual path
        final_path.append(direction)
        # track reverse path for bfs
        reverse_path.append(opposite[direction])

    return final_path


# def walk_path(player):
#     dft_stack.push(player.current_room)
#     final_path = []
#     random_dir = None
#     prev_room = None

#     while len(graph) < len(room_graph):
#         curr_room = dft_stack.pop()
#         print("BEGINNING DFT", curr_room.id)
#         exit_directions = curr_room.get_exits()
#         # if not in graph
#         if not curr_room.id in graph:
#             graph[curr_room.id] = {
#             }
#             for d in exit_directions:
#                 graph[curr_room.id][d] = "?"

#         if prev_room is not None:
#             graph[curr_room.id][opposite[random_dir]] = prev_room.id

#         # find random direction
#         if random_dir is None:
#             random_dir = random.choice(exit_directions)

#         if random_dir not in graph[curr_room.id]:
#             print("finding new direction")
#             invocations = 0
#             while invocations < 5:
#                 random_dir = random.choice(exit_directions)
#                 if graph[curr_room.id][random_dir] == "?":
#                     break
#                 else:
#                     invocations += 1

#         next_room = curr_room.get_room_in_direction(random_dir)
#         # if we can move in this random direction
#         # AND its unexplored
#         if next_room and graph[curr_room.id][random_dir] == "?":
#             prev_room = curr_room
#             # travel random direction
#             player.travel(random_dir)
#             print(random_dir)
#             # log direction moved
#             final_path.append(random_dir)

#             # adjust current rooms attributes
#             graph[curr_room.id][random_dir] = next_room.id

#             # add the new current room to stack
#             dft_stack.push(player.current_room)

#         else:
#             print("BEGINNING bfs, final_path rn =>", final_path)
#             # LOOP UNTIL WE FIND ? IN GRAPH

#             bfs_queue.enqueue(([], player.current_room))
#             found = False

#             while bfs_queue.size() > 0 and found == False:
#                 curr_tuple = bfs_queue.dequeue()
#                 global bfs_curr_path
#                 global bfs_curr_room
#                 bfs_curr_path = curr_tuple[0]
#                 bfs_curr_room = curr_tuple[1]
#                 visited.add(bfs_curr_room)
#                 new_directions = bfs_curr_room.get_exits()
#                 last_direction = None
#                 if len(bfs_curr_path) > 1:
#                     last_direction = bfs_curr_path[-1]

#                 if not bfs_curr_room.id in graph:
#                     graph[bfs_curr_room.id] = {}
#                     for d in new_directions:
#                         # adjust pointer to room before
#                         if bfs_curr_room.get_room_in_direction(d) in visited:
#                             graph[bfs_curr_room.id][d] = bfs_curr_room.get_room_in_direction(
#                                 d).id

#                         graph[bfs_curr_room.id][d] = "?"

#                 if last_direction:
#                     graph[bfs_curr_room.id][opposite[last_direction]
#                                             ] = bfs_curr_room.get_room_in_direction(opposite[last_direction]).id

#                 for d in new_directions:

#                     if graph[bfs_curr_room.id][d] == "?":
#                         bfs_curr_path.append(d)
#                         found = True
#                     else:
#                         if bfs_curr_room.get_room_in_direction(d) not in visited:
#                             next_path = list(bfs_curr_path)
#                             next_path.append(d)
#                             bfs_queue.enqueue(
#                                 (next_path, bfs_curr_room.get_room_in_direction(d)))
#             # PLAYER ACTUALLY WALKS now
#             if found == True:
#                 visited.clear()
#                 # print("BREAKING LOOP BECAUSE OF ?", bfs_curr_path)
#                 print("about to walk this path", bfs_curr_path)
#                 for d in bfs_curr_path:
#                     player_room = player.current_room
#                     if player_room.id not in graph:
#                         graph[player_room.id] = {}
#                         for d in player_room.get_exits():
#                             graph[player_room.id][d] = "?"
#                     # fill in graph with directions walked
#                     print(player_room.id, d)
#                     graph[player_room.id][d] = player_room.get_room_in_direction(
#                         d).id  # SOMETHING
#                     random_dir = d
#                     player.travel(d)
#                     final_path.append(d)

#                 # print("this is the final path after '?' was found", final_path)
#                 dft_stack.push(player.current_room)
#             else:
#                 print("finishing bfs, no '?' found", final_path)
#                 return final_path
#     print(final_path)
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
