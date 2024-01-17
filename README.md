# File Entropy Calculator

This Python program calculates the Shannon entropy of a file, providing insights into its randomness. It is capable of processing very large files and supports sparse sampling to handle large datasets efficiently.

## Features
- Calculate the Shannon entropy of any file (on a scale of 0-8, 8 being completely random data).
- Handle large files without loading them entirely into RAM.
- Optional sparse sampling of the file for quicker analysis.
- Use the OS file picker for easy file selection.
- Command-line interface for easy use and integration.
- Determine if a file is likely "encrypted" due to the random nature of the data (e.g. a VeraCrypt encrypted volume).

## Installation

1. To use this program, ensure you have Python installed on your system. 
2. Clone the repository or download the files to your local machine.
3. Run ```pip install -r requirements.txt``` in the cloned repo directory.

## Usage

Run the script from the command line, providing the path to the file you want to analyze. The script offers the following options:

- `-p`, `--picker`: Use the OS file picker to select a file. This option ignores any path value provided.
- `-s`, `--sparse`: Specify the number of samples to gather for entropy calculation. Supports shorthand notations like 'k' (thousand), 'm' (million), 'b' or 'g' (billion), and 't' (trillion).
- `-r`, `--is-random-data`: Program will provide an assessment on whether the supplied file is close to truly random, instead of a raw Shannon randomness number.

### Example Commands

Calculate entropy of a specific file:

```
python entropy.py path_to_your_file
```

Use the OS file picker:
```
python entropy.py -p
```

Calculate entropy using sparse sampling (e.g., 1 million samples):

```
python entropy.py -s 1m path_to_your_file
```

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page](#) if you want to contribute.

## License

This project is [MIT licensed](LICENSE).
