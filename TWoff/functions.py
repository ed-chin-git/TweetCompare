from TWpred.twitter_API import *

def adduser(tw_handle):
   #   Get TW user info 
   twitter_user = TWITTER.get_user(tw_handle)

   #  get their tweets from TW timeline
   tweets = twitter_user.timeline(count=200, exclude_replies=True, include_rts=False, tweet_mode='extended')

   # create a DB User -  use the model.py class
   db_user = User(id=twitter_user.id, name=twitter_user.screen_name, newest_tweet_id=tweets[0].id)

   # load the tweets
   for tweet in tweets:
      embedding = BASILICA.embed_sentence(tweet.full_text, model='twitter')
      db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500], embedding=embedding)
      DB.session.add(db_tweet)        #  add the tweets to the DB first
      db_user.tweets.append(db_tweet) # then connect/append to the user
   
   DB.session.add(db_user)  # can this be done earlier??
   DB.session.commit()
   #------
   return


def add_or_update_user(username):

   """Add or update a user *and* their Tweets, error if no/private user."""
   try:
      twitter_user = TWITTER.get_user(username)
      #  if userId exists .get it  or if not create one 
      db_user = (User.query.get(twitter_user.id) or
                  User(id=twitter_user.id, name=username))
      DB.session.add(db_user)
      # We want as many recent non-retweet/reply statuses as we can get
      tweets = twitter_user.timeline(
         count=200, exclude_replies=True, include_rts=False,
         tweet_mode='extended', since_id=db_user.newest_tweet_id)
      if tweets:
         db_user.newest_tweet_id = tweets[0].id
      for tweet in tweets:
         # Get embedding for tweet, and store in db
         embedding = BASILICA.embed_sentence(tweet.full_text,
                                             model='twitter')
         db_tweet = Tweet(id=tweet.id, text=tweet.full_text[:500],
                           embedding=embedding)
         db_user.tweets.append(db_tweet)
         DB.session.add(db_tweet)
   
   except Exception as e:
      print('Error processing {}: {}'.format(username, e))
      raise e
   else:
      DB.session.commit()
