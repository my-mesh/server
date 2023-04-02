import struct
import requests
from app.threads.base import BackgroundThread

#from pyrf24 import RF24, RF24Network, RF24Mesh

from app.utils.payload import convert_payload


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
            index = -1

            header, payload = self.network.read()
            mesh_id = self.mesh.get_node_id(header.from_node)

            if mesh_id in self.new_nodes and mesh_id != 255:
                print("remove node")
                self.new_nodes.remove(mesh_id)

            try:
                index = self.new_node.index(mesh_id)
            except:
                print("no index")

            # If node is already inside new_nodes but mesh_id not updateted
            if mesh_id in self.new_nodes and mesh_id == 255:
                print("write mesh id second time")
                self.mesh.write(
                    struct.pack("i", self.new_nodes[index]["mesh_id"]), 90, 255
                )

            # If node is not inside new_nodes and mesh_id is 255
            if mesh_id not in self.new_nodes and mesh_id == 255:
                print("write mesh id first time")
                req = requests.post(
                    "http://127.0.0.1:5000/nodes", data={"type": "test"}
                )
                req_json = req.json()

                self.new_nodes.append(int(req_json["id"]))

                self.mesh.write(struct.pack("i", int(req_json["id"])), 90, 255)

            payload_converted = convert_payload(payload, header.type)
            req = requests.post("http://127.0.0.1:5000/data", data=payload_converted)
            print(f"Received message {header.to_string()}")
