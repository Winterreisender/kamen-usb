# %%
from typing import List
import psutil
from pathlib import Path
import winsound
import json
from time import sleep

kamen_drives = []
class KamenDrive:
    def play_sound(self):
        sound_file = self.root/'add.wav'
        try:
            winsound.PlaySound(str(sound_file),winsound.SND_FILENAME)
        except Exception as err:
            print(err)

    def on_remove(self):
        print(f"Removed: {self.root}")

    def __init__(self, root :Path) -> None:
        self.root = root
        self.comboed = False

        with (self.root / 'info.json').open() as file:
            self.info = json.load(file)

        print(f"New: {self.info['type']}")
        self.play_sound()


def combo(drives :List[KamenDrive]):
    henshinable = {
        ('Trigger', 'Fang') : './private/luna_trigger.wav'
    }
    unhenshined_drive_types = [ drive.info['type'] for drive in drives if not drive.comboed ]
    for requires,henshinsound in henshinable.items():
        if all([ require in unhenshined_drive_types for require in requires ]):
            # 播放变身音效
            winsound.PlaySound(str(henshinsound),winsound.SND_FILENAME)

            # 将变身过的Memory设为不可再变身
            for drive in drives:
                if drive.info['type'] in requires and not drive.comboed:
                    drive.comboed = True

# 获取所有U盘的根路径, 例: ["F:\kamen", "G:\kamen"]
def get_roots():
    usb_drive_roots = [Path(device.mountpoint)/'kamen' for device in psutil.disk_partitions() if device.opts.find('removable')!=-1]
    return [path for path in usb_drive_roots if path.exists()]

# 获取新添加的U盘的根路径 例: ["F:\kamen", "G:\kamen"]
cached_roots = []
def get_new_roots(current_roots :List[Path]):
    global cached_roots

    # 获取差别
    new_roots = set(current_roots) - set(cached_roots)
    removed_roots = set(cached_roots) - set(current_roots)

    # 更新缓存
    cached_roots = current_roots

    return list(new_roots),list(removed_roots)

# 按条件删掉列表元素
# remove_if([1,3,4,5], lambda x: x % 2==1, lambda x:print(x))
def remove_if(l :List, conditon, before_remove):
    to_remove = [x for x in l if conditon(x)]
    for i in to_remove:
        before_remove(i)
        l.remove(i)

def main():
    global kamen_drives
    print("Running...")
    while(True):
        current_roots = get_roots() # 当前所有U盘
        new_roots,removed_roots = get_new_roots(current_roots) #新的U盘

        for root in new_roots:
            kamen_drives.append(KamenDrive(root))

        for root in removed_roots:
            remove_if(
                kamen_drives,
                conditon = lambda x: x.root == root,
                before_remove= lambda x: x.on_remove()
            )
        
        combo(kamen_drives)
        sleep(1.0)
# %%
if __name__ == '__main__':
    winsound.PlaySound('./private/luna_trigger.wav',winsound.SND_FILENAME)
    #main()