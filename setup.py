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

    # Owner id
    print('Your id in discord.')
    userid = input('ID: ')
    env.write(f"ID={userid}\n")
    print("------")

    # Ifunny
    print("We need ifunny info to make these commands work so please input a valid response")
    iFunnyemail = input("Your iFunnyemail: ")
    env.write(f"iFunnyemail={iFunnyemail}\n")

    iFunnypass = input("Your iFunnypass: ")
    env.write(f"iFunnypass={iFunnypass}\n")

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

    env.close()

    print('All done, enjoy Conchbot.')

else:
    print("You already done this before")
