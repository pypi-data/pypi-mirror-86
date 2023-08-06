from freehub import git_ops
from freehub.utils import *
import logging

_BRANCH_DICT='branch_dict'
_FAKE2TRUE='fake2true'
_TRUE2FAKE='true2fake'
_BRANCH_LIST='remote_branch_list'
USER_HOME=os.path.expanduser('~')
STORE_HOME=USER_HOME+'/.store'
BRANCH_LIST_DIR=STORE_HOME+'/BranchLists'
SHADOW_STORE_HOME=STORE_HOME+'/ShadowStores'
STORE_TMP_DIR=STORE_HOME+'/tmp'
STORE_CLASS_DIR=STORE_HOME+'/Store.Class'
FREEHUB_LOCATION='https://OpenGitspace:Gitspace@123456@gitee.com/OpenGitspace/meta'

def copy_repo_files_to(src,dst):
    if not os.path.exists(dst):
        os.makedirs(dst)
    assert os.path.isdir(dst)
    for child in os.listdir(src):
        if child=='.git':
            continue
        child_path=os.path.join(src,child)
        dst_child_path=os.path.join(dst,child)
        if os.path.isdir(child_path):
            shutil.copytree(child_path,dst_child_path)
        else:
            shutil.copy(child_path,dst_child_path)
def download_branch(remote_location,branch,dst,overwrite=False):
    check_and_make_empty_dir(dst,overwrite)
    repo=git_ops.git_init(dst)
    git_ops.create_head(repo)
    git_ops.pull_remote_branch(repo,remote_location,branch)

def upload_branch(repo,remote_location,branch,overwrite=False):
    if git_ops.exists_remote_branch(remote_location,branch):
        if not overwrite:
            raise Exception('Remote branch %s already exists at %s .'%(branch,remote_location))
        else:
            logging.warning('Will overwrite remote branch %s at %s .'%(branch,remote_location))
    else:
        logging.info('Will upload to a new branch %s at %s .'%(branch,remote_location))
    branches=git_ops.list_branch(repo)
    if not branch in branches:
        raise Exception('Local branch %s does not exist.'%(branch))
    git_ops.push_local_branch(repo, branch, remote_location)



def download_to_dir(remote_location,branch,dst,cache_dir=None,overwrite=True):
    cache_dir=cache_dir or os.path.join(STORE_HOME,branch)
    check_and_make_empty_dir(cache_dir,overwrite=True)
    download_branch(remote_location,branch,dst=cache_dir,overwrite=overwrite)
    copy_repo_files_to(cache_dir,dst)

def upload_to_remote(remote_location,branch,src,cache_dir=None,overwrite=True):
    cache_dir = cache_dir or os.path.join(STORE_HOME, branch)
    check_and_make_empty_dir(cache_dir,overwrite=True)
    dst_path=os.path.join(cache_dir,os.path.basename(src))
    if os.path.isdir(src):
        shutil.copytree(src,dst_path)
    else:
        shutil.copy(src,dst_path)
    repo=git_ops.git_init(cache_dir)
    git_ops.create_head(repo)
    git_ops.create_branch(repo,branch,force=True)
    git_ops.switch_branch(repo,branch,recover=False)
    git_ops.stage_all_changes(repo)
    git_ops.commit_current_branch(repo)
    upload_branch(repo,remote_location,branch,overwrite=overwrite)

def freehub_download(src,dst,overwrite=False):
    download_to_dir(FREEHUB_LOCATION,src,dst,overwrite=overwrite)
def freehub_upload(src,dst,overwrite=False):
    upload_to_remote(FREEHUB_LOCATION,dst,src,overwrite=overwrite)


def test():
    default_remote_location = FREEHUB_LOCATION
    repo_path = './data/OpenGitspace'
    import wk
    wk.remake(repo_path)

    # repo_path = './data/'
    # download_branch(default_remote_location,'test',repo_path)
    # upload_branch(default_remote_location,'test2',repo_path,overwrite=True)
    # download_to_dir(default_remote_location,'test',repo_path)
    # upload_to_remote(default_remote_location,'0',repo_path,overwrite=True,cache_dir='data/cache')
    # upload_to_remote(default_remote_location,'0',repo_path,overwrite=True,cache_dir='data/cache')

    wk.Folder(repo_path).open('readme.txt','w').write('yes')
    #freehub
    freehub_upload(repo_path,'0')
    shutil.rmtree(repo_path)
    freehub_download('0',os.path.dirname(repo_path))
if __name__ == '__main__':
    test()







