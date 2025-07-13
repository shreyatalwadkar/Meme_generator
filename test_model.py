import os
import random
import tkinter as tk
from PIL import Image, ImageDraw, ImageFont
from guizero import App, TextBox, Drawing, Combo, PushButton, Box, Window, Text

EMOJI_MEME_DIRECTORY = 'emoji_memes'
KEYWORD_MEME_DIRECTORY = 'memes'

images = []
current_image = 0
top_color = "orange"
bottom_color = "blue"

available_keywords = [
    'sad', 'cool', 'bad', 'baby',
    'love', 'hope', 'fear', 'calm',
    'bold', 'lazy', 'wild', 'hard',
    'fast', 'cute', 'fire'
]


def load_meme_by_emoji(emoji):
    emoji_path = os.path.join(EMOJI_MEME_DIRECTORY, emoji)

    if not os.path.exists(emoji_path):
        print(f"No directory found for emoji: {emoji}")
        return None

    meme_files = [
        f for f in os.listdir(emoji_path)
        if f.endswith(('.png', '.jpg', '.jpeg'))
    ]

    if not meme_files:
        print(f"No memes found for emoji: {emoji}")
        return None

    meme_file = random.choice(meme_files)
    return os.path.join(emoji_path, meme_file)

def load_memes_by_keyword(keyword):
    memes = []
    directory = os.path.join(KEYWORD_MEME_DIRECTORY, keyword)
    if os.path.exists(directory):
        for filename in os.listdir(directory):
            if filename.endswith(('.jpg', '.png')):
                caption_file = os.path.join(directory, os.path.splitext(filename)[0] + '.txt')
                if os.path.exists(caption_file):
                    with open(caption_file, 'r') as f:
                        caption = f.read().strip()
                    memes.append((os.path.join(directory, filename), caption))
    return memes


def create_meme(image_path, caption, output_path):

    img = Image.open(image_path)
    draw = ImageDraw.Draw(img)

    try:

        font = ImageFont.truetype("arial.ttf", size=28)
    except IOError:

        font = ImageFont.load_default()

    width, height = img.size

    bbox = font.getbbox(caption)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    text_position = ((width - text_width) / 2, height - text_height - 10)

    outline_color = "black"
    # Outline
    draw.text((text_position[0] - 1, text_position[1] - 1), caption, font=font, fill=outline_color)
    draw.text((text_position[0] + 1, text_position[1] - 1), caption, font=font, fill=outline_color)
    draw.text((text_position[0] - 1, text_position[1] + 1), caption, font=font, fill=outline_color)
    draw.text((text_position[0] + 1, text_position[1] + 1), caption, font=font, fill=outline_color)
    # Text
    draw.text(text_position, caption, font=font, fill="white")

    # Save the meme
    img.save(output_path)


def draw_meme():
    meme.clear()

    if images:
        meme_image_path = images[current_image]
        try:
            meme_image = Image.open(meme_image_path)
            meme_image = meme_image.resize((500, 500), Image.LANCZOS)
            meme_image.save("temp_meme.png")
            meme.image(0, 0, "temp_meme.png")
        except Exception as e:
            print(f"Error loading image: {e}")
            meme.text(150, 250, "Error loading image", size=28, color="red")
            return

        if top_text.value:
            meme.text(10, 10, top_text.value, color=top_color, size=28, font="comic sans")

        if bottom_text.value:

            try:
                font = ImageFont.truetype("arial.ttf", size=28)
            except IOError:
                font = ImageFont.load_default()
            bbox = font.getbbox(bottom_text.value)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            bottom_y_position = 500 - text_height -20
            meme.text(10, bottom_y_position, bottom_text.value, color=bottom_color, size=28, font="comic sans")


def next_meme():
    global current_image
    if images:
        current_image = (current_image + 1) % len(images)
        draw_meme()


# Functions to change text colors
def change_top_color(color):
    global top_color
    top_color = color
    draw_meme()

def change_bottom_color(color):
    global bottom_color
    bottom_color = color
    draw_meme()

def on_emoji_click(emoji):
    meme_path = load_meme_by_emoji(emoji)

    if meme_path:
        global images, current_image
        images = [meme_path]
        current_image = 0
        draw_meme()
    else:
        meme.clear()
        meme.text(150, 250, "No meme available", size=28, color="red")


def on_keyword_submit(selected_keyword=None):
    if selected_keyword:
        keyword = selected_keyword
    else:
        keyword = keyword_input.value.strip().lower()

    if not keyword:
        keyword_feedback.value = "Please enter a keyword."
        keyword_feedback.color = "red"
        return

    if keyword not in available_keywords:
        keyword_feedback.value = f"Keyword '{keyword}' not found."
        keyword_feedback.color = "red"
        return

    memes = load_memes_by_keyword(keyword)

    if not memes:
        meme.clear()
        meme.text(150, 250, "No memes found for this keyword.", size=28, color="red")
        keyword_feedback.value = f"No memes found for keyword '{keyword}'."
        keyword_feedback.color = "red"
        return

    meme_image, caption = random.choice(memes)
    output_path = os.path.join(KEYWORD_MEME_DIRECTORY, keyword, f"generated_{random.randint(1000, 9999)}.png")

    create_meme(meme_image, caption, output_path)
    print(f"Meme created: {output_path}")

    global images, current_image
    images = [output_path]
    current_image = 0
    draw_meme()

    keyword_feedback.value = f"Meme created for keyword '{keyword}'."
    keyword_feedback.color = "green"

    if not selected_keyword:
        keyword_input.value = ""


def on_keyword_select(selected_keyword):
    keyword_input.value = selected_keyword
    on_keyword_submit(selected_keyword)


app = App("Meme Generator", width=800, height=800)

main_box = Box(app, layout="grid")

# Left side: Controls
controls_box = Box(main_box, layout="vertical", grid=[0, 0], align="left", width="fill", height="fill")

color_label = PushButton(controls_box, text="Select Text Color", enabled=False)
color = Combo(controls_box, options=["black", "white", "red", "green", "blue", "orange"], command=draw_meme,
              grid=[0, 0])
color.value = "orange"

top_text = TextBox(controls_box, text="Top Text", width=40, command=draw_meme, grid=[0, 1])
bottom_text = TextBox(controls_box, text="Bottom Text", width=40, command=draw_meme, grid=[0, 2])

top_color_button = PushButton(controls_box, text="Change Top Color", command=lambda: change_top_color(color.value),
                              grid=[0, 3])
bottom_color_button = PushButton(controls_box, text="Change Bottom Color",
                                 command=lambda: change_bottom_color(color.value), grid=[0, 4])

next_button = PushButton(controls_box, text="Next Meme", command=next_meme, grid=[0, 5])

keyword_input = TextBox(controls_box, text="Enter keyword (e.g., baby, bad, water)", width=40, grid=[0, 6])
keyword_button = PushButton(controls_box, text="Generate Meme by Keyword", command=on_keyword_submit, grid=[0, 7])

keyword_feedback = Text(controls_box, text="", color="red", grid=[0, 8])

separator = Box(controls_box, width="fill", height=2, grid=[0, 9], align="left")
separator.bg = "gray"

if available_keywords:
    keywords_buttons_label = Text(controls_box, text="Available Keywords:", grid=[0, 10], size=12, color="blue")
    keywords_buttons_box = Box(controls_box, layout="grid", grid=[0, 11], width="fill")

    columns = 3
    button_width = 15
    button_height = 2

    for index, keyword in enumerate(available_keywords):
        row = index // columns
        col = index % columns
        btn = PushButton(
            keywords_buttons_box,
            text=keyword.capitalize(),
            command=lambda k=keyword: on_keyword_submit(k),
            grid=[col, row],
            width=button_width,
            align="left"
        )
        btn.bg = "lightblue"
else:
    keywords_buttons_label = Text(controls_box, text="No available keywords found.", grid=[0, 10], color="red")

meme_box = Box(main_box, layout="grid", grid=[1, 0], align="right", width="fill", height="fill")

meme = Drawing(meme_box, width=500, height=500, grid=[0, 0])
draw_meme()

emoji_window = Window(app, title="Select Emoji", width=200, height=600)
emoji_window.bg = "white"

canvas = tk.Canvas(emoji_window.tk, borderwidth=0, background="#ffffff")
scrollbar = tk.Scrollbar(emoji_window.tk, orient="vertical", command=canvas.yview)
scrollable_frame = tk.Frame(canvas, background="#ffffff")

scrollable_frame.bind(
    "<Configure>",
    lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
)

canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
canvas.configure(yscrollcommand=scrollbar.set)

canvas.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

emojis = [
    "😀", "😥", "😎", "🤔", "😂", "🥳", "🤯", "😱", "😴",
    "😍", "😇", "🧐", "🤪", "😈", "👻", "💩", "😺", "🙈",
    "🙉", "🙊"
]

for emoji in emojis:
    btn = tk.Button(
        scrollable_frame,
        text=emoji,
        font=("Arial", 24),
        command=lambda e=emoji: on_emoji_click(e)
    )
    btn.pack(pady=5, padx=10)

app.display()