#!/usr/bin/python
import os
import socket
import cgi
import cgitb
import subprocess


__author__ = "Anoop P Alias"
__copyright__ = "Copyright Anoop P Alias"
__license__ = "GPL"
__email__ = "anoopalias01@gmail.com"


installation_path = "/opt/nDeploy"  # Absolute Installation Path
app_template_file = installation_path+"/conf/apptemplates.yaml"
backend_config_file = installation_path+"/conf/backends.yaml"


cgitb.enable()


def close_cpanel_liveapisock():
    """We close the cpanel LiveAPI socket here as we dont need those"""
    cp_socket = os.environ["CPANEL_CONNECT_SOCKET"]
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect(cp_socket)
    sock.sendall('<cpanelxml shutdown="1" />')
    sock.close()


close_cpanel_liveapisock()
form = cgi.FieldStorage()


print('Content-Type: text/html')
print('')
print('<html>')
print('<head>')
print('<title>XtendWeb</title>')
print(('<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous">'))
print(('<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.10.2/jquery.min.js" crossorigin="anonymous"></script>'))
print(('<script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js" integrity="sha384-Tc5IQib027qvyjSMfHjOMaLkfuWVxZxUPnCJA7l2mCWNIpG9mGCD8wGNIcPD7Txa" crossorigin="anonymous"></script>'))
print(('<script src="js.js"></script>'))
print(('<link rel="stylesheet" href="styles.css">'))
print('</head>')
print('<body>')
print('<div id="main-container" class="container text-center">')
print('<div class="row">')
print('<div class="col-md-6 col-md-offset-3">')
print('<div class="logo">')
print('<a href="xtendweb.live.py" data-toggle="tooltip" data-placement="bottom" title="Start Over"><span class="glyphicon glyphicon-globe" aria-hidden="true"></span></a>')
print('<h4>XtendWeb</h4>')
print('</div>')
print('<ol class="breadcrumb">')
print('<li><a href="xtendweb.live.py"><span class="glyphicon glyphicon-refresh"></span></a></li>')
print('<li><a href="xtendweb.live.py">Select Domain</a></li><li class="active">Passenger Module Installer</li>')
print('</ol>')
print('<div class="panel panel-default">')
if form.getvalue('domain') and form.getvalue('backend_category') and form.getvalue('backend_version') and form.getvalue('document_root'):
    # Get the domain name from form data
    mydomain = form.getvalue('domain')
    mybackend = form.getvalue('backend_category')
    mybackendversion = form.getvalue('backend_version')
    mydocroot = form.getvalue('document_root')
    print(('<div class="panel-heading"><h3 class="panel-title">Project</h3></div>'))
    print('<div class="panel-body">')
    print('<ul class="list-group">')
    print(('<div class="alert alert-info alert-top">'+mydomain))
    print(('<br><span class="label label-info">'+mybackend+'</span> <span class="label label-info">'+mybackendversion+'</span>'))
    print(('<br><br><span class="label label-info">Project root: '+mydocroot+'</span>'))
    print('</div>')
    print('</div>')
    print('</li>')
    print('</ul>')
    if mybackend == 'RUBY':
        if os.path.isfile(mydocroot+'/Gemfile'):
            if os.path.isfile('/usr/local/rvm/gems/'+mybackendversion+'/bin/bundle'):
                install_cmd = '/usr/local/rvm/bin/rvm '+mybackendversion+' do bundle install --path vendor/bundle'
                myinstaller = subprocess.Popen(install_cmd, cwd=mydocroot, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                output, err = myinstaller.communicate()
                if output:
                    # section start here
                    print(('<div class="panel-heading"><h3 class="panel-title">Output:</h3></div>'))
                    print('<div class="panel-body">')
                    print('<ul class="list-group">')
                    print(('<div class="alert alert-info alert-top">'+install_cmd+':<br><br><kbd>'+ output +'</kbd></div>'))
                    print('</div>')
                    print('</li>')
                    print('</ul>')
                if err:
                    # section start here
                    print(('<div class="panel-heading"><h3 class="panel-title">Error:</h3></div>'))
                    print('<div class="panel-body">')
                    print('<ul class="list-group">')
                    print(('<div class="alert alert-info alert-top">'+install_cmd+':<br><br><kbd>'+ err +'</kbd><br><br>'))
                    print(('Run the following command in your shell to proceed with manual installation:<br>'))
                    print(('cd '+mydocroot+'<br>'))
                    print(('/usr/local/rvm/bin/rvm '+mybackendversion+' do bundle install --path vendor/bundle'))
                    print('</div>')
                    print('</li>')
                    print('</ul>')
        else:
            print(('<div class="alert alert-info alert-top">Gemfile not found for <span class="label label-info">RUBY</span> project, specify project dependencies in <br><br><kbd>'+ mydocroot +'/Gemfile</kbd></div>'))
    elif mybackend == 'NODEJS':
        if os.path.isfile(mydocroot+'/package.json'):
            if os.path.isfile('/usr/local/nvm/versions/node/'+mybackendversion+'/bin/npm'):
                install_cmd = '/usr/local/nvm/versions/node/'+mybackendversion+'/bin/npm -q install --production'
                my_env = os.environ.copy()
                my_env["PATH"] = "/usr/local/nvm/versions/node/"+mybackendversion+"/bin:"+my_env["PATH"]
                myinstaller = subprocess.Popen(install_cmd, cwd=mydocroot, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=my_env, shell=True)
                output, err = myinstaller.communicate()
                if output:
                    # section start here
                    print(('<div class="panel-heading"><h3 class="panel-title">Output:</h3></div>'))
                    print('<div class="panel-body">')
                    print('<ul class="list-group">')
                    print(('<div class="alert alert-info alert-top">'+install_cmd+':<br><br><kbd>'+output+'</kbd></div>'))
                    print('</div>')
                    print('</li>')
                    print('</ul>')
                if err:
                    # section start here
                    print(('<div class="panel-heading"><h3 class="panel-title">Error:</h3></div>'))
                    print('<div class="panel-body">')
                    print('<ul class="list-group">')
                    print(('<div class="alert alert-info alert-top">'+install_cmd+':<br><br><kbd>'+ err +'</kbd><br><br>'))
                    print(('Run the following command in your shell to proceed with manual installation:<br>'))
                    print(('export PATH="/usr/local/nvm/versions/node/'+mybackendversion+'/bin:$PATH"<br>'))
                    print(('cd '+mydocroot))
                    print(('<br>npm install --production'))
                    print(('</div>'))
                    print('</div>')
                    print('</li>')
                    print('</ul>')
        else:
            print(('<div class="alert alert-info alert-top">package.json not found for <span class="label label-info">NODEJS</span> project, specify project dependencies in <br><br><kbd>'+mydocroot+'/package.json</kbd></div>'))
    elif mybackend == 'PYTHON':
        if os.path.isfile(mydocroot+'/requirements.txt'):
            if os.path.isfile('/usr/local/pythonz/pythons/'+mybackendversion+'/bin/pip'):
                install_cmd = '/usr/local/pythonz/pythons/'+mybackendversion+'/bin/pip install --user -r requirements.txt'
                myinstaller = subprocess.Popen(install_cmd, cwd=mydocroot, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
                output, err = myinstaller.communicate()
                if output:
                    # section start here
                    print(('<div class="panel-heading"><h3 class="panel-title">Output:</h3></div>'))
                    print('<div class="panel-body">')
                    print('<ul class="list-group">')
                    print(('<div class="alert alert-info alert-top">'+install_cmd+':<br><br><kbd>'+output+'</kbd></div>'))
                    print('</div>')
                    print('</li>')
                    print('</ul>')
                if err:
                    # section start here
                    print(('<div class="panel-heading"><h3 class="panel-title">Error:</h3></div>'))
                    print('<div class="panel-body">')
                    print('<ul class="list-group">')
                    print(('<div class="alert alert-info alert-top">'+install_cmd+':<br><br><kbd>'+ err +'</kbd><br><br>'))
                    print(('Run the following command in your shell to proceed with manual installation:<br>'))
                    print(('export PATH="/usr/local/pythonz/pythons/'+mybackendversion+'/bin:$PATH"<br>'))
                    print(('cd '+mydocroot))
                    print(('<br>pip install --user -r requirements.txt'))
                    print(('</div>'))
                    print('</div>')
                    print('</li>')
                    print('</ul>')
        else:
            print(('<div class="alert alert-info alert-top">requirements.txt not found for <span class="label label-info">PYTHON</span> project, specify project dependencies in <br><br><kbd>'+mydocroot+'/requirements.txt</kbd></div>'))
else:
    print('<div class="alert alert-danger"><span class="glyphicon glyphicon-alert" aria-hidden="true"></span> Forbidden</div>')
print('</div>')
print('<div class="panel-footer"><small>Need Help <span class="glyphicon glyphicon-circle-arrow-right" aria-hidden="true"></span> <a target="_blank" href="https://autom8n.com/xtendweb/UserDocs.html">XtendWeb Docs</a></small></div>')
print('</div>')
print('</div>')
print('</div>')
print('</div>')
print('</body>')
print('</html>')
