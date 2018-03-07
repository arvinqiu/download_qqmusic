# -*- coding:utf-8 -*-


import requests
import re
import random
import time
import os
import json


# 获取音乐搜索结果
def search_music(music_name, headers):
	song_num = 0
	mid = []
	songs_name = []
	page_num = 1
	print('\n************ 歌曲搜索结果如下：************\n')
	while True:
		search_url = ('https://c.y.qq.com/soso/fcgi-bin/client_search_cp?new_json' +
		'=1&aggr=1&cr=1&catZhida=1&p={}&n=10&w='.format(page_num) + music_name + '&format=jsonp')
		response = requests.get(search_url, headers=headers)
		content = response.text[9:-1]
		content_json = json.loads(content)
		songs_list = content_json['data']['song']['list']
		if len(songs_list) == 0:
			print("已经是最后一页了！(●'◡'●)\n")
			break

		for message in songs_list:
			if not message['name']:
				print("已经是最后一页了！(●'◡'●)\n")
				break
			song_num += 1
			print(str(song_num) + '. ', end='')
			print('《' + message['name'] + "》")
			print('歌手：' + message['singer'][0]['name'])
			print('专辑：' + message['album']['name'] + '\n')
			songs_name.append([message['name'], message['singer'][0]['name']])
			mid.append(message['mid'])
		print('--> 请输入下载歌曲的编号：')
		print('（输入"N"=下一页，直接Enter退出！）')
		download_num = input('--> ')

		if not download_num:
			print('返回首层！\n')
			return 0, 0
		elif download_num == 'N' or download_num == 'n':
			page_num += 1
			continue
		try:
			download_num = int(download_num)
			if download_num <= len(mid) and download_num > 0:
				print('\n您要下载的是 {} 演唱的《{}》！\n'.format(
					songs_name[download_num - 1][1], songs_name[download_num - 1][0]))
				msg = '《{}》- {}'.format(songs_name[download_num - 1][0],
					songs_name[download_num - 1][1])
				return mid[download_num - 1], msg
			else:
				raise
		except:
			print('输入有误，返回首层！\n')
			return 0, 0
	print('--> 请输入下载歌曲的编号（直接Enter退出）：')
	download_num = input('--> ')
	try:
		download_num = int(download_num)
		if download_num <= len(mid) and download_num > 0:
			print('\n您要下载的是 {} 演唱的《{}》！\n'.format(
				songs_name[download_num - 1][1], songs_name[download_num - 1][0]))
			msg = '《{}》- {}'.format(songs_name[download_num - 1][0],
					songs_name[download_num - 1][1])
			return mid[download_num - 1], msg
		else:
			raise
	except:
		print('输入有误，返回首层！\n')
		return 0, 0

# 下载音乐
def download_music(songs_id, msg, headers):
	print('****** 正在下载，请稍后... ******')
	api = (
		'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg',
		'http://dl.stream.qqmusic.qq.com/{}?vkey={}&guid={}&uin=0&fromtag=66'
		)
	music_url = 'https://y.qq.com/n/yqq/song/{}.html'.format(songs_id)

	# 获取songmid和filename的值
	response = requests.get(music_url, headers=headers)
	content = response.text
	re_judge = re.compile(r'"songmid":"\S+?"')
	songmid = re_judge.findall(content)[0].split('"')[3]
	filename = 'C400' + songmid + '.m4a'

	# 计算guid的值
	get_time = time.time()
	getUTCMilliseconds = int((get_time - int(get_time)) * 1000)
	guid = int(random.random() * 2147483647) * getUTCMilliseconds % 10000000000

	# 设置get参数
	params = {
	        'format': 'json',
	        'cid': 205361747,
	        'uin': 0,
	        'songmid': songmid,
	        'filename': filename,
	        'guid': guid
	    	}

	# 获取vkey的值
	response = requests.get(api[0], params=params)
	content = response.text
	re_judge = re.compile(r'"vkey":"\S+?"')
	vkey = re_judge.findall(content)[0].split('"')[3]

	# 建立下载地址
	music_dlurl = api[1].format(filename, vkey, guid)
	response = requests.get(music_dlurl)

	if not os.path.exists('Music'):
		os.mkdir('Music')

	# 下载音乐
	with open('Music/{}.m4a'.format(msg), 'wb') as music:
		music.write(response.content)
	print('********** 下载完成！**********\n')
	print('已下载歌曲 ' + msg + ' 至Music文件夹中')
	time.sleep(3)
	os.system('cls')

# 获取网页连接信息
def get_music_msg(music_url):
	response = requests.get(music_url)
	content = response.text
	re_judge = re.compile(r'title>[\s\S]+?<')
	song_name = re_judge.findall(content)[0].split('-')[0][6:-1]
	song_name = song_name.split('&')
	song_name = '《' + song_name[0] + '》' + '- ' + song_name[1].split(';')[1]
	return song_name

# 主程序
def main():
	# 头文件
	headers = {'User-Agent':
	'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like ' + 
	'Gecko) Chrome/63.0.3239.132 Safari/537.36'}

	while True:
		print('************ 此程序仅供学习交流，切勿用作商业用途！************\n\n')
		music_name = input(('--> 请输入您要下载的歌曲名或QQ音乐上该歌曲的网址' +
			'（直接Enter退出）：\n--> 网址格式如：https://y.qq.com/n/yqq/song/XXXXXXX.html\n--> '))
		re_url = re.compile(r'//y.qq.com/n/yqq/song/[a-zA-Z0-9]+?\.html')
		if not music_name:
			return
		elif re_url.search(music_name):
			print('')
			re_url = re.compile(r'song/[a-zA-Z0-9]+?\.')
			songs_msg = re_url.findall(music_name)[0][5:-1]
			music_msg =  get_music_msg(music_name)
			download_music(songs_msg, music_msg, headers)
			continue
		elif '.com' in music_name:
			print('\n网址格式不正确，请重新输入！\n')
			continue

		songs_msg, msg = search_music(music_name, headers)
		if songs_msg == 0:
			continue
		else:
			download_music(songs_msg, msg, headers)


if __name__ == '__main__':
	main()