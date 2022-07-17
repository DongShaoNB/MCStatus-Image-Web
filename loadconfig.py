import configparser

gh = configparser.ConfigParser()
gh.read(".\\config\\config.ini", encoding="utf-8")


suffix = gh.get("Settings", "Suffix")
port = int(gh.get("Settings", "Port"))
