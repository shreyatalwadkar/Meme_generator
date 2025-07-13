import os
import random
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk

# Set the path to your meme dataset
MEME_DIRECTORY = 'emoji_memes'


# Function to load a random meme image based on the selected emoji
def load_meme(emoji):
    emoji_path = os.path.join(MEME_DIRECTORY, emoji)

    if not os.path.exists(emoji_path):
        print(f"No directory found for emoji: {emoji}")
        return None

    # Select a random meme from the folder
    meme_files = [f for f in os.listdir(emoji_path) if f.endswith(('.png', '.jpg', '.jpeg'))]

    if not meme_files:
        print(f"No memes found for emoji: {emoji}")
        return None

    meme_file = random.choice(meme_files)
    return os.path.join(emoji_path, meme_file)


# Function to display the selected meme
def display_meme(image_path):
    image = Image.open(image_path)
    image.thumbnail((500, 500))  # Resize the image to fit in the window
    img = ImageTk.PhotoImage(image)

    meme_label.config(image=img)
    meme_label.image = img  # Keep a reference of the image to prevent garbage collection


# Function to handle emoji button click
def on_emoji_click(emoji):
    meme_path = load_meme(emoji)

    if meme_path:
        display_meme(meme_path)
    else:
        meme_label.config(text="No meme available")


# Create the main window
root = tk.Tk()
root.title("Meme Selector")

# Display area for the meme
meme_label = tk.Label(root, text="Select an emoji to see a meme")
meme_label.pack(pady=20)

# Frame to hold emoji buttons
emoji_frame = tk.Frame(root)
emoji_frame.pack(pady=20)

# Define a set of emojis to choose from
emoji_list = ["😀", "😥", "😎", "🤔", "😂"]

# Create buttons for each emoji
for emoji in emoji_list:
    button = tk.Button(emoji_frame, text=emoji, font=("Arial", 24), command=lambda e=emoji: on_emoji_click(e))
    button.pack(side=tk.LEFT, padx=10)

# Run the Tkinter event loop
root.mainloop()



