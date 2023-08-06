from types import SimpleNamespace as Namespace
import requests
import json

class BosslikeExecutors:
	def __init__ (self, key):
		self.headers = {
				'X-Api-Key': key,
				'accept': 'application/json'
			}

		self.url = 'https://api-public.bosslike.ru'

		self.urlbots = '/v1/bots/'

		self.usersme = f'{self.urlbots}users/me/'

	def appheaders (self, headers):
		if isinstance(headers, dict):
			self.headers.update(headers)
		else:
			return {"error": " headersapp - " + "'" + headers + "' "}

	def users_me (self):
		res = requests.get(self.url+self.usersme, headers=self.headers)
		x = json.loads(res.text, object_hook=lambda d: Namespace(**d))
		return x


	def socials (self):
		res = requests.get(self.url+self.usersme+'socials/', headers=self.headers)
		x = json.loads(res.text, object_hook=lambda d: Namespace(**d))
		return x

	def delete_social (self, type):
		res = requests.delete(self.url+self.usersme+'social/', params={'type': type}, headers=self.headers)
		x = json.loads(res.text, object_hook=lambda d: Namespace(**d))
		return x

	def check_profile (self, url, type):
		res = requests.post(self.url+self.usersme+'social/auth/like/check-profile/', data={'url': url,'type': type}, headers=self.headers)
		x = json.loads(res.text, object_hook=lambda d: Namespace(**d))
		return x

	def show_like (self, token):
		res = requests.get(self.url+self.usersme+'social/auth/like/show-like/', params={'token': token}, headers=self.headers)
		x = json.loads(res.text, object_hook=lambda d: Namespace(**d))
		return x

	def check_like (self, token):
		res = requests.get(self.url+self.usersme+'social/auth/like/check-like/', params={'token': token}, headers=self.headers)
		x = json.loads(res.text, object_hook=lambda d: Namespace(**d))
		return x

	def bost_tasks (self, serviceType, taskType, jsons = False, i = 0):
		res = requests.get(self.url+self.urlbots+'tasks/', params={'service_type': serviceType, 'task_type': taskType}, headers=self.headers)
		x = json.loads(res.text, object_hook=lambda d: Namespace(**d))
		if jsons == False:
			return x
		elif jsons == True:
			if i != True:
				return x.data.items[i].id
			elif i == True:
				arr = []
				for key in x.data.items:
					arr.append(key.id)
				return arr
		else:
			return x

	def task_do (self, id, url = False, point = False):
		res = requests.get(self.url+"/v1/bots/tasks/"+id+"/do/", params={'id': id}, headers=self.headers)
		x = json.loads(res.text, object_hook=lambda d: Namespace(**d))
		if url == False and point == False:
			return x
		elif url == True and point == False:
			return x.data.url
		elif point == True and url == False:
			return x.data.user_price
		elif url == True and point == True:
			data = '{"url": "'+x.data.url+'", "point": "'+x.data.user_price+'"}'
			x = json.loads(str(data), object_hook=lambda d: Namespace(**d))
			return x

	def task_check (self, id):
		res = requests.get(self.url+"/v1/bots/tasks/"+id+"/check/", params={'id': id}, headers=self.headers)
		x = json.loads(res.text, object_hook=lambda d: Namespace(**d))
		return x