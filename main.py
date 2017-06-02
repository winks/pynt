import requests
import sys
import qtx

POSTS_URL = "{}/posts.json"
USER_URL = "{}/user.json"
AVATAR_URL = "{}/user.jpg"

class Pynt(object):
  host = {}
  _req = {}
  users = {}

  def __init__(self, host):
    host["url"] = "{}://{}".format(host["protocol"], host["hostname"])
    print("Target: {}".format(host["url"]))
    self.host = host

  def read_posts(self):
    self.host["posts_url"] = "{}".format(POSTS_URL.format(self.host["url"]))
    print("Accessing {}".format(self.host["posts_url"]))
    self._req["posts"] = requests.get(self.host["posts_url"])
    print("Status: {}".format(self._req["posts"].status_code))
    self.posts = self._req["posts"].json()
    return self.posts

  def read_avatar(self):
    self.host["avatar_url"] = "{}".format(AVATAR_URL.format(self.host["url"]))
    print("Accessing {}".format(self.host["avatar_url"]))
    self._req["avatar"] = requests.get(self.host["avatar_url"])
    print("Status: {}".format(self._req["avatar"].status_code))
    #return self._req["avatar"].raw
    filename = "./assets/{}_user.jpg".format(self.host["hostname"])
    with open(filename, 'wb') as fd:
      for chunk in self._req["avatar"].iter_content(128):
        fd.write(chunk)
    self.avatar = filename
    return self.avatar

  def read_user(self):
    self.host["user_url"] = "{}".format(USER_URL.format(self.host["url"]))
    print("Accessing {}".format(self.host["user_url"]))
    self._req["user"] = requests.get(self.host["user_url"])
    print("Status: {}".format(self._req["user"].status_code))
    payload = self._req["user"].json()
    self.users[payload["domain"]] = payload
    return self.users

  def show_posts(self, posts, num=3):
    counter = 0
    for post in posts:
      if counter > num-1:
        continue
      print('{} - {}'.format(post["url"], post["edited_at"]))
      if len(post["tags"]) > 0:
        for tag in post["tags"]:
          print("  #{}".format(tag)),
      print("")
      counter += 1

  def show_users(self, users):
    for _, user in list(users.items()):
      print('User: {} @ {}'.format(user["display_name"], user["domain"]))


if __name__ == "__main__":
  print("hi")
  DEBUG = True
  if len(sys.argv) > 1:
    host = {}
    host["hostname"] = sys.argv[1]
    host["protocol"] = "http"
    if len(sys.argv) > 2 and sys.argv[2] == "-d":
      DEBUG = True
    elif len(sys.argv) > 2 and sys.argv[2] == "-s":
      host["protocol"] = "https"

    pynt = Pynt(host)
    #avatar_file = pynt.read_avatar()
    if not DEBUG:
      user = pynt.read_user()
      pynt.show_users(user)
      posts = pynt.read_posts()
      print('Posts:', len(posts))
      pynt.show_posts(posts)
      #print(posts)
    else:
      post = {
        'url': "http://example.org/foo",
        'edited_at': "2014-09-23 12:34:56",
        'guid': "example.org/foo",
        'body_html': "<h1>hello</h1><h1>hello</h1><h1>hello</h1><h1>hello</h1> world, <b>bold</b>",
      }

      posts = [
        post,
        post,
        post,
        post
      ]
      user = {
        'display_name': 'Charlie Root'
      }
      pynt.users[post['guid'].split('/')[0]] = user

    gui = qtx.PyntGui(pynt)
    gui.addStuff(posts[0:3])
    sys.exit(gui.run())

  else:
    print("Usage: {} HOSTNAME".format(sys.argv[0]))
