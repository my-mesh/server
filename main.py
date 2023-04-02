test = [{"node_id": 255, "network_id": 1}, {"node_id": 255, "network_id": 2}]

def get_index(data, id, search):
    for index, element in enumerate(data):
        if (element[search] == id):
            return index
    
    return -1



index_network = get_index(test, network_id, "network_id")
index_node = get_index(test, network_id, "node_id")

print(index_network)
print(index_node)