# Advanced Data Structures and Algorithms Implementation

## Files

### 1. [1_dynamic_array.cpp](1_dynamic_array.cpp)
Dynamic array implementation with automatic resizing (doubling/halving capacity).

### 2. [2_dictionary_dynamic_array.cpp](2_dictionary_dynamic_array.cpp)
Dictionary implementation using dynamic arrays for key-value storage.

### 3. [3_perfect_hashing_fks.cpp](3_perfect_hashing_fks.cpp)
**FKS Algorithm - Two-Level Perfect Hashing**

Perfect hashing implementation providing O(1) worst-case lookup time.

#### Algorithm Overview:
- **Level 1**: Primary hash table with n buckets using universal hash function
- **Level 2**: For each bucket with k keys, create secondary hash table of size k²
  - Guarantees collision-free hashing by design
  - Uses trial-and-error to find collision-free hash function parameters
  - Secondary table size k² ensures high probability of finding such function

#### Key Characteristics:
- **Lookup Time**: O(1) worst-case
- **Insertion Time**: O(1) average-case
- **Space Complexity**: O(n)
- **Universal Hashing**: Uses parameterized hash functions at both levels
- **Collision Resolution**: Theoretical guarantee of no collisions

#### Hash Functions Used:
```
h(x) = (a·x + b) mod p
```
Where a, b are randomly chosen parameters and p is a large prime.

#### Practical Applications:
- Static dictionary construction
- Compiler symbol tables
- Database indexing
- IP routing tables
- Perfect hash code generation
