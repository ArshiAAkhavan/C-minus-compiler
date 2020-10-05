class Buffer_reader:
    
    def __init__(self,path,buffer_size):
        
        self.buffer_size=buffer_size
        self.buffer_pointer=0
        self.buffer=[]

        self.path=path
        self.input_file=open(self.path, "r")

        self.refill_buffer()        

    def get_next_char(self):
        if self.buffer_pointer == self.buffer_size:
            self.refill_buffer()

        next_char=self.buffer[self.buffer_pointer]    
        self.buffer_pointer+=1
        
        return next_char

    def refill_buffer(self):
        self.buffer = self.input_file.read(self.buffer_size)
        self.buffer_pointer=0

    def has_next(self):
        if self.buffer_pointer >= len(self.buffer):
            return False
        elif self.buffer_pointer <self.buffer_size:
             return True
        else:
            self.refill_buffer()
            return self.has_next()


if __name__=="__main__":
    b=Buffer_reader("input.txt",3)
    for i in range(1,40,1):
        print(b.get_next_char()+"\n")
        print(len(b.buffer))