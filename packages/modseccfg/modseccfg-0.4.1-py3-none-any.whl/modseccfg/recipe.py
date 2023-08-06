# api: modseccfg
# encoding: utf-8
# version: 0.2
# type: data
# title: recipe
# description: Apache/mod_security config examples or conversions
# category: config
# config:
#    { name: replace_rules, type: bool, value: 0, description: "try to find replacement spot, else just append" }
#
# Basically just blobs of text and an editor window.
# [Save] will append directives to selected vhost/*.conf file.
#
# Some samples from:
#  · https://wiki.atomicorp.com/wiki/index.php/Mod_security
#


from modseccfg import utils, vhosts
import PySimpleGUI as sg
import re, random
from textwrap import dedent



class templates:

    locationmatch = """
        <LocationMatch "/app/">
          SecRuleRemoveById $id   # $msg
          # SecRuleEngine DetectionOnly
        </LocationMatch>
    """

    directory = """
        <Directory "/srv/www/app/">
          SecRuleRemoveById $id   # $msg
        </Directory>
    """

    filesmatch = """
        <FilesMatch "\.php$">
          SecRuleRemoveById $id   # $msg
        </FilesMatch>
    """
    
    exclude_parameter = """
        # Exclude GET/POST parameter from rule
        #
        SecRuleUpdateTargetByID $id "!ARGS:param"
    """
    
    rule_to_detectiononly = """
        # One rule to DetectionOnly
        #
        SecRuleUpdateActionById $id "pass,status:200,log,auditlog"
    """

    url_to_detectiononly = """
        # Set one URL to DetectionOnly
        #
        SecRule REQUEST_URI "$request_uri" "phase:1,id:$rand,t:none,t:lowercase,pass,msg:'DetectionOnly for $request_uri',ctl:ruleEngine=DetectionOnly"
    """
    
    exempt_remote_addr = """
        # Exempt client addr from all SecRules
        #
        SecRule REMOTE_ADDR "^\\Q$remote_addr\\E$" "phase:1,id:$rand,t:none,nolog,allow,ctl:ruleEngine=Off,ctl:auditEngine=Off"
    """

    whitelist_ip_file = """
        # List of IPs from filename trigger DetectionOnly mode
        #
        SecRule REMOTE_ADDR "@pmFromFile $confn.whitelist" "phase:1,id:$rand,t:none,nolog,allow,ctl:ruleEngine=DetectionOnly"
    """
    
    ip2location = """
        # Use mod_ip2location or Cloudflare header
        #
        SetEnvIfExpr "req('CF-IPCountry') =~ '\w\w'" IP2LOCATION_COUNTRY_SHORT=%{HTTP_CF_IPCOUNTRY}
        SecRule ENV:IP2LOCATION_COUNTRY_SHORT "!^(UK|DE|FR)$" "id:$rand,deny,status:500,msg:'Req not from whitelisted country'"
    """
    
    macros = """
        # This directive block defines some macros, which you can use to simplify a few
        # SecRules exceptions. Best applied to a central *.conf file, rather# than vhost.
        # An `Use` directive/prefix is necessary to expand these macros.
        #     ↓
        #    Use SecRuleRemoveByPath 900410 /app/exempt/
        #
        <IfModule mod_macro.c>

          <Macro NEWID $STR>
            # define %{ENV:NEWID} in the 50000 range; might yield duplicates
            SetEnvIfExpr "md5('$STR') =~ /(\d).*(\d).*(\d).*(\d)/" "NEWID=5$1$2$3$4"
          </Macro>

          <Macro SecRuleRemoveByPath $ID $PATH>
            Use NEWID "$ID$PATH"
            SecRule REQUEST_URI "@eq $PATH" "id:%{ENV:NEWID},t:none,msg:'Whitelist «$PATH»',ctl:removeById=$ID"
          </Macro>

        </IfModule>
    """
    
    apache_cloudflare_remoteip = """
        # Sets REMOTE_ADDR for Apache at large.
        # @url https://support.cloudflare.com/hc/en-us/articles/360029696071-Orig-IPs
        # @bug Seemingly mod_security needs another fix.
        #
        <IfModule mod_remoteip.c>
           RemoteIPHeader CF-Connecting-IP
           RemoteIPTrustedProxy 173.245.48.0/20
           RemoteIPTrustedProxy 103.21.244.0/22
           RemoteIPTrustedProxy 103.22.200.0/22
           RemoteIPTrustedProxy 103.31.4.0/22
           RemoteIPTrustedProxy 141.101.64.0/18
           RemoteIPTrustedProxy 108.162.192.0/18
           RemoteIPTrustedProxy 190.93.240.0/20
           RemoteIPTrustedProxy 188.114.96.0/20
           RemoteIPTrustedProxy 197.234.240.0/22
           RemoteIPTrustedProxy 198.41.128.0/17
           RemoteIPTrustedProxy 162.158.0.0/15
           RemoteIPTrustedProxy 104.16.0.0/12
           RemoteIPTrustedProxy 172.64.0.0/13
           RemoteIPTrustedProxy 131.0.72.0/22
           RemoteIPTrustedProxy 2400:cb00::/32
           RemoteIPTrustedProxy 2606:4700::/32
           RemoteIPTrustedProxy 2803:f800::/32
           RemoteIPTrustedProxy 2405:b500::/32
           RemoteIPTrustedProxy 2405:8100::/32
           RemoteIPTrustedProxy 2a06:98c0::/29
           RemoteIPTrustedProxy 2c0f:f248::/32
        </IfModule>
    """
     
    apache_errorlog_format = """
        # Extend error log w/ REQUEST_URI and somewhat standard datetime format (not quite 8601)
        #
        #  → Feedback appreciated. What ought to be the post-90s Apache default?
        #
        SetEnvIf Request_URI "(^.*$)" REQ=$1
        ErrorLogFormat "[%{cu}t] [%m:%l] [pid %P:tid %T] [client %a] %E: %M [request_uri %{REQ}e]"
    """


def ls():
    return [title.replace("_", " ").title() for title in templates.__dict__.keys() if not title.startswith("__")]

def has(name):
    return hasattr(templates, name.lower().replace(" ", "_"))

def show(name, data, id=0, vhost={}):
    # resolve
    vars = bag(data)
    name = name.lower().replace(" ", "_")
    text = getattr(templates, name)
    if type(text) is str:
        text = dedent(text).lstrip()
        text = repl(text, vars)
            #@ToDo: mainwindow should supply a data bag (either full secrule entry, or params from log - depending on which is active)
    else:
        text = text(data, vars)
    print(data)
    print(text)

    # window
    w = sg.Window(title=f"Recipe '{name}'", resizable=1, layout=[
        [sg.Multiline(default_text=text, key="src", size=(90,24), font="Mono 12")],
        [sg.Button("Save", key="save"), sg.Button("Cancel", key="cancel")]
    ])
    event, values = w.read()
    print(event, values)
    w.close()
    
    # write …
    if event == "save":
        writer.append(vhost.fn, text)


# prepare vars dict from mainwindow event data + selected log line
def bag(data):
    vars = {
        "id": "0",
        "rand": random.randrange(2000,5000),
        "request_uri": "/PATH",
        "confn": data.get("confn")
    }
    if data.get("log"):
        for k,v in re.findall('\[(\w+) "([^"]+)"\]', str(data["log"])):
            if k in ("uri", "request_line"): k = "request_uri"
            vars[k] = v
    if data.get("rule"):
        vars["id"] = data["rule"][0]
    return vars

# substitute $varnames in text string
def repl(text, vars):
    text = re.sub(r"\$(\w+)", lambda m,*k: str(vars.get(m.group(1), m.group(0))), text)
    return text

