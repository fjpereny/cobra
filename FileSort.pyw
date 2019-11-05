import os
import shutil
import sys
import threading
import tkinter as tk
import tkinter.filedialog
import tkinter.messagebox
import tkinter.ttk

filePath = os.path.dirname(os.path.abspath(__file__))

def about_window():
    license_text = ''
    with open(filePath + '/License.txt', 'r') as f:
        license_text += '\n\n' + f.read()
    f.close()
    tk.messagebox.showinfo('About File Sort', license_text)

def center_window(window):
        # Get Screen Width & Height
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        w_width = window.winfo_width() 
        w_height = window.winfo_height() 
        x = (screen_width / 2) - (w_width / 2)
        y = (screen_height / 2) - (w_height / 2)
        window.geometry('%dx%d+%d+%d' % (w_width, w_height, x, y))

def source_button_click():
    path = tk.filedialog.askdirectory(parent=root, title='Select Folder')
    source_path.set(path)

def dest_button_click():
    path = tk.filedialog.askdirectory(parent=root, title='Select Folder')
    dest_path.set(path)

def start_button_click():
    start_button.config(state='disabled')
    source_button.config(state='disabled')
    dest_button.config(state='disabled')
    t1 = threading.Thread(target=scan_files)
    t1.start()

def scan_files():
    files_found = tk.StringVar(root, value='Scanning Files - Please Wait...')
    tk.Label(root, textvariable=files_found).grid(row=3, column=1, padx='3px', pady='3px', sticky='ew')
    root.update_idletasks()
    prog_bar.configure(mode='indeterminate', value=0)
    
    file_index = []
    for rt, dirs, files in os.walk(source_path.get()):
        for f in files:
            path = rt + '/' + f
            file_index.append(path)

    files_found = str(len(file_index)) + ' Files Found!'
    root.update_idletasks()

    prog_value = 0
    prog_bar.config(maximum=len(file_index))
    for f in file_index:
        filename, extension = os.path.splitext(f)
        d_path = dest_entry.get() + '/' + extension[1:]
        if not os.path.exists(d_path):
            os.mkdir(d_path)
        shutil.copy(str(f), d_path)
        prog_value += 1
        prog_bar.config(value=prog_value)
    
    files_found = 'Transfer Complete!'
    root.update_idletasks()
    source_button.config(state='normal')
    dest_button.config(state='normal')
    start_button.config(state='normal')


# Main Window
root = tk.Tk()
root.title('File Sort')
root.minsize(width=500, height=150)
root.resizable(False, False)

# Menu Bar
menuBar = tk.Menu(root)
# File Menu
fileMenu = tk.Menu(menuBar, tearoff=0)
fileMenu.add_command(label='Open', accelerator='Ctrl+O')
fileMenu.add_separator()
fileMenu.add_command(label='Exit', command=root.quit)
menuBar.add_cascade(menu=fileMenu, label='File', underline=0)
# Edit Menu
editMenu = tk.Menu(menuBar, tearoff=0)
editMenu.add_command(label='Cut', accelerator='Ctrl+C')
editMenu.add_command(label='Copy', accelerator='Ctrl+X')
editMenu.add_command(label='Paste', accelerator='Ctrl+V')
editMenu.add_command(label='Delete', accelerator='Del')
editMenu.add_separator()
editMenu.add_command(label='Select All', accelerator='Ctrl+A')
menuBar.add_cascade(menu=editMenu, label='Edit', underline=0)
# Help Menu
helpMenu = tk.Menu(menuBar, tearoff=0)
menuBar.add_cascade(menu=helpMenu, label='Help', underline=0)
helpMenu.add_command(label='About', command=about_window)


# Folder Selection
source_path = tk.StringVar()
source_button = tk.Button(root, text='Source Folder', command=source_button_click)
source_button.grid(row=0, column=0, padx='3px', pady='3px', sticky='ew')
source_entry = tk.Entry(root, textvar=source_path)
source_entry.grid(row=0, column=1, padx='3px', pady='3px', sticky='ew')

tk.ttk.Separator(root, orient=tk.HORIZONTAL).grid(row=1, column=0, columnspan=2, sticky='ew', padx='3px', pady='3px')

dest_path = tk.StringVar()
dest_button = tk.Button(root, text='Destination Folder', command=dest_button_click)
dest_button.grid(row=2, column=0, padx='3px', pady='3px', sticky='ew')
dest_entry = tk.Entry(root, textvar=dest_path)
dest_entry.grid(row=2, column=1, padx='3px', pady='3px', sticky='ew')


# Start Button
start_button = tk.Button(root, text='Start', command=start_button_click)
start_button.grid(row=3, column=0, padx='3px', pady='3px', sticky='ew')


# Progress Bar
prog_bar = tk.ttk.Progressbar(root, orient=tk.HORIZONTAL, value=100, maximum=100)
prog_bar.grid(row=4, column=0, columnspan=2, sticky='ew', padx='3px', pady='3px')


root.grid_columnconfigure(0, weight=0)
root.grid_columnconfigure(1, weight=1)
root.config(menu=menuBar)
root.update_idletasks()

# Center Window
root.eval('tk::PlaceWindow . center')
center_window(root)
root.mainloop()
