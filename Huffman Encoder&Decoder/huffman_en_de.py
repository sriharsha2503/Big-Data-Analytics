import heapq
from collections import Counter, namedtuple

# Define a class for the Huffman Tree nodes
class HuffmanNode:
    def __init__(self, char, freq, left=None, right=None):
        self.char = char
        self.freq = freq
        self.left = left
        self.right = right

    # Define comparison operators for heap operations
    def __lt__(self, other):
        return self.freq < other.freq

class HuffmanCoding:
    def __init__(self):
        self.heap = []
        self.codes = {}
        self.reverse_mapping = {}

    def build_frequency_dict(self, text):
        frequency = Counter(text)
        return frequency

    def build_heap(self, frequency):
        for key in frequency:
            node = HuffmanNode(key, frequency[key])
            heapq.heappush(self.heap, node)

    def merge_nodes(self):
        while len(self.heap) > 1:
            node1 = heapq.heappop(self.heap)
            node2 = heapq.heappop(self.heap)
            merged = HuffmanNode(None, node1.freq + node2.freq, node1, node2)
            heapq.heappush(self.heap, merged)

    def build_codes_helper(self, root, current_code):
        if root is None:
            return

        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return

        self.build_codes_helper(root.left, current_code + "0")
        self.build_codes_helper(root.right, current_code + "1")

    def build_codes(self):
        root = heapq.heappop(self.heap)
        self.build_codes_helper(root, "")

    def get_encoded_text(self, text):
        encoded_text = ""
        for char in text:
            encoded_text += self.codes[char]
        return encoded_text

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"

        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        if len(padded_encoded_text) % 8 != 0:
            print("Encoded text not padded properly")
            exit(0)

        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b

    def compress(self, text):
        frequency = self.build_frequency_dict(text)
        self.build_heap(frequency)
        self.merge_nodes()
        self.build_codes()

        encoded_text = self.get_encoded_text(text)
        padded_encoded_text = self.pad_encoded_text(encoded_text)

        return self.get_byte_array(padded_encoded_text), self.codes

    def remove_padding(self, padded_encoded_text):
        padded_info = padded_encoded_text[:8]
        extra_padding = int(padded_info, 2)

        padded_encoded_text = padded_encoded_text[8:] 
        encoded_text = padded_encoded_text[:-1*extra_padding]

        return encoded_text

    def decode_text(self, encoded_text):
        current_code = ""
        decoded_text = ""

        for bit in encoded_text:
            current_code += bit
            if current_code in self.reverse_mapping:
                character = self.reverse_mapping[current_code]
                decoded_text += character
                current_code = ""

        return decoded_text

    def decompress(self, byte_array):
        bit_string = ""

        for byte in byte_array:
            bit_string += "{0:08b}".format(byte)

        encoded_text = self.remove_padding(bit_string)

        return self.decode_text(encoded_text)

# Example usage
if __name__ == "__main__":
    text = "this is an example for huffman encoding"

    huffman_coding = HuffmanCoding()
    compressed_data, huffman_codes = huffman_coding.compress(text)
    print(f"Compressed data: {compressed_data}")
    print(f"Huffman Codes: {huffman_codes}")

    decompressed_data = huffman_coding.decompress(compressed_data)
    print(f"Decompressed data: {decompressed_data}")
