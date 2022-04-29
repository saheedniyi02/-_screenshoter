import re
import emoji
import string
import numpy as np
from pilmoji import Pilmoji
from PIL import Image, ImageFont, ImageDraw
from utils import (
    get_tweet_info,
    check_last_space,
    remove_start_space,
    get_profile_name_score,
    get_profile_pics_mask,
)

verified = Image.open("verified.png")
verified = verified.convert("RGB")
verified = verified.resize((45, 45))

verified_dark = Image.open("verified_dark.png")
verified_dark = verified_dark.convert("RGB")
verified_dark = verified_dark.resize((45, 45))

my_username = "@_screenshoter"


def clean_text(text, i, length):
    words_per_line = 43
    no_lines = (len(text) // words_per_line) + 1
    lines = []
    for line_no in range(no_lines + 1):
        if len(text) <= words_per_line:
            line = text
            line = remove_start_space(line)
            if i == length - 1:
                line = re.sub("http[s]?://\S+", "", line)
            lines.append(line)
            new_text = "".join(lines)
            return new_text, len(lines)
        line, words_per_line = check_last_space(words_per_line, text)
        text = text.replace(text[:words_per_line], "")
        words = line.split()
        line = " ".join(words)
        line = remove_start_space(line)
        line = line + "\n"
        lines.append(line)
        words_per_line = 43


def find_n(text, text_range):
    text = text[text_range[0] :]
    text_split = text.split("\n")
    new_text = ""
    total_lines = 0
    i = 0
    for txt in text_split:
        if txt == "":
            new_text = new_text + "\n"
            total_lines = total_lines + 1
        else:
            txt_lines, no_lines = clean_text(txt, i, len(text_split))
            new_text = new_text + txt_lines + "\n"
            total_lines = total_lines + no_lines
        i = i + 1
    return new_text, total_lines


def create_tweet_screenshot_light(id):
    tweet_info = get_tweet_info(id)
    profile_name, username, user_verified, text, profile_pics, date, text_range = (
        tweet_info["name"],
        tweet_info["username"],
        tweet_info["verified"],
        tweet_info["text"],
        tweet_info["image"],
        tweet_info["date"],
        tweet_info["text_range"],
    )
    text, no_lines = find_n(text, text_range)
    profile_pics, mask = get_profile_pics_mask(profile_pics)
    profile_name_score = get_profile_name_score(profile_name)
    width = 1300
    border_top_bottom = 120
    space_text = 45 * no_lines * 1.5
    space_profile = 186
    date_height = int(space_text + border_top_bottom + space_profile + 20)
    total_height = int(space_text + 2 * border_top_bottom + space_profile)
    img = Image.new(mode="RGB", size=(width, total_height), color=(256, 256, 256))
    drawer = ImageDraw.Draw(img)
    drawer.rectangle(
        [(int(width * 0.76), int(total_height - 55)), (width, total_height)],
        fill=(235, 240, 235),
    )
    drawer_emoji = Pilmoji(img)
    font = ImageFont.truetype("OpenSans-Regular.ttf", 55)
    font_username = ImageFont.truetype("OpenSans-Regular.ttf", 45)
    bold_font = ImageFont.truetype("Roboto-Bold.ttf", 50)
    font_my_username = ImageFont.truetype("OpenSans-Regular.ttf", 35)
    # Add Text to image
    drawer.text(
        (int(width * 0.76) + 15, total_height - 47),
        my_username,
        font=font_my_username,
        fill=(46, 45, 45),
    )
    drawer_emoji.text(
        (70, 305),
        text,
        font=font,
        fill=(0, 0, 0),
        embedded_color=True,
        emoji_scale_factor=1.1,
        emoji_position_offset=(10, 15),
    )
    drawer_emoji.text((240, 130), profile_name, font=bold_font, fill=(0, 0, 0))
    drawer.text((240, 185), username, font=font_username, fill=(134, 135, 134))
    drawer.text((70, date_height), date, font=font_username, fill=(134, 135, 134))
    img.paste(profile_pics, (70, 120), mask)
    if user_verified == True:
        img.paste(verified, (int(240 + 28.15 * (profile_name_score)), 140))
    return img


def create_tweet_screenshot_dark(id):
    tweet_info = get_tweet_info(id)
    profile_name, username, user_verified, text, profile_pics, date, text_range = (
        tweet_info["name"],
        tweet_info["username"],
        tweet_info["verified"],
        tweet_info["text"],
        tweet_info["image"],
        tweet_info["date"],
        tweet_info["text_range"],
    )
    text, no_lines = find_n(text, text_range)
    profile_pics, mask = get_profile_pics_mask(profile_pics)
    profile_name_score = get_profile_name_score(profile_name)
    width = 1300
    border_top_bottom = 120
    space_text = 45 * no_lines * 1.5
    space_profile = 186
    date_height = int(space_text + border_top_bottom + space_profile + 20)
    total_height = int(space_text + 2 * border_top_bottom + space_profile)
    img = Image.new(mode="RGB", size=(width, total_height), color=(0, 0, 0))
    drawer = ImageDraw.Draw(img)
    drawer.rectangle(
        [(int(width * 0.76), int(total_height - 55)), (width, total_height)],
        fill=(41, 39, 39),
    )
    drawer_emoji = Pilmoji(img)
    font = ImageFont.truetype("OpenSans-Regular.ttf", 55)
    font_username = ImageFont.truetype("OpenSans-Regular.ttf", 45)
    font_my_username = ImageFont.truetype("OpenSans-Regular.ttf", 35)
    bold_font = ImageFont.truetype("Roboto-Bold.ttf", 50)
    drawer.text(
        (int(width * 0.76) + 15, total_height - 47),
        my_username,
        font=font_my_username,
        fill=(209, 205, 205),
    )
    # Add Text to image
    drawer_emoji.text(
        (70, 305),
        text,
        font=font,
        fill=(255, 255, 255),
        embedded_color=True,
        align="left",
        emoji_scale_factor=1,
        emoji_position_offset=(10, 15),
    )
    drawer_emoji.text((240, 130), profile_name, font=bold_font, fill=(255, 255, 255))
    drawer.text((240, 185), username, font=font_username, fill=(196, 195, 194))
    drawer.text((70, date_height), date, font=font_username, fill=(196, 195, 194))
    img.paste(profile_pics, (70, 120), mask)
    if user_verified == True:
        img.paste(verified_dark, (int(240 + 28.15 * (profile_name_score)), 128))
    return img
