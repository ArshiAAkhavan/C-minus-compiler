class Buffer_reader:

    def __init__(self, path, buffer_size=100,reserved_chunk=5):

        self.buffer_size = buffer_size
        self.buffer_pointer = 0
        self.buffer = []
        self.reserved_chunk=reserved_chunk

        self.input_file = open(path, "r")

        self.__refill_buffer()

    def push_back(self,char):
        if self.buffer_pointer>0:
            self.buffer_pointer-=1
        else:
            self.buffer=[].append(char)+self.buffer

    def get_next_char(self):
        if self.buffer_pointer == self.buffer_size:
            self.__refill_buffer()

        next_char = self.buffer[self.buffer_pointer]
        self.buffer_pointer += 1

        return next_char

    def __refill_buffer(self):
        self.buffer = self.input_file.read(self.buffer_size)
        self.buffer_pointer = 0

    def has_next(self):
        if self.buffer_pointer >= len(self.buffer):
            return False
        elif self.buffer_pointer < self.buffer_size:
            return True
        else:
            try:
                self.__refill_buffer()
            except Exception:
                return False
            return self.has_next()

if __name__ == "__main__":
    b = Buffer_reader("input.txt", 3)
    while(b.has_next()):
        print(b.get_next_char()+"\n")
        print(len(b.buffer))
