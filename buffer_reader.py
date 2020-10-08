class BufferReader:

    def __init__(self, path, buffer_size=100):

        self.buffer_size = buffer_size
        self.buffer_pointer = 0
        self.buffer = ""

        self.input_file = open(path, "r")

        self._refill_buffer()

    def push_back(self,char):
        if self.buffer_pointer>0:
            self.buffer_pointer-=1
        else:
            self.buffer=char+self.buffer

    def get_next_char(self):
        if self.buffer_pointer == len(self.buffer):
            self._refill_buffer()

        next_char = self.buffer[self.buffer_pointer]
        self.buffer_pointer += 1

        return next_char

    def _refill_buffer(self):
        self.buffer = self.input_file.read(self.buffer_size)
        if len(self.buffer)<self.buffer_size:
            self.buffer+=chr(26)
        self.buffer_pointer = 0

    def has_next(self):
        if self.buffer_pointer < len(self.buffer):
            return True
        elif self.buffer_pointer > len(self.buffer):
            return False
        elif len(self.buffer)<self.buffer_size:
            return False
        else:
            try:
                self._refill_buffer()
                return self.has_next()
            except Exception:
                return False

if __name__ == "__main__":
    b = BufferReader("input.txt", 3)
    while(b.has_next()):
        print(f"buffer length:{len(b.buffer)}")
        print(b.get_next_char()+"\n")
    
    
    b= BufferReader("input.txt",3)
    b.has_next()

    b.push_back("a")
    print(f"buffer length:{len(b.buffer)}")
    print(b.get_next_char()+"\n")
    b.push_back("a")
    print(b.get_next_char()+"\n")
    b.push_back("a")
    print(b.get_next_char()+"\n")
    b.push_back("a")
    print(b.get_next_char()+"\n")
    b.push_back("a")
    print(b.get_next_char()+"\n")
    b.push_back("a")