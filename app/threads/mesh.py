from app.threads.base import BackgroundThread

from pyrf24 import RF24, RF24Network, RF24Mesh

class MeshThread(BackgroundThread):
    def startup(self) -> None:
        self.radio = RF24(22, 0)
        self.network = RF24Network(self.radio)
        self.mesh = RF24Mesh(self.radio, self.network)
        self.mesh.node_id = 0

        if not self.mesh.begin():
            raise OSError("Radio hardware not responding.")
        print("NotificationThread started")

    def shutdown(self) -> None:
        self.power = False
        print("NotificationThread stopped")

    def handle(self) -> None:
        while True:
            self.mesh.update()
            self.mesh.dhcp()

            while self.network.available():
                header, payload = self.network.read()
                print(f"Received message {header.to_string()}")
