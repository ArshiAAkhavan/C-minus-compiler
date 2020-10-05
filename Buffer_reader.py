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

        print(f"pointer={self.buffer_pointer}")
        next_char=self.buffer[self.buffer_pointer]    
        self.buffer_pointer+=1
        
        return next_char

    def refill_buffer(self):
        self.buffer = self.input_file.read(self.buffer_size)
        self.buffer_pointer=0



b=Buffer_reader("input.txt",3)
for i in range(1,20,1):
    print(b.get_next_char()+"\n")