import heapq
from collections import defaultdict, Counter
from tkinter import Tk, Label, Button, Text, Scrollbar, END, messagebox

class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_frequency_table(text):
    return Counter(text)

def build_huffman_tree(freq_table):
    priority_queue = [Node(char, freq) for char, freq in freq_table.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)

        merged = Node(None, left.freq + right.freq)
        merged.left = left
        merged.right = right
        heapq.heappush(priority_queue, merged)

    return priority_queue[0]

def build_codes(node, prefix='', codebook=defaultdict()):
    if node is not None:
        if node.char is not None:
            codebook[node.char] = prefix
        build_codes(node.left, prefix + '0', codebook)
        build_codes(node.right, prefix + '1', codebook)
    return codebook

def encode(text):
    freq_table = build_frequency_table(text)
    huffman_tree = build_huffman_tree(freq_table)
    codebook = build_codes(huffman_tree)
    return ''.join(codebook[char] for char in text), codebook

def decode(encoded_text, codebook):
    reversed_codebook = {v: k for k, v in codebook.items()}
    current_code = ''
    decoded_text = ''
    for bit in encoded_text:
        current_code += bit
        if current_code in reversed_codebook:
            decoded_text += reversed_codebook[current_code]
            current_code = ''
    return decoded_text
def encode_text():
    text = input_text.get("1.0", END).strip()
    if not text:
        messagebox.showwarning("Input Error", "Please enter some text to encode.")
        return
    
    encoded_text, codebook = encode(text)
    encoded_output.delete("1.0", END)
    encoded_output.insert(END, encoded_text)
    
    code_output.delete("1.0", END)
    for char, code in codebook.items():
        code_output.insert(END, f"{char}: {code}\n")

def decode_text():
    encoded_text = encoded_input.get("1.0", END).strip()
    codebook_text = code_output.get("1.0", END).strip()
    
    if not encoded_text:
        messagebox.showwarning("Input Error", "Please enter encoded text to decode.")
        return
    
    codebook = {}
    for line in codebook_text.splitlines():
        if ':' in line:
            char, code = line.split(':')
            codebook[code.strip()] = char.strip()

    try:
        decoded_text = decode(encoded_text, codebook)
        decoded_output.delete("1.0", END)
        decoded_output.insert(END, decoded_text)
    except Exception as e:
        messagebox.showerror("Decoding Error", f"Error decoding text: {e}")

def main():
    global input_text, encoded_output, code_output, encoded_input, decoded_output

    root = Tk()
    root.title("Huffman Coding GUI")

    Label(root, text="Input Text:").grid(row=0, column=0, padx=10, pady=10)
    input_text = Text(root, height=10, width=40)
    input_text.grid(row=1, column=0, padx=10, pady=10)

    Button(root, text="Encode", command=encode_text).grid(row=2, column=0, padx=10, pady=10)

    Label(root, text="Encoded Output:").grid(row=3, column=0, padx=10, pady=10)
    encoded_output = Text(root, height=5, width=40)
    encoded_output.grid(row=4, column=0, padx=10, pady=10)

    Label(root, text="Codebook:").grid(row=5, column=0, padx=10, pady=10)
    code_output = Text(root, height=10, width=40)
    code_output.grid(row=6, column=0, padx=10, pady=10)

    Label(root, text="Encoded Input for Decoding:").grid(row=0, column=1, padx=10, pady=10)
    encoded_input = Text(root, height=5, width=40)
    encoded_input.grid(row=1, column=1, padx=10, pady=10)

    Button(root, text="Decode", command=decode_text).grid(row=2, column=1, padx=10, pady=10)

    Label(root, text="Decoded Output:").grid(row=3, column=1, padx=10, pady=10)
    decoded_output = Text(root, height=10, width=40)
    decoded_output.grid(row=4, column=1, padx=10, pady=10)

    root.mainloop()

if __name__ == "__main__":
    main()

