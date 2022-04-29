import os
from tweepy import API, Client, OAuth1UserHandler
from screenshot_tweet import create_tweet_screenshot_light, create_tweet_screenshot_dark
from screenshot_reply import (
    create_replies_screenshot_light,
    create_replies_screenshot_dark,
)


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


def get_tweet_id_text(mention):
    try:
        return (
            mention.in_reply_to_status_id,
            mention.full_text[mention.display_text_range[0] :],
        )
    except AttributeError:
        return None


def get_mention_id(mention):
    try:
        return mention.id
    except AttributeError:
        pass


def reply_mentions():
    count = 5
    mentions = api.mentions_timeline(
        count=count, include_entities=True, tweet_mode="extended"
    )
    replied_ids = open("replied_ids.txt", "r")
    replied_ids_list = [replied_id for replied_id in replied_ids]
    replied_ids.close()
    for mention in reversed(mentions):
        try:
            mention_id = mention.id
            if f"{mention_id}\n" not in replied_ids_list:
                author = mention.user.screen_name
                replied_to_id, full_text = get_tweet_id_text(mention)
                if "dark" in full_text:
                    if "conversation" in full_text:
                        image = create_replies_screenshot_dark(replied_to_id)
                        if image == None:
                            image = create_tweet_screenshot_dark(replied_to_id)
                    else:
                        image = create_tweet_screenshot_dark(replied_to_id)
                elif "light" in full_text:
                    if "conversation" in full_text:
                        image = create_replies_screenshot_light(replied_to_id)
                        if image == None:
                            image = create_tweet_screenshot_light(replied_to_id)
                    else:
                        image = create_tweet_screenshot_light(replied_to_id)
                else:
                    if "conversation" in full_text:
                        image = create_replies_screenshot_dark(replied_to_id)
                        if image == None:
                            image = create_tweet_screenshot_dark(replied_to_id)
                    else:
                        image = create_tweet_screenshot_dark(replied_to_id)
                image.save("screenshot.jpg")
                media = api.media_upload(filename="screenshot.jpg")
                api.update_status(
                    status=f"@{author} Your screenshot can be found here \n",
                    in_reply_to_status_id=str(mention_id),
                    media_ids=[media.media_id_string],
                )
                replied_ids = open("replied_ids.txt", "a")
                replied_ids.write(f"{mention_id}\n")
                replied_ids.close()
                print(mention_id)
            else:
                print("replied already")
        except:
            pass


def clean_replied():
    replied_ids = open("replied_ids.txt", "w")
    replied_ids.close()


reply_mentions()
