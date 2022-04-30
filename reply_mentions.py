import os
from tweepy import API, Client, OAuth1UserHandler
from screenshot_tweet import create_tweet_screenshot_light, create_tweet_screenshot_dark
from screenshot_reply import (
    create_replies_screenshot_light,
    create_replies_screenshot_dark,
)
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

api = API(auth)


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
    count = 5
    reply = "Your screenshot can be found below"
    mentions = api.mentions_timeline(
        count=count, include_entities=True, tweet_mode="extended"
    )
    replied_ids = open("replied_ids.txt", "r")
    replied_ids_list = [replied_id for replied_id in replied_ids]
    replied_ids.close()
    for mention in reversed(mentions):
        try:
            mention_id = mention.id
            author = mention.user.screen_name
            replied_to_id, full_text = get_tweet_id_text(mention)
            if (
                (f"{mention_id}\n" not in replied_ids_list)
                and ("screenshot" in full_text)
                and (reply not in full_text)
            ):
                if "light" in full_text:
                    if (" conversation " in full_text) or (" all " in full_text):
                        image = create_replies_screenshot_light(replied_to_id)
                        if image == None:
                            image = create_tweet_screenshot_light(replied_to_id)
                    elif (" quotes " in full_text) or (" quote " in full_text):
                        image = screenshot_quote_light(replied_to_id)
                        if image == None:
                            image = create_tweet_screenshot_light(replied_to_id)
                    else:
                        image = create_tweet_screenshot_light(replied_to_id)
                else:
                    if (" conversation " in full_text) or (" all " in full_text):
                        image = create_replies_screenshot_dark(replied_to_id)
                        if image == None:
                            image = create_tweet_screenshot_dark(replied_to_id)
                    elif (" quotes " in full_text) or (" quote " in full_text):
                        image = screenshot_quote_dark(replied_to_id)
                        if image == None:
                            image = create_tweet_screenshot_dark(replied_to_id)
                    else:
                        image = create_tweet_screenshot_dark(replied_to_id)
                image.save("screenshot.jpg")
                # media = api.media_upload(filename="screenshot.jpg")
                # api.update_status(status=f"@{author} {reply} \n",in_reply_to_status_id=str(mention_id),media_ids=[media.media_id_string],)
                replied_ids = open("replied_ids.txt", "a")
                replied_ids.write(f"{mention_id}\n")
                replied_ids.close()
                print(mention_id)
            else:
                print("replied already or not a valid screenshot request")
        except:
            pass


def clean_replied():
    replied_ids = open("replied_ids.txt", "w")
    replied_ids.close()
