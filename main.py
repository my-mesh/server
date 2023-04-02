test = [{"node_id": 255, "network_id": 1}, {"node_id": 255, "network_id": 2}]

def get_index(data, id):
    for index, element in enumerate(test):
        if (element["network_id"] == 2):
            return index
    
    return -1

print(get_index(test, 20))