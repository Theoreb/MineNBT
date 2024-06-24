from typing import List
from nbt.stream import Stream
from nbt.nbt_tag import Tag


import gzip as gzip_module


class NBT:
    """A class representing a Named Binary Tag (NBT), a data format used in Minecraft.

    Attributes:
        data (bytes): Binary data representing NBT content.
        tags (List[Tag]): A list of Tag objects parsed from the data.
    """

    def __init__(self, data: bytes = b''):
        """Initialize an NBT object with optional binary data.

        Args:
            data (bytes): Initial binary data for the NBT object. Defaults to empty bytes.
        """
        self.data: bytes = data
        self.tags: list[Tag] = []
        self.read()

    @staticmethod
    def load(path: str, gzip: bool = False) -> 'NBT':
        """Reads NBT data from a file, optionally decompressing it if gzipped.

        Args:
            path (str): Path to the NBT data file.
            gzip_enabled (bool): True if the file is gzipped; otherwise, False.

        Returns:
            NBT: An initialized NBT object with data read from the file.
        """
        with open(path, 'rb') as f:
            data = f.read()
        if gzip:
            data = gzip_module.decompress(data)
        return NBT(data)
    
    def save(self, path: str, gzip: bool = False) -> None:
        """Writes the NBT data to a file, optionally compressing it if gzipped.

        Args:
            path (str): Path to the NBT data file.
            gzip_enabled (bool): True if the file should be gzipped; otherwise, False.
        """
        if gzip:
            self.data = gzip_module.compress(self.data)
        with open(path, 'wb') as f:
            f.write(self.data)

    def read(self) -> None:
        """Parses the binary data to populate the tags list with Tag objects."""
        stream = Stream(self.data)
        while stream.alive():
            self.tags.append(Tag.create(stream))
        return self.tags

    def add(self, tag: Tag):
        """Adds a Tag object to the NBT object.

        Args:
            tag (Tag): The Tag object to add.
        """
        self.tags.append(tag)

    def build(self) -> bytes:
        """Constructs the binary representation of the NBT from its Tag objects.

        Returns:
            bytes: The binary representation of the NBT data.
        """
        self.data = b"".join([tag.build() for tag in self.tags])
        return self.data

    def show(self) -> None:
        """Displays the tags in a human-readable format."""
        console = "[NBT]\n" + "\n".join(repr(tag) for tag in self.tags)
        print(console)

    def dict(self) -> dict:
        """Converts the tags to a JSON-compatible list format.

        Returns:
            List[dict]: A list of dictionaries representing the Tag objects in JSON format.
        """
        return [tag.__json__() for tag in self.tags]
