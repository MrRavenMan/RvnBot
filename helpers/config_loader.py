import configparser

config = configparser.ConfigParser()
config.read("config/config.ini")
admin = config["General"]["manage_all"]