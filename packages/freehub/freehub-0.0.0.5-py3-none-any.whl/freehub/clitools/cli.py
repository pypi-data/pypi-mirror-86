from freehub import apis
import os
os.environ['ANSI_COLORS_DISABLED']="1"
import shutil
import fire

class Cli:

    @classmethod
    def download(cls,key,path=None,overwrite=False):
        path=path or './'
        apis.freehub_download(key,path,overwrite=overwrite)
    @classmethod
    def upload(cls,path,key=None,overwrite=True):
        key=key or os.path.basename(path)
        apis.freehub_upload(path,key,overwrite=overwrite)
def main():
    fire.Fire(Cli)
if __name__ == '__main__':
    main()