import re
import emoji
import string
import numpy as np
from pilmoji import Pilmoji
import random
from PIL import Image, ImageFont, ImageDraw
from utils import (
    get_tweet_info,
    check_last_space,
    remove_start_space,
    get_profile_pics_mask,
    get_images_height,
    attach_images
)




my_username = "@_screenshoter"


def clean_text(text):
    words_per_line = 44
    no_lines = (len(text) // words_per_line) + 1
    lines = []
    for line_no in range(no_lines + 1):
        if len(text) <= words_per_line:
            line = text
            line = remove_start_space(line)
            line = re.sub("http[s]://t.co\S+", "", line)
            lines.append(line)
            new_text = "".join(lines)
            return new_text, len(lines)
        line, words_per_line = check_last_space(words_per_line, text)
        line = re.sub("http[s]://t.co\S+", "", line)
        text = text.replace(text[:words_per_line], "")
        words = line.split()
        line = " ".join(words)
        line = remove_start_space(line)
        line = line + "\n"
        lines.append(line)
        words_per_line = 47


def find_n(text, text_range):
    text = text[text_range[0] :]
    text_split = text.split("\n")
    new_text = ""
    total_lines = 0
    for txt in text_split:
        if txt == "":
            new_text = new_text + "\n"
            total_lines = total_lines + 1
        else:
            txt_lines, no_lines = clean_text(txt)
            new_text = new_text + txt_lines + "\n"
            total_lines = total_lines + no_lines
    new_text_stripped = new_text.rstrip("\n")
    total_lines = total_lines - (len(new_text) - len(new_text_stripped)) + 1
    return new_text, total_lines


def write_word_to_img(font, width, height, color, drawer, word):
    if word.startswith("@") or word.startswith("#"):
        color = (66, 173, 245)
    drawer.text(
        (width, height),
        word,
        font=font,
        fill=color,
        embedded_color=True,
        emoji_scale_factor=1,
    )
    width, height = drawer.getsize(word, font)
    return width, height


def write_line_to_img(font, height, color, drawer, line):
    words = line.split(" ")
    space_words = 12
    width = 70
    for word in words:
        write_word_to_img(font, width, height, color, drawer, word)
        word_width, height_ = drawer.getsize(word, font)
        width = space_words + width + word_width
    return height_


def write_sentence_to_img(font, color, drawer, text):
    text = text.split("\n")
    space_lines = 10
    original_height = 305
    height = original_height
    for line in text:
        line_height = write_line_to_img(font, height, color, drawer, line)
        height = space_lines + height + 55
    return height - original_height - 55

def create_verified(color=(255, 255, 255)):
    im = Image.open("assets/verified.png")
    rgba = im.convert("RGB")
    newData = []
    datas = rgba.getdata()
    for item in datas:
        if item[0] >= 230 and item[1] >= 230 and item[2] >= 230:
            newData.append(color)
        else:
            newData.append(item)

    rgba.putdata(newData)
    rgba.save("assets/verified_new.png", "PNG")

def create_tweet_screenshot_color(
    id, tweet_info=None, background_color=(255, 255, 255)
):
    if tweet_info == None:
        tweet_info = get_tweet_info(id)
    (profile_name,username,user_verified,text,profile_pics,
        date,
        text_range,
        attached_images,
        attached_image_widths,
        attached_image_heights,
        sensitive
    ) = (
        tweet_info["name"],
        tweet_info["username"],
        tweet_info["verified"],
        tweet_info["text"],
        tweet_info["image"],
        tweet_info["date"],
        tweet_info["text_range"],
        tweet_info["attached_images"],
        tweet_info["widths"],
        tweet_info["heights"],
        tweet_info["sensitive"]
    )
    default_width = 1150
    attached_image_height=get_images_height(attached_image_widths,attached_image_heights)

    text, no_lines = find_n(text, text_range)
    profile_pics, mask = get_profile_pics_mask(profile_pics)
    width = 1300
    border_top_bottom = 120
    if no_lines == 1:
        space_text = 100
    elif no_lines == 2:
        space_text = 45 * no_lines * 2
    elif no_lines == 3:
        space_text = 45 * no_lines * 1.6
    elif no_lines == 4:
        space_text = 45 * no_lines * 1.5
    elif no_lines > 4:
        space_text = 45 * no_lines * 1.45
    elif no_lines > 9:
        space_text = 45 * no_lines * 1.4
    space_profile = 186
    attached_image_loc = int(space_text + border_top_bottom + space_profile + 10)
    date_height = int(
        space_text + border_top_bottom + +attached_image_height + space_profile + 30
    )
    total_height = int(
        space_text + 2 * border_top_bottom + space_profile + attached_image_height + 30
    )
    img = Image.new(mode="RGB", size=(width, total_height), color=background_color)
    drawer = ImageDraw.Draw(img)
    drawer.rectangle(
        [(int(width * 0.76), int(total_height - 55)), (width, total_height)],
        fill=(235, 240, 235),
    )
    drawer_emoji = Pilmoji(img)
    font = ImageFont.truetype("assets/arial 1.ttf", 55)
    font_username = ImageFont.truetype("assets/arial 1.ttf", 45)
    bold_font = ImageFont.truetype("assets/Roboto-Bold.ttf", 50)
    font_my_username = ImageFont.truetype("assets/arial 1.ttf", 35)
    # Add Text to image

    color = (0, 0, 0)
    space_text = write_sentence_to_img(font, color, drawer_emoji, text)

    drawer.text(
        (int(width * 0.76) + 15, total_height - 47),
        my_username,
        font=font_my_username,
        fill=(46, 45, 45),
    )
    drawer_emoji.text((240, 130), profile_name, font=bold_font, fill=(0, 0, 0))
    drawer.text((240, 185), username, font=font_username, fill=(134, 135, 134))
    drawer.text((70, date_height), date, font=font_username, fill=(134, 135, 134))
    img.paste(profile_pics, (70, 120), mask)
    img=attach_images(img,attached_images,attached_image_loc, attached_image_height)
    if user_verified == True:
        create_verified(color=background_color)
        verified = Image.open("assets/verified_new.png")
        verified = verified.convert("RGB")
        verified = verified.resize((45, 45))

        profile_name_width, _ = drawer_emoji.getsize(profile_name, bold_font)
        img.paste(verified, (int(240 + 15 + profile_name_width), 135))
    return img, total_height, width,sensitive


def create_twitter_logo(color=(255, 255, 255)):
    im = Image.open("assets/twitter_logo.png")
    rgba = im.convert("RGB")
    newData = []
    datas = rgba.getdata()
    for item in datas:
        if item[0] >= 230 and item[1] >= 230 and item[2] >= 230:
            newData.append(color)
        else:
            newData.append(item)

    rgba.putdata(newData)
    rgba.save("assets/twitter_logo_new.png", "PNG")


def create_beautiful_screenshot(id, tweet_info=None):
    colors_dict = {
        0: {"tweet_color": (194, 217, 255), "background_color": (66, 135, 245)},
        1: {"tweet_color": (255, 205, 199), "background_color": (250, 144, 130)},
        2: {"tweet_color": None, "background_color": (248, 199, 255)},
        3: {"tweet_color": None, "background_color": (199, 233, 255)},
        4: {"tweet_color": None, "background_color": (66, 135, 245)},
        5: {"tweet_color": None, "background_color": (130, 250, 146)},
        6: {"tweet_color": (210, 242, 247), "background_color": (164, 239, 252)},
        7: {"tweet_color": (248, 252, 227), "background_color": (222, 240, 141)},
    }
    try:
        color_selection = random.choice(colors_dict)
    except:
        color_selection = colors_dict[2]
    #color_selection = random.choice(colors_dict)

    background_color = color_selection["background_color"]
    tweet_color = color_selection["tweet_color"]
    if tweet_color == None:
        tweet_color = (255, 255, 255)
    img, total_height, width,sensitive= create_tweet_screenshot_color(
        id, tweet_info, background_color=tweet_color
    )
    background_image = Image.new(
        mode="RGB", size=(width + 400, total_height + 250), color=background_color
    )
    # mask
    mask_image = Image.new("L", [width, total_height], 0)
    mask_drawer = ImageDraw.Draw(mask_image)
    mask_drawer.rounded_rectangle(
        [(0, 0), (width, total_height)],
        fill=255,
        width=2,
        radius=80,
    )
    # paste tweet
    background_image.paste(img, (200, 125), mask=mask_image)
    # paste twitter
    create_twitter_logo(tweet_color)

    twitter_logo = Image.open("assets/twitter_logo_new.png")
    twitter_logo = twitter_logo.convert("RGB")
    twitter_logo = twitter_logo.resize((120, 100))
    # paste
    background_image.paste(twitter_logo, (width, 200))
    return background_image,sensitive
