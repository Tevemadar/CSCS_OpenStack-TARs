from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneauth1.extras._saml2 import V3Saml2Password
from keystoneclient.v3 import client
import swiftclient.client as swiftclient
from getpass import getpass
import requests,glob,time,sys,os

if not os.path.exists("done"):
  os.mkdir("done")

container = sys.argv[1]
username = input('User name: ')
password = getpass()

batch=time.monotonic()-1
with open(str(int(time.time()))+".txt","w") as logfile:
  logfile.write(container)
  logfile.write("\r\n")
  for tar in glob.glob("*.tar"):
    print(time.asctime())
    print(tar)
    logfile.write(time.asctime())
    logfile.write("\r\n")
    if batch<time.monotonic():
      logfile.write("login "+username)
      logfile.write("\r\n")
      batch=time.monotonic()+60*60
      auth = V3Saml2Password(auth_url='https://pollux.cscs.ch:13000/v3',
                             identity_provider='cscskc',
                             protocol='mapped',
                             identity_provider_url='https://auth.cscs.ch/auth/realms/cscs/protocol/saml/',
                             username=username,
                             password=password)
      sess = session.Session(auth=auth)
      token = sess.get_token()
    logfile.write(tar)
    logfile.write("\r\n")
    with open(tar,"rb") as tarfile:
      req=requests.put("https://object.cscs.ch/v1/AUTH_08c08f9f119744cbbf77e216988da3eb/"+container+"/?extract-archive=tar",
                       data=tarfile,
                       headers={"X-Auth-Token":token})
    os.rename(tar,"done/"+tar)
    logfile.write(time.asctime())
    logfile.write("\r\n")
    logfile.write(str(req.headers))
    logfile.write("\r\n")
    logfile.write(str(req.content))
    logfile.write("\r\n")
    req=requests.head("https://object.cscs.ch/v1/AUTH_08c08f9f119744cbbf77e216988da3eb/"+container,
                      headers={"X-Auth-Token":token})
    logfile.write(str(req.headers))
    logfile.write("\r\n")
