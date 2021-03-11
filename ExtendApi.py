# 实现一些扩展功能
# 1. 返回接口第一页（maximum 100首）收藏数前10的歌曲信息
from operator import itemgetter
from Api import Api


class ExtendApi:

    @staticmethod
    def GetSingerList(singerinfo):  # 获取歌手名列表，用中文分号分隔
        """
        :param singerinfo: 歌手信息list
        :return: singerInfo: 歌手名列表，用中文分号分隔
        """
        singerList = []
        for singer in singerinfo:
            singerList.append(singer['name'])
        singerInfo = "；".join(singerList)
        return singerInfo



    @staticmethod
    def GetTopkFavbyName(k, singername):  # 返回接口第一页（maximum 100首）收藏数前k的歌曲信息
        """
        :param k: 返回收藏数前k的歌曲信息
        :param singername: 歌手名
        :return: songInfoList: 歌曲信息列表
        """
        Mid = Api.searchSinger(singername)  # 获得歌手MID
        songList = Api.getSonglistBysinger(Mid)
        songInfoList = []
        for song in songList:
            songMid = song['songInfo']['mid']
            songID = str(song['songInfo']['id'])
            songName = song['songInfo']['title']  # 页显歌名
            FavNum = Api.getMusicFavNum(songID)[songID]  # 获取歌曲收藏数
            singerInfo = ExtendApi.GetSingerList(song['songInfo']['singer'])  # 歌手名列表，用中文分号分隔
            songInfo = {'songName': songName, 'singerInfo': singerInfo, 'FavNum': FavNum}  # 存储歌曲信息
            songInfoList.append(songInfo)
        sorted(songInfoList, key=itemgetter('FavNum'))
        songInfoList = songInfoList[:k]
        return songInfoList


