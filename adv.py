from room import Room
from player import Player
from world import World

import random
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
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

# create a dict to store rooms
rooms = {}
# create a dict w/ key-value pairs to programatically find inverse directions
inverse_dir = { 'n': 's', 's': 'n', 'e': 'w', 'w': 'e' }
# create a list to track the reverse direction for traveling backwards
# initialize with a value of None to satisfy first pass
reverse_path = [None]

# initialize both dicts by storing key-values of the current room & its exits
rooms[player.current_room.id] = player.current_room.get_exits()

# until the rooms dict includes all rooms from room_graph...
while len(rooms) < len(room_graph):

    # if the current room is not already in the rooms dict,
    # add a list of its exits in the rooms and exits dict
    if player.current_room.id not in rooms:
        rooms[player.current_room.id] = player.current_room.get_exits()

        # grab the reverse of the last direction we traveled so that we can
        # remove this direction from potential exits out of the current room
        reverse_dir = reverse_path[-1]
        rooms[player.current_room.id].remove(reverse_dir)

    # when a room has no exits, it means we've hit a dead end & must reverse course
    while len(rooms[player.current_room.id]) < 1:
        # pop the last reverse-direction traveled to remove it from
        # the reverse_path list and add it to our traversal_path
        # then move the player in this reverse-direction
        reverse_dir = reverse_path.pop()
        traversal_path.append(reverse_dir)
        player.travel(reverse_dir)

    # pop the first available exit direction to remove it from possible exits and
    # add it to our traversal_path. then add it to the end of the reverse_path list
    exit_dir = rooms[player.current_room.id].pop(0)
    traversal_path.append(exit_dir)
    reverse_path.append(inverse_dir[exit_dir])

    # move the player in the direction of the first available exit
    player.travel(exit_dir)

    # if there's only one room left unvisited, to avoid the error "cannot execute
    # pop() of empty list", simply store the last room & its exits in the rooms dict
    if len(room_graph) - len(rooms) == 1:
        rooms[player.current_room.id] = player.current_room.get_exits()


# TRAVERSAL TEST - DO NOT MODIFY
visited = set()
player.current_room = world.starting_room
visited.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited.add(player.current_room)

if len(visited) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited)} unvisited rooms")


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
