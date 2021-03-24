from ExtendApi import ExtendApi
import xlwt  # 写excel
# 包含多人歌曲

main_singer_list = ["G.E.M. 邓紫棋"]  # xxx为歌手姓名
f = xlwt.Workbook()
for main_singer in main_singer_list:
    sheet = f.add_sheet(main_singer, cell_overwrite_ok=True)  # 一个表格存储一个歌手
    row0 = ['歌名', '歌手信息', '专辑信息', '收藏数']
    for i in range(0, len(row0)):  # 生成第一行
        sheet.write(0, i, row0[i])
    tot = 0  # 正在存储表格的第几行
    songInfoList = ExtendApi.GetTopkFavbyName(100, main_singer)
    for song in songInfoList:
        tot += 1
        songName = song['songName']
        singerInfo = song['singerInfo']
        albumInfo = song['albumInfo']
        FavNum = song['FavNum']
        sheet.write(tot, 0, songName)
        sheet.write(tot, 1, singerInfo)
        sheet.write(tot, 2, albumInfo)
        sheet.write(tot, 3, FavNum)

f.save("data/temp_multi_singer.xls")



