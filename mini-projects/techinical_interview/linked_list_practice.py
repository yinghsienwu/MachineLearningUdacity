# The LinkedList code #

class Element(object):
    def __init__(self,value):
        self.value=value
        self.next=None

class LinkedList(object):
    def __init__(self,head=None):
        self.head=head

    def append(self,new_element):
        # append the new_element at the end
        current=self.head
        if self.head:
            while current.next:
                curren=current.next 
                #iterate through the next element until the end
            current.next=new_element
            # put the new_element at the end
        else:
            self.head=new_element 

    def get_position(self,position):
        # get the element with the given position
        # return None if position is not in the list
        current=self.head
        ct=1 # length of iterated elements
        if position<1:
            return None
        while current and ct<=position: 
            if position==ct:
                return current  
            current=current.next
            ct+=1
        return None

    def insert(self,new_element,position):
        # insert a new node at the given position
        current=self.head
        ct=1
        if position >1:
            while current and position >ct:
                if (position-1)==ct:
                    new_element.next=current.next
                    current.next=new_element
                current=current.next
                ct+=1
        elif position==1:
            new_element.next=self.head
            self.head=new_element

    def delete(self,value):
        # delete the first node with a given value
        current=self.head
        previous=None
        while current.value!=value and current.next:
            previous=current
            current=current.next
            # iterate through the list until current.value==value
        if current.value==value:
            if previous: # delete the value (which is not the 1st one)
                previous.next=current.next
            else:  # delete 1st element
                self.head=current.next

# Test cases
# Set up some Elements
e1= Element(1)
e2= Element(2)
e3= Element(3)
e4= Element(4)

# Start setting up a LinkedList
ll=LinkedList(e1)  # 1
ll.append(e2)      #1=>2
ll.append(e3)      #1=>2=>3

# Test get_position
print ll.head.next.next.value  #should print 3
print ll.get_position(3).value # should also print 3

# Test insert
ll.insert(e4,3)  #1=>2=>4=>3
print ll.get_position(3).value # should print 4 now

# Test delete
ll.delete(1)  # 2=>4=>3
print ll.get_position(1).value # should print 2
print ll.get_position(2).value # should print 4
print ll.get_position(3).value # should print 3




            

