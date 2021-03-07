from Api import Api
import xlwt  # 写excel

# main_singer_list即为要统计的对象
# main_singer_list = ["蔡徐坤", "陈立农", "范丞丞", "黄明昊", "林彦俊", "朱正廷", "王子异", "Lil Ghost小鬼", "尤长靖"]  # 偶
# main_singer_list = ["孟美岐", "吴宣仪", "杨超越", "段奥娟", "Yamy郭颖", "赖美云", "张紫宁", "Sunnee杨芸晴", "李紫婷", "傅菁", "徐梦洁"]  # 炒
# main_singer_list = ["R1SE周震南", "R1SE何洛洛", "R1SE焉栩嘉", "R1SE夏之光", "R1SE姚琛", "R1SE翟潇闻", "R1SE张颜齐", "R1SE刘也", "R1SE任豪", "R1SE赵磊", "R1SE赵让"]  # 壶
# main_singer_list = ["李汶翰", "李振宁", "姚柏南", "管栎", "嘉羿", "胡春杨", "夏瀚宇", "陈宥维", "何昶希"]  # 摇
# main_singer_list = ["THE9", "THE9-刘雨昕", "THE9-虞书欣", "THE9-许佳琪", "THE9-喻言", "THE9-谢可寅", "THE9-安崎", "THE9-赵小棠", "THE9-孔雪儿", "THE9-陆柯燃"]  # 汰
# main_singer_list = ["硬糖少女303", "硬糖少女303希林娜依·高", "硬糖少女303赵粤", "硬糖少女303王艺瑾", "硬糖少女303陈卓璇", "硬糖少女303郑乃馨", "硬糖少女303刘些宁", "硬糖少女303张艺凡"]  # 溏
main_singer_list = ["NINE PERCENT"]
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
        # 仅统计独唱歌曲的收藏数
        singer_list = song['songInfo']['singer']  # 读取歌手信息以判断是否独唱
        if len(singer_list) > 1:  # 非独唱则不统计
            continue
        tot += 1
        songName = song['songInfo']['title']  # 页显歌名
        songId = song['songInfo']['id']  # 获得歌曲ID
        songId = str(songId)  # 以字符串形式传输
        songFanNum = Api.getMusicFavNum(songId)[songId]
        sheet.write(tot, 0, main_singer)
        sheet.write(tot, 1, fanNum)
        sheet.write(tot, 2, songName)
        sheet.write(tot, 3, songFanNum)

# f.save("data/Idol Producer.xls")
f.save("data/temp.xls")



