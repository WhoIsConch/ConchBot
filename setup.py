from logging import error
import os


if not os.path.exists('.env'):
    env = open(".env", "w")

    print("------")    
    print('Welcome to Conchbot setup.')
    print("------")    

    # TOKEN
    print('Your bot\'s token can be obtained from https://discord.com/developers/applications.')
    token = input('Bot token: ')
    env.write(f"TOKEN={token}\n")
    print("------")

    # Reddit ID
    reddit_application_id = input("Your Reddit API id application key: ")
    env.write(f"redditid={reddit_application_id}\n")
    print("------")

    # Reddit Secret
    reddit_application_secret = input("Your Reddit API secret application key: ")
    env.write(f"redditsecret={reddit_application_secret}\n")
    print("------")

    # Reddit Password
    reddit_application_password = input("Your Reddit API password application key: ")
    env.write(f"redditpassword={reddit_application_secret}\n")
    print("You can get PGamerx API by going to this link: https://api-info.pgamerx.com/register.html")

    # PGamerx API Key
    print("------")
    pgamerx_api_key = input("Your PGamerx API id application key: ")
    env.write(f"aiapikey={pgamerx_api_key}\n")
    print("------")

    # Github Repo Link
    print("To get the github repository go to https://github.com and use a existing or create a repository. This is for refresh command. Note: Private repository might not work")
    print("------")
    github_repo_link = input("Your Github Repository Link: ")
    env.write(f"GITHUB_REPO_LINK={github_repo_link}\n")

    # Github Repo Branch
    print("------")
    print("To get the github repository branch go to https://github.com and create or use existing a repository. This is for refresh command. Note: Private repository might not work")
    print("To get branch is where it says branch and a number if you don't see it create file or upload the code to the repo and it should appear and click on it. The default should be `main`")
    print("------")
    github_repo_branch = input("Your Github Repository Name: ")
    env.write(f"GITHUB_REPO_BRANCH={github_repo_branch}\n")
    print("------")

    # Error channel
    print("We need error reporting channel so that means you need to get the id of the channel")
    print("------")
    error_reporting_channel = input("Your error channel id: ")
    env.write(f"ERROR_CHANNEL={error_reporting_channel}\n")
    print("------")

    # Ifunny info

    # Ifunny
    print("We need ifunny info to make these commands work so please input a valid response")
    iFunnyemail = input("Your iFunnyemail: ")
    env.write(f"iFunnyemail={iFunnyemail}\n")

    iFunnypass = input("Your iFunnypass: ")
    env.write(f"iFunnypass={iFunnypass}\n")

    print("If you dont wanna do this please delete the functions - up and down and remove self.up() and self.down()")
    print("If you want please input a valid response")
    print("Create a status by going to https://manage.statuspage.io/")
    print("Status email starts with `component+`")
    status_email = input("Status email: ")
    env.write(f"STATUSEMAIL={status_email}\n")

    print("Your gmail email")
    gmail_email = input("Your gmail email: ")
    env.write(f"EMAIL={gmail_email}\n")

    print("Your gmail password")
    gmail_pass = input("Your gmail password: ")
    env.write(f"EMAIL_PASS={gmail_pass}\n")
    # Close File
    env.close()

    print('All done, enjoy Conchbot.')

else:
    print("You already done this before")
