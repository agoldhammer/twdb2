from twdb.dbconnect import twitterdb
from twdb.dbif import getTopics, esearch
from twdb.cmdline import processCmdLine
from twdb.dupdetect import isURL, tokenize, filter_dups, dedupe


def test_connect():
    info = twitterdb.client.server_info()
    assert(info['version'] == "3.2.17")


def test_topics():
    topics = getTopics()
    for topic in topics:
        assert(topic["desc"] != "")


def test_bad_topic():
    """
    If we query with a *topic not in db, shd get back empty string
    """
    search_context = processCmdLine("-d 1 *xyznonsense")
    err, cursor = esearch(search_context)
    assert(err is not None)
    assert(cursor == [])


def test_isURL():
    s1 = "https://www.agmardor.com"
    s2 = "http://www.agm.com"
    s3 = "xyz"
    assert(isURL(s1))
    assert(isURL(s2))
    assert(isURL(s3) is False)


def test_tokenize():
    text = "Now is the time for all good men http://www.agm.com"
    tokenized = ["Now", "is", "the", "time", "for", "all", "good", "men"]
    assert(tokenize(text) == tokenized)


def test_filter_dups1():
    cursor = [{"text": "this is a tweet"}, {"text": "this is another"},
              {"text": "this is a tweet"},
              {"text": "this is another http://www.example.com"},
              {"text": "this is à fifth"}]
    results = [False, False, True, True, False]
    for isdup, _ in filter_dups(cursor):
        assert(isdup == results.pop(0))
    filtered = [status for status in dedupe(cursor)]
    assert(filtered == [cursor[0], cursor[1], cursor[4]])
