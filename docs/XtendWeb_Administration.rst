Administration of XtendWeb plugin
=================================

The end user has an intuitive UI for managing domains hosted on cPanel.

Sysadmins can manipulate server wide settings using various scripts accessible from command line

The ultimate goal of XtendWeb is to be an extensible nginx config management system that is easy for the sysadmins and enduser alike .

Usually a Sysadmin will need to have minimal inetraction with the system. Following are some commands that may be required to run and a brief description of what it does.

Mostly only the below commands will be needed by the sysAdmin

Quick Reference of scripts for sysadmins
-----------------------------------------------

::

  # Enable or disable the plugin .Once you disable plugin the system will act as it was prior to plugin install
  /opt/nDeploy/scripts/cpanel-nDeploy-setup.sh disable
  /opt/nDeploy/scripts/cpanel-nDeploy-setup.sh enable

  # Automatically fix all errors.Can be run if you notice nginx config error or php error etc
  # Following will regenerate all config and restart associated services. Use force only if normal run does not fix
  /opt/nDeploy/scripts/attempt_autofix.sh
  /opt/nDeploy/scripts/attempt_autofix.sh force  # force regenerate

  # A best effort to switch as many websites as possible to native nginx
  # See file /opt/nDeploy/conf/appsignatures.yaml for switching logic
  # Add username to /opt/nDeploy/conf/auto_config.exclude to exclude a specific user
  /opt/nDeploy/scripts/switch_to_native_nginx.sh

  #Install various application servers
  /opt/nDeploy/scripts/easy_php_setup.sh
  /opt/nDeploy/scripts/easy_hhvm_setup.sh
  /opt/nDeploy/scripts/easy_passenger_setup.sh

  #Install netdata monitoring
  /opt/nDeploy/scripts/easy_netdata_setup.sh

  # Restart application server .note that Passenger apps gets restarted with nginx
  systemctl restart ndeploy_backends  # PHP
  systemctl restart ndeploy_hhvm@USER  #HHVM

  # Retart cluster file syncing service
  systemctl restart ndeploy_unison

  # Adding/removing application servers
  /opt/nDeploy/scripts/update_backend.py [add|del] backend_category backend_name backend_path

  # Adding/removing application template (generic)
  /opt/nDeploy/scripts/update_profiles.py [add|del] [root|cpanelusername] [main|subdir] [backend] [templatefilename] [quoted description]
  # Examples
  /opt/nDeploy/scripts/update_profiles.py add root main PHP 5001.j2 "Wordpress"
  /opt/nDeploy/scripts/update_profiles.py add root subdir PHP 5001_subdir.j2 "Wordpress in subdir"
  /opt/nDeploy/scripts/update_profiles.py add cpanelusername main PHP 5001.j2 "Wordpress"
  /opt/nDeploy/scripts/update_profiles.py add cpanelusername subdir PHP 5001_subdir.j2 "Wordpress in subdir"


Config Generation logic and customizations
------------------------------------------------

Config generation is based on Templates and YAML settings (  Jinja2 templating engine and YAML settings )
For generating a single nginx vhost following files are parsed in order .The customization options are mentioned beside them with CUSTOMIZE
If the customized files are present ,it is used instead of original
A Sysadmin mostly only need to add /edit application templates and this use minimum template logic for easy manipulation

::

  /opt/nDeploy/domain-data/domain.com # User settings for domain
  # if above file is not present ,it is created with default settings from
  /opt/nDeploy/conf/domain_data_default.yaml # CUSTOMIZE /opt/nDeploy/conf/domain_data_default_local.yaml
  /opt/nDeploy/conf/domain_data_suspended.yaml # CUSTOMIZE /opt/nDeploy/conf/domain_data_suspended_local.yaml

  # Following file generate /etc/nginx/sites-enabled/domain.com.conf
  /opt/nDeploy/conf/server.j2 # CUSTOMIZE /opt/nDeploy/conf/server_local.j2

  # The application template defined in domain_data setting file is used for generating /etc/nginx/sites-enabled/domain.com.include
  /opt/nDeploy/conf/APPTEMPLATENAME.j2


Layer7(Application layer) DDOS mitigation
-----------------------------------------

::

  To deal with a server wide DDOS on http (application layer)
  Edit /etc/nginx/conf.d/http_settings.conf
  and uncomment the include line as mentioned

  # Uncomment following to enable DOS mitigation server wide
  # include /etc/nginx/conf.d/dos_mitigate.conf;

  nginx -s reload



Upgrading XtendWeb and Nginx
----------------------------

nDeploy-nginx is mated with a phusion passenger ruby gem .
So we don't encourage unmanned upgrades and have therefore set enable=0 in the yum repository.
The upgrade must be done manually by running the following commands
::

  yum -y install https://github.com/AnoopAlias/XtendWeb/raw/ndeploy4/nDeploy-release-centos-1.0-6.noarch.rpm
  yum --enablerepo=ndeploy upgrade
  #For setups using Phusion Passenger app server
  /opt/nDeploy/scripts/easy_passenger_setup.sh


XtendWeb cluster upgrade
----------------------------

On All slaves

::

  yum --enablerepo=ndeploy upgrade

On master


::

  yum --enablerepo=ndeploy upgrade
  cd /opt/nDeploy/conf/nDeploy-cluster
  ansible-playbook -i ./hosts cluster.yml


Migrating Xtendweb settings
--------------------------------
In case you are migrating the entire cPanel accounts to a new server.

1. Do the cPanel migration
2. Install Xtendweb on the new server
3. Edit the file /opt/nDeploy/scripts/migrate_xtendweb_settings.sh and change REMOTE_SERVER='ip.ip.ip.ip' with the remote servers IP address
4. Run the script /opt/nDeploy/scripts/migrate_xtendweb_settings.sh  #Input password of remote server whenever prompted


Temporarily disable the plugin
-------------------------------

  ``/opt/nDeploy/scripts/cpanel-nDeploy-setup.sh disable``

Uninstall the plugin
---------------------

::

  /opt/nDeploy/scripts/cpanel-nDeploy-setup.sh disable
  yum remove nginx-nDeploy nDeploy

Remove PHP-FPM selector plugin on cPanel v66 and above(feature overlap)
----------------------------------------------------------------------------

As of cPanel v66 , cPanel support setting up php-fpm as default php handler server wide .Since this feature overlap with XtendWeb's PHP-FPM selector plugin
We advise that you remove the php-fpm selector functionality .Folowing command does it
::

  /opt/nDeploy/scripts/init_backends.py httpd-php-uninstall
  /opt/nDeploy/scripts/attempt_autofix.sh

Once the above is done, you must use WHM >> Home »Software »MultiPHP Manager to set all domains to PHP-FPM
as PHP-FPM will greatly improve your system performance.


.. disqus::
