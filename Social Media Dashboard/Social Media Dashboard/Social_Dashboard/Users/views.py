from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import auth
import os
from dotenv import load_dotenv
import facebook
import tweepy
from django.contrib.auth.decorators import login_required
from datetime import datetime, timedelta

# Load token from .env file
load_dotenv()
# Fetch Facebook credentials from .env
access_token = os.getenv("FACEBOOK_ACCESS_TOKEN")
APP_ID = os.getenv("FACEBOOK_APP_ID")
APP_SECRET = os.getenv("FACEBOOK_APP_SECRET")

# Create your views here.


def Base(request):
    return render(request,'Home/Base.html')

#signup
def Signup(request):
    if request.method == 'POST':
        f_name = request.POST['first_name']
        l_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['confirm_password']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'Email Already Exists')
            else:
                user = User.objects.create_user(username=username,email=email,password=password,first_name=f_name,last_name=l_name)
                user.save()
                messages.info(request,'User Created')
                return redirect('login')
    return render(request,'Home/Signup.html')



#login
def Login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('Base')
        else:
            messages.info(request,'Invalid Credentials')
    return render(request,'Home/Login.html')

#profile
def Profile(request):
    if request.user.is_authenticated:
        return render(request,'Home/profile.html')
    else:
        messages.info(request,'Please Login')
        return redirect('login')

#facebook
def get_facebook_data(template_name, request):
    try:
        graph = facebook.GraphAPI(access_token=access_token)
        profile = graph.get_object("me", fields="name,email,picture")
        posts = graph.get_connections(id='me', connection_name='posts')

        return render(request, f'Home/{template_name}.html', {
            'profile': profile,
            'posts': posts.get('data', [])
        })

    except facebook.GraphAPIError as e:
        messages.error(request, f"Facebook API Error: {str(e)}")
        return render(request, f'Home/{template_name}.html', {'error': str(e)})

    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
        return render(request, f'Home/{template_name}.html', {'error': str(e)})


def Facebook(request):
    if request.user.is_authenticated:
        return get_facebook_data('Facebook', request)
    else:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('login')


def Create_post(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('login')

    if request.method == 'POST':
        message = request.POST.get('message')
        if message:
            try:
                graph = facebook.GraphAPI(access_token=access_token)
                graph.put_object("me", "feed", message=message)
                messages.success(request, "Post created successfully!")
                return redirect('create_post')  # Prevent form resubmission
            except facebook.GraphAPIError as e:
                messages.error(request, f"Facebook API Error: {str(e)}")
        else:
            messages.error(request, "Please enter a message.")
    
    return get_facebook_data('Create_post', request)

    
    
    
def use_mock_twitter_data(username=None):
    print("Using mock Twitter data due to API limitations")
    
    if not username:
        username = "demo_user"
    
    # Create mock profile
    profile = {
        'id_str': '987654321',
        'name': 'Twitter Demo',
        'screen_name': username,
        'profile_image_url': 'https://via.placeholder.com/400x400',
        'created_at': datetime.now() - timedelta(days=365),
        'location': 'Demo Location',
        'followers_count': 1500,
        'friends_count': 350,
        'statuses_count': 2200,
        'description': 'This is a demo Twitter account for testing purposes.',
    }
    
    # Create mock stats
    stats = {
        'followers_count': 1500,
        'followers_change': 2.5,
        'engagement_rate': 3.8,
        'engagement_change': 3.2,
        'retweets_count': 85,
        'retweets_change': 5.7,
    }
    
    # Create mock tweets
    tweets = [
        {
            'id_str': f'tweet_{i}',
            'full_text': f'This is a sample tweet #{i} with some #hashtags and @mentions',
            'created_at': datetime.now() - timedelta(days=i),
            'favorite_count': 15 * i,
            'retweet_count': 5 * i,
            'reply_count': 3 * i,
            'is_retweet': i % 3 == 0,
            'in_reply_to_screen_name': 'someone' if i % 4 == 0 else None,
        } for i in range(1, 11)
    ]
    
    return profile, stats, tweets    



def get_twitter_client():
    try:
        bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        
        # Check if bearer token is available
        if not bearer_token:
            raise ValueError("Missing Twitter API Bearer Token in environment variables")
            
        # Use Client for v2 API
        return tweepy.Client(bearer_token=bearer_token)
    except Exception as e:
        print(f"Error initializing Twitter client: {str(e)}")
        raise

def fetch_twitter_data(username=None):
    try:
        client = get_twitter_client()
        
        # Use v2 endpoints
        if username:
            user_response = client.get_user(username=username, user_fields=["profile_image_url", "description", "created_at", "location", "public_metrics"])
            if not user_response or not user_response.data:
                raise ValueError(f"User {username} not found")
            user_profile = user_response.data
        else:
            # For demo purposes, use a default user since v2 doesn't have verify_credentials
            # In production, you'd store the authenticated user's username
            default_username = os.getenv("TWITTER_DEFAULT_USERNAME", "twitter")
            user_response = client.get_user(username=default_username, user_fields=["profile_image_url", "description", "created_at", "location", "public_metrics"])
            if not user_response or not user_response.data:
                raise ValueError(f"Default user not found")
            user_profile = user_response.data
            username = user_profile.username

        # Get user ID for tweet lookup
        user_id = user_profile.id
        
        # Get tweets using v2 endpoint
        tweets_response = client.get_users_tweets(
            id=user_id,
            max_results=10,
            tweet_fields=["created_at", "public_metrics", "referenced_tweets"],
            expansions=["referenced_tweets.id"]
        )
        
        tweets = tweets_response.data if tweets_response and tweets_response.data else []

        # Extract metrics from user profile
        metrics = user_profile.public_metrics
        total_followers = metrics.get("followers_count", 0)
        total_friends = metrics.get("following_count", 0)
        total_tweets = metrics.get("tweet_count", 0)

        # Calculate engagement metrics
        if tweets:
            total_likes = sum(tweet.public_metrics.get("like_count", 0) for tweet in tweets)
            total_retweets = sum(tweet.public_metrics.get("retweet_count", 0) for tweet in tweets)
            avg_engagement = (total_likes + total_retweets) / len(tweets)
            engagement_rate = round((avg_engagement / total_followers) * 100, 1) if total_followers > 0 else 0
        else:
            engagement_rate = 0
            total_retweets = 0

        # Create profile dictionary
        profile = {
            'id_str': str(user_profile.id),
            'name': user_profile.name,
            'screen_name': user_profile.username,
            'profile_image_url': user_profile.profile_image_url,
            'created_at': user_profile.created_at,
            'location': getattr(user_profile, 'location', ""),
            'followers_count': total_followers,
            'friends_count': total_friends,
            'statuses_count': total_tweets,
            'description': getattr(user_profile, 'description', ""),
        }

        # Create stats dictionary
        stats = {
            'followers_count': total_followers,
            'followers_change': 2.5,  # Example value
            'engagement_rate': engagement_rate,
            'engagement_change': 3.2,  # Example value
            'retweets_count': total_retweets,
            'retweets_change': 5.7,  # Example value
        }

        # Process tweets
        processed_tweets = []
        for tweet in tweets:
            # Check if it's a retweet
            is_retweet = False
            if hasattr(tweet, 'referenced_tweets') and tweet.referenced_tweets:
                for ref in tweet.referenced_tweets:
                    if ref.type == 'retweeted':
                        is_retweet = True
                        break
            
            processed_tweets.append({
                'id_str': str(tweet.id),
                'full_text': tweet.text,
                'created_at': tweet.created_at,
                'favorite_count': tweet.public_metrics.get('like_count', 0),
                'retweet_count': tweet.public_metrics.get('retweet_count', 0),
                'reply_count': tweet.public_metrics.get('reply_count', 0),
                'is_retweet': is_retweet,
                'in_reply_to_screen_name': None,  # Not available in v2 without additional lookups
            })

        return profile, stats, processed_tweets
        
    except tweepy.TweepyException as e:
        print(f"Twitter API Error: {str(e)}")
        raise
    except Exception as e:
        print(f"Unexpected error in fetch_twitter_data: {str(e)}")
        raise





def twitter(request):
    if request.user.is_authenticated:
        try:
            profile, stats, processed_tweets = fetch_twitter_data()
            return render(request, 'Home/Twitter.html', {
                'profile': profile,
                'stats': stats,
                'tweets': processed_tweets
            })
        except tweepy.TweepyException as e:
            messages.error(request, f"Twitter API Error: {str(e)}")
        except Exception as e:
            messages.error(request, f"An error occurred: {str(e)}")
        return render(request, 'Home/Twitter.html', {'profile': {}, 'stats': {}, 'tweets': []})
    else:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('login')

def twitter_user_view(request, username=None):
    try:
        profile, stats, processed_tweets = fetch_twitter_data(username=username)
        return render(request, 'Home/Twitter.html', {
            'profile': profile,
            'stats': stats,
            'tweets': processed_tweets
        })
    except tweepy.TweepyException as e:
        messages.error(request, f"Twitter API Error: {str(e)}")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")
    return render(request, 'Home/Twitter.html', {'profile': {}, 'stats': {}, 'tweets': []})




def Create_twitter_post(request):
    if not request.user.is_authenticated:
        messages.error(request, "You must be logged in to access this page.")
        return redirect('login')

    if request.method == 'POST':
        tweet_text = request.POST.get('tweet_text')
        tweet_hashtags = request.POST.get('tweet_hashtags', '')
        media_file = request.FILES.get('tweet_media')
        
        if tweet_text:
            try:
                # Get Twitter API credentials
                bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
                consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
                consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
                access_token = os.getenv("TWITTER_ACCESS_TOKEN")
                access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")
                
                # Check if we have the required credentials for posting
                if not all([consumer_key, consumer_secret, access_token, access_token_secret]):
                    messages.error(request, "Twitter API credentials for posting are not configured.")
                    return redirect('create_twitter_post')
                
                # Combine tweet text with hashtags
                full_tweet = tweet_text
                if tweet_hashtags:
                    full_tweet += ' ' + tweet_hashtags
                
                # Initialize Twitter API v1.1 client for posting
                auth = tweepy.OAuth1UserHandler(
                    consumer_key, consumer_secret,
                    access_token, access_token_secret
                )
                api = tweepy.API(auth)
                
                # Post the tweet
                if media_file:
                    # Save the uploaded file temporarily
                    temp_file = f"temp_media_{request.user.id}.jpg"
                    with open(temp_file, 'wb+') as destination:
                        for chunk in media_file.chunks():
                            destination.write(chunk)
                    
                    # Upload media and post tweet with media
                    media = api.media_upload(temp_file)
                    api.update_status(status=full_tweet, media_ids=[media.media_id])
                    
                    # Remove temporary file
                    os.remove(temp_file)
                else:
                    # Post tweet without media
                    api.update_status(full_tweet)
                
                messages.success(request, "Tweet posted successfully!")
                return redirect('create_twitter_post')
                
            except tweepy.TweepyException as e:
                messages.error(request, f"Twitter API Error: {str(e)}")
            except Exception as e:
                messages.error(request, f"An error occurred: {str(e)}")
        else:
            messages.error(request, "Please enter tweet text.")
    
    try:
        # Get user's Twitter profile and tweets to display
        profile, stats, tweets = fetch_twitter_data()
        return render(request, 'Home/Create_twitter_post.html', {
            'profile': profile,
            'tweets': tweets
        })
    except Exception as e:
        messages.error(request, f"Error fetching Twitter data: {str(e)}")
        return render(request, 'Home/Create_twitter_post.html', {
            'profile': {},
            'tweets': []
        })





def instagram(request):
    pass
    # return render(request,'Home/Instagram.html')

def linkedin(request):
    pass
    # return render(request,'Home/Linkedin.html')

def analytics(request):
    pass
    # return render(request,'Home/Analytics.html')
    
def schedule(request):
    pass
    # return render(request,'Home/Schedule.html')
    
def settings(request):
    pass
    # return render(request,'Home/Settings.html')
    

def logout(request):
    auth.logout(request)
    return redirect('login')
    # return render(request,'Home/Logout.html')
