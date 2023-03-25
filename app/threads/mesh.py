from app.threads.base import BackgroundThread

from pyrf24 import RF24, RF24Network, RF24Mesh

class MeshThread(BackgroundThread):
    def startup(self) -> None:
        self.radio = RF24(22, 10)
        self.network = RF24Network(self.radio)
        self.mesh = RF24Mesh(self.radio, self.network)
        self.mesh.node_id = 0

        if not self.mesh.begin():
            raise OSError("Radio hardware not responding.")
        print("Mesh started")

    def shutdown(self) -> None:
        self.power = False
        print("Mesh stopped")

    def handle(self) -> None:
        self.mesh.update()
        self.mesh.dhcp()

        if self.network.available():
            header, payload = self.network.read()
            print(f"Received message {header.to_string()}")
