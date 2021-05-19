from logging import error
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
    print("To get the github repository go to https://github.com and use a existing or create a repository. This is for refresh command. Note: Private repository might not work")
    github_repo_link = input("Your Github Repository Link: ")
    env.write(f"GITHUB_REPO_LINK={github_repo_link}\n")

    # Github Repo Branch
    print("To get the github repository branch go to https://github.com and create or use existing a repository. This is for refresh command. Note: Private repository might not work")
    print("To get branch is where it says branch and a number if you don't see it create file or upload the code to the repo and it should appear and click on it. The default should be `main`")
    github_repo_branch = input("Your Github Repository Name: ")
    env.write(f"GITHUB_REPO_BRANCH={github_repo_branch}\n")

    print("We need error reporting channel so that means you need to get the id of the channel")
    error_reporting_channel = input("Your error channel id: ")
    env.write(f"ERROR_CHANNEL={error_reporting_channel}")


    # Close File
    env.close()

    print('All done, enjoy Conchbot.')

else:
    print("You already done this before")
