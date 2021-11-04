# WARNING
This is far from production ready!!! Security is even disabled in some areas, e.g. API keys! It is a pure development example!

**DO NOT USE THIS IN PRODUCTION SYSTEMS**

# Howto
## Quick Start
- Start `docker-compose up`
- Run `pip install -r requirements.txt` as inital setup
- Run `python main.py` to start the application

## Maintain / Background
- Keycloak instance http://localhost:8080
- `admin/admin` to maintain
- `test/test` (on `test` realm) for login
- `devicegrant` client id ("public", no secret necessary)
- Keycloak data is imported from `test-realm-export.json`

# Configuration
Create a `.env` file and configure it with e.g.
```
AGENT_ENDPOINT=
AGENT_HTTP_PORT=
ACAPY_AGENT_URL=
# IDENTITY_SERVER_URL=
# IDENTITY_SERVER_WEB_HOOK_URL=
# REDIRECT_URI=
```

If you run it on a local machine with the docker setup, you need port forwarding from the internet, you can use ngrok or if you have a server use SSH port forwarding and nginx proxy_pass with SSL certificates from letsencrypt

If you run this on a domain name NOT being localhost, you need to change the Identity Provider in keycloak:
```
Identity Provider -> Verifiable Credential Access -> Authorization URL
```
You can leave the `Token URL` as is because it uses the container-2-container connection.

## nginx example configuration
Minimalistic config, e.g. `/etc/nginx/sites-enabled/xxx.config`
```
server {

    server_name subdomain.domain.org;

    location / {
        proxy_pass http://127.0.0.1:6000;
    }

```
Run letsencrypt config
```
certbot --nginx
# select the hostname from the list
```

If you want to connect with Android Smartphones which are affected by the letsencrypt certificate chain issue, you can manually select another root ca with:
```
certbot --nginx --preferred-chain "ISRG Root X1"
```
Keept in mind, that for this command you need a recent version of certbot. On e.g. Ubuntu 18.04 LTS this is not in the default apt repository and you have to follow the instructions to install it via `snap`
https://certbot.eff.org/lets-encrypt/ubuntubionic-nginx


## SSH port forwarding
Example
```
ssh -R1000:localhost:20000 -R<remote_port>:localhost:<local_port> root@myserver.org
```

## Browser
If you use the local (localhost) configuration provided here, you have to keep in mind CORS. Disable your browser CORS with e.g.

```
chromium-browser --disable-web-security --user-data-dir=./
```

# Concepts / Links
Very minimalistic documentation in Keycloak:
https://www.keycloak.org/docs/latest/securing_apps/#device-authorization-endpoint

Keycloak feature implemented in version 13 (now 15):
https://issues.redhat.com/browse/KEYCLOAK-7675

How to try in Keycloak:
https://github.com/keycloak/keycloak-community/blob/master/design/oauth2-device-authorization-grant.md#how-to-try-it

Help from Microsoft with a nice protocol flow diagram:
https://docs.microsoft.com/en-us/azure/active-directory/develop/v2-oauth2-device-code

# Screenshots
under [screenshots](./screenshots/)

# Dev
## Keycloak export (including user/password!)
Exports into the mounted `test-realm-export.json`

Beware: If you add new user/passwords, the execution of the following command also exports those passwords!
```
docker-compose exec keycloak /opt/jboss/keycloak/bin/standalone.sh -Djboss.socket.binding.port-offset=100 -Dkeycloak.migration.action=export -Dkeycloak.migration.provider=singleFile -Dkeycloak.migration.realmName=test -Dkeycloak.migration.usersExportStrategy=REALM_FILE -Dkeycloak.migration.file=/tmp/test-realm-export.json
```
Ref: https://github.com/keycloak/keycloak-documentation/blob/master/server_admin/topics/export-import.adoc


## Android Screen
```
scrcpy
```
