import os
from numpy import full
from tweepy import API, Client, OAuth1UserHandler
from screenshot_tweet import create_tweet_screenshot_light, create_tweet_screenshot_dark
from screenshot_reply import (
    create_replies_screenshot_light,
    create_replies_screenshot_dark,
)
from beautiful_screenshots import create_beautiful_screenshot
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
    count = 4
    reply = "Your screenshot can be found below😁!\n\nRemember your commands:\n 'All' command gets all the tweets above the tweet you commented on in the thread.\n\n 'light' and 'dark' commands returns your screenshot in light mode⬜ and dark mode⬛"
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
                        image,tweet_info= create_replies_screenshot_light(replied_to_id)
                        if image == None:
                            image = create_tweet_screenshot_light(replied_to_id,tweet_info)
                    else:
                        image, tweet_info = screenshot_quote_light(replied_to_id)
                        if image == None:
                            image = create_tweet_screenshot_light(
                                replied_to_id, tweet_info
                            )
                else:
                    if (
                        ("conversation" in full_text)
                        or ("all" in full_text)
                        or ("thread" in full_text)
                        or ("everything" in full_text)
                    ):
                        image,tweet_info = create_replies_screenshot_dark(replied_to_id)
                        if image == None:
                        	if ("dark" in full_text) or ("black" in full_text):
                        		image = create_tweet_screenshot_dark(replied_to_id,tweet_info)
                        	else:
                        		                                image=create_beautiful_screenshot(replied_to_id, tweet_info)
                        		
                    else:

                        image, tweet_info = screenshot_quote_dark(replied_to_id)
                        if image == None:
                            if ("dark" in full_text) or ("black" in full_text):
                                image = create_tweet_screenshot_dark(
                                    replied_to_id, tweet_info
                                )
                            else:
                                image = create_beautiful_screenshot(
                                    replied_to_id, tweet_info
                                )
                if not isinstance(image, list):
                    image.save("screenshot.jpg")
                    media = api.media_upload(filename="screenshot.jpg")
                    response = api.update_status(
                        status=f"@{author} {reply} \n",
                        in_reply_to_status_id=str(mention_id),
                        media_ids=[media.media_id_string],
                    )
                    replied_ids = open("assets/replied_ids.txt", "a")
                    replied_ids.write(f"{mention_id}\n")
                    replied_ids.write(f"{response.id}\n")
                    replied_ids.close()
                    print(mention_id)
                else:
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
                    )
                    replied_ids = open("assets/replied_ids.txt", "a")
                    replied_ids.write(f"{mention_id}\n")
                    replied_ids.write(f"{response.id}\n")
                    replied_ids.close()

            else:
                print("replied already or not a valid screenshot request")
        except Exception as e:
            print(e)
            pass


def clean_replied():
    replied_ids = open("assets/replied_ids.txt", "w")
    replied_ids.close()
