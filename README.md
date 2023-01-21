# RavenBot
RavenBot is a discord bot written in python using the library py-cord.


## Features
### Role assignment features
RavenBot has multiple commands that help discord servers assign and unassign user roles.

#### Role assignment buttons:
`/role @ROLE`  generates a button for assigning the selected role, and a button unassigning the role. 
On command, a modal with options to customize a description before the buttons and the button labels will pop up.
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



### Blacklist feature
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
        "allow_user_options": true,
        "full_word": true,
        "whitelisted_role_ids": [854340374138716180, 853692936465940501],
        "blacklisted_items": [
            "exampleWord1",
            "noNoWord2",
            "NotAllowedWORD3",
        ],
        "user_msg_path": ""
    },
    {
        "timeout_minutes": 5,
        "kick_on_use": false,
        "ban_on_use": false,
        "warn_on_use": false,
        "allow_user_options": true,
        "full_word": true,
        "whitelisted_role_ids": [854340374138716180, 853692936465940501],
        "blacklisted_items": [
            "f##k you"
        ],
        "user_msg_path": "example_warning.txt"
    }
]
```
The fields "timeout_minutes", "kick_on_use", "ban_on_use", "warn_on_use" all defines different possible punishments that can be used against users writing blacklisted words.
IMPORTANT: Only 1 punishment may be enabled!

`"timeout_minutes"` must be an int, and can be set to 0, to disable timeout as a punishment.

`"kick_on_use"` must be a bool, set to true, to enable kick as punishment

`"ban_on_use"` must be a bool, set to true, to enable ban as punishment

`"warn_on_use"` must be a bool, set to true, to enable written warning as punishment. Will send a warning msg (DM) to user. If `"user_msg_path": ""` is set to `""` (none) a standard warning will be sent.

`"allow_user_options"` must be a bool. Set to `true` to enable moderators to click a button to kick or barn user. 
Note: `"kick_on_use", "ban_on_use"` must be set to `false` for this to be enabled!

Note: Regardsless of what punishment is enabled, RavenBot will remove the message containing the blacklsited word immediatly.

`"full_word"`: If true, blacklisted items must be written as independent words in a discord message. That means a blacklisted item called "test", will not act against a message where the word "tests" is written.

`"whitelisted_role_ids"`: List of ints, which are role ids of roles who may write blacklsited items without any consequences.

`"blacklisted_items"`: List of items blacklisted. (Note: capital letters do not matter)

`"user_msg_path"`: if set to `""` this feature will be disabled. If you want a custom message to be sent to offending users, enter the file name like `example_warning.txt` of a txt file created 
in config/memberWatchConfig/userWarnings containing a warning message that will be sent to users. See config/memberWatchConfig/userWarnings/example_warning.txt for example.


`/blacklist` Command to reload blacklist (Use when changes have been made to blacklist.json)



### Chatter feature
Allows predefined chats to be defined to make RavenBot feel more human/inteligent. These chats can be defined in config/chats.json
chats.json must follow the format of the example below. chats.json must be a object with fields:

"always_respond_to_role_ids": List of role ids (int) that the chatter will always respond.

"chats" List of chat objects that contain the following fields:
    "call" List of strings. These are the calls that will prompt a repsonse. 
    "response" List of strings. Possible responses (Will be picked randomly). Use {user_mention} to tag the user that has made the call
    "probability" Float (Must be between 0.1 and 1). Chance of RavenBot reacting on call and typing a response.
    
See dice example in example below for special dice functionality.
    
```json
{
    "always_respond_to_role_ids": [854340374138716180, 853692936465940501],
    "chats": [
        {
            "call": ["good morning", "morning", "morning!"],
            "response": ["Good morning dude!", "Good morning {user_mention}"],
            "probability": 0.8
        },
        {
            "call": ["good night"],
            "response": ["Night dude!", "Fuck off {user_mention}. You do not belong in **{server_mention}**"],
            "probability": 0.1
        },
        {
            "call": ["Roll a dice"],
            "response": ["You got {result}", "I rolled a dice with numbers between {min} and {max}. I got {result}"],
            "probability": 0.8,
            "min": 1,
            "max": 9
        }
    ]
}
```

`/chats` Command to reload chats if chats.json has been updated

`/roulette` Command to spawn a button which will prompt a response or timeout as defined in config/roulette.json to the user clicking the button. 
On command, a modal with options to customize button description and label will pop up.
The button may be used by everyone.

config/roulette.json must follow format of example below. Define a list of objects, where each object has a response field (str) and a timeout field (int).
"timeout" can be set to 0 to not give a timeout. 
On button click, RavenBot will pick a random roulette item for the user and send a message to the user in the buttons channel with the response as text, and time them out if timeout is more than 0. Timeout must be an int and represents the timeout in minutes.
```json
[
    {
        "response": "When live gives you lemons, eat shit!",
        "timeout": 0
    },
    {
        "response": "You talk too much - Now be quiet for the next minute!",
        "timeout": 1
    }
]
```


### Other commands
`/test` Command to test if bot is online. Will prompt a short response from RavenBot

`/close` Command to shut down RavenBot

`!message` or `!msg`. Command to write a message, that RavenBot will write in same channel. Can be used to make RavenBot write a message or send a picture in a channel. 
Type !message or !msg followed by the text or pictures you want RavenBot to send in the channel.



## Setup
Install and run:

`pip install -r requirements.txt`

`python RvnBot.py`


## Configuration
Configure bot in config/config.ini
`TOKEN` Token generated by discord. Warning: Do not share your token with anyone

`status` Bot's status displayed in Discord. Must be a number between 0-5. 0: Off 1: Playing, 2: Streaming, 3: Watching, 4: Competing in, 5: Listening to

`status_message` Status meesage displayed after the suffix defined by the number in `status`

`status_streaming_url` Url displayed if `status` is set to 2

`enable_Assigner` Set to True to use /role, /assign, /unassign, /add_role, /remove_role commands

`enable_MemberWatch` Set to True to enable blacklist functionality 

`enable_Chatter` Set to True to enable chats and roulette functionality


## GNU License
see LICENSE file
