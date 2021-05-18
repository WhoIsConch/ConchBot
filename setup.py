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

    # Github Repo Link
    print("To get the github repository go to https://github.com and create a repository. This is for refresh command. Note: Private repository might not work")
    github_repo_link = input("Your Github Repository Link: ")
    env.write(f"GITHUB_REPO_LINK={github_repo_link}")

    # Close File
    env.close()

    print('All done, enjoy Conchbot.')

else:
    print("You already done this before")
