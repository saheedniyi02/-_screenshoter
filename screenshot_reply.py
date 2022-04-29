import numpy as np
from PIL import Image, ImageFont, ImageDraw
from pilmoji import Pilmoji
import string
import re
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


def clean_text_replies(text, i, length):
    words_per_line = 46
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
        words_per_line = 46


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
            txt_lines, no_lines = clean_text_replies(txt, i, len(text_split))
            new_text = new_text + txt_lines + "\n"
            total_lines = total_lines + no_lines
        i = i + 1
    return new_text, total_lines


def get_reply_history(id):
    reply_history = []
    max_conversation = 6
    for i in range(max_conversation):
        if i == 0:
            tweet_info = get_tweet_info(id)
            reply_history.append(tweet_info)
        else:
            _id = tweet_info["in_reply_to_status_id"]
            if _id != None:
                tweet_info = get_tweet_info(_id)
                reply_history.append(tweet_info)
            else:
                new_history = []
                for reply in reversed(reply_history):
                    new_history.append(reply)

                return len(reply_history), new_history
    new_history = []
    for reply in reversed(reply_history):
        new_history.append(reply)

    return len(reply_history), new_history


def create_total_height(reply_history):
    width = 1300
    border_top_bottom = 120
    space_profile = 186
    total_height = int(2 * border_top_bottom)
    for tweet in reply_history:
        text, text_range = tweet["text"], tweet["text_range"]
        text, no_lines = find_n(text, text_range)
        tweet_height = 45 * no_lines * 1.25
        total_height = int(total_height + space_profile + tweet_height + 50)
    return total_height


def create_screenshot_light(tweet_info, identify, increase_height, img):
    profile_name, username, user_verified, text, profile_pics, date, text_range = (
        tweet_info["name"],
        tweet_info["username"],
        tweet_info["verified"],
        tweet_info["text"],
        tweet_info["image"],
        tweet_info["date"],
        tweet_info["text_range"],
    )
    if identify == 0:
        border_top_bottom = 0
    else:
        border_top_bottom = 0
    text, no_lines = find_n(text, text_range)
    profile_pics, mask = get_profile_pics_mask(profile_pics)
    profile_name_score = get_profile_name_score(profile_name)
    space_text = 45 * no_lines * 1.25
    space_profile = 185
    tweet_height = int(space_text + border_top_bottom + space_profile + 50)
    # date_height = int(space_text + border_top_bottom + space_profile + 5)
    profile_name_height = 120 + increase_height
    username_height = 185 + increase_height
    profile_pics_height = 120 + increase_height
    verified_height = 128 + increase_height
    text_height = 290 + increase_height
    drawer = ImageDraw.Draw(img)
    drawer_emoji = Pilmoji(img)
    font = ImageFont.truetype("OpenSans-Regular.ttf", 50)
    font_username = ImageFont.truetype("OpenSans-Regular.ttf", 45)
    bold_font = ImageFont.truetype("Roboto-Bold.ttf", 50)
    # Add Text to image
    drawer_emoji.text(
        (70, text_height),
        text,
        font=font,
        fill=(0, 0, 0),
        embedded_color=True,
        emoji_scale_factor=1.1,
        emoji_position_offset=(10, 15),
    )
    drawer_emoji.text(
        (240, profile_name_height), profile_name, font=bold_font, fill=(0, 0, 0)
    )
    drawer.text(
        (240, username_height), username, font=font_username, fill=(134, 135, 134)
    )
    # drawer.text((70, date_height), date, font=font_username, fill=(134, 135, 134))
    img.paste(profile_pics, (70, profile_pics_height), mask)
    if user_verified == True:
        img.paste(verified, (int(240 + 28.15 * (profile_name_score)), verified_height))
    return img, tweet_height


def create_screenshot_dark(tweet_info, identify, increase_height, img):
    profile_name, username, user_verified, text, profile_pics, date, text_range = (
        tweet_info["name"],
        tweet_info["username"],
        tweet_info["verified"],
        tweet_info["text"],
        tweet_info["image"],
        tweet_info["date"],
        tweet_info["text_range"],
    )
    if identify == 0:
        border_top_bottom = 0
    else:
        border_top_bottom = 0
    text, no_lines = find_n(text, text_range)
    profile_pics, mask = get_profile_pics_mask(profile_pics)
    profile_name_score = get_profile_name_score(profile_name)
    space_text = 45 * no_lines * 1.25
    space_profile = 185
    tweet_height = int(space_text + border_top_bottom + space_profile + 50)
    # date_height = int(space_text + border_top_bottom + space_profile + 5)
    profile_name_height = 120 + increase_height
    username_height = 185 + increase_height
    profile_pics_height = 120 + increase_height
    verified_height = 128 + increase_height
    text_height = 290 + increase_height
    drawer = ImageDraw.Draw(img)
    drawer_emoji = Pilmoji(img)
    font = ImageFont.truetype("OpenSans-Regular.ttf", 50)
    font_username = ImageFont.truetype("OpenSans-Regular.ttf", 45)
    bold_font = ImageFont.truetype("Roboto-Bold.ttf", 50)
    # Add Text to image
    drawer_emoji.text(
        (70, text_height),
        text,
        font=font,
        fill=(255, 255, 255),
        embedded_color=True,
        emoji_scale_factor=1.1,
        emoji_position_offset=(10, 15),
    )
    drawer_emoji.text(
        (240, profile_name_height), profile_name, font=bold_font, fill=(255, 255, 255)
    )
    drawer.text(
        (240, username_height), username, font=font_username, fill=(196, 195, 194)
    )
    # drawer.text((70, date_height), date, font=font_username, fill=(196, 195, 194))
    img.paste(profile_pics, (70, profile_pics_height), mask)
    if user_verified == True:
        img.paste(
            verified_dark, (int(240 + 28.15 * (profile_name_score)), verified_height)
        )
    return img, tweet_height


def create_replies_screenshot_light(id):
    no_replies, reply_history = get_reply_history(id)
    if len(reply_history) == 1:
        return None
    total_height = create_total_height(reply_history)
    width = 1250
    img = Image.new(mode="RGB", size=(width, total_height), color=(256, 256, 256))
    drawer = ImageDraw.Draw(img)
    drawer.rectangle(
        [(int(width * 0.76), int(total_height - 55)), (width, total_height)],
        fill=(235, 240, 235),
    )
    font_my_username = ImageFont.truetype("OpenSans-Regular.ttf", 35)
    drawer.text(
        (int(width * 0.76) + 15, total_height - 47),
        my_username,
        font=font_my_username,
        fill=(46, 45, 45),
    )
    increase_height = 0
    identify = 0
    for reply in reply_history:
        img, tweet_height = create_screenshot_light(
            reply, identify, increase_height, img
        )
        increase_height = increase_height + tweet_height
        identify = identify + 1
    return img


def create_replies_screenshot_dark(id):
    no_replies, reply_history = get_reply_history(id)
    if len(reply_history) == 1:
        return None
    total_height = create_total_height(reply_history)
    width = 1250
    img = Image.new(mode="RGB", size=(width, total_height), color=(0, 0, 0))
    drawer = ImageDraw.Draw(img)
    drawer.rectangle(
        [(int(width * 0.76), int(total_height - 55)), (width, total_height)],
        fill=(41, 39, 39),
    )
    font_my_username = ImageFont.truetype("OpenSans-Regular.ttf", 35)
    drawer.text(
        (int(width * 0.76) + 15, total_height - 47),
        my_username,
        font=font_my_username,
        fill=(209, 205, 205),
    )
    increase_height = 0
    identify = 0
    for reply in reply_history:
        img, tweet_height = create_screenshot_dark(
            reply, identify, increase_height, img
        )
        increase_height = increase_height + tweet_height
        identify = identify + 1
    return img
