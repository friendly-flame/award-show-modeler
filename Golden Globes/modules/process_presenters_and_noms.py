import nltk
import operator
import sys
import datetime
from dateutil import tz

import regex
import util


def run(db, target, event):
    event.wait()
    queue = list(target.winners)
#    current_winner = queue.pop(0)
    for winner, value, time in target.winners:
        presenter_names = {}
        nominee_names = {}
        for i in [-1,1]:
            if i == -1:
                current_dict = presenter_names
            else:
                current_dict = nominee_names
            cursor = db.collection.find({'created_at': regex.time_model(time.hour, time.minute, i)})
            for tweet in cursor:
                n = regex.name.match(tweet['text'])
                if n:
                    n = n.group()
                    toks = nltk.word_tokenize(n)
                    if toks[0].lower() in util.common_words or toks[1].lower() in util.common_words:
                        continue
                    else:
                        if n in current_dict:
                            current_dict[n] += 1
                        # elif not weed_out(n, target):
                        else:
                            current_dict[n] = 1
        p = sorted(presenter_names.items(), key=operator.itemgetter(1), reverse=True)
        n = sorted(nominee_names.items(), key = operator.itemgetter(1),reverse=True)

        # TODO: As long as didn't win, isn't host, etc
        target.presenters[winner] = (p[0], p[1])
        target.nominees[winner] = (n[0], n[1], n[2], n[3])
    return




    # for tweet in mega_cursor:
    #     tweet_time = datetime.datetime.strptime(tweet['created_at'], '%a %b %d %H:%M:%S +0000 %Y')
    #     # print current_winner[2]
    #     # print tweet_time
    #     delta = current_winner[2] - tweet_time.replace(tzinfo=tz.gettz('UTC'))
    #     if 180 > delta.total_seconds() > 0:
    #         tweet_text = tweet['text']
    #         tokens = nltk.word_tokenize(tweet_text)
    #         bgs = nltk.bigrams(tokens)
    #         for name in bgs:
    #             if name[0][0].isupper() and name[1][0].isupper():
    #                 if name in result:
    #                     presenter_names[name] += 1
    #                 else:
    #                     presenter_names[name] = 1
    #     elif -180 < delta.total_seconds() < 0:
    #         tweet_text = tweet['text']
    #         tokens = nltk.word_tokenize(tweet_text)
    #         bgs = nltk.bigrams(tokens)
    #         for name in bgs:
    #             if name[0][0].isupper() and name[1][0].isupper():
    #                 if name in result:
    #                     nominee_names[name] += 1
    #                 else:
    #                     nominee_names[name] = 1
    #     elif delta.total_seconds() < -180:
    #         if len(queue) > 0:
    #             current_winner = queue.pop(0)
    #         else:
    #             print nominee_names
    #             print presenter_names

            # n = regex.name.match(tweet['text'])
            # if n:
            #     n = n.group()
            #     toks = nltk.word_tokenize(n)
            #     if toks[0].lower() in util.common_words or toks[1].lower() in util.common_words:
            #         continue
            #     else:
            #         if n in names:
            #             names[n] += 1
            #         # elif not weed_out(n, target):
            #         else:
            #             names[n] = 1
            # else:
            #     continue


# TODO: tweak; remove duplicates


def weed_out(name, target):
    # hits = ia.search_person(name)
    # if not hits:
    #     return True
    if name in target.hosts:
        return True
    if name in target.winning_people:
        return True
    return False