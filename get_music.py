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
		print('（输入"N"=下一页，直接Enter返回上层！）')
		download_num = input('--> ')

		if not download_num:
			print('输入有误，正在返回首层！\n')
			time.sleep(3)
			os.system('cls')
			return 0, 0
		elif download_num == 'N' or download_num == 'n':
			page_num += 1
			continue
		try:
			download_num = int(download_num)
			if download_num <= len(mid) and download_num > 0:
				print('\n您要下载的是 {} 演唱的 《{}》 ！\n'.format(
					songs_name[download_num - 1][1], songs_name[download_num - 1][0]))
				msg = '《{}》- {}'.format(songs_name[download_num - 1][0],
					songs_name[download_num - 1][1])
				return mid[download_num - 1], msg
			else:
				raise
		except:
			print('输入有误，返回首层！\n')
			time.sleep(3)
			os.system('cls')
			return 0, 0
	print('--> 请输入下载歌曲的编号（直接Enter退出）：')
	download_num = input('--> ')
	try:
		download_num = int(download_num)
		if download_num <= len(mid) and download_num > 0:
			print('\n您要下载的是 {} 演唱的 《{}》 ！\n'.format(
				songs_name[download_num - 1][1], songs_name[download_num - 1][0]))
			msg = '《{}》- {}'.format(songs_name[download_num - 1][0],
					songs_name[download_num - 1][1])
			return mid[download_num - 1], msg
		else:
			raise
	except:
		print('\n输入有误，正在返回首层！\n')
		time.sleep(3)
		os.system('cls')
		return 0, 0

# 判断下载格式：
def judge_songtype(api_url, songmid_list, vkey, guid):
	print('\n******* 请稍后，正在获取歌曲可支持的下载格式 *******\n')
	count = 0
	download_url_list = []
	judge_name = []
	for i in range(5):
		download_url = api_url.format(songmid_list[i], vkey, guid)
		judge_get = requests.head(download_url).status_code
		if judge_get == 200:
			judge_name.append(i)
			count += 1
			download_url_list.append(download_url)
			if i == 0:
				print('- ' + str(count) + '：m4a格式（96Kbps）\n')
			elif i == 1:
				print('- ' + str(count) + '：mp3格式（128Kbps）\n')
			elif i == 2:
				print('- ' + str(count) + '：mp3格式（320Kbps）\n')
			elif i == 3:
				print('- ' + str(count) + '：ape格式（无损音质）\n')
			elif i == 4:
				print('- ' + str(count) + '：flac格式（无损音质）\n')
	if len(download_url_list) == 0:
		print('****** 对不起，此歌曲不支持下载 ******\n')
		return 0, 0
	
	while True:
		download_url = input(('****** 请输入您要下载的歌曲格式编号，默认为flac！******\n--> '))
		try:
			if download_url:
				if int(download_url) > len(download_url_list):
					print('\n您的输入有误，正在返回首层！\n')
					return 0, 0
		except:
			print('\n您的输入有误，请重新输入!\n')
			continue
		break

	if not download_url or int(download_url) == 5:
		download_url = download_url_list[4]
		return download_url, judge_name[4]
	elif int(download_url) == 4:
		download_url = download_url_list[3]
		return download_url, judge_name[3]
	elif int(download_url) == 3:
		download_url = download_url_list[2]
		return download_url, judge_name[2]
	elif int(download_url) == 2:
		download_url = download_url_list[1]
		return download_url, judge_name[1]
	elif int(download_url) == 1:
		download_url = download_url_list[0]
		return download_url, judge_name[0]
	else:
		print('\n您的输入有误，正在返回首层！\n')
		return 0, 0

# 下载音乐
def download_music(songs_id, msg, headers):
	api = (
		'https://c.y.qq.com/base/fcgi-bin/fcg_music_express_mobile3.fcg',
		'http://dl.stream.qqmusic.qq.com/{}?fromtag=64&vkey={}&guid={}&fromtag=1'
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
	try:
		vkey = re_judge.findall(content)[0].split('"')[3]
	except:
		print(' ----------------------------------------------------')
		print(' 此歌曲或许由于版权原因无法下载，如有疑问请联系作者！')
		print(' ----------------------------------------------------\n')
		time.sleep(5)
		os.system('cls')
		return

	songmid_list = [filename,
					'M500' + songmid + '.mp3',
					'M800' + songmid + '.mp3',
					'A000' + songmid + '.ape',
					'F000' + songmid + '.flac']

	download_url, judge_name = judge_songtype(api[1], songmid_list, vkey, guid)
	if download_url == 0:
		time.sleep(3)
		os.system('cls')
		return

	print('\n****** 正在下载，请稍后... ******')

	# 建立下载地址
	music_dlurl = download_url
	response = requests.get(music_dlurl)

	if not os.path.exists('Music'):
		os.mkdir('Music')

	# 下载音乐
	if judge_name == 0:
		filetype = 'Music/{}.m4a'
	elif judge_name == 1:
		filetype = 'Music/{}.mp3'
	elif judge_name == 2:
		filetype = 'Music/{}.mp3'
	elif judge_name == 3:
		filetype = 'Music/{}.ape'
	elif judge_name == 4:
		filetype = 'Music/{}.flac'


	with open(filetype.format(msg), 'wb') as music:
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
	print('************ 再次重申，此程序仅供程序交流************')
	print('********** 如有问题或疑问请在项目网址中留言！**********\n\n')
	print(' ----------------------------------------------------------')
	print('  GitHub网址：https://github.com/arvinqiu/download_qqmusic')
	print(' ----------------------------------------------------------')
	time.sleep(3)