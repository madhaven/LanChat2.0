try:
#if (1):
# -- INITIAL SETUPS

    from socket import *
    from re import *
    from time import ctime
    host, port, messages, passwordtoterminate = '', 45566, [], input('Set a password to terminate server : ')
    heads, closepage, termpage, knockpage, page404 = ['''HTTP/1.1 200 OK
Connection: close
Server: JaysPythonServer
Date: Mon, 10 Aug 1998 15:44:04 GMT
Content-Type: text/html

''',
    '''<!DOCTYPE html>
<html>
<head>
	<title>Close this connection</title>
</head>
<body>
	<form method="post" action="http://'''+gethostbyname(gethostname())+':'+str(port)+'''/closesubmit">
		<input type=text placeholder=password name=password>
		<input type=submit value=submit>
	</form>
</body>
</html>''',
    '''<html><head><title>set</title></head><body>The Server has been Shut Down.</body></html>''',
    open('knock.html', 'r').read(),
    "<html><body>ayyo 404 adich moonchiyallo</body></html>"]
    
    def respond(sock, reqpage, reqdata=None):
        switchoff, resp = False, heads;
        if not reqpage : reqpage = 'knock'
        
        if reqpage == 'favicon.ico': resp = "HTTP/1.1 404 wtf";
        elif reqpage == 'knock': resp += knockpage;
        elif reqpage == 'close': resp += closepage
        elif reqpage == 'closesubmit':
            password = search('password\=[a-zA-Z]*.*$', reqdata)
            if (password): 
                if password.group()[9:] == passwordtoterminate:
                    resp += termpage
                    switchoff = True;
                else:
                    resp += knockpage
        elif reqpage == 'back':
            input("BACK CAUGHT")
            if search('0<<.*>>', reqdata):
                messages.append(ctime()[11:-5]+' : '+search('0<<.*>>', reqdata).group()[3:-2]+' Joined')
            elif search('1<<.*>><<.*>>', reqdata):
                messages.append(ctime()[11:-5]+' : '+search('>><<.*>>', reqdata).group()[4:-2]+' < '+search('<<.*>><<', reqdata).group()[2:-4])
            elif search('listening', reqdata):
                print("LISTEN CAUGHT##############");
            resp += "ACKNOWLEDGED"
        else: resp += page404
        sock.send(bytes(resp.replace('\r\n', '\\r\\n'), 'utf-8'))
        return switchoff
    
# -- RECEPTION OF A REQUEST AND EXTRACTING INFO TO BE PASSSED INTO RESPOND FUNCTION
    sock = socket(2, 1);
    sock.bind((host, port))
    sock.listen(5)
    print('Connect clients to %s:%d'%(gethostbyname(gethostname()), port))
    while (True):
        print("awaiting connection");
        newsock, adr = sock.accept(); print("Connection : %s\n"%str(adr))
        httpreq = str(newsock.recv(1024))[2:-1].replace('\\r\\n', '\r\n')
        if httpreq:
            print(httpreq);
            if   (search("^GET /[a-zA-Z]* ", httpreq)): reqpage = search("^GET /[a-zA-Z]* ", httpreq).group()[5:-1]
            elif (search("^POST /[a-zA-Z]* ",httpreq)): reqpage = search("^POST /[a-zA-Z]* ",httpreq).group()[6:-1]
            else: reqpage = None;
            if respond(newsock, reqpage, httpreq) or (httpreq == passwordtoterminate):
                newsock.close()
                break
        newsock.close(); print('\nConnection closed');
    sock.close(); print("Server Terminated");
    
except Exception as e:
    newsock.close()
    sock.close()
    input(e);
