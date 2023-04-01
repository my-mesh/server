from app.threads.base import BackgroundThread
from app.threads.mesh import MeshThread


class BackgroundThreadFactory:
    @staticmethod
    def create(thread_type: str) -> BackgroundThread:
        if thread_type == "notification":
            return MeshThread()

        raise NotImplementedError("Specified thread type is not implemented.")
