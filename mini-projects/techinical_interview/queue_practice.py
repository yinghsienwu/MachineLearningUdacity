"""Make a Queue class using a list!
Hint: You can use any Python list method
you'd like! Try to write each one in as 
few lines as possible.
Make sure you pass the test cases too!"""
class Queue:
    def __init__(self,head=None):
        self.storage=[head]

    def enqueue(self,new_element):
        self.storage.append(new_element)

    def peek(self):
        return self.storage[0]

    def dequeue(self):
        temp=self.storage[0]
        self.storage=self.storage[1:]
        return temp

# Setup
q=Queue(1)    #[1]
q.enqueue(2)  #[1,2]
q.enqueue(3)  #[1,2,3]

# Test peek
# should be 1
print q.peek()

# Test dequeue
# should be 1, then q=[2,3]
print q.dequeue()  

# Test enqueue
q.enqueue(4)  # q=[2,3,4]
# should be 2, then q=[3,4]
print q.dequeue()
# should be 3, then q=[4]
print q.dequeue()
# should be 4, then q=None
print q.dequeue()
q.enqueue(5)  # now q=[5]
# should be 5
print q.peek()
