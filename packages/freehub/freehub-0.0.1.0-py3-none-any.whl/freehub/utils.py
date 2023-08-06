import os
import glob
import shutil
def is_empty_dir(path):
    return os.path.exists(path) and os.path.isdir(path) and len(os.listdir(path))==0
def clean_dir(path):
    assert os.path.isdir(path)
    for item in os.listdir(path):
        child_path=os.path.join(path,item)
        if os.path.isdir(child_path):
            shutil.rmtree(child_path)
        else:
            os.remove(child_path)
def check_and_make_empty_dir(dst,overwrite):
    if os.path.exists(dst):
        if os.path.isfile(dst):
            if overwrite:
                os.remove(dst)
                os.makedirs(dst)
            raise NotADirectoryError('Not a directory:%s'%(dst))
        elif not is_empty_dir(dst):
            if overwrite:
                clean_dir(dst)
            else:
                raise RuntimeError('Directory nor empty : %s'%(dst))
    else:
        os.makedirs(dst)
def generate_hash(s,times=1):
    assert times>=1
    import hashlib
    m = hashlib.md5()
    def gen():
        m.update(s.encode('utf-8'))
        return m.hexdigest()[:10]
    for i in range(times):
        data=gen()
    return data