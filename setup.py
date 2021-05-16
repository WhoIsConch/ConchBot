import os

if not os.path.exists('.env'):
    env = open(".env", "w")

    print('Welcome to Conchbot setup.')

    # TOKEN
    print('Your bot\'s token can be obtained from https://discord.com/developers/applications.')
    token = input('Bot token: ')
    env.write(f"TOKEN={token}\n")

    # Reddit ID
    reddit_application_id = input("Your Reddit API id application key: ")
    env.write(f"redditid={reddit_application_id}\n")

    # Reddit Secret
    reddit_application_secret = input("Your Reddit API secret application key: ")
    env.write(f"redditsecret={reddit_application_secret}\n")

    # Reddit Password
    reddit_application_password = input("Your Reddit API password application key: ")
    env.write(f"redditpassword={reddit_application_secret}\n")
    print("You can get PGamerx API by going to this link: https://api-info.pgamerx.com/register.html")

    # PGamerx API Key
    pgamerx_api_key = input("Your PGamerx API id application key: ")
    env.write(f"aiapikey={pgamerx_api_key}\n")

    # Close File
    env.close()

    print('All done, enjoy Conchbot.')
    print("Press any key to close")

else:
    print("You already done this before")
    print("Press any key to close")
