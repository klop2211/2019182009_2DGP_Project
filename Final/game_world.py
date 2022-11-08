# 0 back
# 1 front

world = [[], []]

def add_object(object, depth):
    world[depth].append(object)

def add_objects(object_list, depth):
    world[depth] += object_list

def remove_object(object):
    for layer in world:
        if object in layer:
            layer.remove(object)
            del object
            return

def all_object():
    for layer in world:
        for object in layer:
            yield object

def clear():
    for object in all_object():
        remove_object(object)
