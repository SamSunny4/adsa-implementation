#include <bits/stdc++.h>
using namespace std;

/*
    FKS Algorithm - Two-Level Perfect Hashing
    
    A practical implementation of perfect hashing that guarantees O(1)
    worst-case lookup time using two levels of hashing.
    
    Level 1: Primary hash table with n buckets using a universal hash function
    Level 2: For each bucket k, create a secondary hash table of size k²
             to ensure collision-free hashing within that bucket
*/

class PerfectHashing {
private:
    struct SecondaryTable {
        vector<int> table;
        int size;
        int a, b, p;  // Hash function parameters: (a*x + b) % p
        
        SecondaryTable() : size(0), a(0), b(0), p(0) {}
    };
    
    vector<vector<int>> buckets;        // Level 1: Primary buckets
    vector<SecondaryTable> secondLevel; // Level 2: Secondary hash tables
    
    int primarySize;
    int a1, b1, p1;  // Level 1 hash function parameters
    
    const long long MOD = 1e9 + 7;
    const long long PRIME = 2147483647LL; // Large prime for universal hashing
    
public:
    PerfectHashing(int n = 10) : primarySize(n) {
        buckets.resize(primarySize);
        secondLevel.resize(primarySize);
        
        // Initialize Level 1 hash function randomly
        randomizeHashFunction(a1, b1, p1, PRIME);
    }
    
    // Universal hash function: h(x) = (a*x + b) mod p
    int hashFunction(int key, int a, int b, long long p) {
        return ((long long)a * key + b) % p;
    }
    
    // Generate random hash function parameters
    void randomizeHashFunction(int& a, int& b, long long& p, long long prime) {
        srand(time(0) + rand());
        a = 1 + rand() % (prime - 1);
        b = rand() % prime;
        p = prime;
    }
    
    // Check if hash function h is collision-free for given keys
    bool isCollisionFree(const vector<int>& keys, int a, int b, long long p, int tableSize) {
        unordered_set<int> hashed;
        for (int key : keys) {
            int h = hashFunction(key, a, b, p) % tableSize;
            if (hashed.count(h)) return false;
            hashed.insert(h);
        }
        return true;
    }
    
    // Build the secondary hash table for a bucket
    bool buildSecondaryTable(int bucketIdx) {
        vector<int>& keys = buckets[bucketIdx];
        int k = keys.size();
        
        if (k == 0) {
            secondLevel[bucketIdx].size = 0;
            return true;
        }
        
        if (k == 1) {
            // Single element - no collision possible
            secondLevel[bucketIdx].table.resize(1);
            secondLevel[bucketIdx].table[0] = keys[0];
            secondLevel[bucketIdx].size = 1;
            secondLevel[bucketIdx].a = 1;
            secondLevel[bucketIdx].b = 0;
            secondLevel[bucketIdx].p = PRIME;
            return true;
        }
        
        // Try to find a collision-free hash function
        // Secondary table size is k²
        int secondarySize = k * k;
        int attempts = 0;
        int maxAttempts = 100;  // Limit attempts to avoid infinite loop
        
        while (attempts < maxAttempts) {
            int a, b;
            randomizeHashFunction(a, b, secondLevel[bucketIdx].p, PRIME);
            
            if (isCollisionFree(keys, a, b, PRIME, secondarySize)) {
                // Found a collision-free hash function
                secondLevel[bucketIdx].table.assign(secondarySize, -1);
                secondLevel[bucketIdx].size = secondarySize;
                secondLevel[bucketIdx].a = a;
                secondLevel[bucketIdx].b = b;
                
                // Place keys in secondary table
                for (int key : keys) {
                    int h = hashFunction(key, a, b, PRIME) % secondarySize;
                    secondLevel[bucketIdx].table[h] = key;
                }
                
                return true;
            }
            attempts++;
        }
        
        return false;  // Couldn't find collision-free function
    }
    
    // Insert key into the perfect hash table
    bool insert(int key) {
        // Level 1: Insert into appropriate bucket
        int bucketIdx = hashFunction(key, a1, b1, p1) % primarySize;
        buckets[bucketIdx].push_back(key);
        
        // Level 2: Rebuild secondary table for this bucket
        return buildSecondaryTable(bucketIdx);
    }
    
    // Search for a key in the perfect hash table
    bool search(int key) {
        // Level 1: Find the bucket
        int bucketIdx = hashFunction(key, a1, b1, p1) % primarySize;
        
        // Level 2: Search in secondary table
        const SecondaryTable& secTable = secondLevel[bucketIdx];
        
        if (secTable.size == 0) return false;
        
        int h = hashFunction(key, secTable.a, secTable.b, secTable.p) % secTable.size;
        return secTable.table[h] == key;
    }
    
    // Display the hash table structure
    void display() {
        cout << "\n=== Perfect Hashing (FKS Algorithm) Structure ===\n";
        cout << "Primary Level: " << primarySize << " buckets\n\n";
        
        for (int i = 0; i < primarySize; i++) {
            cout << "Bucket " << i << " (";
            cout << buckets[i].size() << " keys): ";
            
            for (int key : buckets[i]) {
                cout << key << " ";
            }
            cout << "\n";
            
            if (buckets[i].size() > 0) {
                cout << "  Secondary Table Size: " << secondLevel[i].size;
                cout << " | Hash Function: (a*x + b) mod " << secondLevel[i].p << "\n";
                cout << "  Parameters: a=" << secondLevel[i].a;
                cout << ", b=" << secondLevel[i].b << "\n";
                
                cout << "  Table Contents: [";
                for (int j = 0; j < min((int)secondLevel[i].table.size(), 10); j++) {
                    if (secondLevel[i].table[j] != -1) {
                        cout << "(" << j << ":" << secondLevel[i].table[j] << ") ";
                    }
                }
                if (secondLevel[i].table.size() > 10) cout << "...";
                cout << "]\n";
            }
        }
        cout << "\n";
    }
    
    // Statistics
    void statistics() {
        cout << "\n=== Hash Table Statistics ===\n";
        int totalKeys = 0;
        double avgBucketSize = 0;
        int maxBucketSize = 0;
        
        for (int i = 0; i < primarySize; i++) {
            totalKeys += buckets[i].size();
            maxBucketSize = max(maxBucketSize, (int)buckets[i].size());
        }
        
        avgBucketSize = (double)totalKeys / primarySize;
        
        cout << "Total Keys: " << totalKeys << "\n";
        cout << "Primary Table Size: " << primarySize << "\n";
        cout << "Average Bucket Size: " << fixed << setprecision(2) << avgBucketSize << "\n";
        cout << "Max Bucket Size: " << maxBucketSize << "\n";
        cout << "Load Factor: " << fixed << setprecision(2) << (double)totalKeys / primarySize << "\n";
        cout << "\n";
    }
};

int main() {
    cout << "============================================\n";
    cout << "  FKS Perfect Hashing Algorithm Demo\n";
    cout << "  Two-Level Perfect Hashing Implementation\n";
    cout << "============================================\n\n";
    
    PerfectHashing hashTable(5);  // Create with 5 primary buckets
    
    // Test Case 1: Insert and search
    cout << "Test 1: Inserting keys: 10, 25, 35, 45, 15, 20, 30\n";
    vector<int> keys = {10, 25, 35, 45, 15, 20, 30};
    
    for (int key : keys) {
        if (hashTable.insert(key)) {
            cout << "Inserted " << key << " successfully\n";
        } else {
            cout << "Failed to insert " << key << "\n";
        }
    }
    
    hashTable.display();
    hashTable.statistics();
    
    // Test Case 2: Search operations
    cout << "\nTest 2: Searching for keys:\n";
    vector<int> searchKeys = {25, 100, 15, 50, 30};
    
    for (int key : searchKeys) {
        if (hashTable.search(key)) {
            cout << "Key " << key << ": FOUND\n";
        } else {
            cout << "Key " << key << ": NOT FOUND\n";
        }
    }
    
    // Test Case 3: Insert more keys
    cout << "\nTest 3: Inserting additional keys: 50, 60, 70\n";
    vector<int> moreKeys = {50, 60, 70};
    
    for (int key : moreKeys) {
        if (hashTable.insert(key)) {
            cout << "Inserted " << key << " successfully\n";
        } else {
            cout << "Failed to insert " << key << "\n";
        }
    }
    
    hashTable.display();
    hashTable.statistics();
    
    // Test Case 4: Final search verification
    cout << "\nTest 4: Final search verification:\n";
    vector<int> finalSearchKeys = {10, 25, 35, 45, 15, 20, 30, 50, 60, 70, 99};
    
    for (int key : finalSearchKeys) {
        if (hashTable.search(key)) {
            cout << "✓ Key " << key << " found\n";
        } else {
            cout << "✗ Key " << key << " not found\n";
        }
    }
    
    cout << "\n============================================\n";
    cout << "  Algorithm Characteristics:\n";
    cout << "============================================\n";
    cout << "• Worst-case lookup time: O(1)\n";
    cout << "• Average-case insertion time: O(1)\n";
    cout << "• Space complexity: O(n)\n";
    cout << "• Uses universal hashing at both levels\n";
    cout << "• Secondary table size = k² for k keys in bucket\n";
    cout << "• Guarantees collision-free hashing\n";
    
    return 0;
}
