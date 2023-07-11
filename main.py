import os
from tkinter import *
from tkinter.ttk import *
from tkinter import font, colorchooser, filedialog, messagebox
import tempfile
import pyttsx3

is_bold = 'normal'
is_italic = 'roman'
save_file_name = ''
filename = ''
selected_text = ''


def choose_text_style(event):
    font_chosen = font_choice.get()
    size_chosen = font_size.get()
    text_area.config(font=(font_chosen, size_chosen, is_bold, is_italic))


def bold_text():
    font_chosen = font_choice.get()
    size_chosen = font_size.get()
    text_properties = font.Font(font=text_area['font']).actual()
    if text_properties['weight'] == 'normal':
        global is_bold
        is_bold = 'bold'
    else:
        is_bold = 'normal'
    text_area.config(font=(font_chosen, size_chosen, is_bold, is_italic))


def italicize_text():
    font_chosen = font_choice.get()
    size_chosen = font_size.get()
    text_properties = font.Font(font=text_area['font']).actual()
    if text_properties['slant'] == 'roman':
        global is_italic
        is_italic = 'italic'
    else:
        is_italic = 'roman'
    text_area.config(font=(font_chosen, size_chosen, is_bold, is_italic))


def align_left():
    content = text_area.get(1.0, END)
    text_area.tag_config('left', justify=LEFT)
    text_area.delete(1.0, END)
    text_area.insert(INSERT, content, 'left')


def align_center():
    content = text_area.get(1.0, END)
    text_area.tag_config('center', justify=CENTER)
    text_area.delete(1.0, END)
    text_area.insert(INSERT, content, 'center')


def align_right():
    content = text_area.get(1.0, END)
    text_area.tag_config('right', justify=RIGHT)
    text_area.delete(1.0, END)
    text_area.insert(INSERT, content, 'right')


def text_to_speech():
    engine = pyttsx3.init()
    engine.setProperty('rate', 130)
    engine.say(text_area.get(1.0, END))
    engine.runAndWait()
    engine.stop()


def select_color():
    color = colorchooser.askcolor()
    text_area.config(fg=str(color[1]))


def save_file(event=None):
    global save_file_name
    if save_file_name == '':
        save_as_file("")
    else:
        content = text_area.get(1.0, END)
        with open(save_file_name, 'w') as text_file:
            text_file.write(content)


def save_as_file(event=None):
    text_file = filedialog.asksaveasfilename(defaultextension=".*", initialdir="C:/", title="Save File",
                                             filetypes=(("Text File", "*.txt"), ("HTML File", "*.html"),
                                                        ("Python File", "*.py"), ("All Files", "*.*")))
    global save_file_name
    save_file_name = text_file

    if text_file != "":
        global filename
        filename = os.path.basename(text_file)
        root.title(f"{filename}")
        content = text_area.get(1.0, END)
        with open(text_file, 'w') as file:
            file.write(content)


def new_file(event=None):
    global save_file_name
    global filename
    root.title("Text Editor")
    save_file_name = ''
    filename = ''
    text_area.delete(1.0, END)


def open_file(event=None):
    text_file = filedialog.askopenfilename(initialdir="C:/", title="Open File",
                                           filetypes=(("Text Files", "*.txt"), ("HTML Files", "*.html"),
                                                      ("Python Files", "*.py"), ("All Files", "*.*")))
    global filename
    global save_file_name
    save_file_name = text_file

    if text_file != '':
        filename = os.path.basename(text_file)
        root.title(f"{filename}")

        with open(text_file, 'r') as file:
            content = file.read()
            text_area.delete(1.0, END)
            text_area.insert(1.0, content)


def exit_file(event=None):
    global filename
    if text_area.edit_modified():
        if filename == '':
            filename = "file"
        action = messagebox.askyesnocancel('Warning!', f"Do you want to save changes to {filename}?")
        if action:
            save_file("")
        elif action is None:
            pass
        else:
            root.quit()
    else:
        root.quit()


def print_file(event=None):
    tmp_file = tempfile.mktemp('.txt')
    open(tmp_file, 'w').write(text_area.get(1.0, END))
    os.startfile(tmp_file, 'print')


def cut_text(e):
    global selected_text
    if e:
        selected_text = root.clipboard_get()
    else:
        if text_area.selection_get():
            selected_text = text_area.selection_get()
            text_area.delete("sel.first", "sel.last")
            root.clipboard_clear()
            root.clipboard_append(selected_text)


def copy_text(e):
    global selected_text
    if e:
        selected_text = root.clipboard_get()
    else:
        if text_area.selection_get():
            selected_text = text_area.selection_get()
            root.clipboard_clear()
            root.clipboard_append(selected_text)


def paste_text(e):
    global selected_text
    if e:
        selected_text = root.clipboard_get()
    else:
        if selected_text:
            position = text_area.index(INSERT)
            text_area.insert(position, selected_text)


def find_text(event):
    new_root = Toplevel()

    def find_words():
        text_area.tag_remove("found", "1.0", END)
        word = find_field.get()
        start_pos = 1.0
        if word:
            while True:
                start_pos = text_area.search(word, start_pos, stopindex=END)
                if start_pos == "":
                    break
                end_pos = f'{start_pos}+{len(word)}c'
                text_area.tag_add("found", start_pos, end_pos)
                text_area.tag_config("found", foreground="white", background="blue")
                start_pos = end_pos

    def replace_word():
        word = find_field.get()
        if word:
            replace = replace_field.get()
            text = text_area.get(1.0, END)
            new_text = text.replace(word, replace)
            text_area.delete(1.0, END)
            text_area.insert(1.0, new_text)

    def clear():
        text_area.tag_remove("found", 1.0, END)
        new_root.destroy()

    new_root.title("Find")
    new_root.geometry('300x150+750+100')
    new_root.resizable(False, False)

    label = LabelFrame(new_root, text="Find/Replace")
    label.pack(pady=10)

    find_label = Label(label, text="Find")
    find_label.grid(row=0, column=0, pady=5)
    find_field = Entry(label)
    find_field.grid(row=0, column=1, padx=5, pady=5)

    replace_label = Label(label, text="Replace")
    replace_label.grid(row=1, column=0, pady=5)
    replace_field = Entry(label)
    replace_field.grid(row=1, column=1, padx=5, pady=10)

    find_button = Button(label, text='Find', command=find_words)
    find_button.grid(row=2, column=0, padx=30, pady=8)

    replace_button = Button(label, text='Replace', command=replace_word)
    replace_button.grid(row=2, column=1, padx=10, pady=8)

    new_root.protocol("WM_DELETE_WINDOW", clear)
    new_root.mainloop()


def toggle_toolbar():
    if not show_toolbar.get():
        toolbar.pack_forget()
    else:
        text_area.pack_forget()
        toolbar.pack(fill=X)
        text_area.pack(fill=BOTH, expand=TRUE)


def toggle_status_bar():
    if not show_statbar.get():
        status_bar.pack_forget()
    else:
        status_bar.pack(fill=X)


def change_background_theme(bg_color, fg_color):
    text_area.config(background=bg_color, foreground=fg_color)


def choose_custom_bg_color():
    color = colorchooser.askcolor()
    text_area.config(background=str(color[1]))


# Create the main window
root = Tk()
root.title("Text Editor")
root.geometry("1200x700+10+10")

menu_bar = Menu(root)  # Create a menu bar
root.config(menu=menu_bar)

# Toolbar
toolbar = Label(root)
toolbar.pack(side=TOP, fill=X)

# Font Family
font_families = font.families()
font_choice = StringVar()
font_family = Combobox(toolbar, width=30, font="Verdana 11", values=font_families, state="readonly",
                       textvariable=font_choice)  # Font family selection dropdown
font_family.current(font_families.index("Calibri"))  # Set default font
font_family.grid(row=0, column=0, padx=2)

# Font Size
size_choice = IntVar()
font_size = Combobox(toolbar, width=15, font="Verdana 11", values=tuple(range(5, 81)), state="readonly",
                     textvariable=size_choice)  # Font size selection dropdown
font_size.current(7)  # Set default font size
font_size.grid(row=0, column=1, padx=2)

# Bind combobox selection to the function
font_family.bind("<<ComboboxSelected>>", choose_text_style)
font_size.bind("<<ComboboxSelected>>", choose_text_style)

# Buttons
img_bold = PhotoImage(file="images/bold_icon.png")
img_italic = PhotoImage(file="images/italic_icon.png")
img_font_color = PhotoImage(file="images/font_color_icon.png")
img_left_align = PhotoImage(file="images/left_align_icon.png")
img_center_align = PhotoImage(file="images/center_align_text.png")
img_right_align = PhotoImage(file="images/right_align_text.png")
img_text_to_speech = PhotoImage(file="images/text_to_speech_icon.png")

boldButton = Button(toolbar, image=img_bold, state=NORMAL, command=bold_text)
boldButton.grid(row=0, column=2, padx=2)
italicButton = Button(toolbar, image=img_italic, command=italicize_text)
italicButton.grid(row=0, column=3, padx=2)
fontColorButton = Button(toolbar, image=img_font_color, command=select_color)
fontColorButton.grid(row=0, column=4, padx=2)
leftAlignButton = Button(toolbar, image=img_left_align, command=align_left)
leftAlignButton.grid(row=0, column=5, padx=2)
centerAlignButton = Button(toolbar, image=img_center_align, command=align_center)
centerAlignButton.grid(row=0, column=6, padx=2)
rightAlignButton = Button(toolbar, image=img_right_align, command=align_right)
rightAlignButton.grid(row=0, column=7, padx=2)
textToSpeechButton = Button(toolbar, image=img_text_to_speech, command=text_to_speech)
textToSpeechButton.grid(row=0, column=8, padx=2)

# Text Area
scrollBar = Scrollbar(root)
scrollBar.pack(side=RIGHT, fill=Y)
text_area = Text(root, yscrollcommand=scrollBar.set, font="Calibri, 11", selectbackground="blue",
                 selectforeground="white",
                 undo=True)
text_area.pack(fill=BOTH, expand=True)
scrollBar.config(command=text_area.yview)  # Enable scrolling

# Status Bar
status_bar = Label(root, text="Status Bar", font="Verdana 10")
status_bar.pack(side=BOTTOM, anchor="w")

# File Menu Option
file_m = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="File", menu=file_m)

# Loading icon images for file menu options
img_new = PhotoImage(file="images/new_icon.png")
img_open = PhotoImage(file="images/open_icon.png")
img_save = PhotoImage(file="images/save_icon.png")
img_save_as = PhotoImage(file="images/save_as_icon.png")
img_exit = PhotoImage(file="images/exit_icon.png")
img_print = PhotoImage(file="images/print_icon.png")

file_m.add_command(label="New", accelerator='Ctrl+N', image=img_new,compound=LEFT,
                   command=new_file)
file_m.add_command(label="Open", accelerator='Ctrl+O', image=img_open, compound=LEFT,
                   command=open_file)
file_m.add_command(label="Save", accelerator='Ctrl+S', image=img_save, compound=LEFT, command=save_file)
file_m.add_command(label="Save As", accelerator='Ctrl+Alt+S', image=img_save_as, compound=LEFT, command=save_as_file)
file_m.add_command(label="Print", accelerator='Ctrl+P', image=img_print, compound=LEFT, command=print_file)
file_m.add_separator()
file_m.add_command(label="Exit", accelerator='Ctrl+Q', image=img_exit, compound=LEFT, command=exit_file)

# Bind shortcut keys to functions
root.bind('<Control-s>', save_file)
root.bind('<Control-o>', open_file)
root.bind('<Control-n>', new_file)
root.bind('<Control-Alt-s>', save_as_file)
root.bind('<Control-q>', exit_file)
root.bind('<Control-p>', print_file)

# Edit Menu Option
edit_m = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Edit", menu=edit_m)

img_copy = PhotoImage(file="images/copy_icon.png")
img_paste = PhotoImage(file="images/paste_icon.png")
img_cut = PhotoImage(file="images/cut_icon.png")
img_undo = PhotoImage(file="images/undo_icon.png")
img_redo = PhotoImage(file="images/redo_icon.png")
img_find = PhotoImage(file="images/find_icon.png")

edit_m.add_command(label="Copy", accelerator="Ctrl+C", image=img_copy, compound=LEFT,
                   command=lambda: copy_text(False))
edit_m.add_command(label="Paste", accelerator="Ctrl+V", image=img_paste, compound=LEFT,
                   command=lambda: paste_text(False))
edit_m.add_command(label="Cut", accelerator="Ctrl+X", image=img_cut, compound=LEFT, command=lambda: cut_text(False))
edit_m.add_command(label="Undo", accelerator="Ctrl+Z", image=img_undo, compound=LEFT, command=text_area.edit_undo)
edit_m.add_command(label="Redo", accelerator="Ctrl+Y", image=img_redo, compound=LEFT, command=text_area.edit_redo)
edit_m.add_command(label="Find", accelerator="Ctrl+F", image=img_find, compound=LEFT, command=find_text)

# Bind shortcut keys to functions
root.bind('<Control-x>', cut_text)
root.bind('<Control-c>', copy_text)
root.bind('<Control-v>', paste_text)
root.bind('<Control-f>', find_text)

# View Menu Option
show_toolbar = BooleanVar()  # Boolean variable for toolbar visibility
show_toolbar.set(True)
show_statbar = BooleanVar()  # Boolean variable for status bar visibility
show_statbar.set(True)

view_m = Menu(menu_bar, tearoff=False)
view_m.add_checkbutton(label="Tool Bar", variable=show_toolbar, onvalue=True, offvalue=False, command=toggle_toolbar)
view_m.add_checkbutton(label="Status Bar", variable=show_statbar, onvalue=True, offvalue=False,
                       command=toggle_status_bar)
menu_bar.add_cascade(label="View", menu=view_m)

# Themes Menu Option
themes_m = Menu(menu_bar, tearoff=False)
menu_bar.add_cascade(label="Themes", menu=themes_m)
theme_choice = StringVar()

img_light = PhotoImage(file="images/light_icon.png")
img_dark = PhotoImage(file="images/dark_icon.png")
img_light_blue = PhotoImage(file="images/light_blue_icon.png")
img_custom_bg_color = PhotoImage(file="images/custom_bg_color_icon.png")

themes_m.add_radiobutton(label="Light (default)", image=img_light, compound=LEFT, variable=theme_choice,
                         command=lambda: change_background_theme("#ffffff", "#000000"))
themes_m.add_radiobutton(label="Dark", image=img_dark, compound=LEFT, variable=theme_choice,
                         command=lambda: change_background_theme("#000000", "#a1afb3"))
themes_m.add_radiobutton(label="Light Blue", image=img_light_blue, compound=LEFT, variable=theme_choice,
                         command=lambda: change_background_theme("#7bd0e3", "#000000"))
themes_m.add_radiobutton(label="Custom", image=img_custom_bg_color, compound=LEFT, variable=theme_choice,
                         command=change_background_theme)

root.mainloop()
