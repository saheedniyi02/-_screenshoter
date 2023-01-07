import os
import html
import requests
import string
import numpy as np
from urllib.request import urlopen
from datetime import datetime, timedelta
from PIL import Image, ImageFont, ImageDraw
from tweepy import API, Client, OAuth1UserHandler
from statistics import mean


API_KEY = os.environ.get("API_KEY")
API_SECRET_KEY = os.environ.get("API_SECRET_KEY")
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
ACCESS_TOKEN = os.environ.get("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.environ.get("ACCESS_TOKEN_SECRET")



auth = OAuth1UserHandler(
    consumer_key=API_KEY,
    consumer_secret=API_SECRET_KEY,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET,
)

api = API(auth,wait_on_rate_limit=True)


def get_tweet_info(id):
    replied_to = api.get_status(
        id, include_ext_alt_text=True, include_entities=True, tweet_mode="extended"
    )
    user_info = replied_to.user
    date_created = replied_to.created_at.strftime("%H:%M . %b %d, %Y")
    profile_url = user_info.profile_image_url
    mentions = replied_to.entities.get("user_mentions")
    mentioned_usernames = ["@" + mention["screen_name"] for mention in mentions]
    try:
        profile_picture = Image.open(urlopen(profile_url))
    except:
        profile_picture = Image.open("assets/default_profile.png")
        profile_picture = profile_picture.convert("RGB")
    try:
        quoted_id = replied_to.quoted_status.id
    except:
        quoted_id = None
    try:
        image_urls = [media["media_url_https"] for media in replied_to.extended_entities["media"]]
        attached_images = [Image.open(urlopen(image_url)) for image_url in image_urls]
        widths,heights=[],[]
        for image in attached_images:
        	image_size=image.size
        	widths.append(image_size[0])
        	heights.append(image_size[1])
        sensitive=replied_to.possibly_sensitive
    except:
        attached_images = []
        widths=[]
        heights=[]
        sensitive=False

    return {
        "name": user_info.name,
        "username": "@" + str(user_info.screen_name),
        "verified": user_info.verified,
        "text": replied_to.full_text,
        "image": profile_picture,
        "date": date_created,
        "in_reply_to_status_id": replied_to.in_reply_to_status_id,
        "mentioned_users": mentioned_usernames,
        "text_range": replied_to.display_text_range,
        "quoted_id": quoted_id,
        "attached_images": attached_images,
        "widths":widths,
        "heights":heights,
        "sensitive":sensitive
    }


def decode_html(text):
    text = html.unescape(text)
    return text


def check_last_space(last_index, text):
    try:
        while last_index > 1:
            if text[last_index] != " ":
                last_index = last_index - 1
            else:
                return text[:last_index], last_index
    except:
        return text, len(text)


def remove_start_space(line):
    line = decode_html(line)
    try:
        if line[0] == " ":
            line = line[1 : len(line)]
            return line
        return line
    except:
        return line


def get_profile_name_score(profile_name):
    score = 0
    for i in profile_name:
        if i in string.punctuation:
            score = score + 0.2
        elif i in [" "]:
            score = score + 0.5
        elif i in string.ascii_uppercase:
            score = score + 1.24
        else:
            score = score + 1
    return score


def get_profile_pics_mask(profile_pics):
    h, w = profile_pics.size
    lum_img = Image.new("L", [h, w], 0)
    draw = ImageDraw.Draw(lum_img)
    draw.pieslice([(0, 0), (h, w)], 0, 360, fill=255)
    img_arr = np.array(profile_pics)
    lum_img_arr = np.array(lum_img)
    mask_im = Image.fromarray(lum_img_arr)
    profile_pics = profile_pics.resize((130, 130))
    mask_im = mask_im.resize((130, 130))
    return profile_pics, mask_im
    
def attach_one_image(img,attached_images,attached_image_loc, height):
    default_width=1150
    image_margin=6
    mask_image = Image.new("L", [default_width,height], 0)
    mask_drawer = ImageDraw.Draw(mask_image)
    mask_drawer.rounded_rectangle([(0, 0), (default_width,height)],fill=255,width=2,radius=40,)
    attached_images[0]=attached_images[0].resize((default_width,height))
    img.paste(attached_images[0], (70, attached_image_loc), mask=mask_image)
    return img
    
def attach_two_images(img,attached_images,attached_image_loc, height):
    default_width=1150
    image_margin=4
    width=int((default_width-image_margin)/2)
    #1st image
    mask_image = Image.new("L", [width,height], 0)
    mask_drawer = ImageDraw.Draw(mask_image)
    mask_drawer.rounded_rectangle([(0, 0), (width,height)],fill=255,width=2,radius=20)
    attached_images[0]=attached_images[0].resize((width,height))
    img.paste(attached_images[0], (70, attached_image_loc), mask=mask_image)
     		
    #2nd image
    attached_images[1]=attached_images[1].resize((width,height))
    img.paste(attached_images[1], (70+width+image_margin, attached_image_loc), mask=mask_image)
    return img
    
    
def attach_three_images(img,attached_images,attached_image_loc, height):
    default_width=1150
    image_margin=4
    width=int((default_width-image_margin)/2)
    reduced_height=int((height-image_margin)/2)
    #1st image
    mask_image = Image.new("L", [width,height], 0)
    mask_drawer = ImageDraw.Draw(mask_image)
    mask_drawer.rounded_rectangle([(0, 0), (width,height)],fill=255,width=2,radius=20)
    attached_images[0]=attached_images[0].resize((width,height))
    img.paste(attached_images[0], (70, attached_image_loc), mask=mask_image)
    
    #2nd image
    mask_image = Image.new("L", [width,reduced_height], 0)
    mask_drawer = ImageDraw.Draw(mask_image)
    mask_drawer.rounded_rectangle([(0, 0), (width,reduced_height)],fill=255,width=2,radius=10)
    attached_images[1]=attached_images[1].resize((width,reduced_height))
    img.paste(attached_images[1], (70+width+image_margin, attached_image_loc), mask=mask_image)
    
    #3rd image
    attached_images[2]=attached_images[2].resize((width,reduced_height))
    img.paste(attached_images[2], (70+width+image_margin, attached_image_loc++reduced_height+image_margin), mask=mask_image)
    return img
     	
def attach_four_images(img,attached_images,attached_image_loc, height):
    default_width=1150
    image_margin=2
    width=int((default_width-image_margin)/2)
    reduced_height=int((height-image_margin)/2)
    
    #1st image
    mask_image = Image.new("L", [width,reduced_height], 0)
    mask_drawer = ImageDraw.Draw(mask_image)
    mask_drawer.rounded_rectangle([(0, 0), (width,reduced_height)],fill=255,width=2,radius=10)
    attached_images[0]=attached_images[0].resize((width,reduced_height))
    img.paste(attached_images[0], (70, attached_image_loc), mask=mask_image)
    
    #2nd image    
    attached_images[1]=attached_images[1].resize((width,reduced_height))
    img.paste(attached_images[1], (70+width+image_margin, attached_image_loc), mask=mask_image)
    
    #3rd image
    attached_images[2]=attached_images[2].resize((width,reduced_height))
    #attached_images[2].save("static/test_images/test_attached.jpg")
    img.paste(attached_images[2], (70, attached_image_loc+reduced_height+image_margin), mask=mask_image)	    
    
    #4th image
    attached_images[3]=attached_images[3].resize((width,reduced_height))
    img.paste(attached_images[3], (70+width+image_margin, attached_image_loc+reduced_height+image_margin), mask=mask_image)
    return img
	 
def attach_images(img,attached_images,attached_image_loc, height):
     if attached_images:
     	if len(attached_images)==1:
     		img=attach_one_image(img,attached_images,attached_image_loc, height)
     	elif len(attached_images)==2:
     		img=attach_two_images(img,attached_images,attached_image_loc, height)  	
     	elif len(attached_images)==3:
     		img=attach_three_images(img,attached_images,attached_image_loc, height)
     	elif len(attached_images)==4:
     		img=attach_four_images(img,attached_images,attached_image_loc, height)
     return img

	
def get_images_height(widths,heights):
	if heights:
		default_width=1150
		height=int(default_width*(mean(heights)/mean(widths)))
		return height
	return 0