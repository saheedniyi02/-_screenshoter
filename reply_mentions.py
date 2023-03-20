import os
import random
from numpy import full
from tweepy import API, Client, OAuth1UserHandler
from screenshot_tweet import create_tweet_screenshot_light, create_tweet_screenshot_dark
from screenshot_reply import (
    create_replies_screenshot_light,
    create_replies_screenshot_dark,
)
from beautiful_screenshots import create_beautiful_screenshot
from beautiful_thread import create_beautiful_thread
from screenshot_quotes import screenshot_quote_light, screenshot_quote_dark


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


def get_tweet_id_text(mention):
    try:
        return (
            mention.in_reply_to_status_id,
            mention.full_text[mention.display_text_range[0] :].lower(),
        )
    except AttributeError:
        return None


def get_mention_id(mention):
    try:
        return mention.id
    except AttributeError:
        pass


def reply_mentions():
    bot_name = "_screenshoter"
    count = 2
    reply_1 = "Your screenshot can be found below😁!\n\nRemember your commands:\n 'All' command gets all the tweets above the tweet you commented on in the thread.\n\n 'light' and 'dark' commands returns your screenshot in light mode⬜ and dark mode⬛"
    reply_2="Your screenshot can be found below 😁!\n\n🤩Want to get your screenshot without using the bot? Visit : screenshoter.live ."
    reply=random.choice([reply_1,reply_2])
    #reply = "Your screenshot can be found below😁!\n\nAd: Everyone will run after this if they knew how good this was.\nThis?🤔\nYea, what I'm about to tell you😎👇\nGet Free daily trade Calls on Cryptos and NFts with Giveaways here http://t.me/tradewithwealth"
    #reply="Your screenshot can be found below 😁!\n\n🤩Ad: MyCowrie is the 1st crypto to launch with a moneyback guarantee & by a legal team. Join their group to buy some before the next pump & CEX Listing: https://t.co/BeDkx0bNES"




    #reply=random.choice([reply_1,reply_2])
    #reply="Your screenshot can be found below😁!\nAd: HOW OTHER NIGERIANS ARE EARNING IN DOLLARS, BY JUST UPLOADING BOOKS ON AMAZON\n~Even ithout a writing skill or you've not written  a book before\nJOIN CLASS FOR FREE CLICK HERE👇\nhttps://t.co/V2HCK9S5kj\nlink expires soon"
    mentions = api.mentions_timeline(
        count=count, include_entities=True, tweet_mode="extended"
    )
    replied_ids = open("assets/replied_ids.txt", "r")
    replied_ids_list = [replied_id for replied_id in replied_ids]
    replied_ids.close()
    for mention in reversed(mentions):
        try:
            mention_id = mention.id
            author = mention.user.screen_name
            replied_to_id, full_text = get_tweet_id_text(mention)
            if (
                (f"{mention_id}\n" not in replied_ids_list)
                and (bot_name in full_text)
                and (author != bot_name)
            ):
                if ("light" in full_text) or ("white" in full_text):
                    if (
                        ("conversation" in full_text)
                        or ("all" in full_text)
                        or ("thread" in full_text)
                        or ("everything" in full_text)
                    ):
                        image,tweet_info,sensitive= create_replies_screenshot_light(replied_to_id)
                        if image == None:
                            image,sensitive= create_tweet_screenshot_light(replied_to_id,tweet_info)
                    else:
                        image, tweet_info,sensitive = screenshot_quote_light(replied_to_id)
                        if image == None:
                            image,sensitive = create_tweet_screenshot_light(
                                replied_to_id, tweet_info
                            )
                elif ("dark" in full_text) or ("black" in full_text):
                    if (
                        ("conversation" in full_text)
                        or ("all" in full_text)
                        or ("thread" in full_text)
                        or ("everything" in full_text)
                    ):
                        image,tweet_info ,sensitive= create_replies_screenshot_dark(replied_to_id)
                        if image == None:
                        	image,sensitive = create_tweet_screenshot_dark(replied_to_id,tweet_info)               		
                    else:
                        image, tweet_info,sensitive = screenshot_quote_dark(replied_to_id)
                        if image == None:
                            image ,sensitive= create_tweet_screenshot_dark(replied_to_id, tweet_info)
                else:
                   if (("conversation" in full_text) or ("all" in full_text) or ("thread" in full_text) or ("everything" in full_text)):
                        image,tweet_info ,sensitive= create_beautiful_thread(replied_to_id)
                        if image == None:
                        	image,sensitive = create_beautiful_screenshot(replied_to_id,tweet_info) 
                   else:
                        image, tweet_info,sensitive = screenshot_quote_dark(replied_to_id)
                        if image == None:
                            image ,sensitive= create_beautiful_screenshot(replied_to_id, tweet_info)
   
               
                              
                if not isinstance(image, list):
                    replied_ids = open("assets/replied_ids.txt", "a")
                    replied_ids.write(f"{mention_id}\n")
                    replied_ids.close()
                    image.save("screenshot.jpg")
                    media = api.media_upload(filename="screenshot.jpg")
                    response = api.update_status(
                        status=f"@{author} {reply} \n",
                        in_reply_to_status_id=str(mention_id),
                        media_ids=[media.media_id_string],
                        possibly_sensitive=sensitive
                    )

                    print(mention_id)
                else:
                    replied_ids = open("assets/replied_ids.txt", "a")
                    replied_ids.write(f"{mention_id}\n")
                    replied_ids.close()
                    media_dict = {}
                    for i in range(len(image)):
                        image[i].save(f"screenshot{i}.jpg")
                        media_dict[i] = api.media_upload(f"screenshot{i}.jpg")
                    media_ids = [
                        media_dict[i].media_id_string for i in range(len(image))
                    ]
                    response = api.update_status(
                        status=f"@{author} {reply} \n",
                        in_reply_to_status_id=str(mention_id),
                        media_ids=media_ids,
                        possibly_sensitive=sensitive
                    )
                    print(mention_id)


            else:
                print("replied already or not a valid screenshot request")
        except Exception as e:
            print(e)
            pass


def clean_replied():
    replied_ids = open("assets/replied_ids.txt", "w")
    replied_ids.close()
    
def reply_form(id,type,color):
	if type=="tweet":
		if color=="light":
			img,_=create_tweet_screenshot_light(id)
		elif color=="dark":
			img,_=create_tweet_screenshot_dark(id)
		elif color=="colorful":
			img,_=create_beautiful_screenshot(id)
		images=[img]
	elif type=="thread":
		if color=="light":
			images,_,_=create_replies_screenshot_light(id)
		elif color=="dark":
			images,_,_=create_replies_screenshot_dark(id)	
		elif color=="colorful":
			images,_,_=create_beautiful_thread(id)
		if images==None:
			return reply_form(id,"tweet",color)
	return images
