from flask import Flask, render_template, redirect, request
import tweepy
import constants


app = Flask(__name__)


@app.route('/', methods =['POST', 'GET'])
def home():
    if request.method == 'GET':
        return render_template('home.html')

    # post
    status_id = parse_status_id(request.form['resource'])
    tweet = get_tweet(status_id)

    return({"tweet":tweet})
    # return render_template('home.html')


def get_tweet(id):
    # authenticate to Twitter
    auth = tweepy.OAuthHandler(constants.API_KEY, constants.API_SECRET)
    auth.set_access_token(constants.ACCESS_TOKEN, constants.ACCESS_TOKEN_SECRET)

    # create API object
    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

    # fetch tweet and return subset of properties
    tweet = api.get_status(id)
    return({"created_at":tweet.created_at, "author":tweet.user.name, "text":tweet.text})


def parse_status_id(resource):
    # TODO need error handling
    start = -1
    for _ in range(0, 5):
        start = resource.find('/', start + 1)
    
    resource_starting_at_id = resource[start + 1:]
    query_start = resource_starting_at_id.find('?')

    if query_start > -1:
        return(resource_starting_at_id[:query_start])
    else:
        return(resource_starting_at_id)


if __name__ == "__main__":
	app.run()