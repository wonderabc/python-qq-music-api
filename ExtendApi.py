# 实现一些扩展功能，基于多线程优化效率
# 1. 通过歌手姓名（与QQ音乐显示的完全一致）返回接口第一页（maximum 100首）收藏数前k的歌曲信息
# 2. 通过歌名获得最相关的十首歌曲的收藏信息
import json
import time
from threading import current_thread
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, as_completed, wait
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
    def GetTopkFavbyName(k, singername):  # 通过歌手姓名（与QQ音乐显示的完全一致）返回接口第一页（maximum 100首）收藏数前k的歌曲信息
        """
        :param k: 返回收藏数前k的歌曲信息
        :param singername: 歌手名
        :return: songInfoList: 歌曲信息列表
        """
        Mid = Api.searchSinger(singername)  # 获得歌手MID
        songList = Api.getSonglistBysinger(Mid)
        songInfoList = []
        pool = ThreadPoolExecutor(max_workers=64)  # 线程池
        obj_list = []  # 存储线程
        songIDInfo = ""
        for song in songList:
            songID = str(song['songInfo']['id'])
            songIDInfo += songID + ","
            # 多线程
            # 提高效率关键部分
            # obj = pool.submit(Api.getMusicFavNum, songID)
            # obj_list.append(obj)

            # FavNum = Api.getMusicFavNum(songID)  # 单线程
        songIDInfo = songIDInfo[:-1]
        FavNumList = Api.getMusicFavNum(songIDInfo)
        # wait(obj_list, timeout=None)  # 全部执行完毕
        for song in songList:
            # index = songList.index(song)  # 根据index取运行结果
            songID = str(song['songInfo']['id'])
            songName = song['songInfo']['title']  # 页显歌名
            singerInfo = ExtendApi.GetSingerList(song['songInfo']['singer'])  # 歌手名列表，用中文分号分隔
            # FavNum = obj_list[index].result()  # 根据index取运行结果
            FavNum = FavNumList[songID]
            songInfo = {'songName': songName, 'singerInfo': singerInfo, 'FavNum': int(FavNum)}  # 存储歌曲信息
            songInfoList.append(songInfo)
        songInfoList = sorted(songInfoList, key=itemgetter('FavNum'), reverse=True)  # reverse=True表示降序
        songInfoList = songInfoList[:k]
        # pool.shutdown(wait=True)
        return songInfoList

    @staticmethod
    def GetRelasongFavInfo(songName):  # 通过歌名获得最相关的十首歌曲的收藏信息
        result = Api.keywordSearch(songName, type='lyric')
        songList = list(json.loads(result)['data']['lyric']['list'])
        songInfoList = []
        pool = ThreadPoolExecutor(max_workers=8)  # 线程池
        obj_list = []  # 存储线程
        songIDInfo = ""
        for song in songList:
            songID = str(song['id'])
            songIDInfo += songID + ","
            # 多线程
            # 提高效率关键部分
            # obj = pool.submit(Api.getMusicFavNum, songID)
            # obj_list.append(obj)
            # FavNum = Api.getMusicFavNum(songID)  # 单线程
        songIDInfo = songIDInfo[:-1]
        FavNumList = Api.getMusicFavNum(songIDInfo)
        # wait(obj_list, timeout=None)  # 全部执行完毕
        for song in songList:
            # index = songList.index(song)  # 根据index取运行结果
            songID = str(song['id'])
            songName = song['title']
            singerInfo = ExtendApi.GetSingerList(song['singer'])
            # FavNum = obj_list[index].result()  # 根据index取运行结果
            FavNum = FavNumList[songID]
            songInfo = {'songName': songName, 'singerInfo': singerInfo, 'FavNum': int(FavNum)}
            songInfoList.append(songInfo)
        return songInfoList


if __name__ == "__main__":
    begin = time.time()
    print(ExtendApi.GetTopkFavbyName(10, "容祖儿"))
    times = time.time() - begin
    print("运行时间是：", times)
    begin = time.time()
    print(ExtendApi.GetRelasongFavInfo("告白气球"))
    times = time.time() - begin
    print("运行时间是：", times)
