"""
Dynamic Array Implementation in Python
Demonstrates automatic resizing with doubling/halving capacity
"""

class DynamicArray:
    def __init__(self):
        self.arr = [None]
        self.size = 0
        self.capacity = 1
    
    def show(self):
        """Display current array state"""
        elements = [str(self.arr[i]) for i in range(self.size)]
        print(f"sz={self.size} cap={self.capacity} [{','.join(elements)}]")
    
    def resize(self, new_capacity):
        """Resize the internal array to new capacity"""
        new_arr = [None] * new_capacity
        for i in range(self.size):
            new_arr[i] = self.arr[i]
        self.arr = new_arr
        self.capacity = new_capacity
    
    def push(self, value):
        """Add element to the end of array"""
        if self.size == self.capacity:
            self.resize(self.capacity * 2)
        self.arr[self.size] = value
        self.size += 1
        self.show()
    
    def pop(self):
        """Remove element from the end of array"""
        if self.size == 0:
            print("Array is empty!")
            return
        
        self.size -= 1
        if self.size > 0 and self.size <= self.capacity // 4:
            self.resize(self.capacity // 2)
        self.show()


def main():
    dyn_array = DynamicArray()
    
    print("Dynamic Array Operations:")
    print("1. Push value")
    print("2. Pop value")
    print("3. Show array")
    print("4. Exit\n")
    
    while True:
        try:
            choice = int(input("Enter choice: "))
            
            if choice == 1:
                value = int(input("Enter value: "))
                dyn_array.push(value)
            elif choice == 2:
                dyn_array.pop()
            elif choice == 3:
                dyn_array.show()
            elif choice == 4:
                break
            else:
                print("Invalid choice!")
        except ValueError:
            print("Please enter a valid number!")
        except KeyboardInterrupt:
            print("\nExiting...")
            break


if __name__ == "__main__":
    main()
