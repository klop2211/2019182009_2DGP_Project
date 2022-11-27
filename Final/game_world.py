# 0 back
# 1 front

world = [[], [], []]
collision_group = dict()

def add_object(object, depth):
    world[depth].append(object)

def add_objects(object_list, depth):
    world[depth] += object_list

def remove_object(object):
    for layer in world:
        if object in layer:
            layer.remove(object)
            remove_collision_object(object)
            del object
            return

def remove_collision_object(o):
    for pairs in collision_group.values():
        while o in pairs[0]:
            pairs[0].remove(o)
        while o in pairs[1]:
            pairs[1].remove(o)

def all_object():
    for layer in world:
        for object in layer:
            yield object

def clear():
    for o in all_object():
        del o
    for layer in world:
        layer.clear()


def all_collision_pairs():
    for group, pairs in collision_group.items():
        for a in pairs[0]:
            for b in pairs[1]:
                yield a, b, group


def add_collision_pairs(a, b, group):

    if group not in collision_group:
        print('Add new group ', group)
        collision_group[group] = [[], []] # list of list : list pair
    if a:
        if type(a) is list:
            collision_group[group][1] += a
        else:
            collision_group[group][1].append(a)
    if b:
        if type(b) is list:
            collision_group[group][0] += b
        else:
            collision_group[group][0].append(b)
