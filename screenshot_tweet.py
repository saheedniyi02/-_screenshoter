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
    total_lines = total_lines - (len(new_text) - len(new_text_stripped)) +1
    return new_text, total_lines

def write_word_to_img(font,width,height,color,drawer,word):
	if word.startswith("@") or word.startswith("#"):
		color=(66,173,245)
	drawer.text((width,height),word,font=font,fill=color,embedded_color=True,emoji_scale_factor=1,)
	width,height=drawer.getsize(word,font)
	return width,height
 
def write_line_to_img(font,height,color,drawer,line):
	words=line.split(" ")
	space_words=12
	width=70
	for word in words:
		write_word_to_img(font,width,height,color,drawer,word)
		word_width,height_=drawer.getsize(word,font)
		width=space_words+width+word_width			
	return height_

def write_sentence_to_img(font,color,drawer,text):
	text=text.split("\n")
	space_lines=10
	original_height=305
	height=original_height
	for line in text:
		line_height=write_line_to_img(font,height,color,drawer,line)
		height=space_lines+height+55
	return height-original_height-55

def create_tweet_screenshot_light(id,tweet_info=None):
    if tweet_info==None:
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
    attached_image_height=get_images_height(attached_image_widths,attached_image_heights)
    text, no_lines = find_n(text, text_range)
    profile_pics, mask = get_profile_pics_mask(profile_pics)
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
    space_profile = 186
    attached_image_loc = int(space_text + border_top_bottom + space_profile + 10)
    date_height = int(
        space_text + border_top_bottom + +attached_image_height + space_profile + 30
    )
    total_height = int(
        space_text + 2 * border_top_bottom + space_profile + attached_image_height + 30
    )
    img = Image.new(mode="RGB", size=(width, total_height), color=(255, 255, 255))
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

    color=(0, 0, 0)
    space_text=write_sentence_to_img(font,color,drawer_emoji,text)
    
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
    #paste attached_images
    img=attach_images(img,attached_images,attached_image_loc, attached_image_height)
    if user_verified == True:
        profile_name_width,_=drawer_emoji.getsize(profile_name,bold_font)
        img.paste(verified, (int(240+15+profile_name_width), 135))
    twitter_logo = Image.open("assets/twitter_logo.png")
    twitter_logo = twitter_logo.convert("RGB")
    twitter_logo = twitter_logo.resize((120, 100))
    # paste
    img.paste(twitter_logo, (width-200, 100))
    return img,sensitive


def create_tweet_screenshot_dark(id,tweet_info=None):
    	
    if tweet_info==None:
    	tweet_info = get_tweet_info(id)
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
    attached_image_height=get_images_height(attached_image_widths,attached_image_heights)
    text, no_lines = find_n(text, text_range)
    profile_pics, mask = get_profile_pics_mask(profile_pics)
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
    attached_image_loc = int(space_text + border_top_bottom + space_profile + 10)
    date_height = int(
        space_text + border_top_bottom + attached_image_height + space_profile + 30
    )
    total_height = int(
        space_text + 2 * border_top_bottom + space_profile + attached_image_height + 30
    )
    img = Image.new(mode="RGB", size=(width, total_height), color=(0, 0, 0))
    drawer = ImageDraw.Draw(img)
    drawer.rectangle(
        [(int(width * 0.76), int(total_height - 55)), (width, total_height)],
        fill=(41, 39, 39),
    )
    drawer_emoji = Pilmoji(img)
    font = ImageFont.truetype("assets/arial 1.ttf", 55)
    font_username = ImageFont.truetype("assets/arial 1.ttf", 45)
    font_my_username = ImageFont.truetype("assets/arial 1.ttf", 35)
    bold_font = ImageFont.truetype("assets/Roboto-Bold.ttf", 50)
    drawer.text(
        (int(width * 0.76) + 15, total_height - 47),
        my_username,
        font=font_my_username,
        fill=(209, 205, 205),
    )
    # Add Text to image
    color=(255, 255, 255)
    space_text=write_sentence_to_img(font,color,drawer_emoji,text)
    
    drawer_emoji.text((240, 130), profile_name, font=bold_font, fill=(255, 255, 255))
    drawer.text((240, 185), username, font=font_username, fill=(196, 195, 194))
    drawer.text((70, date_height), date, font=font_username, fill=(196, 195, 194))
    img.paste(profile_pics, (70, 120), mask)
    #paste attached_images
    img=attach_images(img,attached_images,attached_image_loc, attached_image_height)
    if user_verified == True:
        profile_name_width,_=drawer_emoji.getsize(profile_name,bold_font)
        img.paste(verified_dark, ((int(240 +15+ profile_name_width)), 135))
    twitter_logo = Image.open("assets/twitter_logo_dark.png")
    twitter_logo = twitter_logo.resize((120, 100))
    # paste
    img.paste(twitter_logo, (width-200, 100))        
    return img,sensitive

