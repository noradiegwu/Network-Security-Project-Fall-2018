from bottle import route, request, response, run, template
# source http://omz-software.com/pythonista/docs/ios/bottle/deployment.html
# '0.0.0.0' to listen on all interfaces
# run(host ='0.0.0.0', port=80)
#run(host ='192.168.0.1', port=8000)
# other source : http://omz-software.com/pythonista/docs/ios/bottle/index.html
@route('/hello/<name>')
def index(name):
    return template('<b>Hello {{name}}</b>!', name=name)

# source : http://omz-software.com/pythonista/docs/ios/bottle/tutorial.html#request-data section : query variable
@route('/forum')
def display_forum():
    forum_id = request.query.id
    page = request.query.page or '1'
    return template('Forum ID: {{id}} (page {{page}})', id=forum_id, page=page)


#run(host='localhost', port=8080)
# access http://localhost:8080/hello/world
# other possible url localhost:8080/forum?id=1&page=5
# On my phone hotspot, where the host was my iPad I ran this script on pythonista
run(host='172.20.10.2', port=50000)
