from PIL import Image, ImageDraw, ImageFont

def wrap_text(text, font, max_width, draw):
    '''
    Split string into array of string, where each element
    is a string which represents the text on a single line.
    '''
    lines = []
    current_line = ""
    words = text.split()
    for word in words:
        # Check if the word itself fits on the current line
        if draw.textlength(current_line + word, font=font) <= max_width:
            current_line += " " + word
        else:
        # If the word doesn't fit, check if it's longer than max_width
            if draw.textlength(word, font=font) > max_width:
            # Handle long words that wouldn't fit on any line
                raise ValueError(f"Encountered word '{word}' that is longer than max width")
            else:
            # If the word fits on a single line, start a new line with it
                lines.append(current_line.strip())
                current_line = word
    lines.append(current_line.strip())
    return lines

def generate_image(text):
    '''
    Creates thumbnail for the video.

    Parameters:
    text: string to be overlayed on the template image.

    Returns:
    Does not return anything but saved generated image to 
    image folder as output_image.jpg
    '''
    # for testing
    # text = "This is a very long long long title for a post, \
    #         did it wrap around? well it should have, fix it! \
    #         some text to make this even longer longer!"

    image_path = "../image/template.jpg"
    font_path = "../font/LTSaeada-Regular.otf"  
    font_size = 100
    output_url = "../image/output_image.jpg"
    max_line_width = 1500

    try:
        # Open the image
        image = Image.open(image_path)

        # Create a drawing object
        draw = ImageDraw.Draw(image)

        # Load the font
        font = ImageFont.truetype(font_path, size=font_size)

        # Wrap the text into multiple lines
        wrapped_text = wrap_text(text, font, max_line_width, draw)
        # print(wrapped_text)

        # Set text starting position ie top left
        x = 200
        y = 320

        # Draw each line of text with a slight vertical offset
        for line in wrapped_text:
            draw.text((x, y), line, font=font, fill="black")
            y += font_size  # Adjust y based on your desired line spacing

        image.save(output_url)
        print("image generated")

    except Exception as e:
        print(f"An error occurred: {e}")

# for testing
# generate_image()
