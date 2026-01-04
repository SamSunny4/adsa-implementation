"""
Dictionary Implementation using Dynamic Array in Python
Maps strings to integers with automatic resizing
"""

class Entry:
    """Represents a key-value pair in the dictionary"""
    def __init__(self, key, value):
        self.key = key
        self.value = value
    
    def __repr__(self):
        return f"({self.key}:{self.value})"


class Dictionary:
    def __init__(self):
        self.arr = [None]
        self.size = 0
        self.capacity = 1
    
    def show(self):
        """Display current dictionary state"""
        elements = [str(self.arr[i]) for i in range(self.size)]
        print(f"sz={self.size} cap={self.capacity} [{','.join(elements)}]")
    
    def resize(self, new_capacity):
        """Resize the internal array to new capacity"""
        new_arr = [None] * new_capacity
        for i in range(self.size):
            new_arr[i] = self.arr[i]
        self.arr = new_arr
        self.capacity = new_capacity
    
    def find_index(self, key):
        """Find the index of a key in the array"""
        for i in range(self.size):
            if self.arr[i].key == key:
                return i
        return -1
    
    def set(self, key, value):
        """Set a key-value pair (insert or update)"""
        idx = self.find_index(key)
        if idx != -1:
            # Update existing key
            self.arr[idx].value = value
        else:
            # Insert new key
            if self.size == self.capacity:
                self.resize(max(1, self.capacity * 2))
            self.arr[self.size] = Entry(key, value)
            self.size += 1
        self.show()
    
    def get(self, key):
        """Get the value associated with a key"""
        idx = self.find_index(key)
        if idx == -1:
            print("Key not found")
        else:
            print(self.arr[idx].value)
    
    def erase(self, key):
        """Remove a key-value pair from the dictionary"""
        idx = self.find_index(key)
        if idx == -1:
            print("Key not found")
            return
        
        # Move last element to deleted position
        self.arr[idx] = self.arr[self.size - 1]
        self.size -= 1
        
        # Shrink if needed
        if self.size > 0 and self.size <= self.capacity // 4:
            self.resize(max(1, self.capacity // 2))
        self.show()


def main():
    dictionary = Dictionary()
    
    print("Dictionary (string->int) using dynamic array")
    print("1: set key value")
    print("2: get key")
    print("3: erase key")
    print("4: show")
    print("5: exit\n")
    
    while True:
        try:
            command = input("> ").strip().split()
            
            if not command:
                continue
            
            cmd = int(command[0])
            
            if cmd == 1:
                # set key value
                if len(command) < 3:
                    key = input("Enter key: ")
                    value = int(input("Enter value: "))
                else:
                    key = command[1]
                    value = int(command[2])
                dictionary.set(key, value)
            
            elif cmd == 2:
                # get key
                if len(command) < 2:
                    key = input("Enter key: ")
                else:
                    key = command[1]
                dictionary.get(key)
            
            elif cmd == 3:
                # erase key
                if len(command) < 2:
                    key = input("Enter key: ")
                else:
                    key = command[1]
                dictionary.erase(key)
            
            elif cmd == 4:
                # show
                dictionary.show()
            
            elif cmd == 5:
                # exit
                break
            
            else:
                print("Invalid command")
        
        except (ValueError, IndexError):
            print("Invalid input format!")
        except KeyboardInterrupt:
            print("\nExiting...")
            break


if __name__ == "__main__":
    main()
