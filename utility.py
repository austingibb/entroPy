from tkinter import Tk, filedialog

def file_picker():
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename()
    root.destroy()
    return file_path