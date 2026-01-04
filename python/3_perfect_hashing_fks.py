"""
FKS Algorithm - Two-Level Perfect Hashing Implementation in Python

A practical implementation of perfect hashing that guarantees O(1)
worst-case lookup time using two levels of hashing.

Level 1: Primary hash table with n buckets using a universal hash function
Level 2: For each bucket k, create a secondary hash table of size k²
         to ensure collision-free hashing within that bucket
"""

import random
import time


class SecondaryTable:
    """Represents a secondary hash table for a bucket"""
    def __init__(self):
        self.table = []
        self.size = 0
        self.a = 0
        self.b = 0
        self.p = 0


class PerfectHashing:
    """FKS Perfect Hashing implementation with two-level hashing"""
    
    PRIME = 2147483647  # Large prime for universal hashing
    
    def __init__(self, primary_size=10):
        self.primary_size = primary_size
        self.buckets = [[] for _ in range(primary_size)]
        self.second_level = [SecondaryTable() for _ in range(primary_size)]
        
        # Initialize Level 1 hash function randomly
        random.seed(time.time())
        self.a1, self.b1 = self._randomize_hash_function()
    
    def _hash_function(self, key, a, b, p):
        """Universal hash function: h(x) = (a*x + b) mod p"""
        return (a * key + b) % p
    
    def _randomize_hash_function(self):
        """Generate random hash function parameters"""
        a = 1 + random.randint(1, self.PRIME - 2)
        b = random.randint(0, self.PRIME - 1)
        return a, b
    
    def _is_collision_free(self, keys, a, b, p, table_size):
        """Check if hash function h is collision-free for given keys"""
        hashed = set()
        for key in keys:
            h = self._hash_function(key, a, b, p) % table_size
            if h in hashed:
                return False
            hashed.add(h)
        return True
    
    def _build_secondary_table(self, bucket_idx):
        """Build the secondary hash table for a bucket"""
        keys = self.buckets[bucket_idx]
        k = len(keys)
        sec_table = self.second_level[bucket_idx]
        
        if k == 0:
            sec_table.size = 0
            return True
        
        if k == 1:
            # Single element - no collision possible
            sec_table.table = [keys[0]]
            sec_table.size = 1
            sec_table.a = 1
            sec_table.b = 0
            sec_table.p = self.PRIME
            return True
        
        # Try to find a collision-free hash function
        # Secondary table size is k²
        secondary_size = k * k
        max_attempts = 100
        
        for _ in range(max_attempts):
            a, b = self._randomize_hash_function()
            
            if self._is_collision_free(keys, a, b, self.PRIME, secondary_size):
                # Found a collision-free hash function
                sec_table.table = [-1] * secondary_size
                sec_table.size = secondary_size
                sec_table.a = a
                sec_table.b = b
                sec_table.p = self.PRIME
                
                # Place keys in secondary table
                for key in keys:
                    h = self._hash_function(key, a, b, self.PRIME) % secondary_size
                    sec_table.table[h] = key
                
                return True
        
        return False  # Couldn't find collision-free function
    
    def insert(self, key):
        """Insert key into the perfect hash table"""
        # Level 1: Insert into appropriate bucket
        bucket_idx = self._hash_function(key, self.a1, self.b1, self.PRIME) % self.primary_size
        self.buckets[bucket_idx].append(key)
        
        # Level 2: Rebuild secondary table for this bucket
        return self._build_secondary_table(bucket_idx)
    
    def search(self, key):
        """Search for a key in the perfect hash table"""
        # Level 1: Find the bucket
        bucket_idx = self._hash_function(key, self.a1, self.b1, self.PRIME) % self.primary_size
        
        # Level 2: Search in secondary table
        sec_table = self.second_level[bucket_idx]
        
        if sec_table.size == 0:
            return False
        
        h = self._hash_function(key, sec_table.a, sec_table.b, sec_table.p) % sec_table.size
        return sec_table.table[h] == key
    
    def display(self):
        """Display the hash table structure"""
        print("\n=== Perfect Hashing (FKS Algorithm) Structure ===")
        print(f"Primary Level: {self.primary_size} buckets\n")
        
        for i in range(self.primary_size):
            bucket_keys = self.buckets[i]
            print(f"Bucket {i} ({len(bucket_keys)} keys): {' '.join(map(str, bucket_keys))}")
            
            if len(bucket_keys) > 0:
                sec_table = self.second_level[i]
                print(f"  Secondary Table Size: {sec_table.size} | Hash Function: (a*x + b) mod {sec_table.p}")
                print(f"  Parameters: a={sec_table.a}, b={sec_table.b}")
                
                # Show non-empty slots
                slots = []
                for j in range(min(len(sec_table.table), 10)):
                    if sec_table.table[j] != -1:
                        slots.append(f"({j}:{sec_table.table[j]})")
                
                print(f"  Table Contents: [{' '.join(slots)}", end="")
                if len(sec_table.table) > 10:
                    print(" ...", end="")
                print("]\n")
        
        print()
    
    def statistics(self):
        """Display hash table statistics"""
        print("\n=== Hash Table Statistics ===")
        
        total_keys = sum(len(bucket) for bucket in self.buckets)
        avg_bucket_size = total_keys / self.primary_size if self.primary_size > 0 else 0
        max_bucket_size = max(len(bucket) for bucket in self.buckets) if self.buckets else 0
        
        print(f"Total Keys: {total_keys}")
        print(f"Primary Table Size: {self.primary_size}")
        print(f"Average Bucket Size: {avg_bucket_size:.2f}")
        print(f"Max Bucket Size: {max_bucket_size}")
        print(f"Load Factor: {total_keys / self.primary_size:.2f}")
        print()


def main():
    print("=" * 50)
    print("  FKS Perfect Hashing Algorithm Demo")
    print("  Two-Level Perfect Hashing Implementation")
    print("=" * 50)
    print()
    
    hash_table = PerfectHashing(primary_size=5)  # Create with 5 primary buckets
    
    # Test Case 1: Insert and search
    print("Test 1: Inserting keys: 10, 25, 35, 45, 15, 20, 30")
    keys = [10, 25, 35, 45, 15, 20, 30]
    
    for key in keys:
        if hash_table.insert(key):
            print(f"Inserted {key} successfully")
        else:
            print(f"Failed to insert {key}")
    
    hash_table.display()
    hash_table.statistics()
    
    # Test Case 2: Search operations
    print("\nTest 2: Searching for keys:")
    search_keys = [25, 100, 15, 50, 30]
    
    for key in search_keys:
        if hash_table.search(key):
            print(f"Key {key}: FOUND")
        else:
            print(f"Key {key}: NOT FOUND")
    
    # Test Case 3: Insert more keys
    print("\nTest 3: Inserting additional keys: 50, 60, 70")
    more_keys = [50, 60, 70]
    
    for key in more_keys:
        if hash_table.insert(key):
            print(f"Inserted {key} successfully")
        else:
            print(f"Failed to insert {key}")
    
    hash_table.display()
    hash_table.statistics()
    
    # Test Case 4: Final search verification
    print("\nTest 4: Final search verification:")
    final_search_keys = [10, 25, 35, 45, 15, 20, 30, 50, 60, 70, 99]
    
    for key in final_search_keys:
        if hash_table.search(key):
            print(f"✓ Key {key} found")
        else:
            print(f"✗ Key {key} not found")
    
    print("\n" + "=" * 50)
    print("  Algorithm Characteristics:")
    print("=" * 50)
    print("• Worst-case lookup time: O(1)")
    print("• Average-case insertion time: O(1)")
    print("• Space complexity: O(n)")
    print("• Uses universal hashing at both levels")
    print("• Secondary table size = k² for k keys in bucket")
    print("• Guarantees collision-free hashing")


if __name__ == "__main__":
    main()
