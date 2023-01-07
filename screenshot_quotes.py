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
    get_images_height,
    attach_images
)


verified = Image.open("assets/verified.png")
verified = verified.convert("RGB")
verified = verified.resize((45, 45))

verified_dark = Image.open("assets/verified_dark.png")
verified_dark = verified_dark.convert("RGB")
verified_dark = verified_dark.resize((45, 45))


my_username = "@_screenshoter"


def clean_text(text):
    words_per_line = 49
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
        words_per_line = 49


def clean_text_quotes(text):
    words_per_line = 43
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
        words_per_line = 43


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
    total_lines = total_lines - (len(new_text) - len(new_text_stripped)) +1
    return new_text, total_lines


def find_n_quotes(text, text_range):
    text = text[text_range[0] :]
    text_split = text.split("\n")
    new_text = ""
    total_lines = 0
    for txt in text_split:
        if txt == "":
            new_text = new_text + "\n"
            total_lines = total_lines + 1
        else:
            txt_lines, no_lines = clean_text_quotes(txt)
            new_text = new_text + txt_lines + "\n"
            total_lines = total_lines + no_lines
    new_text_stripped = new_text.rstrip("\n")
    total_lines = total_lines - (len(new_text) - len(new_text_stripped)) +1
    return new_text, total_lines


def screenshot_quote_light(id):
    tweet_info = get_tweet_info(id)
    (
        profile_name,
        username,
        user_verified,
        text,
        profile_pics,
        date,
        text_range,
        quoted_id,
        attached_image,
        attached_image_width,
        attached_image_height,
        sensitive
    ) = (
        tweet_info["name"],
        tweet_info["username"],
        tweet_info["verified"],
        tweet_info["text"],
        tweet_info["image"],
        tweet_info["date"],
        tweet_info["text_range"],
        tweet_info["quoted_id"],
        tweet_info["attached_images"],
        tweet_info["widths"],
        tweet_info["heights"],
        tweet_info["sensitive"]
    )

    	
    if quoted_id == None:
        sensitive=False
        image=None
        return image,tweet_info,sensitive
    if attached_image:
    	attached_image,attached_image_width,attached_image_height=attached_image[0],attached_image_width[0],attached_image_height[0]
    else:
    	attached_image,attached_image_width,attached_image_height=None,0,0
    quoted_info = get_tweet_info(quoted_id)
    (
        profile_name_quoted,
        username_quoted,
        user_verified_quoted,
        quote_text,
        profile_pics_quoted,
        date_quote,
        text_range_quoted,
        _,
        quoted_image,
        quoted_image_width,
        quoted_image_height,
        quoted_sensitive
    ) = (
        quoted_info["name"],
        quoted_info["username"],
        quoted_info["verified"],
        quoted_info["text"],
        quoted_info["image"],
        quoted_info["date"],
        quoted_info["text_range"],
        quoted_info["quoted_id"],
        quoted_info["attached_images"],
        quoted_info["widths"],
        quoted_info["heights"],
        quoted_info["sensitive"]
    )
    if quoted_image:
    	quoted_image,quoted_image_width,quoted_image_height=quoted_image[0],quoted_image_width[0],quoted_image_height[0]
    else:
    	quoted_image,quoted_image_width,quoted_image_height=None,0,0
    if True in [quoted_sensitive,sensitive]:
    	sensitive=True
    else:
    	sensitive=False
    text, no_lines = find_n(text, text_range)
    default_width=1150
    if attached_image:
    	attached_image_height=int(default_width*(attached_image_height/attached_image_width))
    	attached_image=attached_image.resize((default_width,attached_image_height))
    	attached_image_width=default_width
    default_width_quoted=1050	
    	
    if quoted_image:
        quoted_image_height=int(default_width_quoted*(quoted_image_height/quoted_image_width))
        quoted_image = quoted_image.resize((default_width_quoted, quoted_image_height))
        quoted_image_width=default_width_quoted
    quote_text, no_lines_quoted = find_n_quotes(quote_text, text_range_quoted)
    profile_pics, mask = get_profile_pics_mask(profile_pics)
    profile_name_score = get_profile_name_score(profile_name)
    profile_pics_quoted, mask = get_profile_pics_mask(profile_pics_quoted)
    profile_name_quoted_score = get_profile_name_score(profile_name_quoted)

    # dimensions
    width = 1300
    border_top_bottom = 120
    if no_lines == 1:
        space_text = 100
    elif no_lines == 2:
        space_text = 45 * no_lines * 2
    elif no_lines==3:
        space_text = 45 * no_lines * 1.6
    elif no_lines==4:
        space_text=45*no_lines*1.5
    elif no_lines>4:
        space_text=45*no_lines*1.45
    elif no_lines>9:
    	space_text=45*no_lines*1.4
    space_profile = 185
    
    
    if no_lines_quoted == 1:
        space_text_quoted = 100
    elif no_lines_quoted == 2:
        space_text_quoted = 45 * no_lines_quoted * 2
    elif no_lines_quoted==3:
        space_text_quoted = 45 * no_lines_quoted * 1.6
    elif no_lines_quoted==4:
        space_text_quoted=45*no_lines_quoted*1.5
    elif no_lines_quoted>4:
        space_text_quoted=45*no_lines_quoted*1.45
    elif no_lines_quoted>9:
    	space_text_quoted=45*no_lines_quoted*1.4
    border_top_bottom_quoted = 60
    attached_image_loc = int(space_text + border_top_bottom + space_profile)
    quoted_start_height = int(
        space_text + border_top_bottom + space_profile + 10 + attached_image_height + 20
    )
    quoted_image_loc = int(
        quoted_start_height
        + border_top_bottom_quoted
        + space_text_quoted
        + space_profile
        + 10
    )
    quoted_end_height = (
        quoted_image_loc + border_top_bottom_quoted + quoted_image_height + 75
    )
    quoted_date_height = quoted_end_height - 40 - border_top_bottom_quoted
    date_height = quoted_end_height + 30
    total_height = quoted_end_height + border_top_bottom
    # image
    img = Image.new(mode="RGB", size=(width, int(total_height)), color=(255, 255, 255))
    drawer = ImageDraw.Draw(img)
    drawer.rounded_rectangle(
        [(100, quoted_start_height), (width - 35, quoted_end_height)],
        fill=(255, 255, 255),
        width=2,
        outline=(224, 224, 224),
        radius=30,
    )
    drawer.rectangle(
        [(int(width * 0.76), int(total_height - 55)), (width, total_height)],
        fill=(41, 39, 39),
    )
    drawer_emoji = Pilmoji(img)
    font = ImageFont.truetype("assets/arial 1.ttf", 55)
    font_username = ImageFont.truetype("assets/arial 1.ttf", 45)
    font_my_username = ImageFont.truetype("assets/arial 1.ttf", 35)
    font_quote_date = ImageFont.truetype("assets/arial 1.ttf", 35)
    bold_font = ImageFont.truetype("assets/Roboto-Bold.ttf", 50)
    # tweet
    drawer.text(
        (int(width * 0.76) + 15, total_height - 47),
        my_username,
        font=font_my_username,
        fill=(209, 205, 205),
    )
    drawer_emoji.text(
        (70, 305),
        text,
        font=font,
        fill=(0, 0, 0),
        embedded_color=True,
        align="left",
        emoji_scale_factor=1,
    )
    drawer_emoji.text((240, 130), profile_name, font=bold_font, fill=(0, 0, 0))
    drawer.text((240, 185), username, font=font_username, fill=(134, 135, 134))
    drawer.text((70, date_height), date, font=font_username, fill=(134, 135, 134))
    if attached_image:
        mask_image = Image.new("L", [attached_image_width, attached_image_height], 0)
        mask_drawer = ImageDraw.Draw(mask_image)
        mask_drawer.rounded_rectangle(
            [(0, 0), (attached_image_width, attached_image_height)],
            fill=255,
            width=2,
            radius=40,
        )
        img.paste(attached_image, (70, attached_image_loc), mask=mask_image)

    img.paste(profile_pics, (70, 120), mask)
    if user_verified == True:
        img.paste(verified, (int(240 + 28.15 * (profile_name_score)), 140))
    # quote
    drawer_emoji.text(
        (170, quoted_start_height + 185 + border_top_bottom_quoted),
        quote_text,
        font=font,
        fill=(0, 0, 0),
        embedded_color=True,
        align="left",
        emoji_scale_factor=1,
    )
    drawer_emoji.text(
        (340, quoted_start_height + border_top_bottom_quoted + 10),
        profile_name_quoted,
        font=bold_font,
        fill=(0, 0, 0),
    )
    drawer.text(
        (340, quoted_start_height + border_top_bottom_quoted + 75),
        username_quoted,
        font=font_username,
        fill=(134, 135, 134),
    )
    drawer.text(
        (170, quoted_date_height),
        date_quote,
        font=font_quote_date,
        fill=(134, 135, 134),
    )
    img.paste(
        profile_pics_quoted, (170, quoted_start_height + border_top_bottom_quoted), mask
    )
    if quoted_image:
        mask_image = Image.new("L", [quoted_image_width, quoted_image_height], 0)
        mask_drawer = ImageDraw.Draw(mask_image)
        mask_drawer.rounded_rectangle(
            [(0, 0), (quoted_image_width, quoted_image_height)],
            fill=255,
            width=2,
            radius=40,
        )
        img.paste(quoted_image, (170, quoted_image_loc), mask=mask_image)

    if user_verified_quoted == True:
        img.paste(
            verified,
            (
                int(340 + 28.15 * (profile_name_quoted_score)),
                quoted_start_height + border_top_bottom_quoted + 20,
            ),
        )
    return img,None,sensitive


def screenshot_quote_dark(id):
    tweet_info = get_tweet_info(id)
    (
        profile_name,
        username,
        user_verified,
        text,
        profile_pics,
        date,
        text_range,
        quoted_id,
        attached_image,
        attached_image_width,
        attached_image_height,
        sensitive
    ) = (
        tweet_info["name"],
        tweet_info["username"],
        tweet_info["verified"],
        tweet_info["text"],
        tweet_info["image"],
        tweet_info["date"],
        tweet_info["text_range"],
        tweet_info["quoted_id"],
        tweet_info["attached_images"],
        tweet_info["widths"],
        tweet_info["heights"],
        tweet_info["sensitive"]
    )

    	
    if quoted_id == None:
        sensitive=False
        image=None
        return image,tweet_info,sensitive
    if attached_image:
    	attached_image,attached_image_width,attached_image_height=attached_image[0],attached_image_width[0],attached_image_height[0]
    else:
    	attached_image,attached_image_width,attached_image_height=None,0,0
    quoted_info = get_tweet_info(quoted_id)
    (
        profile_name_quoted,
        username_quoted,
        user_verified_quoted,
        quote_text,
        profile_pics_quoted,
        date_quote,
        text_range_quoted,
        _,
        quoted_image,
        quoted_image_width,
        quoted_image_height,
        quoted_sensitive
    ) = (
        quoted_info["name"],
        quoted_info["username"],
        quoted_info["verified"],
        quoted_info["text"],
        quoted_info["image"],
        quoted_info["date"],
        quoted_info["text_range"],
        quoted_info["quoted_id"],
        quoted_info["attached_images"],
        quoted_info["widths"],
        quoted_info["heights"],
        quoted_info["sensitive"]
    )
    if quoted_image:
    	quoted_image,quoted_image_width,quoted_image_height=quoted_image[0],quoted_image_width[0],quoted_image_height[0]
    else:
    	quoted_image,quoted_image_width,quoted_image_height=None,0,0
    if True in [quoted_sensitive,sensitive]:
    	sensitive=True
    else:
    	sensitive=False
    text, no_lines = find_n(text, text_range)
    default_width=1150
    if attached_image:
    	attached_image_height=int(default_width*(attached_image_height/attached_image_width))
    	attached_image=attached_image.resize((default_width,attached_image_height))
    	attached_image_width=default_width
    default_width_quoted=1050	
    	
    if quoted_image:
        quoted_image_height=int(default_width_quoted*(quoted_image_height/quoted_image_width))
        quoted_image = quoted_image.resize((default_width_quoted, quoted_image_height))
        quoted_image_width=default_width_quoted
    quote_text, no_lines_quoted = find_n_quotes(quote_text, text_range_quoted)
    profile_pics, mask = get_profile_pics_mask(profile_pics)
    profile_name_score = get_profile_name_score(profile_name)
    profile_pics_quoted, mask = get_profile_pics_mask(profile_pics_quoted)
    profile_name_quoted_score = get_profile_name_score(profile_name_quoted)

    # dimensions
    width = 1300
    border_top_bottom = 120
    if no_lines == 1:
        space_text = 100
    elif no_lines == 2:
        space_text = 45 * no_lines * 2
    elif no_lines==3:
        space_text = 45 * no_lines * 1.6
    elif no_lines==4:
        space_text=45*no_lines*1.5
    elif no_lines>4:
        space_text=45*no_lines*1.45
    elif no_lines>9:
    	space_text=45*no_lines*1.4
    space_profile = 185
    
    
    if no_lines_quoted == 1:
        space_text_quoted = 100
    elif no_lines_quoted == 2:
        space_text_quoted = 45 * no_lines_quoted * 2
    elif no_lines_quoted==3:
        space_text_quoted = 45 * no_lines_quoted * 1.6
    elif no_lines_quoted==4:
        space_text_quoted=45*no_lines_quoted*1.5
    elif no_lines_quoted>4:
        space_text_quoted=45*no_lines_quoted*1.45
    elif no_lines_quoted>9:
    	space_text_quoted=45*no_lines_quoted*1.4
    border_top_bottom_quoted = 60
    attached_image_loc = int(space_text + border_top_bottom + space_profile)
    quoted_start_height = int(
        space_text + border_top_bottom + space_profile + 10 + attached_image_height + 20
    )
    quoted_image_loc = int(
        quoted_start_height
        + border_top_bottom_quoted
        + space_text_quoted
        + space_profile
        + 10
    )
    quoted_end_height = (
        quoted_image_loc + border_top_bottom_quoted + quoted_image_height + 75
    )
    quoted_date_height = quoted_end_height - 40 - border_top_bottom_quoted
    date_height = quoted_end_height + 30
    total_height = quoted_end_height + border_top_bottom
    # image
    img = Image.new(mode="RGB", size=(width, int(total_height)), color=(0, 0, 0))
    drawer = ImageDraw.Draw(img)
    drawer.rounded_rectangle(
        [(100, quoted_start_height), (width - 35, quoted_end_height)],
        fill=(0, 0, 0),
        width=3,
        outline=(35, 35, 35),
        radius=30,
    )
    drawer.rectangle(
        [(int(width * 0.76), int(total_height - 55)), (width, total_height)],
        fill=(235, 240, 235),
    )
    drawer_emoji = Pilmoji(img)
    font = ImageFont.truetype("assets/arial 1.ttf", 55)
    font_username = ImageFont.truetype("assets/arial 1.ttf", 45)
    font_my_username = ImageFont.truetype("assets/arial 1.ttf", 35)
    font_quote_date = ImageFont.truetype("assets/arial 1.ttf", 35)
    bold_font = ImageFont.truetype("assets/Roboto-Bold.ttf", 50)

    # tweet
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
        fill=(255, 255, 255),
        embedded_color=True,
        align="left",
        emoji_scale_factor=1.1,
    )
    drawer_emoji.text((240, 130), profile_name, font=bold_font, fill=(255, 255, 255))
    drawer.text((240, 185), username, font=font_username, fill=(196, 195, 194))
    drawer.text((70, date_height), date, font=font_username, fill=(196, 195, 194))
    img.paste(profile_pics, (70, 120), mask)
    if attached_image:
        mask_image = Image.new("L", [attached_image_width, attached_image_height], 0)
        mask_drawer = ImageDraw.Draw(mask_image)
        mask_drawer.rounded_rectangle(
            [(0, 0), (attached_image_width, attached_image_height)],
            fill=255,
            width=2,
            radius=40,
        )
        img.paste(attached_image, (70, attached_image_loc), mask=mask_image)

    if user_verified == True:
        img.paste(verified_dark, (int(240 + 28.15 * (profile_name_score)), 140))
        # quote
    drawer_emoji.text(
        (170, quoted_start_height + 185 + border_top_bottom_quoted),
        quote_text,
        font=font,
        fill=(255, 255, 255),
        embedded_color=True,
        align="left",
        emoji_scale_factor=1
    )
    drawer_emoji.text(
        (340, quoted_start_height + border_top_bottom_quoted + 10),
        profile_name_quoted,
        font=bold_font,
        fill=(255, 255, 255),
    )
    drawer.text(
        (340, quoted_start_height + border_top_bottom_quoted + 75),
        username_quoted,
        font=font_username,
        fill=(196, 195, 194),
    )
    drawer.text(
        (170, quoted_date_height),
        date_quote,
        font=font_quote_date,
        fill=(196, 195, 194),
    )
    img.paste(
        profile_pics_quoted, (170, quoted_start_height + border_top_bottom_quoted), mask
    )

    if quoted_image:
        mask_image = Image.new("L", [quoted_image_width, quoted_image_height], 0)
        mask_drawer = ImageDraw.Draw(mask_image)
        mask_drawer.rounded_rectangle(
            [(0, 0), (quoted_image_width, quoted_image_height)],
            fill=255,
            width=2,
            radius=40,
        )
        img.paste(quoted_image, (170, quoted_image_loc), mask=mask_image)

    if user_verified_quoted == True:
        img.paste(
            verified_dark,
            (
                int(340 + 28.15 * (profile_name_quoted_score)),
                quoted_start_height + border_top_bottom_quoted + 20,
            ),
        )
    return img,None,sensitive
    
