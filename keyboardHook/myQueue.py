

class Node:
    def __init__(self, value, next=None):
        self.value = value
        self.next = next





class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0


    def peek(self, depth=1):
        nextNode = self.head
        for i in range(depth-1):
            if not nextNode:
                return None
            nextNode = nextNode.next
        if not nextNode:
            return None
        return nextNode.value

    def push(self, val):
        newItem = Node(val)
        if self.empty():
            self.head = newItem
            self.tail = newItem
        else:
            self.tail.next = newItem
            self.tail = newItem
        self.size += 1


    def pop(self):
        if self.size:
            val = self.head.value
            if self.head is self.tail:
                self.tail = None
            self.head = self.head.next
            self.size -= 1
            return val
        return None

    def drop(self):
        self.pop()


    def empty(self):
        return self.size == 0





if __name__ == "__main__":
    queue = Queue()

    queue.push(1)
    queue.push(2)
    queue.push(3)

    assert queue.size == 3
    assert queue.pop() == 1
    assert queue.pop() == 2
    assert queue.pop() == 3
    assert queue.size == 0
    assert queue.pop() is None

    queue.push(1)
    queue.push(2)
    queue.push(3)

    assert queue.peek() == 1
    assert queue.peek(2) == 2
    assert queue.peek(3) == 3
    assert queue.peek(4) == None


