# RavenBot
RavenBot is a discord bot written in python using the library py-cord.


## Features
### Role assignment features
RavenBot has multiple commands that help discord servers assign and unassign user roles.

#### Role assignment buttons:
`/role @ROLE`  generates a button for assigning the selected role, and a button unassigning the role. 
The buttons may be used by everyone on the discord server to assign/unassign the wished role.

![Button Example](https://user-images.githubusercontent.com/61353115/156388445-1645f3a8-1580-49c7-9852-8a253016a213.png)


#### Assignment roles:
Define special roles on your server that are able to assign specified roles using the 
`/assign @USER` and `/unassign @USER` commands.
If the user typing the command has a role with a corresponding role id to one or more of the assigner role ids defined in config/assigner_roles.json,
the user will get a select menuof roles it can assign/unassign to the @USER defined in the command. The roles which a assign role can assign/unassign are 
also defined in config/assigner_roles.json.

![Assign Example](https://user-images.githubusercontent.com/61353115/156391784-765f7ad7-76c9-486b-9091-b39d8d9eed51.png)


Assigner_roles.json need to be setup as a list of objects each containing a "role_ids" field, where the value is a list of role ids and a "assigner_role_id" field, where the value may only be one role id (int). See examples below:
```json
[
    {
        "role_ids": [IdForARoleToAssign/Unassign, IdForAnotherRoleToAssign/Unassign],
        "assigner_role_id": IdForRoleThatCanAssign/UnassignRolesDefinedAbove
    }
]
```
Real example of assigner_roles.json:
```json
[
    {
        "role_ids": [947888127823990814],
        "assigner_role_id": 947891370503315567
    },
    {
        "role_ids": [948310365127720961, 948310544362917958],
        "assigner_role_id": 948310466873139301
    }
]
```

#### Other Role Assignment commands
`/add_role @ROLE @USER` gives the selected user the selected role
`/remove_role @ROLE @USER` removes the selected role from the selected user


### Blacklist
RavenBot has blacklist functionality that allows a multiple blacklists to be defined.
Blacklists are defined in config/blacklist.json

blacklist.json must be a list of objects following the format of the example below:
```json
[
    {
        "timeout_minutes": 0,
        "kick_on_use": false,
        "ban_on_use": true,
        "warn_on_use": false,
        "full_word": true,
        "whitelisted_role_ids": [854340374138716180, 853692936465940501],
        "blacklisted_items": [
            "exampleWord1",
        ]
    },
    {
        "timeout_minutes": 5,
        "kick_on_use": false,
        "ban_on_use": false,
        "warn_on_use": false,
        "full_word": true,
        "whitelisted_role_ids": [854340374138716180, 853692936465940501],
        "blacklisted_items": [
            "fuck you"
        ]
    }
]
```
The fields "timeout_minutes", "kick_on_use", "ban_on_use", "warn_on_use" all defines different possible punishments that can be used against users writing blacklisted words.
IMPORTANT: Only 1 punishment may be enabled!

`"timeout_minutes"` must be an int, and can be set to 0, to disable timeout as a punishment.

`"kick_on_use"` must be a bool, set to true, to enable kick as punishment

`"ban_on_use"` must be a bool, set to true, to enable ban as punishment

`"warn_on_use"` must be a bool, set to true, to enable written warning as punishment (NOT IMPLEMENTED)

Note: Regardsless of what punishment is enabled, RavenBot will remove the message containing the blacklsited word immediatly.

`"full_word"`: If true, blacklisted items must be written as independent words in a discord message. That means a blacklisted item called "test", will not act against a message where the word "tests" is written.

`whitelisted_role_ids`: List of ints, which are role ids of roles who may write blacklsited items without any consequences.

`blacklisted_items`: List of items blacklisted. (Note: capital letters do not matter)


`/blacklist` Command to reload blacklist (Use when changes have been made to blacklist.json, if bot has not been restarted)



## Setup
Install and run:

`pip install -r requirements.txt`

`python RvnBot.py`


## Configuration




## GNU License
see LICENSE file
