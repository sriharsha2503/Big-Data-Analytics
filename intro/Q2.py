import tkinter as tk
import random
import time
import threading

class SortingVisualizer:
    def __init__(self, root):
        self.root = root
        self.root.title("Sorting Algorithm Visualization")
        self.canvas = tk.Canvas(root, width=800, height=600, bg='black')
        self.canvas.pack()

        self.array = [random.randint(1, 100) for _ in range(20)]
        self.bars = []
        self.draw_bars()

        button_frame = tk.Frame(root)
        button_frame.pack()

        # Buttons for different sorting algorithms
        self.start_button1 = tk.Button(button_frame, text="Bubble Sort", command=self.bubble_sort)
        self.start_button2 = tk.Button(button_frame, text="Selection Sort", command=self.selection_sort)
        self.start_button3 = tk.Button(button_frame, text="Quick Sort", command=self.quick_sort)
        self.start_button4 = tk.Button(button_frame, text="Merge Sort", command=self.merge_sort)
        self.start_button5 = tk.Button(button_frame, text="Heap Sort", command=self.heap_sort)
        self.start_button6 = tk.Button(button_frame, text="Parallel Selection Sort", command=self.start_parallel_selection_sort)
        self.start_button7 = tk.Button(button_frame, text="Odd-Even Transposition Sort", command=self.start_odd_even_sort)
        self.restart_button = tk.Button(button_frame, text="Restart", command=self.restart)

        self.start_button1.grid(row=0, column=0)
        self.start_button2.grid(row=0, column=1)
        self.start_button3.grid(row=0, column=2)
        self.start_button4.grid(row=0, column=3)
        self.start_button5.grid(row=0, column=4)
        self.start_button6.grid(row=0, column=5)
        self.start_button7.grid(row=0, column=6)
        self.restart_button.grid(row=0, column=7)

        self.sorting_thread = None

    def draw_bars(self):
        self.canvas.delete("all")
        bar_width = 800 // len(self.array)
        self.bars = []
        for i, val in enumerate(self.array):
            x0 = i * bar_width
            y0 = 600 - (val * 5)
            x1 = (i + 1) * bar_width
            y1 = 600
            color = "white"
            bar = self.canvas.create_rectangle(x0, y0, x1, y1, fill=color)
            self.bars.append(bar)

    def update_bars(self, idx1, idx2, color="red"):
        bar_width = 800 // len(self.array)
        x0 = idx1 * bar_width
        y0 = 600 - (self.array[idx1] * 5)
        x1 = (idx1 + 1) * bar_width
        y1 = 600
        self.canvas.coords(self.bars[idx1], x0, y0, x1, y1)

        x0 = idx2 * bar_width
        y0 = 600 - (self.array[idx2] * 5)
        x1 = (idx2 + 1) * bar_width
        y1 = 600
        self.canvas.coords(self.bars[idx2], x0, y0, x1, y1)
        
        self.canvas.itemconfig(self.bars[idx1], fill=color)
        self.canvas.itemconfig(self.bars[idx2], fill=color)
        self.root.update_idletasks()
        time.sleep(0.1)
        self.canvas.itemconfig(self.bars[idx1], fill="white")
        self.canvas.itemconfig(self.bars[idx2], fill="white")

    # Bubble Sort
    def bubble_sort(self):
        n = len(self.array)
        for i in range(n):
            for j in range(0, n - i - 1):
                if self.array[j] > self.array[j + 1]:
                    self.array[j], self.array[j + 1] = self.array[j + 1], self.array[j]
                    self.update_bars(j, j + 1)

    # Selection Sort
    def selection_sort(self):
        n = len(self.array)
        for i in range(n):
            min_idx = i
            for j in range(i + 1, n):
                if self.array[j] < self.array[min_idx]:
                    min_idx = j
            
            self.array[i], self.array[min_idx] = self.array[min_idx], self.array[i]
            self.update_bars(i, min_idx)

    # Quick Sort
    def quick_sort(self):
        self._quick_sort(0, len(self.array) - 1)

    def _quick_sort(self, low, high):
        if low < high:
            pi = self.partition(low, high)
            self._quick_sort(low, pi - 1)
            self._quick_sort(pi + 1, high)

    def partition(self, low, high):
        pivot = self.array[high]
        i = low - 1
        for j in range(low, high):
            if self.array[j] < pivot:
                i += 1
                self.array[i], self.array[j] = self.array[j], self.array[i]
                self.update_bars(i, j)
        self.array[i + 1], self.array[high] = self.array[high], self.array[i + 1]
        self.update_bars(i + 1, high)
        return i + 1

    # Merge Sort
    def merge_sort(self):
        self._merge_sort(0, len(self.array) - 1)

    def _merge_sort(self, left, right):
        if left < right:
            mid = (left + right) // 2
            self._merge_sort(left, mid)
            self._merge_sort(mid + 1, right)
            self.merge(left, mid, right)

    def merge(self, left, mid, right):
        n1 = mid - left + 1
        n2 = right - mid

        L = [self.array[left + i] for i in range(n1)]
        R = [self.array[mid + 1 + i] for i in range(n2)]

        i = j = 0
        k = left

        while i < n1 and j < n2:
            if L[i] <= R[j]:
                self.array[k] = L[i]
                i += 1
            else:
                self.array[k] = R[j]
                j += 1
            self.update_bars(k, k, color="green")
            k += 1

        while i < n1:
            self.array[k] = L[i]
            self.update_bars(k, k, color="green")
            i += 1
            k += 1

        while j < n2:
            self.array[k] = R[j]
            self.update_bars(k, k, color="green")
            j += 1
            k += 1

    # Heap Sort
    def heap_sort(self):
        n = len(self.array)

        for i in range(n // 2 - 1, -1, -1):
            self.heapify(n, i)

        for i in range(n - 1, 0, -1):
            self.array[i], self.array[0] = self.array[0], self.array[i]
            self.update_bars(i, 0)
            self.heapify(i, 0)

    def heapify(self, n, i):
        largest = i
        left = 2 * i + 1
        right = 2 * i + 2

        if left < n and self.array[i] < self.array[left]:
            largest = left

        if right < n and self.array[largest] < self.array[right]:
            largest = right

        if largest != i:
            self.array[i], self.array[largest] = self.array[largest], self.array[i]
            self.update_bars(i, largest)
            self.heapify(n, largest)

    # Parallel Selection Sort
    def parallel_selection_sort(self):
        n = len(self.array)
        threads = []

        def find_min_and_swap(start, end):
            for i in range(start, end):
                min_idx = i
                for j in range(i + 1, n):
                    if self.array[j] < self.array[min_idx]:
                        min_idx = j
                if min_idx != i:
                    self.array[i], self.array[min_idx] = self.array[min_idx], self.array[i]
                    self.update_bars(i, min_idx)

        mid = len(self.array) // 2
        t1 = threading.Thread(target=find_min_and_swap, args=(0, mid))
        t2 = threading.Thread(target=find_min_and_swap, args=(mid, len(self.array)))

        t1.start()
        t2.start()

        t1.join()
        t2.join()

    def start_parallel_selection_sort(self):
        if self.sorting_thread is None or not self.sorting_thread.is_alive():
            self.sorting_thread = threading.Thread(target=self.parallel_selection_sort)
            self.sorting_thread.start()

    # Odd-Even Transposition Sort
    def odd_even_transposition_sort(self):
        n = len(self.array)
        sorted = False

        while not sorted:
            sorted = True
            
            # Odd phase
            for i in range(1, n - 1, 2):
                if self.array[i] > self.array[i + 1]:
                    self.array[i], self.array[i + 1] = self.array[i + 1], self.array[i]
                    self.update_bars(i, i + 1)
                    sorted = False

            # Even phase
            for i in range(0, n - 1, 2):
                if self.array[i] > self.array[i + 1]:
                    self.array[i], self.array[i + 1] = self.array[i + 1], self.array[i]
                    self.update_bars(i, i + 1)
                    sorted = False

    def start_odd_even_sort(self):
        if self.sorting_thread is None or not self.sorting_thread.is_alive():
            self.sorting_thread = threading.Thread(target=self.odd_even_transposition_sort)
            self.sorting_thread.start()

    def restart(self):
        self.array = [random.randint(1, 100) for _ in range(20)]
        self.draw_bars()

if __name__ == "__main__":
    root = tk.Tk()
    gui = SortingVisualizer(root)
    root.mainloop()
