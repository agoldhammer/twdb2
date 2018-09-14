#!/usr/bin/env python

"""read news feeds from twitter"""

import logging
from logging import FileHandler
from time import sleep
from twdb2.twauthenticate import getTwitterApi
from twdb2.dbif import storeStatus, DuplicateStatus
from twdb2.dbif import get_lastread, store_lastread
from twdb2.prettytext import printStatus
from tweepy import Cursor

LOGFILENAME = "/var/log/twdb2/twdb2.log"

processed = 0
added = 0
skipped = 0
maxid = 0

def pruneStatus(status):
    """Prunes status record to store only info of interest
    :param status: the status record
    :returns pruned status as dictionary
    """
    return({"id": status.id, "author": status.author.screen_name,
            "created_at": status.created_at, "source": status.source,
            "text": status.text})



def processStatus(i, status, quiet):
    """Process a Twitter status record
    :param i: sequence number
    :param status: the status record
    :returns nothing
     .. prints notification of duplicate record and does not insert
    """
    global processed, added, skipped, maxid
    processed += 1
    author = status.author.screen_name
    status_id = status.id
    if status_id > maxid:
        maxid = status_id
    created_at = status.created_at
    try:
        status = pruneStatus(status)
        storeStatus(status)
        # If, successful, display the entry being processed ...
        if not quiet:
            out = "\n---\n{}. author {} id {}  time {} via {}"
            print(out.format(i + 1, author, status_id,
                            created_at, status["source"]))
            printStatus(status)
        added += 1
    # if status is already in db, we get here
    except DuplicateStatus:
        skipped += 1


def main(quiet=True):
    global maxid, processed, added, skipped
    processed = added = skipped = 0
    _, maxid = get_lastread()
    msg = f"Reading twitter statuses after id {maxid}"
    logger.info(msg)
    # print(msg)
    api = getTwitterApi(wait=True, notify=True)
    for i, status in enumerate(Cursor(api.list_timeline,
                                      owner_screen_name="artgoldhammer",
                                      slug="EuropeanNews",
                                      since_id=maxid).items()):
        processStatus(i, status, quiet)

    store_lastread(maxid)
    msg = "processed {}. added {}. skipped {} maxid {}".format(processed,
                                                            added, skipped, maxid)
    logger.info(msg)
    # print(msg)

if __name__ == "__main__":
    SLEEPTIME=900
    # print("Processing usnews feeds for twdb")
    logger = logging.getLogger("twdb2")
    logger.setLevel(logging.INFO)
    fh = FileHandler(LOGFILENAME, 'w')
    fh.setLevel(logging.INFO)
    myformat = logging.Formatter(
        '%(asctime)s-%(name)s:%(levelname)s--%(message)s')
    fh.setFormatter(myformat)
    logger.addHandler(fh)
    while True:

        try:
            logger.debug("Starting read")
            main()
            logger.debug(f"Sleeping for {SLEEPTIME} seconds")
            sleep(SLEEPTIME)
        except Exception as e:
            logger.info(f"exception while processing twitteer feed {e}")
