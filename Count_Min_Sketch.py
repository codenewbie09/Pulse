import mmh3
import numpy as np


class CountMinSketch:
    def __init__(self, width, depth):
        """
        width: No. of columns (determines error rate)
        depth: No. of rows (determines probablity of accuracy)
        """
        self.width = width
        self.depth = depth
        # Initialize a 2D matrix of zeroes
        self.table = np.zeros((depth, width), dtype=int)

    def _hashes(self, item):
        """
        Generate 'depth' number of hash values for a given item (string).
        We use different seeds for each row to simulate different hash functions.
        """
        hashes = []
        for i in range(self.depth):
            # mmh3.hash can return a negative integer, so we take abs()
            hash_val = abs(mmh3.hash(item, seed=i)) % self.width
            hashes.append(hash_val)
        return hashes

    def add(self, item):
        """
        Adds an item in the sketch.
        Time Complexity: O(depth) = O(1)
        """
        hashes = self._hashes(item)
        for i in range(self.depth):
            self.table[i][hashes[i]] += 1

    def estimate(self, item):
        """
        Estimate the count of the item.
        Returns the minimum value found at the hash locations.
        """
        hashes = self._hashes(item)
        min_count = float("inf")
        for i in range(self.depth):
            count = self.table[i][hashes[i]]
            if count < min_count:
                min_count = count
        return min_count
