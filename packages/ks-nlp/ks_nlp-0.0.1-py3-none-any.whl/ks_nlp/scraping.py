import twint
import os

def scrape_tweets(class_name: str, query=None, username=None, limit=100):
    if " " in class_name:
        print("Class names can't contains spaces")
        return

    if query is None and username is None:
        print("You must specify a query and/or an username")
        return

    # Configure
    c = twint.Config()

    if username is not None:
        c.Username = username

    if query is not None:
        c.Search = query

    c.Limit = limit
    print("Limit: ", limit)
    c.Output = "tmp.txt"

    # Run
    twint.run.Search(c)

    os.makedirs(class_name, exist_ok=True)

    nb_files = len([name for name in os.listdir(class_name) if os.path.isfile(os.path.join(class_name, name))])

    i = nb_files
    print(i)
    with open("tmp.txt", "r") as f:
        lines = f.readlines()
        for l in lines:
            # get tweet content
            idx = l.find(">")
            tweet = l[idx+2:-1]
            with open(os.path.join(class_name, str(i).zfill(6)+".txt"), "w") as t:
                t.write(tweet)
            i+=1

    os.remove("tmp.txt")



