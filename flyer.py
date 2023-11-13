from PIL import Image, ImageDraw, ImageFont
import qrcode

def draw_multiline_text(draw, text, position, font, fill, max_width):
    """
    Draw multiline text on the image, splitting lines automatically based on max_width.
    """
    lines = []
    words = text.split()

    while words:
        line = ''
        while words and draw.textsize(line + words[0], font=font)[0] <= max_width:
            line += (words.pop(0) + ' ')
        lines.append(line)

    y = position[1]
    for line in lines:
        draw.text((position[0], y), line, font=font, fill=fill)
        y += font.getsize(line)[1]

 
def create_flyer(background_image_path, logo_image_path, font_name, header_text, sub_header_text, body_text, when_text, where_text, url, output_path):
    # Load the background image and convert it to 'RGBA'
    background = Image.open(background_image_path).convert("RGBA")
    desired_size = (1080, 1080)  # Set your desired width and height
    background = Image.new("RGBA", desired_size, "white")  # Or any other background color
    original_background = Image.open(background_image_path).convert("RGBA")
    # Optionally resize or reposition the original background before pasting
    background.paste(original_background, (0, 0))  # Adjust position as needed


    # Load the logo
    logo = Image.open(logo_image_path)
    logo_size = 250  # Adjust this size as needed
    logo.thumbnail((logo_size, logo_size))

    # Create QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white").convert("RGBA")
    qr_size = 250  # Adjust this size as needed
    qr_img.thumbnail((qr_size, qr_size))

    # Prepare draw object
    draw = ImageDraw.Draw(background)
    
    # Fonts - Increase font sizes
    header_font_size = 50  # No change
    sub_header_font_size = 75  # No change
    body_font_size = 60    # No change
    time_font_size = 60    # Increased font size for date/time
    venue_font_size = 40   # No change

    header_font = ImageFont.truetype(font_name, header_font_size)
    sub_header_font = ImageFont.truetype(font_name, sub_header_font_size)
    body_font = ImageFont.truetype(font_name, body_font_size)
    time_font = ImageFont.truetype(font_name, time_font_size)
    venue_font = ImageFont.truetype(font_name, venue_font_size)


    # Adjusted positions for header and sub-header
    header_start_y = background.height // 9  # Adjust as needed
    sub_header_start_y = header_start_y + header_font_size + 20  # Adjust as needed

    # Main Header Text - Centered
    header_width, header_height = draw.textsize(header_text, font=header_font)
    header_position = ((background.width - header_width) // 2, header_start_y)
    draw.text(header_position, header_text, font=header_font, fill="white")

    # Sub-header Text - Centered
    sub_header_width, sub_header_height = draw.textsize(sub_header_text, font=sub_header_font)
    sub_header_position = ((background.width - sub_header_width) // 2, sub_header_start_y)
    draw.text(sub_header_position, sub_header_text, font=sub_header_font, fill="white")

    # Time Text - Centered above Venue
    additional_offset = 80  # You can adjust this value

    # Time Text position with additional offset
    time_text_position = (background.width // 2, background.height - qr_img.height - 10 - time_font_size - venue_font_size - 60 - additional_offset)


    time_width, time_height = draw.textsize(when_text, font=time_font)
    time_position = ((background.width - time_width) // 2, time_text_position[1])
    draw.text(time_position, when_text, font=time_font, fill="white")

    # Venue Text - Centered below Time
    venue_text_position = (background.width // 2, time_text_position[1] + time_font_size + 20)
    venue_width, venue_height = draw.textsize(where_text, font=venue_font)
    venue_position = ((background.width - venue_width) // 2, venue_text_position[1])
    draw.text(venue_position, where_text, font=venue_font, fill="white")


    # Body Text - Multiline with narrower column, starting lower
    column_width = background.width - 250  # Narrower column width
    body_start_position = (10 + (background.width - column_width) // 2, background.height // 3.5)  # Starting lower
    draw_multiline_text(draw, body_text, body_start_position, body_font, "white", column_width)

    # Paste logo and QR code
    background.paste(logo, (background.width - logo.width - 10, background.height - logo.height - 10), logo)
    background.paste(qr_img, (10, background.height - qr_img.height - 10), qr_img)

    # Convert to 'RGB' if saving as JPEG
    if output_path.lower().endswith('.jpg') or output_path.lower().endswith('.jpeg'):
        background = background.convert('RGB')

    # Save the result
    background.save(output_path)


# Example usage
create_flyer("llms.png", "logo.png", "Quicksand-Bold.ttf", "Calango Hacker Clube : Future Coding #2","Programação com LLMs", "Olhando o novo API do OpenAI", "Quinta, dia 16 de novembro. 19:30 ", 
             "SCLN 405 Bloco D Loja 26 Subsolo CEP 70846-540 ", "https://calango.club/projetos/futurecoding", "futurecode2.jpg")

 
 
