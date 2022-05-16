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
max_conversation=5

verified = Image.open("assets/verified.png")
verified = verified.convert("RGB")
verified = verified.resize((45, 45))

verified_dark = Image.open("assets/verified_dark.png")
verified_dark = verified_dark.convert("RGB")
verified_dark = verified_dark.resize((45, 45))
my_username = "@_screenshoter"


def clean_text_replies(text, i, length):
    words_per_line = 49
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
        words_per_line = 49


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
    max_conversation = 20
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
    max_conversations=5
    reply_set=[]
    len_history=len(reply_history)
    while len_history!=0:
    	if len(reply_history)>max_conversations:
    		reply_set.append(reply_history[:max_conversations])
    		reply_history=reply_history[max_conversations:]
    	else:
    		reply_set.append(reply_history)
    		reply_history=[]
    		len_history=0
    image_heights=[]
    for set in reply_set:
    	border_top_bottom = 60
    	space_profile = 186
    	total_height = int(2 * border_top_bottom)
    	for tweet in set:
        	text, text_range,attached_image_width,attached_image_height = tweet["text"], tweet["text_range"],tweet["width"],tweet["height"]
        	text, no_lines = find_n(text, text_range)
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
        	total_height = int(total_height + space_profile + space_text+50)
        	
        	if tweet["attached_image"]:
        		default_width=1150
        		error=50
        		attached_image_height=int(default_width*(attached_image_height/attached_image_width))
        		total_height = total_height + attached_image_height + error
        	else:
        		pass
    	
    	
    	
    	
    	image_heights.append(total_height)
    return image_heights,reply_set


def create_screenshot_light(tweet_info, identify, increase_height, img):
    (
        profile_name,
        username,
        user_verified,
        text,
        profile_pics,
        date,
        text_range,
        attached_image,
        attached_image_width,
        attached_image_height
    ) = (
        tweet_info["name"],
        tweet_info["username"],
        tweet_info["verified"],
        tweet_info["text"],
        tweet_info["image"],
        tweet_info["date"],
        tweet_info["text_range"],
        tweet_info["attached_image"],
        tweet_info["width"],
        tweet_info["height"]
    )
    border_top_bottom = 50
    text, no_lines = find_n(text, text_range)
    profile_pics, mask = get_profile_pics_mask(profile_pics)
    profile_name_score = get_profile_name_score(profile_name)
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
    default_width=1150
    if attached_image:
    	attached_image_height=int(default_width*(attached_image_height/attached_image_width))
    	attached_image=attached_image.resize((default_width,attached_image_height))
    	attached_image_width=default_width
    	error = 50
    else:
        attached_image_height = 0
        error = 0
    tweet_height = int(
        space_text + border_top_bottom + space_profile + error + attached_image_height
    )

    # date_height = int(space_text + border_top_bottom + space_profile + 5)
    profile_name_height = 120 + increase_height
    username_height = 185 + increase_height
    profile_pics_height = 120 + increase_height
    verified_height = 128 + increase_height
    text_height = 290 + increase_height
    attached_image_loc = int(
        space_text + border_top_bottom + space_profile + 15 + increase_height
    )
    drawer = ImageDraw.Draw(img)
    drawer_emoji = Pilmoji(img)
    font = ImageFont.truetype("assets/OpenSans-Regular.ttf", 50)
    font_username = ImageFont.truetype("assets/OpenSans-Regular.ttf", 45)
    bold_font = ImageFont.truetype("assets/Roboto-Bold.ttf", 50)
    # Add Text to image
    drawer_emoji.text(
        (70, text_height),
        text,
        font=font,
        fill=(0, 0, 0),
        embedded_color=True,
        emoji_scale_factor=1.1,
    )
    drawer_emoji.text(
        (240, profile_name_height), profile_name, font=bold_font, fill=(0, 0, 0)
    )
    drawer.text(
        (240, username_height), username, font=font_username, fill=(134, 135, 134)
    )
    # drawer.text((70, date_height), date, font=font_username, fill=(134, 135, 134))
    img.paste(profile_pics, (70, profile_pics_height), mask)
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
        img.paste(verified, (int(240 + 28.15 * (profile_name_score)), verified_height))
    return img, tweet_height


def create_screenshot_dark(tweet_info, identify, increase_height, img):
    (
        profile_name,
        username,
        user_verified,
        text,
        profile_pics,
        date,
        text_range,
        attached_image,
        attached_image_width,
        attached_image_height
    ) = (
        tweet_info["name"],
        tweet_info["username"],
        tweet_info["verified"],
        tweet_info["text"],
        tweet_info["image"],
        tweet_info["date"],
        tweet_info["text_range"],
        tweet_info["attached_image"],
        tweet_info["width"],
        tweet_info["height"]
    )
    border_top_bottom = 50
    text, no_lines = find_n(text, text_range)
    profile_pics, mask = get_profile_pics_mask(profile_pics)
    profile_name_score = get_profile_name_score(profile_name)
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
    default_width=1150
    if attached_image:
    	attached_image_height=int(default_width*(attached_image_height/attached_image_width))
    	attached_image=attached_image.resize((default_width,attached_image_height))
    	attached_image_width=default_width
    	error = 50
    else:
        attached_image_height = 0
        error = 0

    tweet_height = int(
        space_text + border_top_bottom + space_profile + error + attached_image_height
    )
    # date_height = int(space_text + border_top_bottom + space_profile + 5)
    profile_name_height = 120 + increase_height
    username_height = 185 + increase_height
    profile_pics_height = 120 + increase_height
    verified_height = 128 + increase_height
    text_height = 290+ increase_height
    attached_image_loc = int(
        space_text + border_top_bottom + space_profile + 15 + increase_height
    )
    drawer = ImageDraw.Draw(img)
    drawer_emoji = Pilmoji(img)
    font = ImageFont.truetype("assets/OpenSans-Regular.ttf", 50)
    font_username = ImageFont.truetype("assets/OpenSans-Regular.ttf", 45)
    bold_font = ImageFont.truetype("assets/Roboto-Bold.ttf", 50)
    # Add Text to image
    drawer_emoji.text(
        (70, text_height),
        text,
        font=font,
        fill=(255, 255, 255),
        embedded_color=True,
        emoji_scale_factor=1.1,
    )
    drawer_emoji.text(
        (240, profile_name_height), profile_name, font=bold_font, fill=(255, 255, 255)
    )
    drawer.text(
        (240, username_height), username, font=font_username, fill=(196, 195, 194)
    )
    # drawer.text((70, date_height), date, font=font_username, fill=(196, 195, 194))
    img.paste(profile_pics, (70, profile_pics_height), mask)
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
        img.paste(
            verified_dark, (int(240 + 28.15 * (profile_name_score)), verified_height)
        )
    return img, tweet_height


def create_replies_screenshot_light(id):
    no_replies, reply_history = get_reply_history(id)
    if len(reply_history) == 1:
        return None
    total_heights,reply_set= create_total_height(reply_history)
    width = 1300
    counter=0
    imgs=[]
    for set in reply_set:
    	total_height=total_heights[counter]
    	img = Image.new(mode="RGB", size=(width, total_height), color=(256, 256, 256))
    	drawer = ImageDraw.Draw(img)
    	drawer.rectangle([(int(width * 0.76), int(total_height - 55)), (width, total_height)],fill=(235, 240, 235),)
    	font_my_username = ImageFont.truetype("assets/OpenSans-Regular.ttf", 35)
    	drawer.text((int(width * 0.76) + 15, total_height - 47),my_username,font=font_my_username,fill=(46, 45, 45),)
    	increase_height = 0
    	counter=counter+1
    	identify = 0
    	for reply in set:
            img, tweet_height = create_screenshot_light(
            reply, identify, increase_height, img)
            increase_height = increase_height + tweet_height
            identify = identify + 1
    	if total_height>=8192:
    	   	print(total_height)
    	   	img=img.resize((width,8191))
        	
    	imgs.append(img)
    print(imgs)
    return imgs


def create_replies_screenshot_dark(id):
    no_replies, reply_history = get_reply_history(id)
    if len(reply_history) == 1:
        return None
    total_heights,reply_set = create_total_height(reply_history)
    width = 1300
    counter=0
    imgs=[]
    for set in reply_set:
    	total_height=total_heights[counter]
    	img = Image.new(mode="RGB", size=(width, total_height), color=(0, 0, 0))
    	drawer = ImageDraw.Draw(img)
    	drawer.rectangle([(int(width * 0.76), int(total_height - 55)), (width, total_height)],fill=(41, 39, 39),)
    	font_my_username = ImageFont.truetype("assets/OpenSans-Regular.ttf", 35)
    	drawer.text((int(width * 0.76) + 15, total_height - 47),my_username,font=font_my_username,fill=(209, 205, 205),)
    	increase_height = 0
    	counter=counter+1
    	identify = 0
    	for reply in set:
            img, tweet_height = create_screenshot_dark(reply, identify, increase_height, img)
            increase_height = increase_height + tweet_height
            identify = identify + 1
    	   	
    	if total_height>=8192:
    		print(total_height)
    		img=img.resize((width,8191))
    	imgs.append(img)
    print(imgs)
    return imgs
    