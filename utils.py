import os
import html
import requests
import string
import numpy as np
from urllib.request import urlopen
from datetime import datetime, timedelta
from PIL import Image, ImageFont, ImageDraw
from tweepy import API, Client, OAuth1UserHandler


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

api = API(auth)


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
        profile_picture = Image.open("default_profile.png")
        profile_picture = profile_picture.convert("RGB")
    try:
        quoted_id = replied_to.quoted_status.id
        print(quoted_id)
    except:
        quoted_id = None
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
