import cherrypy
from vaderSentiment import SentimentIntensityAnalyzer
import sys
webform = """
<!DOCTYPE html>
<html lang="en">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=UTF-8"/>
	<meta name="viewport" content="width=device-width, initial-scale=1, maximum-scale=1.0, user-scalable=no"/>
	<title>Status Assessment</title>

	<!-- CSS  -->
	<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
	<link href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.99.0/css/materialize.min.css" type="text/css" rel="stylesheet" media="screen,projection"/>

	<!--  Scripts-->
	<script	src="https://code.jquery.com/jquery-3.1.1.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.99.0/js/materialize.min.js"></script>

	<script type="text/javascript">
		$(document).ready(function() {
			$('select').material_select();
			$("#status1").val($("#var1").html()).trigger("change");
			$("#status2").val($("#var2").html()).trigger("change");
			$("#status3").val($("#var3").html()).trigger("change");
			document.getElementById('var1').style.display = 'none';
			document.getElementById('var2').style.display = 'none';
			document.getElementById('var3').style.display = 'none';

		});

	</script>
</head>
<body>
	<span id="var1">%s</span>
	<span id="var2">%s</span>
	<span id="var3">%s</span>

	<nav class="teal lighten-1" role="navigation">
		<div class="nav-wrapper container">
			<a id="logo-container" href="#" class="brand-logo white-text">Status Assessment</a>
			<ul class="right hide-on-med-and-down">
			</ul>

			<ul id="nav-mobile" class="side-nav grey darken-3">
			</ul>
			<a href="#" data-activates="nav-mobile" class="button-collapse white-text"><i class="material-icons">menu</i></a>
		</div>
	</nav>

	<div class="container section">
		<div class="row">
			<br>
			<form class="col s12" action = "DoAnalyze" method = post id="form" onsubmit="">
				<!-- comment-1 -->
				<div class="row">
					<div class="input-field col s2">
						<select id="status1" name="status1" class="browser-default">
							<option value="select_stat" disabled selected>Status</option>						
							<option value="Green">Green</option>
							<option value="Amber">Amber</option>
							<option value="Red">Red</option>
						</select>
					</div>
					<div class="input-field col s8">
						<input value = "%s", name = "comment1" id="comment1" type="text" class="validate">
						<label for="comment1">Enter Comment</label>
					</div>
					<a class="btn-floating btn-large waves-effect waves-light %s"><i class="material-icons">%s</i></a>
				</div>
				<!-- comment-2 -->
				<br>
				<div class="row">
					<div class="input-field col s2">
						<select id="status2", name="status2", class="browser-default">
							<option value="select_stat" disabled selected>Status</option>
							<option value="Green">Green</option>
							<option value="Amber">Amber</option>
							<option value="Red">Red</option>
						</select>
					</div>
					<div class="input-field col s8">
						<input value="%s", name = "comment2" id="comment2" type="text" class="validate">
						<label for="comment2">Enter Comment</label>
					</div>
					<a class="btn-floating btn-large waves-effect waves-light %s"><i class="material-icons">%s</i></a>
				</div>
				<!-- comment-3 -->
				<br>
				<div class="row">
					<div class="input-field col s2">
						<select id = "status3", name="status3", class="browser-default">
							<option value="select_stat" disabled selected>Status</option>
							<option value="Green">Green</option>
							<option value="Amber">Amber</option>
							<option value="Red">Red</option>
						</select>
					</div>
					<div class="input-field col s8">
						<input value="%s", name = "comment3" id="comment3" type="text" class="validate">
						<label for="comment3">Enter Comment</label>
					</div>
					<a class="btn-floating btn-large waves-effect waves-light %s"><i class="material-icons">%s</i></a>
				</div>
				<!-- submit-->
				<div class="center-align">
					<button class="btn waves-effect waves-light" type="submit">Analyze</button>
				</div>
			</form>
		</div>
		
	</div>
</body>
</html>

"""
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
	@cherrypy.expose
	@cherrypy.tools.response_headers(headers=[('Content-Type', 'text/html')])
	def index(self):
		def_status="select_stat"
		def_color="grey lighten-1"
		def_comment=""
		def_flag=""
		#fx=open("index.html","r")
		#webform = fx.read()%(def_status,def_status,def_status,def_comment,def_color,def_flag,def_comment,def_color,def_flag,def_comment,def_color,def_flag)
		#return webform
		return webform%(def_status,def_status,def_status,def_comment,def_color,def_flag,def_comment,def_color,def_flag,def_comment,def_color,def_flag)

	@cherrypy.expose
	@cherrypy.tools.response_headers(headers=[('Content-Type', 'text/html')])
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

		#fx_result = open("index.html","r")
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

		#webform_result=fx_result.read()%(status1,status2,status3,comment1,color1,flag1,comment2,color2,flag2,comment3,color3,flag3)
		webform_result=webform
		return webform_result%(status1,status2,status3,comment1,color1,flag1,comment2,color2,flag2,comment3,color3,flag3)

#To run locally
#cherrypy.quickstart(analyzer())

#To run on a server
wsgi_app = cherrypy.Application(analyzer(), '/')

if __name__ == '__main__':
	from wsgiref.simple_server import make_server
	httpd = make_server('', 6600, wsgi_app)
	httpd.serve_forever()
