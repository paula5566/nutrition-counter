import tkinter as tk
from tkinter import ttk
import pandas as pd
import tkinter.messagebox  # Import messagebox for showing alerts
import os
import sys

# Function to convert RGB to hex
def rgb_to_hex(r, g, b):
    return f'#{r:02x}{g:02x}{b:02x}'

# Create the main window
root = tk.Tk()
root.title("Nutrition Counter[BETA]")  # Set the title of the window
# Set background color using RGB
bg_color = rgb_to_hex(30, 30, 30)  # RGB value converted to hex
bg_color2 = rgb_to_hex(50, 50, 51)
root.configure(bg=bg_color)

#icon_path = os.path.join(sys._MEIPASS, "nutrition_program_icon2-removebg-preview.ico") if hasattr(sys, '_MEIPASS') else "nutrition_program_icon2-removebg-preview.ico"
#root.iconbitmap(icon_path)

# Load dataset from CSV
df = pd.read_csv("merged_food_dataset.csv")
ds = set(df['food'].str.lower())

class Main:
    @staticmethod
    def on_minimize():
        root.iconify()  # Minimizes the window

    @staticmethod
    def on_maximize():
        # Toggle between maximizing and restoring
        if root.state() == 'normal':
            root.state('zoomed')  # Maximize the window
        else:
            root.state('normal')  # Restore the window to its original size

    @staticmethod
    def on_exit():
        root.destroy()  # Closes the window

    @staticmethod
    def toggle_fullscreen(event=None):
        root.attributes('-fullscreen', not root.attributes('-fullscreen'))

    @staticmethod
    def end_fullscreen(event=None):
        root.attributes('-fullscreen', False)
        root.geometry('800x600')  # Optional: Set a default size when exiting fullscreen

# Bind escape key to exit fullscreen
root.bind('<Escape>', Main.end_fullscreen)

# Create a frame for custom buttons and the title
header_frame = tk.Frame(root, bg=bg_color, height=30)
header_frame.pack(fill=tk.X, side=tk.TOP)

# Create a Label widget to display the title of the app
title_label = tk.Label(header_frame, text="Nutrition Counter[BETA]", bg=bg_color, fg='white', font=("Arial", 16))
title_label.pack(side=tk.LEFT, padx=10, pady=5)

# Function to change color on hover
def on_enter(event):
    event.widget['bg'] = 'red'

def on_leave(event):
    event.widget['bg'] = bg_color

# Function to change color on hover
def on_enter2(event):
    event.widget['bg'] = bg_color2

def on_leave2(event):
    event.widget['bg'] = bg_color

# Create the exit button
exit_button = tk.Button(header_frame, text="❌", command=Main.on_exit, width=3,
                        height=1, bg=bg_color, fg='white', relief='flat',
                        font=("Arial", 12))
exit_button.pack(side=tk.RIGHT, padx=1, pady=1)
# Bind the hover events
exit_button.bind("<Enter>", on_enter)
exit_button.bind("<Leave>", on_leave)

# Create the minimize button
minimize_button = tk.Button(header_frame, text="—", command=Main.on_minimize,
                            width=3, height=1, bg=bg_color, fg='white',
                            relief='flat', font=("Arial", 12))
minimize_button.pack(side=tk.RIGHT, padx=1, pady=1)

minimize_button.bind("<Enter>", on_enter2)
minimize_button.bind("<Leave>", on_leave2)

# Make the window responsive
root.bind("<F11>", lambda event: root.attributes('-fullscreen', True))  # Fullscreen toggle
root.bind("<Escape>", lambda event: root.attributes('-fullscreen', False))  # Exit fullscreen

# Set the window to fullscreen
root.attributes('-fullscreen', True)

class LabelsApp:
    def __init__(self, root):
        self.root = root
        self.labels = []  # List to keep track of dynamically added labels
        self.label_frames = []  # List to keep track of label frames

        # Create a frame for the Treeview and buttons
        main_frame = tk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a frame for buttons
        button_frame = tk.Frame(main_frame, bg=bg_color, width=200)  # Fixed width for button area
        button_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Create a frame for Treeview and buttons
        tree_frame = tk.Frame(main_frame)
        tree_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a Treeview widget to display the table
        self.tree = ttk.Treeview(tree_frame, columns=list(df.columns), show="headings")
        for col in df.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill=tk.BOTH, expand=True)

        # Create and configure the style for the Treeview
        style = ttk.Style()
        style.configure("Custom.Treeview",
                        background=bg_color,
                        fieldbackground=bg_color,
                        foreground="white",
                        highlightthickness=0)  # Optional: Remove the focus highlight

        # Apply the style to the Treeview
        self.tree.configure(style="Custom.Treeview")

        # Create a Canvas widget and a Scrollbar
        self.canvas = tk.Canvas(tree_frame, bg=bg_color)
        self.scrollbar = tk.Scrollbar(tree_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg=bg_color)
        
        # Create a window on the canvas to contain the scrollable frame
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # Bind the configure event to update the scroll region
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Create and pack buttons with updated background colors
        self.create_button(button_frame, "Add Food", self.add_new_label, '#FFFFE0')  # Light black
        self.create_button(button_frame, "Count Calories", self.count_calories, '#D3D3D3')  # Light black
        self.create_button(button_frame, "Count Fats", self.count_fats, '#D3D3D3')  # Light black
        self.create_button(button_frame, "Count Protiens", self.count_protiens, '#D3D3D3')  # Light black
        self.create_button(button_frame, "Count Carbohydrates", self.count_carbohydrates, '#D3D3D3')  # Light black
        self.create_button(button_frame, "Count Cholesterol", self.count_cholesterol, '#D3D3D3')  # Light black
        self.create_button(button_frame, "Count All", self.count_all, '#D3D3D3')  # Light black
        self.create_button(button_frame, "Submit", self.submit_text, 'lightgreen')
        self.create_button(button_frame, "Clear Labels", self.clear_labels, 'lightcoral')
        self.create_button(button_frame, "Clear Table", self.clear_table, 'lightcoral')
        # Add About and Contact Us buttons
        self.create_button(button_frame, "About", self.show_about, '#ADD8E6')
        self.create_button(button_frame, "Contact Us", self.show_contact_us, '#ADD8E6')

    def create_button(self, parent, text, command, bg_color='lightgray'):
        button = tk.Button(parent, text=text, command=command, bg=bg_color, fg='black', width=20, height=2)
        button.pack(pady=10, padx=10)

    def submit_text(self):
        # Clear previous rows in the Treeview
        self.clear_table()

        for label_entry, info_label, _ in self.labels:
            label_text = label_entry.get().strip().lower()  # Get and clean the text from Entry widget
            if label_text in ds:  # Check if the text is in the dataset
                info_label.config(text="Found in dataset")
                label_entry.config(bg='lightgreen')  # Highlight if found in dataset

                # Get the rows of the found food item
                rows = df[df['food'].str.lower() == label_text]
                for _, row in rows.iterrows():
                    self.tree.insert("", "end", values=list(row))

            else:
                info_label.config(text='Not found in dataset.')
                label_entry.config(bg='lightcoral')  # Highlight if not found in dataset

    def clear_table(self):
        # Clear all rows in the Treeview
        for row in self.tree.get_children():
            self.tree.delete(row)

    def clear_labels(self):
        # Clear all label frames and their contents
        for frame in self.label_frames:
            frame.destroy()
        self.labels = []
        self.label_frames = []

    def add_new_label(self):

        # Create a frame to hold the new label and delete button
        frame = tk.Frame(self.scrollable_frame, bg=bg_color)
        frame.pack(pady=10, fill='x', padx=500)  # Add padding around the frame

        # Create a grey rectangle to hold the Entry and Label widgets
        grey_frame = tk.Frame(frame, bg='lightgrey', padx=10, pady=10)
        grey_frame.pack(pady=5, padx=5, fill='x')  # Center grey frame and add padding

        # Create an Entry widget for new label text
        label_entry = tk.Entry(grey_frame, bg='white', font=("Verdana", 15))  # White background for the Entry
        label_entry.grid(row=0, column=0, sticky='ew', pady=(0, 5))  # Center Entry widget with bottom padding

        # Create a dropdown list for suggestions
        suggestions_listbox = tk.Listbox(grey_frame, height=5, font=("Verdana", 12))
        suggestions_listbox.grid(row=1, column=0, pady=5)  # Place Listbox below Entry

        # Bind the key release event to update suggestions
        label_entry.bind("<KeyRelease>", lambda event, entry=label_entry, listbox=suggestions_listbox: self.update_suggestions(entry, listbox))

        # Create a Label widget to show information about the food
        info_label = tk.Label(grey_frame, text='', bg='lightgrey', font=("Verdana", 12))  # White background for the Label
        info_label.grid(row=2, column=0, pady=5)  # Place Label below Listbox

        # Create a Button widget to delete the new label
        delete_button = tk.Button(grey_frame, text="Delete", command=lambda: self.delete_label(frame, label_entry, info_label, suggestions_listbox))
        delete_button.grid(row=3, column=0, pady=5)  # Place Delete button below Label

        # Add the new label, info label, and suggestions listbox to the list
        self.labels.append((label_entry, info_label, suggestions_listbox))
        self.label_frames.append(frame)  # Keep track of label frames

    def delete_label(self, frame, label_entry, info_label, suggestions_listbox):
        # Destroy the frame which contains the label and delete button
        frame.destroy()
        # Remove the label, info label, and suggestions listbox from the list of labels
        self.labels.remove((label_entry, info_label, suggestions_listbox))
        self.label_frames.remove(frame)  # Remove from the list of label frames

    def update_suggestions(self, entry, listbox):
        # Clear the previous suggestions
        listbox.delete(0, tk.END)
        
        # Get the current text from the entry
        text = entry.get().strip().lower()

        # Find suggestions from the dataset
        if text:
            matches = [food for food in ds if food.startswith(text)]
            for match in matches:
                listbox.insert(tk.END, match)

        # Show the selected suggestion in the entry
        def on_select(event):
            selection = listbox.get(listbox.curselection())
            entry.delete(0, tk.END)
            entry.insert(0, selection)
            listbox.delete(0, tk.END)

        listbox.bind("<<ListboxSelect>>", on_select)

    def count_calories(self):
        total_calories = 0
    
        # Iterate over all items in the Treeview
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            try:
                calories = float(values[2])  # Use the index 2 for calories
                total_calories += calories
            except (ValueError, IndexError):
                pass  # Handle the case where the calories value is not a valid number or index is out of range

        tk.messagebox.showinfo("Total Calories", f"Total Calories: {total_calories}")

    def count_fats(self):
        total_fats = 0
    
        # Iterate over all items in the Treeview
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            try:
                fats = float(values[3])  # Use the index 2 for fats
                total_fats += fats
            except (ValueError, IndexError):
                pass  # Handle the case where the fats value is not a valid number or index is out of range

        tk.messagebox.showinfo("Total Fats", f"Total Fats: {total_fats}")

    def count_protiens(self):
        total_protiens = 0
    
        # Iterate over all items in the Treeview
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            try:
                protiens = float(values[4])  # Use the index 2 for protiens
                total_protiens += protiens
            except (ValueError, IndexError):
                pass  # Handle the case where the protiens value is not a valid number or index is out of range

        tk.messagebox.showinfo("Total Protiens", f"Total Protiens: {total_protiens}")

    def count_carbohydrates(self):
        total_carbohydrates = 0
    
        # Iterate over all items in the Treeview
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            try:
                carbohydrates = float(values[5])  # Use the index 2 for carbohydrates
                total_carbohydrates += carbohydrates
            except (ValueError, IndexError):
                pass  # Handle the case where the carbohydrates value is not a valid number or index is out of range

        tk.messagebox.showinfo("Total Carbohydrates", f"Total Carbohydrates: {total_carbohydrates}")

    def count_cholesterol(self):
        total_cholesterol = 0
    
        # Iterate over all items in the Treeview
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            try:
                cholesterol = float(values[6])  # Use the index 2 for cholesterol
                total_cholesterol += cholesterol
            except (ValueError, IndexError):
                pass  # Handle the case where the cholesterol value is not a valid number or index is out of range

        tk.messagebox.showinfo("Total Cholesterol", f"Total Cholesterol: {total_cholesterol}")

    def count_all(self):
        total_calories = 0
        total_fats = 0
        total_proteins = 0
        total_carbohydrates = 0
        total_cholesterol = 0
    
        # Iterate over all items in the Treeview
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            try:
                calories = float(values[2])  # Use the index 2 for calories
                total_calories += calories

                fats = float(values[3])  # Use the index 3 for fats
                total_fats += fats

                proteins = float(values[4])  # Use the index 4 for proteins
                total_proteins += proteins

                carbohydrates = float(values[5])  # Use the index 5 for carbohydrates
                total_carbohydrates += carbohydrates

                cholesterol = float(values[6])  # Use the index 6 for cholesterol
                total_cholesterol += cholesterol
            except (ValueError, IndexError):
                pass  # Handle the case where the cholesterol value is not a valid number or index is out of range

        tk.messagebox.showinfo("All Totals", f"Total Calories: {total_calories}\n\nTotal Fats: {total_fats}\n\nTotal Proteins: {total_proteins}\n\nTotal Carbohydrates: {total_carbohydrates}\n\nTotal Cholesterol: {total_cholesterol}")


    def show_about(self):
        tk.messagebox.showinfo("About", 'Dietly company:\n\nPaula Data(Developer)\n\n"Dietly eat Right, feel Bright"')

    def show_contact_us(self):
        tk.messagebox.showinfo("Contact Us", "For support or feedback, please contact us at:\n\nsupport@nutritioncounter.com")

# Instantiate the LabelsApp class
app = LabelsApp(root)

# Run the application
root.mainloop()
