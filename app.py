import cherrypy
from vaderSentiment import SentimentIntensityAnalyzer
import os
import sys
def sent(comment,status):
	analyzer = SentimentIntensityAnalyzer()
	if(comment==''):
		return 'sample_value'

	#initializations
	flag=''
	val=0

	#values range from -1 to 1
	p_threshold=0.350
	n_threshold=-0.150

	result=analyzer.polarity_scores(comment)

	val=result['compound']
	print("result= ")
	print(result)

	if(val>=p_threshold):
		flag='Green'
	elif(val<=n_threshold):
		flag='Red'
	elif(val<p_threshold and val>n_threshold):
		flag='Amber'

	if(flag==status):
		return 'done'
	else:
		return 'close'

class analyzer:
	def index(self):
		def_status="select_stat"
		def_color="grey lighten-1"
		def_comment=""
		def_flag=""
		fx=open("UI2.html","r")
		webform = fx.read()%(def_status,def_status,def_status,def_comment,def_color,def_flag,def_comment,def_color,def_flag,def_comment,def_color,def_flag)
		return webform
	index.exposed=True

	def DoAnalyze(self,comment1=None,comment2=None,comment3=None,status1=None,status2=None,status3=None):
		comment1=str(comment1)
		comment2=str(comment2)
		comment3=str(comment3)

		if(status1==None):
			status1="select_stat"
		if(status2==None):
			status2="select_stat"
		if(status3==None):
			status3="select_stat"

		status1=str(status1)
		status2=str(status2)
		status3=str(status3)

		flag1=sent(comment1,status1)
		flag2=sent(comment2,status2)
		flag3=sent(comment3,status3)



		fx_result = open("UI2.html","r")
		if(flag1=='close'):
			color1='red'
		elif(flag1=='done'):
			color1='green'
		else:
			color1='grey lighten-1'

		if(flag2=='close'):
			color2='red'
		elif(flag2=='done'):
			color2='green'
		else:
			color2='grey lighten-1'

		if(flag3=='close'):
			color3='red'
		elif(flag3=='done'):
			color3='green'
		else:
			color3='grey lighten-1'

		webform_result=fx_result.read()%(status1,status2,status3,comment1,color1,flag1,comment2,color2,flag2,comment3,color3,flag3)
		return webform_result
	DoAnalyze.exposed=True

#To run locally
#cherrypy.quickstart(analyzer())

#To run on a server
wsgi_app = cherrypy.Application(analyzer(), '/')

if __name__ == '__main__':
	from wsgiref.simple_server import make_server
	httpd = make_server('', 6600, wsgi_app)
	httpd.serve_forever()
