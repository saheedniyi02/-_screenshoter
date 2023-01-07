import numpy as np
from PIL import Image, ImageFont, ImageDraw
from pilmoji import Pilmoji
import string
import re
import random
from utils import (
    get_tweet_info,
    check_last_space,
    remove_start_space,
    get_profile_name_score,
    get_profile_pics_mask,
    get_images_height,
    attach_images
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

def write_sentence_to_img(font,color,drawer,text,height):
	text=text.split("\n")
	space_lines=10
	original_height=height
	height=original_height
	for line in text:
		line_height=write_line_to_img(font,height,color,drawer,line)
		height=space_lines+height+50
	return height-original_height-50
	
def create_total_height(reply_history):
    sensitive=False
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
    	border_top_bottom = 55
    	space_profile = 186
    	total_height = int(2 * border_top_bottom)
    	for tweet in set:
        	text, text_range,attached_image_widths,attached_image_heights = tweet["text"], tweet["text_range"],tweet["widths"],tweet["heights"]
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
        	
        	if tweet["sensitive"]==True:
        		sensitive=True
        	
        	if tweet["attached_images"]:
        		error=50
        		attached_image_height=get_images_height(attached_image_widths,attached_image_heights)
        		total_height = total_height + attached_image_height + error
        	else:
        		pass	
    	image_heights.append(total_height)
    return image_heights,reply_set,sensitive
    	
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
            
def create_screenshot_color(tweet_info, identify, increase_height, img,background_color=(255, 255, 255)):
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
    if attached_images:
    	attached_image_height=get_images_height(attached_image_widths,attached_image_heights)
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
    font = ImageFont.truetype("assets/arial 1.ttf", 50)
    font_username = ImageFont.truetype("assets/arial 1.ttf", 45)
    bold_font = ImageFont.truetype("assets/Roboto-Bold.ttf", 50)
    # Add Text to image
    color=(0, 0, 0)
    space_text=write_sentence_to_img(font,color,drawer_emoji,text,text_height)
    
    drawer_emoji.text(
        (240, profile_name_height), profile_name, font=bold_font, fill=(0, 0, 0)
    )
    drawer.text(
        (240, username_height), username, font=font_username, fill=(134, 135, 134),
    )
    # drawer.text((70, date_height), date, font=font_username, fill=(134, 135, 134))
    img.paste(profile_pics, (70, profile_pics_height), mask)
    #paste attached_images
    img=attach_images(img,attached_images,attached_image_loc, attached_image_height)
    if user_verified == True:
        create_verified(color=background_color)
        verified = Image.open("assets/verified_new.png")
        verified = verified.convert("RGB")
        verified = verified.resize((45, 45))
        profile_name_width,_=drawer_emoji.getsize(profile_name,bold_font)
        img.paste(verified, (int(240 + 15+profile_name_width), verified_height))
    return img, tweet_height
    
    
    
def create_replies_screenshot_color(id,background_color=(255, 255, 255)):
    no_replies, reply_history = get_reply_history(id)
    sensitive=False
    if len(reply_history) == 1:
        return None,None,None,reply_history[0],sensitive
    total_heights,reply_set,sensitive= create_total_height(reply_history)
    width = 1300
    counter=0
    imgs=[]
    for set in reply_set:
    	total_height=total_heights[counter]
    	img = Image.new(mode="RGB", size=(width, total_height), color=background_color)
    	drawer = ImageDraw.Draw(img)
    	drawer.rectangle([(int(width * 0.76), int(total_height - 55)), (width, total_height)],fill=(235, 240, 235),)
    	font_my_username = ImageFont.truetype("assets/arial 1.ttf", 35)
    	drawer.text((int(width * 0.76) + 15, total_height - 47),my_username,font=font_my_username,fill=(46, 45, 45),)
    	increase_height = 0
    	counter=counter+1
    	identify = 0
    	for reply in set:
            img, tweet_height = create_screenshot_color(
            reply, identify, increase_height, img,background_color)
            increase_height = increase_height + tweet_height
            identify = identify + 1
    	if total_height>=8192-125:
    	   	print(total_height)
    	   	img=img.resize((width,8191-125))
        	
    	imgs.append(img)
    return imgs,total_height,width,None,sensitive


def create_beautiful_thread(id, tweet_info=None):
    colors_dict = {
        0: {"tweet_color": (194, 217, 255), "background_color": (66, 135, 245)},
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

    background_color = color_selection["background_color"]
    tweet_color = color_selection["tweet_color"]
    if tweet_color == None:
        tweet_color = (255, 255, 255)
    imgs, total_height, width,reply_history,sensitive= create_replies_screenshot_color(
        id, background_color=tweet_color
    )
    if imgs==None:
    	return None,reply_history,sensitive
   #print(imgs)
    new_imgs=[]
    
    # paste tweet
    for img in imgs:
        w,h=img.size
        background_image = Image.new(mode="RGB", size=(w + 400, h+ 250), color=background_color)
        # mask
        mask_image = Image.new("L", [w, h], 0)
        mask_drawer = ImageDraw.Draw(mask_image)
        mask_drawer.rounded_rectangle([(0, 0), (w, h)],fill=255,width=2,radius=80)
        background_image.paste(img, (200, 125), mask=mask_image)
        #paste twitter
        create_twitter_logo(tweet_color)
        twitter_logo = Image.open("assets/twitter_logo_new.png")
        twitter_logo = twitter_logo.convert("RGB")
        twitter_logo = twitter_logo.resize((120, 100))
        # paste
        background_image.paste(twitter_logo, (w, 200))
        new_imgs.append(background_image)
    return new_imgs,None,sensitive
    
 
