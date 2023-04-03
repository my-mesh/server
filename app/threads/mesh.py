import struct
import requests
from app.threads.base import BackgroundThread

from pyrf24 import RF24, RF24Network, RF24Mesh

from app.utils.payload import convert_payload

def get_index(data, id, search):
    for index, element in enumerate(data):
        if (element[search] == id):
            return index
    
    return -1

class MeshThread(BackgroundThread):
    def startup(self) -> None:
        self.radio = RF24(22, 10)
        self.network = RF24Network(self.radio)
        self.mesh = RF24Mesh(self.radio, self.network)
        self.mesh.node_id = 0
        self.new_nodes = []

        if not self.mesh.begin():
            raise OSError("Radio hardware not responding.")
        print("Mesh started")

    def shutdown(self) -> None:
        print("Mesh stopped")
        self.power = False

    def handle(self) -> None:
        self.mesh.update()
        self.mesh.dhcp()

        if self.network.available():
            header, payload = self.network.read()
            node_id = self.mesh.get_node_id(header.from_node)
            network_id = header.from_node

            node = {"node_id": node_id, "network_id": network_id}

            print(node_id)
            print(network_id)
            print(self.new_nodes)

            index_network = get_index(self.new_nodes, network_id, "network_id")
            index_node = get_index(self.new_nodes, node_id, "node_id")

            if index_node != -1 or node in self.new_nodes:
                self.new_nodes.pop(index_node)

            # If node is already inside new_nodes but mesh_id not updateted
            if index_network != -1:
                self.mesh.write(
                    struct.pack("i", self.new_nodes[index_network]["node_id"]), 90, 255
                )

            # If node is not inside new_nodes and mesh_id is 255
            if node_id == 255 and index_network == -1:
                req = requests.post(
                    "http://127.0.0.1:5000/nodes", data={"type": "test"}
                )
                req_json = req.json()

                node["node_id"] = int(req_json["id"])

                self.new_nodes.append(node)
                self.mesh.write(struct.pack("i", int(req_json["id"])), 90, 255)

            payload_converted = convert_payload(payload, header.type)

            result = dict()
            result["payload"] = payload_converted
            result["node_id"] = node_id

            print(result)
            req = requests.post("http://127.0.0.1:5000/data", data=result)