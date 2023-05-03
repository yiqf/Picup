
import json
import random
from picup import resource_path, config_data


class UserAgent:
    def __init__(self):
        filename = config_data['useragent.filename']
        filepath = f"{resource_path}/{filename}"
        try:
            with open(filepath, encoding='utf-8', mode='rt') as fp:
                self.data = json.loads(fp.read())
                self.data_randomize = list(self.data['randomize'].values())
                self.data_browsers = self.data['browsers']
        except FileNotFoundError:
            print("\nplease download json file from :")
            print("\thttp://fake-useragent.herokuapp.com/browsers/0.1.11")
            print(f"and save as '{filename}'")
            raise FileNotFoundError("Useragent File no found!")

    def __getattr__(self, attr):
        if attr == 'random':
            browser = random.choice(self.data_randomize)
            return random.choice(self.data_browsers[browser])
