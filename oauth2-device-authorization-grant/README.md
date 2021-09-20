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
