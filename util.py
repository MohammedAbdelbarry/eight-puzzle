from typing import List
from collections import deque
import heapq

class Stack:
    "A container with a last-in-first-out (LIFO) queuing policy."
    def __init__(self):
        self.stack = []
        
    def push(self, item):
        "Push 'item' onto the stack."
        self.stack.append(item)
        
    def pop(self):
        "Pop the most recent pushed item from the stack."
        return self.stack.pop()
        
    def size(self):
        "Return the current size of the stack."
        return len(self.stack)
    
    def is_empty(self):
        "Return true if the stack is empty."
        return len(self.stack) == 0
    
    
class Queue:
    "A container with a first-in-first-out (FIFO) queuing policy."
    def __init__(self):
        self.queue = deque([])
        
    def push(self, item):
        "Push 'item' into the right end of the deque."
        self.queue.append(item)
        
    def pop(self):
        "Pop and return the first item from the left end of the deque."
        return self.queue.popleft()
    
    def size(self):
        "Return the current size of the queue."
        return len(self.queue)
    
    def is_empty(self):
        "Return true if the queue is empty."
        return len(self.queue) == 0
    
    
class PriorityQueue:
    """
        Implement a priority queue data structure. Each inserted item
        has a priority associated with it as well as a count to ensure that
        equal priority items to be popped in the same order they were originally
        inserted to the priority queue.
    """
    def __init__(self):
        self.heap = []
        self.count = 0
    
    def push(self, item, priority):
        "Push 'item' with 'priority' into the priority queue."
        heapq.heappush(self.heap, (priority, self.count, item))
        self.count += 1
        
    def pop(self):
        "Pop and return the item with the smallest priority from the priority queue."
        (_, _, item) = heapq.heappop(self.heap)
        return item
    
    def size(self):
        "Return the current size of the priority queue."
        return len(self.heap)
    
    def is_empty(self):
        "Return true if the priority queue is empty."
        return len(self.heap) == 0


def is_sorted(l: List[int]) -> bool:
    """
    Checks if a list is sorted or not
    :param l: The list to be checked
    :return: a bool indicating whether the list is sorted or not
    """
    return all(a <= b for a, b in zip(l, l[1:]))
