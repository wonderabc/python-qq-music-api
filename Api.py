import json
import requests


class Api:
    @staticmethod
    def keywordSearch(keyword, type=''):  # 搜索操作
        url = 'https://c.y.qq.com/soso/fcgi-bin/client_search_cp'
        data = {  # 请求参数
            'new_json': 1,
            'catZhida': 1,
            'w': keyword,
            'format': 'json',
            'inCharset': 'utf8',
            'outCharset': 'utf-8',
            'platform': 'yqq.json',
            'needNewCode': 0,
        }
        if type and type == 'lyric':
            data['t'] = 7
        req = requests.get(url, data).text
        return req

    @staticmethod
    def searchSinger(name):  # 通过歌手姓名获得歌手的歌曲列表（网页版仅能获得前十首）/ 歌手Mid
        # 目前仅返回歌手Mid（歌曲列表通过另一方法获得）
        all_data = json.loads(Api.keywordSearch(name))  # 转换成字典
        song_list = all_data['data']['song']['list']  # 歌曲列表
        song_list = list(song_list)  # 转换成list形式存储
        if len(song_list) > 0:
            singer = song_list[0]  # 获得歌曲对应的歌手信息
        singer = singer['singer']
        singer_Mid = ""
        for s in singer:
            if s['name'] == name:
                singer_Mid = s['mid']
        if singer_Mid == "":
            for singer in song_list:
                singer = singer['singer']
                singer_Mid = ""
                for s in singer:
                    if s['name'] == name:
                        singer_Mid = s['mid']
                if singer_Mid != "":
                    break
        return singer_Mid

    @staticmethod
    def getSingerFanNum(singerMid):  # 获取歌手粉丝数（by Mid）
        url = 'https://u.y.qq.com/cgi-bin/musicu.fcg'
        data = {  # 请求参数
            'data': json.dumps({  # 需要进行json序列化
                'result': {
                    'module': 'Concern.ConcernSystemServer',
                    'method': 'cgi_qry_concern_num',
                    'param': {
                        'vec_userinfo': [{
                            'usertype': 1,
                            'userid': singerMid
                        }],
                        'opertype': 6
                    },
                },
            }),
            'format': 'json',
            'inCharset': 'utf8',
            'outCharset': 'utf-8',
        }
        req = requests.get(url, data).text
        concernNum = json.loads(req)['result']['data']['map_singer_num'][singerMid]['user_fansnum']
        return concernNum

    @staticmethod
    def getMusicFavNum(songId):  # 通过QQ音乐歌曲ID获取歌曲收藏数，返回的是dict，歌曲id对应唯一的收藏数
        songList = list(map(int, songId.split(',')))  # 存储歌曲ID列表
        url = 'https://u.y.qq.com/cgi-bin/musicu.fcg'
        data = {  # 请求参数
            'result': {
                'module': 'music.musicasset.SongFavRead',
                'method': 'GetSongFansNumberById',
                'param': {
                    'v_songId': songList,
                },
            }
        }
        req = requests.post(url, json=data).text
        req = json.loads(req)
        return req['result']['data']['m_numbers']

    @staticmethod
    def getSonglistBysinger(singerMid, page=1, pageSize=100):  # 通过歌手Mid获取该歌手的歌曲列表
        url = 'https://u.y.qq.com/cgi-bin/musicu.fcg'
        data = {  # 请求参数
            'data': json.dumps({  # 需要进行json序列化
                'result': {
                    'module': 'musichall.song_list_server',
                    'method': 'GetSingerSongList',
                    'param': {
                        'singerMid': singerMid,
                        'begin': (page - 1) * pageSize,
                        'num': pageSize,
                        'order': 1,
                    },
                },
            }),
            'format': 'json',
            'inCharset': 'utf8',
            'outCharset': 'utf-8',
        }
        req = requests.get(url, data).text
        req = json.loads(req)
        return req['result']['data']['songList']

    @staticmethod
    def getMusicHitInfo(songMid):  # 通过MID获取歌曲流行指数，流行指数超过阈值才会返回信息
        # 返回的是dict，歌曲Mid对应唯一的流行指数信息（包含流行指数和收听人数等）
        songList = list(songMid.split(','))  # 存储歌曲MID列表
        url = 'https://u.y.qq.com/cgi-bin/musicu.fcg'
        data = {  # 请求参数
            'result': {
                'module': 'music.musicToplist.PlayTopInfoServer',
                'method': 'GetPlayTopData',
                'param': {
                    'songMidList': songList,
                    'requireSongInfo': 0,
                },
            }
        }
        req = requests.post(url, json=data).text
        req = json.loads(req)
        return req['result']['data']['data']


# 000oCQfT3kdonw 黄霄云MID
# 星辰大海MID 002LNOds0rYvpK
print(Api.getMusicHitInfo('002LNOds0rYvpK'))





