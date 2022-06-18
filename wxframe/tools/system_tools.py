'''

Functions for identifying key paths in system

'''

import os, platform

sep = "\\" if platform.system() == 'Windows' else "/"

def get_wrkdir_from_file( file ):
    return os.path.abspath(os.path.join(file, os.pardir))
    
    
def get_pardir_from_file( file ):
    return os.path.abspath(os.path.join(get_wrkdir_from_file(file), os.pardir))


def get_imgdir_from_pardir( repodir ):
    return repodir + sep + "img" + sep


def get_upddir_from_pardir( repodir ):
    return repodir + sep + "upd" + sep


def get_imgdir( ):
    repo_dir = os.path.abspath(os.path.join(get_pardir_from_file(__file__), os.pardir))
    return get_imgdir_from_pardir( repo_dir )


def get_upddir( ):
    repo_dir = os.path.abspath(os.path.join(get_pardir_from_file(__file__), os.pardir))
    return get_upddir_from_pardir( repo_dir )


def get_dirs_from_file( file ):
    wrkdir = get_wrkdir_from_file(file)
    pardir = get_pardir_from_file(file)
    imgdir = get_imgdir_from_pardir(pardir)
    return wrkdir, pardir


img_dir = get_imgdir( )
upd_dir = get_upddir( )

if __name__ == "__main__":
    print(img_dir)