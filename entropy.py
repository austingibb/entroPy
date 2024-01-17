import argparse
import math
import os
import re
from utility import file_picker
from tqdm import tqdm
from random import sample

class Entropy:
    def __init__(self):
        self.frequency = [0] * 256
        self.total_bytes = 0

    def update_frequency(self, data_chunk):
        for byte in data_chunk:
            self.frequency[byte] += 1
        self.total_bytes += len(data_chunk)

    def calculate_entropy(self):
        if self.total_bytes == 0:
            return 0

        probabilities = [f / self.total_bytes for f in self.frequency if f > 0]
        entropy = -sum(p * math.log2(p) for p in probabilities)
        return entropy

    @staticmethod
    def parse_number(num_str):
        match = re.match(r'(\d+)([kmgb]?)', num_str, re.IGNORECASE)
        if not match:
            raise ValueError("Invalid number format")
        number, unit = match.groups()
        number = int(number)
        unit = unit.lower()
        if unit == 'k':
            number *= 1000
        elif unit == 'm':
            number *= 1000000
        elif unit in ['g', 'b']:
            number *= 1000000000
        elif unit == 't':
            number *= 1000000000000
        return number

    def from_file(self, file_path, show_progress=False):
        file_size = os.path.getsize(file_path)

        if show_progress:
            pbar = tqdm(total=file_size//4096, desc="Scanning file")

        with open(file_path, 'rb') as file:
            for i in range(file_size//4096+1):
                self.update_frequency(file.read(4096))
                if show_progress:
                    pbar.update(1)

        if show_progress:
            pbar.close()
        return self.calculate_entropy()

    def sample_file(self, file_path, sample_size, show_progress=False):
        file_size = os.path.getsize(file_path)
        chunk_size = 4096
        file_size_nearest_chunk = math.ceil(file_size/chunk_size)*4096

        bytes_between_samples = file_size_nearest_chunk/sample_size

        if bytes_between_samples < chunk_size:
            raise ValueError(f"Sample size is too large relative to file size, there are only {bytes_between_samples} bytes between samples. Needs at least 4096 bytes between samples.")

        positions_to_sample = [i for i in range(0, file_size_nearest_chunk, int(bytes_between_samples))]

        if show_progress:
            pbar = tqdm(total=sample_size, desc="Sampling file")

        with open(file_path, 'rb') as file:
            for pos in positions_to_sample:
                file.seek(pos)
                self.update_frequency(file.read(chunk_size))
                if show_progress:
                    pbar.update(1)

        if show_progress:
            pbar.close()

        return self.calculate_entropy()

def entropy_argparse():
    parser = argparse.ArgumentParser(description='Calculate the entropy of a file.')
    parser.add_argument('path', nargs='?', default=None, help='path to the file to calculate entropy of')
    parser.add_argument('-p', '--picker', action='store_true', help='use the OS file picker (any path supplied is ignored)')
    parser.add_argument('-s', '--sparse', help='number of samples to gather (supports k, m, b or g, t suffixes)', type=str)
    args = parser.parse_args()

    entropy_calculator = Entropy()

    file_path = None
    if args.picker:
        file_path = file_picker()
    elif args.path:
        file_path = args.path
    else:
        parser.print_help()
        return

    if file_path:
        try:
            if args.sparse:
                sample_size = Entropy.parse_number(args.sparse)
                entropy = entropy_calculator.sample_file(file_path, sample_size, show_progress=True)
            else:
                entropy = entropy_calculator.from_file(file_path, show_progress=True)
            return entropy
        except ValueError as e:
            print(e)
            parser.print_help()
            return None

if __name__ == '__main__':
    entropy_argparse()
