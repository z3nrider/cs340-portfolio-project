# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 12/2/22
# This program utilizes Hash Map DS (separate chaining) with its
# associated methods: put, empty buckets, table load, clear, resize
# table, get contains key, remove, get keys and values, and find mode

from a6_include import (DynamicArray, LinkedList, hash_function_1,
                        hash_function_2)


class HashMap:
    def __init__(self,
                 capacity: int = 11,
                 function: callable = hash_function_1) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(LinkedList())

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number and the find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        This method updates the key/value pair in the hash map. If the 
        given key already exists in the hash map, its associated value must 
        be replaced with the new value. If the given key is not in the hash 
        map, a new key/value pair must be added.

        For this hash map implementation, the table must be resized to double 
        its current capacity when this method is called and the current load 
        factor of the table is greater than or equal to 1.0.
        """
        if self._size == 0:
            index = self._hash_function(key) % self._capacity
            bucket = self._buckets[index]
            if bucket.contains(key):
                bucket.remove(key)
                bucket.insert(key, value)
            else:
                bucket.insert(key, value)
                self._size += 1

        else:
            hash = self._hash_function(key)
            index = hash % self._capacity
            bucket = self._buckets[index]

            # found a duplicate key
            if bucket.contains(key):
                bucket.remove(key)
                bucket.insert(key, value)

            # unbalanced hash map
            elif self.table_load() >= 1.0:
                # double capacity
                self.resize_table(self._capacity * 2)
                hash = self._hash_function(key)
                index = hash % self._capacity
                bucket = self._buckets[index]
                bucket.insert(key, value)
                self._size += 1

            else:
                bucket.insert(key, value)
                self._size += 1

    def empty_buckets(self) -> int:
        """
        This method returns the number of empty buckets in the hash table.        
        """
        count = 0
        for i in range(self.get_capacity()):
            if self._buckets[i].length() == 0:
                count += 1
        return count

    def table_load(self) -> float:
        """
        This method returns the current hash table load factor.
        """
        # (number of elements in table / number of buckets)
        return self._size / self._capacity

    def clear(self) -> None:
        """
        This method clears the contents of the hash map. It does not change 
        the underlying hash table capacity.
        """
        self._buckets = DynamicArray()
        self._size = 0
        for i in range(self._capacity):
            self._buckets.append(LinkedList())

    def resize_table(self, new_capacity: int) -> None:
        """
        This method changes the capacity of the internal hash table. All 
        existing key/value pairs must remain in the new hash map, and all 
        hash table links must be rehashed.

        First check that new_capacity is not less than 1; if so, the method 
        does nothing. If new_capacity is 1 or more, make sure it is a prime 
        number. If not, change it to the next highest prime number. You may 
        use the methods _is_prime() and _next_prime() from the skeleton code.
        """
        if new_capacity < 1:
            return

        # catches prime numbers
        if self._is_prime(new_capacity):
            new_capacity -= 1

        oldBuckets = self._buckets
        oldBucketsCapacity = self._capacity
        self._capacity = self._next_prime(new_capacity)
        self.clear()

        # rehash old values onto new hash map
        for i in range(oldBucketsCapacity):
            if oldBuckets[i].length() != 0:

                # put each ll node in newly resized array
                for node in oldBuckets[i]:
                    self.put(node.key, node.value)

    def get(self, key: str):
        """
        This method returns the value associated with the given key. If the 
        key is not in the hash map, the method returns None.
        """
        if self._size == 0:
            return None

        hash = self._hash_function(key)
        index = hash % self._capacity

        for node in self._buckets[index]:
            if node.key == key:
                return node.value

        return None

    def contains_key(self, key: str) -> bool:
        """
        This method returns True if the given key is in the hash map, 
        otherwise it returns False. An empty hash map does not contain any 
        keys.
        """
        if self._size == 0:
            return False

        hash = self._hash_function(key)
        index = hash % self._capacity
        bucket = self._buckets[index]

        if bucket.contains(key):
            return True
        return False

    def remove(self, key: str) -> None:
        """
        This method removes the given key and its associated value from the 
        hash map. If the key is not in the hash map, the method does nothing 
        (no exception needs to be raised).
        """
        if self._size == 0:
            return None

        hash = self._hash_function(key)
        index = hash % self._capacity
        bucket = self._buckets[index]

        if bucket.contains(key):
            bucket.remove(key)
            self._size -= 1

    def get_keys_and_values(self) -> DynamicArray:
        """
        This method returns a dynamic array where each index contains a tuple
        of a key/value pair stored in the hash map. The order of the keys in
        the dynamic array does not matter.
        """
        if self._size == 0:
            return None

        arr = DynamicArray()

        # iterate over each DA index
        for i in range(self._capacity):
            # iterate over each LL object
            for bucket in self._buckets.get_at_index(i):
                arr.append((bucket.key, bucket.value))

        return arr


def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """
    Write a standalone function outside of the HashMap class that receives a 
    dynamic array (that is not guaranteed to be sorted). This function will 
    return a tuple containing, in this order, a dynamic array comprising the 
    mode (most occurring) value/s of the array, and an integer that represents 
    the highest frequency (how many times they appear).

    If there is more than one value with the highest frequency, all values at 
    that frequency should be included in the array being returned (the order 
    does not matter). If there is only one mode, the dynamic array will only 
    contain that value.

    You may assume that the input array will contain at least one element, and 
    that all values stored in the array will be strings. You do not need to 
    write checks for these conditions.

    For full credit, the function must be implemented with O(N) time complexity. 
    For best results, we recommend using the separate chaining hash map provided 
    for you in the function’s skeleton code.
    """
    map = HashMap()
    modeArr = DynamicArray()  # store the keys that have highest count

    # add key/value pairs to HashMap
    # where each value is the frequency of
    # occurences in the input DA
    for i in range(da.length()):
        if map.contains_key(da.get_at_index(i)):
            oldval = map.get(da.get_at_index(i))  # increment previous val
            oldval += 1
            map.put(da.get_at_index(i), oldval)
        else:
            value = 1
            map.put(da.get_at_index(i), value)

    keyValDA = map.get_keys_and_values()
    highestCountVal = None

    for i in range(keyValDA.length()):
        tup = keyValDA.get_at_index(i)
        tupkey = tup[0]
        tupval = tup[1]

        if highestCountVal is None:
            modeArr.append(tupkey)
            highestCountVal = tupval

        # destroy old modeArr and append key
        elif tupval > highestCountVal:
            modeArr = DynamicArray()
            modeArr.append(tupkey)
            highestCountVal = tupval

        # keys with equal frequencies are appended
        elif tupval == highestCountVal:
            modeArr.append(tupkey)

    return (modeArr, highestCountVal)


# ------------------- BASIC TESTING ---------------------------------------- #
if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2),
                  m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(41, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), round(m.table_load(), 2),
                  m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(101, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(101, hash_function_1)
    print(round(m.table_load(), 2))
    m.put('key1', 10)
    print(round(m.table_load(), 2))
    m.put('key2', 20)
    print(round(m.table_load(), 2))
    m.put('key1', 30)
    print(round(m.table_load(), 2))

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(53, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(round(m.table_load(), 2), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(101, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(53, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(23, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(),
          m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(),
          m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(),
              m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(31, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(151, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(53, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(79, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(53, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys_and_values example 1")
    print("------------------------")
    m = HashMap(11, hash_function_2)
    for i in range(1, 6):
        m.put(str(i), str(i * 10))
    print(m.get_keys_and_values())

    m.put('20', '200')
    m.remove('1')
    m.resize_table(2)
    print(m.get_keys_and_values())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "peach"])
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint",
            "Mint", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode : {mode}, Frequency: {frequency}\n")
