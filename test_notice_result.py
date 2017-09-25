import requests
import json
import random as rd


# # Notice game result to ROCKET CHAT
# game_result = {
# 	"username": "thuongtran",
# 	"message": "*You have new game result notification*\n```Total point in this week: 20```\n[More Detail](http://dounets.com:5003/notice-game-result)"
# }
# game_result = json.dumps(game_result)
# headers = {"Content-Type": "application/json"}
# requests.post("http://dounets.com:5002/rocketchat/notify-game-results", headers=headers, data=game_result)


# # Notice hole result to ROCKET CHAT
# hole_result = {
# 	"username": "thuongtran",
# 	"message": "*You have new hole result notification*\n```Par: 3\nPoint: 3\nTime: Monday```\n[More Detail](http://dounets.com:5003/notice-hole-result)"
# }
# hole_result = json.dumps(hole_result)
# headers = {"Content-Type": "application/json"}
# requests.post("http://dounets.com:5002/rocketchat/notify-game-results", headers=headers, data=hole_result)


# # Notice game result to GAMIFICATION UI
# game_result = {
#   "notificationLs": {
#   "url": "/notice-game-result",
#   "content": "You have new game results notification",
#   "username": "ThuongTran"
#   }
# }
# game_result = json.dumps(game_result)
# headers = {"Content-Type": "application/json"}
# requests.post("http://dounets.com:5003/api/socketApi", headers=headers, data=game_result)


# # Notice hole result to GAMIFICATION UI
# hole_result = {
#   "notificationLs": {
#   "url": "/notice-hole-result",
#   "content": "You have new hole results notification",
#   "username": "ThuongTran"
#   }
# }
# hole_result = json.dumps(hole_result)
# headers = {"Content-Type": "application/json"}
# requests.post("http://dounets.com:5003/api/socketApi", headers=headers, data=hole_result)

### ===================================================================================== ###

# Notice Image to RocketChat
image = {
  "well_done": "https://thumbs.dreamstime.com/b/well-done-23443783.jpg",
  "supper": "https://cdn.schoolstickers.com/products/en/819/128740-05.png",
  "great_job": "https://sites.create-cdn.net/siteimages/37/9/9/379961/12/9/0/12909934/450x430.jpg?1469478215",
  "great_effort": "https://www.thenaughtyseat.co.uk/ekmps/shops/rescapeltd/images/great-effort-well-done-stickers-2155-p.png",
  "fighting": "http://bec.edu.vn/rezise/resize?src=http://bec.edu.vn/asset/upload/bai_hoc/han_quoc/150416_success_kid_10.jpg&w=760&h=400",
  "excellent": "https://cdn.schoolstickers.com/products/en/819/128740-08.png",
  "do_your_best": "http://www.swiss-miss.com/wp-content/uploads/2012/09/Screen-Shot-2012-09-10-at-10.28.44-PM-480x191.png",
  "co_len_tieng_han": "http://trungtamtienghan.edu.vn/uploads/news/2017_02/co-len-tieng-han-phien-am.jpg",
  "work_hard_play_hard": "https://cdn-media-1.lifehack.org/wp-content/files/2017/04/18232920/work-hard-play-hard.001-370x208@2x.jpeg",
  "you_can_do_it": "http://khmer-online.com/wp-content/uploads/2016/09/you-can-do-it.png"
}

image_url = list(image.values())[rd.randint(0, 9)]

notice = {
    "roomId": "thuongtran",
    "text": "Today game result",
    "alias": "Boss",
    "emoji": ":smirk:",
    "avatar": "https://i.pinimg.com/originals/d7/b1/8c/d7b18cfeb93cac2ea7f75f8951f240f1.gif",
    "attachments": [{
        "color": "#ff0000",
				"author_icon": "https://i.pinimg.com/originals/d7/b1/8c/d7b18cfeb93cac2ea7f75f8951f240f1.gif",
				"author_name": "",
				"author_link": "",
				"ts": "",
				"title": "Game Result Notification",
				"title_link": "https://dounets.com:5003",
				"title_link_download": "",
        "text": "",
        "thumb_url": "",
        "message_link": "https://google.com",
        "collapsed": False,
        "image_url": image_url,
        "audio_url": "",
        "video_url": "",
        "fields": [{
            "short": True,
            "title": "Hole result",
            "value": "[Link](http://dounets.com:5003/golfgame-api/notice-hole-result) go to hole results."
        },{
            "short": True,
            "title": "Game result",
            "value": "[Link](http://dounets.com:5003/golfgame-api/notice-game-result) go to game results."
        }]
    }]
}

notice = json.dumps(notice)
headers = {"Content-Type": "application/json"}
requests.post("http://dounets.com:5002/rocketchat/notify-game-results", headers=headers, data=notice)