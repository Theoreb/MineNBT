class Stream:
    """A simple byte stream reader that allows reading and peeking operations within byte data."""
    
    def __init__(self, data: bytes):
        """
        Initialize the Stream with binary data.

        Args:
            data (bytes): The binary data to be read.
        """
        self.data = data
        self.index = 0

    def read(self, size: int) -> bytes:
        """
        Reads a specified number of bytes from the stream, advancing the position.

        Args:
            size (int): The number of bytes to read.
        """
        if self.index + size > len(self.data):
            raise EOFError("Attempt to read beyond the end of the stream")
        
        result = self.data[self.index:self.index+size]
        self.index += size
        return result
    
    def peek(self, size: int) -> bytes:
        """
        Peeks at the next specified number of bytes in the stream without advancing the position.

        Args:
            size (int): The number of bytes to peek at.
        """
        if self.index + size > len(self.data):
            raise EOFError("Attempt to peek beyond the end of the stream")
        
        result = self.data[self.index:self.index+size]
        return result
    
    def alive(self) -> bool:
        """
        Checks if there are more bytes to read in the stream.

        Returns:
            bool: True if there are more bytes to read; False otherwise.
        """
        return self.index < len(self.data)