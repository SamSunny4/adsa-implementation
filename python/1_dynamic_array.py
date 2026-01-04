"""
Dynamic Array Implementation in Python
Demonstrates automatic resizing with doubling/halving capacity
"""

# Remove the DynamicArray class and replace with equivalent functions and variables
arr = [None]
size = 0
capacity = 1

def show():
    """Display current array state"""
    elements = [str(arr[i]) for i in range(size)]
    print(f"sz={size} cap={capacity} [{','.join(elements)}]")

def resize(new_capacity):
    """Resize the internal array to new capacity"""
    global arr, capacity
    new_arr = [None] * new_capacity
    for i in range(size):
        new_arr[i] = arr[i]
    arr = new_arr
    capacity = new_capacity

def push(value):
    """Add element to the end of array"""
    global size, capacity
    if size == capacity:
        resize(capacity * 2)
    arr[size] = value
    size += 1
    show()

def pop():
    """Remove element from the end of array"""
    global size, capacity
    if size == 0:
        print("Array is empty!")
        return
    size -= 1
    if size > 0 and size <= capacity // 4:
        resize(capacity // 2)
    show()

def main():
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
                push(value)
            elif choice == 2:
                pop()
            elif choice == 3:
                show()
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
