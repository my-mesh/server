import struct
import requests
from app.threads.base import BackgroundThread

from pyrf24 import RF24, RF24Network, RF24Mesh


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

            mesh_id = self.mesh.get_node_id(header.from_node)
            node_id = header.from_node

            node = {"node_id": node_id, "mesh_id": mesh_id}

            # If node is not 255 and already inside new_nodes
            if node in self.new_nodes and mesh_id != 255:
                print("remove node")
                self.new_nodes.remove(node)

            # Get index of node in new_nodes
            index = next(
                (
                    i
                    for i, obj in enumerate(self.new_nodes)
                    if obj["node_id"] == node_id
                ),
                -1,
            )

            # If node is already inside new_nodes but mesh_id not updateted
            if index != -1 and mesh_id == 255:
                print("write mesh id second time")
                self.network.write(struct.pack("i", self.new_nodes[index]["mesh_id"]))

            # If node is not inside new_nodes and mesh_id is 255
            if index == -1 and mesh_id == 255:
                print("write mesh id first time")
                req = requests.post(
                    "http://127.0.0.1:5000/nodes", data={"type": "test"}
                )
                req_json = req.json()
                node["mesh_id"] = req_json["id"]
                self.new_nodes.append(node)
                self.network.write(struct.pack("i", req_json["id"]))

            print(f"Received message {header.to_string()}")
