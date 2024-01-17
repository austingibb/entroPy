from entropy import entropy_argparse
from utility import file_picker

def main():
    entropy = entropy_argparse()
    
    if entropy is not None:
        if float(8)-entropy < 0.0001:
            print("File is (virtually) truly random")
        else:
            print("File is not truly random")

if __name__ == '__main__':
    main()