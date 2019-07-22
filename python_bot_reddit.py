import time
import re
import praw

from creds import *

reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_id, username=username,
                     password=password)

subreddits = ['funny', 'memes', 'ProgrammerHumor']

# submit an url to the 3 subreddits above.
pos = 0
title = 'A random meme.'
url = 'https://imgur.com/t/justprogrammerthings/32iFA'
errors = 0


def post():
    global title
    global url
    global subreddits
    global pos
    global errors

    # name of the subreddit we posting to
    try:
        subreddit = reddit.subreddit(subreddits[pos])
        subreddit.submit(title, url=url)

        print ("Posted to r/" + subreddits[pos])
        pos = pos + 1
        if pos <= len(subreddits) - 1:
            post()
        else:
            print 'Done'
    except praw.exceptions.APIException as e:
        if e.error_type == 'RATELIMIT':
            delay = re.search("(\d+) minutes?", e.message)
            # converting the delay into seconds.
            print e.message
            if delay:
                # if error gives delay in minutes.
                delay_seconds = float(int(delay.group(1)) * 60)
                time.sleep(delay_seconds)
                post()
            else:
                # if error gives delay in seconds.
                delay = re.search("(\d+) seconds", e.message)
                delay_seconds = float(int(delay.group(1)))
                time.sleep(delay_seconds)
                post()

    except:
        errors = errors + 1
        if (errors > 5):
            print "Crashed"
            exit(1)


post()
