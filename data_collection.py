# import pandas as pd
# import datetime as dt
# import praw
# from pmaw import PushshiftAPI

def generate_reddit():
    '''
    Docstring
    '''
    import praw

    reddit = praw.Reddit(client_id='8vMcTdF4LlTwoVv3dM1DXg', 
                        client_secret='E_NxxYPlsPxM5vfvNstPKmwc5u4ESQ', 
                        user_agent='Scraper')
    return reddit

def generate_api():
    '''
    Docstring
    '''
    from pmaw import PushshiftAPI

    api = PushshiftAPI(num_workers=40, rate_limit=60)
    return api

def get_epoch(days):
    '''
    Docstring
    '''
    import datetime as dt

    utc_date = dt.date.today() - dt.timedelta(days=days)
    utc_date = dt.datetime.combine(utc_date, dt.datetime.min.time())
    return int(utc_date.timestamp())

def get_submissions(after: int, sub='nba', show_removed_posts=False, 
                    save_to_csv=True, file_name='posts.csv'):
    '''
    Docstring
    '''
    import pandas as pd

    assert type(after) == int
    assert type(sub) == str
    assert type(show_removed_posts) == bool
    assert type(save_to_csv) == bool
    assert type(file_name) == str and file_name[-4:] == '.csv'

    api = generate_api()
    posts = api.search_submissions(subreddit=sub, since=after)
    post_list = [post for post in posts]

    posts_df = pd.DataFrame(post_list)
    posts_df['utc_datetime_str'] = pd.to_datetime(posts_df['utc_datetime_str'])

    if not show_removed_posts:
        posts_df = posts_df[posts_df['removed_by_category'].isnull()].copy().reset_index()

    if save_to_csv:
        posts_df.to_csv(file_name, header=True, index=False)
        return posts_df
    else:
        return posts_df

def get_comments(posts, save_to_csv=True, file_name='comments.csv'):
    '''
    Docstring
    '''
    import pandas as pd

    assert isinstance(posts, pd.DataFrame)
    assert type(save_to_csv) == bool
    assert type(file_name) == str

    reddit = generate_reddit()
    post_ids = posts['id'].tolist()
    comments = []
    for post in post_ids:
        submission = reddit.submission(post)
        submission.comments.replace_more(limit=None)
        comments.extend([comment.__dict__ for comment in submission.comments.list()\
                         if comment.__dict__['removal_reason'] is None])

    comments_df = pd.DataFrame(comments)

    if save_to_csv:
        comments_df.to_csv(file_name, header=True, index=False)
        return comments_df
    else:
        return comments_df

if __name__ == "__main__":
    pass