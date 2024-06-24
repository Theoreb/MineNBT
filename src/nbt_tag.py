import struct
from typing import Dict, List, Type
from nbt.stream import Stream


def read_string(stream: Stream) -> str:
    """Reads a UTF-8 string from a binary stream, prefixed with its length as a short."""
    length = struct.unpack(">h", stream.read(2))[0]
    return stream.read(length).decode("utf-8")


class Tag:
    TAG_ID: int = None
    TAG_NAME: str = "TAG_Unknown"

    def build(self) -> bytes:
        """Builds the binary representation of the tag including its header and content."""
        if self.__class__ == Tag or self.TAG_ID is None:
            raise NotImplementedError(
                "Subclasses of Tag must implement TAG_ID and cannot be Tag directly")

        head = struct.pack(">b", self.TAG_ID)
        if self.__class__ != TagEnd:
            head += struct.pack(">h", len(self.name)) + \
                self.name.encode("utf-8")
        return head + self.write()

    @staticmethod
    def create(stream: Stream) -> 'Tag':
        """Factory method to create a specific Tag based on its ID read from the stream."""
        type_id = stream.read(1)[0]
        if type_id not in TAG_MAP:
            raise NotImplementedError(f"Tag type {type_id} is not implemented")
        return TAG_MAP[type_id].read(stream)


class TagEnd(Tag):
    """Represents the end of a TAG_Compound."""
    SIZE: int = None
    TAG_ID: int = 0x00
    TAG_NAME: str = "TAG_End"

    def write(self) -> bytes:
        """Returns an empty byte string as there is no content in a TagEnd."""
        return b""

    def read(self) -> "TagEnd":
        """Reads and returns a TagEnd instance from the stream."""
        return TagEnd()

    def __json__(self) -> dict:
        return {"type": "TAG_End"}

    def __repr__(self):
        return "[TAG_End]"


class TagByte(Tag):
    """
    A single signed byte 
    """
    SIZE: int = 1
    TAG_ID: int = 0x01
    TAG_NAME: str = "TAG_Byte"

    def __init__(self, name: str, payload: int):
        self.name: str = name
        self.payload: int = payload

    @staticmethod
    def read(stream: Stream, named: bool = True) -> 'TagByte':
        """Reads and returns a TagByte instance from the stream."""
        name = read_string(stream) if named else ""
        payload = struct.unpack(">b", stream.read(1))[0]
        return TagByte(name, payload)

    def write(self) -> bytes:
        """Writes the TagByte payload to bytes."""
        return struct.pack(">b", self.payload)

    def __json__(self) -> dict:
        return {"type": "TAG_Byte", "name": self.name, "payload": self.payload}

    def __repr__(self):
        return f"TAG_Byte({self.name}): {self.payload}"


class TagShort(Tag):
    """
    A single signed, big endian 16 bit integer 
    """
    SIZE: int = 2
    TAG_ID: int = 0x02
    TAG_NAME: str = "TAG_Short"

    def __init__(self, name: str, payload: int):
        self.name: str = name
        self.payload: int = payload

    @staticmethod
    def read(stream: Stream, named: bool = True) -> "TagShort":
        """Reads and returns a TagShort instance from the stream."""
        name = read_string(stream) if named else None
        return TagShort(name, struct.unpack(">h", stream.read(2))[0])

    def write(self) -> bytes:
        """Writes the TagShort payload to bytes."""
        return struct.pack(">h", self.payload)

    def __json__(self) -> dict:
        return {"type": "TAG_Short", "name": self.name, "payload": self.payload}

    def __repr__(self):
        return f"TAG_Short({self.name}): {self.payload}"


class TagInt(Tag):
    """
    A single signed, big endian 32 bit integer 
    """
    SIZE: int = 4
    TAG_ID: int = 0x03
    TAG_NAME: str = "TAG_Int"

    def __init__(self, name: str, payload: int):
        self.name: str = name
        self.payload: int = payload

    @staticmethod
    def read(stream: Stream, named: bool = True) -> "TagInt":
        """Reads and returns a TagInt instance from the stream."""
        name = read_string(stream) if named else None
        return TagInt(name, struct.unpack(">i", stream.read(4))[0])

    def write(self) -> bytes:
        """Writes the TagInt payload to bytes."""
        return struct.pack(">i", self.payload)

    def __json__(self) -> dict:
        return {"type": "TAG_Int", "name": self.name, "payload": self.payload}

    def __repr__(self):
        return f"TAG_Int({self.name}): {self.payload}"


class TagLong(Tag):
    """
    A single signed, big endian 64 bit integer 
    """
    SIZE: int = 8
    TAG_ID: int = 0x04
    TAG_NAME: str = "TAG_Long"

    def __init__(self, name: str, payload: int):
        self.name: str = name
        self.payload: int = payload

    @staticmethod
    def read(stream: Stream, named: bool = True) -> "TagLong":
        """Reads and returns a TagLong instance from the stream."""
        name = read_string(stream) if named else None
        return TagLong(name, struct.unpack(">q", stream.read(8))[0])

    def write(self) -> bytes:
        """Writes the TagLong payload to bytes."""
        return struct.pack(">q", self.payload)

    def __json__(self) -> dict:
        return {"type": "TAG_Long", "name": self.name, "payload": self.payload}

    def __repr__(self):
        return f"TAG_Long({self.name}): {self.payload}"


class TagFloat(Tag):
    """
    A single, big endian IEEE-754 single-precision floating point number (NaN possible) 
    """
    SIZE: int = 4
    TAG_ID: int = 0x05
    TAG_NAME: str = "TAG_Float"

    def __init__(self, name: str, payload: float):
        self.name: str = name
        self.payload: float = payload

    @staticmethod
    def read(stream: Stream, named: bool = True) -> "TagFloat":
        """Reads and returns a TagFloat instance from the stream."""
        name = read_string(stream) if named else None
        return TagFloat(name, struct.unpack(">f", stream.read(4))[0])

    def write(self) -> bytes:
        """Returns the TagFloat payload as bytes."""
        return struct.pack(">f", self.payload)

    def __json__(self) -> dict:
        return {"type": "TAG_Float", "name": self.name, "payload": self.payload}

    def __repr__(self):
        return f"TAG_Float({self.name}): {self.payload}"


class TagDouble(Tag):
    """
    A single, big endian IEEE-754 double-precision floating point number (NaN possible) 
    """
    SIZE: int = 8
    TAG_ID: int = 0x06
    TAG_NAME: str = "TAG_Double"

    def __init__(self, name: str, payload: float):
        self.name: str = name
        self.payload: float = payload

    @staticmethod
    def read(stream: Stream, named: bool = True) -> "TagDouble":
        """Reads and returns a TagDouble instance from the stream."""
        name = read_string(stream) if named else None
        return TagDouble(name, struct.unpack(">d", stream.read(8))[0])

    def write(self) -> bytes:
        """Returns the TagDouble payload as bytes."""
        return struct.pack(">d", self.payload)

    def __json__(self) -> dict:
        return {"type": "TAG_Double", "name": self.name, "payload": self.payload}

    def __repr__(self):
        return f"TAG_Double({self.name}): {self.payload}"


class TagByteArray(Tag):
    """
    A length-prefixed array of signed bytes. The prefix is a signed integer (thus 4 bytes) 
    """
    SIZE: int = None
    TAG_ID: int = 0x07
    TAG_NAME: str = "TAG_Byte_Array"

    def __init__(self, name: str, payload: list[int]):
        self.name: str = name
        self.payload: list[int] = payload
        self.SIZE = len(payload)

    @staticmethod
    def read(stream: Stream, named: bool = True) -> "TagByteArray":
        """Reads and returns a TagByteArray instance from the stream."""
        name = read_string(stream) if named else None
        length = struct.unpack(">i", stream.read(4))[0]
        if length < 0:
            raise ValueError("Negative length in TagByteArray")

        data = Stream(stream.read(length))
        payload = [struct.unpack(">b", data.read(1))[0] for _ in range(length)]
        return TagByteArray(name, payload)

    def write(self) -> bytes:
        """Writes the TagByteArray payload to bytes."""
        # All values should be TagByte
        data = b''.join(struct.pack(">b", value) for value in self.payload)
        return struct.pack(">i", len(self.payload)) + data

    def __json__(self) -> dict:
        # All values should be TagByte
        return {"type": "TAG_ByteArray", "name": self.name, "payload": [value for value in self.payload]}

    def __repr__(self) -> str:
        console = f"TAG_ByteArray({repr(self.name)}) (entries: {len(self.payload)})\n["
        for value in self.payload[:-1]:
            console += hex(value) + ", "
        return console + hex(value) + "]"


class TagString(Tag):
    """
    A length-prefixed modified UTF-8 string.
    The prefix is an unsigned short (thus 2 bytes) signifying the length of the string in bytes 
    """
    SIZE: int = None
    TAG_ID: int = 0x08
    TAG_NAME: str = "TAG_String"

    def __init__(self, name: str, payload: str):
        self.name: str = name
        self.payload: str = payload
        self.SIZE = len(payload)

    @staticmethod
    def read(stream: Stream, named: bool = True) -> "TagString":
        """Reads and returns a TagString instance from the stream."""
        name = read_string(stream) if named else None
        return TagString(name, read_string(stream))

    def write(self) -> bytes:
        """Writes the TagString payload to bytes."""
        return struct.pack(">h", len(self.payload)) + self.payload.encode("utf-8")

    def __json__(self) -> dict:
        return {"type": "TAG_String", "name": self.name, "payload": self.payload}

    def __repr__(self) -> str:
        return f"TAG_String({self.name}): {repr(self.payload)}"


class TagList(Tag):
    """
    A list of nameless tags, all of the same type.
    The list is prefixed with the Type ID of the items it contains (thus 1 byte),
    and the length of the list as a signed integer (a further 4 bytes).

    If the length of the list is 0 or negative, the type may be 0 (TAG_End)
    but otherwise it must be any other type.
    (The notchian implementation uses TAG_End in that situation,
    but another reference implementation by Mojang uses 1 instead;
    parsers should accept any type if the length is <= 0). 
    """
    SIZE: int = None
    TAG_ID: int = 0x09
    TAG_NAME: str = "TAG_List"

    def __init__(self, name: str, payload: list[Tag]):
        self.name: str = name
        self.payload: list[Tag] = payload

    @staticmethod
    def read(stream: Stream, named: bool = True) -> "TagList":
        """Reads and returns a TagList instance from the stream."""
        name = read_string(stream) if named else None
        tag_id = stream.read(1)[0]
        if not tag_id in TAG_MAP:
            raise NotImplementedError(f"Tag type {tag_id} is not implemented")

        length = struct.unpack(">i", stream.read(4))[0]
        payload: list[Tag] = []
        if length > 0:
            tag_type = TAG_MAP[tag_id]
            payload = [tag_type.read(stream, named=False)
                       for _ in range(length)]

        return TagList(name, payload)

    def write(self) -> bytes:
        """Writes the TagList payload to bytes."""
        if len(self.payload) == 0:
            return bytes([0x00])

        tag_type = self.payload[0].__class__
        if not all(isinstance(tag, tag_type) for tag in self.payload):
            raise ValueError(
                f"All tags in a TAG_List must be of the same type: {tag_type}")

        return bytes([tag_type.TAG_ID]) + struct.pack(">i", len(self.payload)) + b''.join(tag.write() for tag in self.payload)

    def __json__(self) -> dict:
        # All values should be the same type
        if len(self.payload) == 0:
            tag_type = "TAG_End"
        else:
            tag_type = self.payload[0].__class__
        return {"type": "TAG_List", "name": self.name, "data_type": tag_type.TAG_NAME, "payload": [tag.__json__()["payload"] for tag in self.payload]}

    def __repr__(self) -> str:
        console = f"TAG_List({repr(self.name)}) (endries: {len(self.payload)})\n["
        for tag in self.payload:
            console += "\n   " + repr(tag).replace('\n', '\n   ')
        return console + "\n]"


class TagCompound(Tag):
    """
    A list of named tags. Order is not guaranteed. 
    """
    SIZE: int = None
    TAG_ID: int = 0x0a
    TAG_NAME: str = "TAG_Compound"

    def __init__(self, name: str, payload: list[Tag]):
        self.name: str = name
        self.payload: list[Tag] = payload

    @staticmethod
    def read(stream: Stream, named: bool = True) -> "TagCompound":
        """Reads and returns a TagCompound instance from the stream."""
        name = read_string(stream) if named else None
        payload: list[Tag] = []
        while True:
            tag = Tag.create(stream)
            if tag.TAG_ID == TagEnd.TAG_ID:
                break
            payload.append(tag)
        return TagCompound(name, payload)

    def write(self) -> bytes:
        """Writes the TagCompound payload to bytes."""
        return b''.join(tag.build() for tag in self.payload) + TagEnd().build()

    def __json__(self) -> dict:
        return {"type": "TAG_Compound", "name": self.name, "payload": [tag.__json__() for tag in self.payload]}

    def __repr__(self) -> str:
        console = f"TAG_Compound({repr(self.name)}) (entries: {len(self.payload)})\n["
        for tag in self.payload:
            console += "\n   " + repr(tag).replace('\n', '\n   ')
        return console + "\n]"


class TagIntArray(Tag):
    """
    A length-prefixed array of signed integers.
    The prefix is a signed integer (thus 4 bytes) and indicates the number of 4 byte integers. 
    """
    SIZE: int = None
    TAG_ID: int = 0x0b
    TAG_NAME: str = "TAG_IntArray"

    def __init__(self, name: str, payload: list[int]):
        self.name: str = name
        self.payload: list[int] = payload
        self.SIZE = len(payload)

    @staticmethod
    def read(stream: Stream, named: bool = True) -> "TagIntArray":
        """Reads and returns a TagIntArray instance from the stream."""
        name = read_string() if named else None
        length = struct.unpack(">i", stream.read(4))[0]
        if length < 0:
            raise ValueError("TAG_IntArray length must be >= 0")

        data = Stream(stream.read(length))
        payload = [struct.unpack(">i", data.read(4))[0] for _ in range(length)]
        return TagIntArray(name, payload)

    def write(self) -> bytes:
        """Writes the TagIntArray payload to bytes."""
        # All tags in a TAG_IntArray must be of type TagInt
        data = b''.join(struct.pack(">i", value) for value in self.payload)
        return struct.pack(">i", len(self.payload)) + data

    def __json__(self) -> dict:
        # All values should be TagInt
        return {"type": "TAG_IntArray", "name": self.name, "payload": [value for value in self.payload]}

    def __repr__(self) -> str:
        console = f"TAG_IntArray({repr(self.name)}) (entries: {len(self.payload)})\n["
        for value in self.payload[:-1]:
            console += repr(value) + ", "
        return console + repr(value) + "]"


class TagLongArray(Tag):
    """
    A length-prefixed array of signed longs.
    The prefix is a signed integer (thus 4 bytes) and indicates the number of 8 byte longs. A length-prefixed array of signed longs. The prefix is a signed integer (thus 4 bytes) and indicates the number of 8 byte longs. 
    """
    SIZE: int = None
    TAG_ID: int = 0x0c
    TAG_NAME: str = "TAG_LongArray"

    def __init__(self, name: str, payload: list[int]):
        self.name: str = name
        self.payload: list[int] = payload
        self.SIZE = len(payload)

    @staticmethod
    def read(stream: Stream, named: bool = True) -> "TagLongArray":
        """Reads and returns a TagLongArray instance from the stream."""
        name = read_string() if named else None
        length = struct.unpack(">i", stream.read(4))[0]
        if length < 0:
            raise ValueError("TAG_LongArray length must be >= 0")

        data = Stream(stream.read(length))
        payload = [struct.unpack(">q", data.read(8))[0] for _ in range(length)]
        return TagLongArray(name, payload)

    def write(self) -> bytes:
        """Writes the TagLongArray payload to bytes."""
        # All tags in a TAG_LongArray must be of type TagLong
        data = b''.join(struct.pack(">q", value) for value in self.payload)
        return struct.pack(">i", len(self.payload)) + data

    def __json__(self) -> dict:
        # All values should be TagLong
        return {"type": "TAG_LongArray", "name": self.name, "payload": [value for value in self.payload]}

    def __repr__(self) -> str:
        console = f"TAG_LongArray({repr(self.name)}) (entries: {len(self.payload)})\n["
        for value in self.payload[:-1]:
            console += repr(value) + ", "
        return console + repr(value) + "]"


TAG_MAP: dict[int, Type[Tag]] = {
    0x00: TagEnd,
    0x01: TagByte,
    0x02: TagShort,
    0x03: TagInt,
    0x04: TagLong,
    0x05: TagFloat,
    0x06: TagDouble,
    0x07: TagByteArray,
    0x08: TagString,
    0x09: TagList,
    0x0a: TagCompound,
    0x0b: TagIntArray,
    0x0c: TagLongArray
}
