import heapq
from collections import Counter, namedtuple, defaultdict

# Node class for Huffman Tree
class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    # Count frequency of each character
    frequency = Counter(text)
    
    # Create priority queue (min-heap) of nodes
    heap = [Node(char, freq) for char, freq in frequency.items()]
    heapq.heapify(heap)
    
    # Combine nodes to build the Huffman Tree
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(heap, merged)
    
    return heap[0]

def generate_codes(node, prefix='', codebook=defaultdict()):
    if node is not None:
        if node.char is not None:
            codebook[node.char] = prefix
        generate_codes(node.left, prefix + '0', codebook)
        generate_codes(node.right, prefix + '1', codebook)
    return codebook

def encode(text, codebook):
    return ''.join(codebook[char] for char in text)

def decode(encoded_text, root):
    decoded_chars = []
    node = root
    for bit in encoded_text:
        if bit == '0':
            node = node.left
        else:
            node = node.right
        
        if node.char is not None:
            decoded_chars.append(node.char)
            node = root
    
    return ''.join(decoded_chars)

# Example usage
text = "i know what i want"
huffman_tree = build_huffman_tree(text)
codebook = generate_codes(huffman_tree)
encoded_text = encode(text, codebook)
decoded_text = decode(encoded_text, huffman_tree)

print("Original Text:", text)
print("Huffman Codes:", codebook)
print("Encoded Text:", encoded_text)
print("Decoded Text:", decoded_text)
