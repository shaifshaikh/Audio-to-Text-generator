#  Audio to Text Converter
#importing required libraries
import tkinter as tk
from tkinter.ttk import *
from tkinter import *
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import messagebox
import os
from pydub import AudioSegment
import speech_recognition as sr
r = sr.Recognizer()

# Creating a directory named History for storing previously converted text files
try:
    files = os.path.join(os.getcwd(), "History")
    os.mkdir(files)

# Skipping if directory exists
except(FileExistsError):
    pass


global text1
text1 = ""

# Definition for Browser button
def browse():
    global path
    path = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                      defaultextension=".mp3", filetypes=(("Mp3 files", "*.mp3*"), ("all files", "*.*")))
    textEntry.delete("0", tk.END)
    textEntry.insert("0", path)
    print(path)

    global new
    new = ""
    for i in path[-5::-1]:
        if (i == "/"):
            break
        else:
            new = new + i
    # storing filename in new variable Eg. D:/Faisal Husain/MY SONGS/01 Chogada - Loveratri.mp3
    new = new[::-1]
    #   extracting "01 Chogada - Loveratri"


# Definition for converting MP3 file to WAV file since our convert function only deals with WAV files only
def mp3ToWav():
    global waveFile
    waveFile = os.getcwd() + "\\temp.wav"
    sound = AudioSegment.from_mp3(path)
    sound.export(waveFile, format="wav")


# Definition for convert button
def convert():
    # Showing error if path is not defined
    if (textEntry.get() == ""):
        messagebox.showerror("Error", "Please Enter path of file")
        return()

    # Converting MP3 file to WAV using mp3ToWav function
    mp3ToWav()

    with sr.AudioFile(waveFile) as source:
        print("Fetching File")
        audio_text = r.listen(source)
        # recoginize_() method will throw a request error if the API is unreachable, hence using exception handling
        try:
            # using google speech recognition
            print("Conversion in process")
            text = r.recognize_google(audio_text, language="en-IN")
            # Deleting existing text in output text
            text_area.delete("1.0", tk.END)
            text_area.insert(tk.END, text)  # Displaying result in text_area
            print("Converted")

        except:
            print("Sorry.. run again...")
            messagebox.showerror("Error", "Please check internet connection")

    # Deleting temp.wav as its needs end
    os.remove(waveFile)
    # Changing directory and pointing towards History folder
    os.chdir("History")
    # Creating new file as name of the file given in path
    with open(new + ".txt", "w") as fp:
        fp.write(text)  # Entering the result in the file
    os.chdir("..")      # Getting back to main directory


#   Definition for History button
def history():
    print(os.getcwd())
    os.chdir("History")
    # Displaying file fetched previously in new window
    file = filedialog.askopenfile(initialdir=os.getcwd(), mode='r', filetypes=[
                                  ('Choose file', '*.txt')])
    if file is not None:
        content = file.read()
        text_area.delete("1.0", tk.END)
        text_area.insert(tk.END, content)  # Displaying result in output window
    os.chdir("..")


# Function for Closing the window
def close_window():
    root.destroy()
    exit()

# Making root as output interface
root = tk.Tk()
root.geometry("800x820")    # Defining fixed size of output
root.resizable(0, 0)        # Making resizing restricted


# Declaring Title
root.title("AUDIO TO TEXT GENERATOR")
# Background as complete black
root.configure(bg="black")


# Importing photo from the system
print(f"{os.getcwd()}\\pic1.png")

pics1 = f"{os.getcwd()}\\pic1.png"   #os.getcwd() + "//pic1.png"
pic1 = PhotoImage(file= pics1)

# Packing photo in the output interface
label1 = tk.Label(root, image=pic1, bg="black")
label1.grid(row=0, column=0, padx=2, pady=2, sticky=NSEW)


# Defining label for user understanding
label2 = tk.Label(root, text="Enter the Path of File: ",
                  bg="white", fg="black", font="bodoni 12 bold")
label2.grid(row=1, column=0, sticky=W, padx=4, pady=5)


# Defining textbox for taking path of input file
textEntry = tk.Entry(root, width=55, font="bodoni 12 bold",
                     bg="white", fg="maroon")
textEntry.grid(row=2, column=0, padx=2, sticky=W)


# Importing photo for browse button
pics2 = os.getcwd() + "\\pic2.png"
pic2 = PhotoImage(file= pics2)
picImage = pic2.subsample(8, 8)

# Defining Browse button for input path for user convenience
browse = tk.Button(root, text=" BROWSE", image=picImage, compound=LEFT, command=browse, width=150,
                   height=25, font="bodoni 12 bold", relief="sunken",  borderwidth=2, bg="white", fg="black",  padx=2)
browse.grid(row=2, sticky=E, padx=2)


# Creating convert button
convert = tk.Button(root, text="CONVERT", command=convert, width=12, height=2,
                    font="bodoni 12 bold", relief="raised", borderwidth=4, bg="white", fg="black",  padx=2)
convert.grid(row=3, pady=10)

# Defining label for user understanding
label3 = tk.Label(root, text="Output Window: ",
                  font="candara 12 bold", bg="white", fg="black")
label3.grid(row=4, column=0, sticky=W, padx=4, pady=5)

# Creating textbox for displaying output
text_area = scrolledtext.ScrolledText(
    root, height=12, width=75, font="bodoni 10 bold", relief="sunken", borderwidth=3, bg="white", fg="black")
text_area.grid(row=5)


# Creating History button
history = tk.Button(root, text="HISTORY", command=history, width=12, height=2,
                    font="bodoni 12 bold", relief="sunken",  borderwidth=2, bg="white", fg="black",  padx=2)
history.grid(row=6, column=0, sticky=W, padx=3, pady=5)

# Creating Close button for Quittng the application
close = tk.Button(root, text="CLOSE", command=close_window, width=12, height=2,
                  font="bodoni 12 bold", relief="sunken",  borderwidth=2, bg="white", fg="black",  padx=2)
close.grid(row=6, column=0, sticky=E, padx=2, pady=5)

root.mainloop() 