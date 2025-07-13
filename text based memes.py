import os
import random
from PIL import Image, ImageDraw, ImageFont

print("Enter any of the following keywords :- baby, bad, water")
# Function to load memes based on the selected keyword
def load_memes(keyword):
  memes = []
  directory = f"memes/{keyword}/"
  if os.path.exists(directory):
    for filename in os.listdir(directory):
      if filename.endswith('.jpg') or filename.endswith('.png'):
        caption_file = os.path.join(directory, filename.replace('.jpg', '.txt').replace('.png', '.txt'))
        if os.path.exists(caption_file):
          with open(caption_file, 'r') as f:
            caption = f.read().strip()
          memes.append((os.path.join(directory, filename), caption))
  return memes


# Function to create a meme
def create_meme(image_path, caption, output_path):
  # Open the image
  img = Image.open(image_path)
  draw = ImageDraw.Draw(img)

  # Choose a font and size
  font = ImageFont.load_default()  # You can load a specific TTF font if desired

  # Positioning the text
  width, height = img.size
  text_position = (10, height - 30)  # Bottom left

  # Draw text on the image
  draw.text(text_position, caption, fill="white", font=font)

  # Save the meme
  img.save(output_path)


# Main function
def main():
  keyword = input("Enter a keyword: ")
  memes = load_memes(keyword)

  if not memes:
    print("No memes found for this keyword.")
    return

  meme_image, caption = random.choice(memes)
  output_path = f"memes/{keyword}.png"
  create_meme(meme_image, caption, output_path)
  print(f"Meme created: {output_path}")


if __name__ == "__main__":
  main()

