from buffer_reader import BufferReader

reader=BufferReader("input.txt",100)
i=0
while (reader.has_next()):
    print(f"char {i} is: {reader.get_next_char()}")
    i+=1


