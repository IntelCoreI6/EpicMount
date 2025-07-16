import os
import json
path = r"C:\ProgramData\Epic\EpicGamesLauncher\Data\Manifests"


class game():
    instances = []
    def __init__(self, filename, dirpath):
        self.filename = filename
        self.path = dirpath
        game.instances.append(self)
    def __str__(self):
        return f"name: {self.name}, external: {self.external}, install path: {self.installPath}"
    
    def extract_info(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.name = data["DisplayName"]
        self.installPath = data["InstallLocation"]
        if data["InstallLocation"].split(":")[0] == "C":
            self.external = False
        else:
            self.external = True
    def move(self, drive_letter):
        old_pathpath = self.installPath.split(":")
        old_pathpath[0] = drive_letter
        new_path = "".join(old_pathpath)
        #writing new json to file system
        self.installPath = new_path
        return new_path
    





for filename in os.listdir(path):
    if filename != "Pending":
        file_path = os.path.join(path, filename)
        game(filename, file_path)


for g in game.instances:
    g.extract_info()
    print(g)


for g in game.instances:
    print(f"before {g.installPath}")
    g.move("C")
    print(f"after  {g.installPath}")    





