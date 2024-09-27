from abc import ABC, abstractmethod


class MediaFile(ABC):
    def __init__(self, filepath):
        self.filepath = filepath

    @abstractmethod
    def get_output_destination(self, output_path: str) -> str:
        pass
