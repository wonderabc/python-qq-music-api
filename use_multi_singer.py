from Api import Api
import xlwt  # 写excel
# 包含多人歌曲

main_singer_list = ["xxx"]  # xxx为歌手姓名
f = xlwt.Workbook()
for main_singer in main_singer_list:
    sheet = f.add_sheet(main_singer, cell_overwrite_ok=True)  # 一个表格存储一个歌手
    row0 = ['singer', 'FanNum', 'SongName', 'Song_Fans_Num']
    for i in range(0, len(row0)):  # 生成第一行
        sheet.write(0, i, row0[i])
    tot = 0  # 正在存储表格的第几行
    Mid = Api.searchSinger(main_singer)  # 歌手Mid
    print(main_singer, Mid)
    fanNum = Api.getSingerFanNum(Mid)  # 歌手粉丝数
    Songlist = Api.getSonglistBysinger(Mid, pageSize=100)  # 歌曲列表
    for song in Songlist:
        tot += 1
        songName = song['songInfo']['title']  # 页显歌名
        songId = song['songInfo']['id']  # 获得歌曲ID
        songId = str(songId)  # 以字符串形式传输
        songFanNum = Api.getMusicFavNum(songId)[songId]
        sheet.write(tot, 0, main_singer)
        sheet.write(tot, 1, fanNum)
        sheet.write(tot, 2, songName)
        sheet.write(tot, 3, songFanNum)

f.save("data/temp_multi_singer.xls")



