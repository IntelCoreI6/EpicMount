import os
import json
import string
import time
path = r"C:\ProgramData\Epic\EpicGamesLauncher\Data\Manifests"

def restart_epic_launcher():
    """Closes and restarts the Epic Games Launcher."""
    launcher_path = r"C:\Program Files (x86)\Epic Games\Launcher\Portal\Binaries\Win64\EpicGamesLauncher.exe"

    print("Closing Epic Games Launcher...")
    # Use taskkill to force the launcher to close. "> nul 2>&1" suppresses output.
    os.system("taskkill /f /im EpicGamesLauncher.exe > nul 2>&1")
    
    # Wait a few seconds for the process to fully terminate
    time.sleep(5)

    if os.path.exists(launcher_path):
        print("Restarting Epic Games Launcher...")
        os.startfile(launcher_path)
        input("Press enter when epic games is launched")
    else:
        print(f"Error: Epic Games Launcher not found at {launcher_path}")
        print("Please update the 'launcher_path' variable with the correct location.")

def get_drive_letters():
    drives = []
    for letter in string.ascii_uppercase:
        drive = f"{letter}:\\"
        if os.path.exists(drive):
            drives.append(letter)
    return drives

def replace_path(path, drive_letter):
    old_path = path.split(":")
    old_path[0] = drive_letter
    print(f"path: {old_path}")
    new_path = old_path[0] + ":" + old_path[1]
    #writing new json to file system
    return new_path
def get_newest(game1, game2):
    """
    Compares two version strings and returns the newer one.
    Handles versions with multiple dots and non-numeric parts.
    """
    version1 = game1.version
    version2 = game2.version
    def to_tuple(v_str):
        # Split the version string and convert numeric parts to integers for comparison
        parts = v_str.replace('-', '.').split('.')
        return tuple(int(p) if p.isdigit() else p for p in parts)

    v1_tuple = to_tuple(version1)
    v2_tuple = to_tuple(version2)

    if v1_tuple > v2_tuple:
        return game1
    else:
        return game2

class game():
    instances = {}
    def __init__(self, filename, dirpath):
        self.filename = filename
        self.path = dirpath
        self.extract_info()

    def __str__(self):
        return f"name: {self.name}, external: {self.external}, install path: {self.path}"
    
    def extract_info(self):
        with open(self.path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        self.name = data["DisplayName"]
        self.installPath = data["InstallLocation"]
        self.version =  data["AppVersionString"] # format: 1.130.2989309, can have as many dots as possible and even strings in between so watch out
        self.drive = data["InstallLocation"].split(":")[0]
        if self.drive == "C":
            self.external = False
        else:
            self.external = True    
        if self.name in game.instances:
            game.instances[self.name] = get_newest(game.instances[self.name], self)

        else:
            game.instances[self.name] = self

    def update_path(self, drive_letter):
        with open(self.path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        for key in ["ManifestLocation", "InstallLocation", "StagingLocation"]:
            data[key] = replace_path(data[key], drive_letter)
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        self.installPath = data["InstallLocation"]
    
    def remount(self, drive_letter):
        self.update_path("A")
        restart_epic_launcher()
        self.update_path(drive_letter)
        restart_epic_launcher()
        print("reaseating complete")
        
        
        
    





for filename in os.listdir(path):
    if filename != "Pending":
        file_path = os.path.join(path, filename)
        game(filename, file_path)


for g in game.instances:
    if game.instances[g].external:
        print(g)

print(game.instances)
for k in game.instances:
    g = game.instances[k]
    print(f"before {g.installPath}")
    if g.external == True:
        if input(f"Do you want to move {g.name}? Y/N") == "Y":
            g.remount(input("Where do you want to move this file"))






