import os
import argparse
import sys
import subprocess
import glob
import shutil
import dvc.api

from collections import Counter
from git.repo.base import Repo
from smexperiments.tracker import Tracker
import torchvision.transforms as T
from torchvision.io import read_image
from torchvision.utils import save_image
# from torchvision.datasets.utils import extract_archive
from utils import extract_archive
from sklearn.model_selection import train_test_split 
from pathlib import Path


dvc_repo_url = "codecommit::us-east-1://sagemaker-intel-classification"#os.environ.get('DVC_REPO_URL')
dvc_branch = "project-dataset"#os.environ.get('DVC_BRANCH')

git_user = os.environ.get('GIT_USER', "sushant")
git_email = os.environ.get('GIT_EMAIL', "sushantgautm@gmail.com")

ml_root = Path("/opt/ml/processing")

dataset_zip = ml_root / "input" / "intel.zip"
git_path = ml_root / "sagemaker-intel-classification"

# define transformt o resize the image with given size
transform = T.Compose([T.Resize(size = (224, 224)),
                      T.ToPILImage()])

def configure_git():
    subprocess.check_call(['git', 'config', '--global', 'user.email', f'"{git_email}"'])
    subprocess.check_call(['git', 'config', '--global', 'user.name', f'"{git_user}"'])
    
def clone_dvc_git_repo():
    print(f"\t:: Cloning repo: {dvc_repo_url}")
    
    repo = Repo.clone_from(dvc_repo_url, git_path.absolute(), allow_unsafe_protocols=True)
    
    return repo

def sync_data_with_dvc(repo):
    os.chdir(git_path)
    print(f":: Create branch {dvc_branch}")
    try:
        repo.git.checkout('-b', dvc_branch)
        print(f"\t:: Create a new branch: {dvc_branch}")
    except:
        repo.git.checkout(dvc_branch)
        print(f"\t:: Checkout existing branch: {dvc_branch}")
    print(":: Add files to DVC")
    
    subprocess.check_call(['dvc', 'add', "dataset"])
    
    repo.git.add(all=True)
    repo.git.commit('-m', f"'add data for {dvc_branch}'")
    
    print("\t:: Push data to DVC")
    subprocess.check_call(['dvc', 'push'])
    
    print("\t:: Push dvc metadata to git")
    repo.remote(name='origin')
    repo.git.push('--set-upstream', repo.remote().name, dvc_branch, '--force')

    sha = repo.head.commit.hexsha
    
    print(f":: Commit Hash: {sha}")

def write_dataset(image_paths, output_dir):
    for img_path in image_paths:
        img_path = Path(img_path)
        Path(output_dir / img_path.parent.stem).mkdir(parents=True, exist_ok=True)
        shutil.copyfile(img_path, output_dir / img_path.parent.stem / img_path.name)

def resize_image():
    dataset_extracted = ml_root / "tmp"
    dataset_extracted.mkdir(parents=True, exist_ok=True)
    
    # split dataset and save to their directories
    print(f":: Extracting Zip {dataset_zip} to {dataset_extracted}")
    extract_archive(
        from_path=dataset_zip,
        to_path=dataset_extracted
    )
    # print all the files in the directory
    print("##############: Files ############")
    print(os.listdir(dataset_extracted))
    print("############## ::: ############")
    dataset_train = list((dataset_extracted / "train").glob("*/*.jpg"))
    labels = [x.parent.stem for x in dataset_train]
    
    print(":: Dataset train Class Counts: ", Counter(labels))
    dataset_test = list((dataset_extracted / "test").glob("*/*.jpg"))
    labels = [x.parent.stem for x in dataset_test]
    
    print(":: Dataset test Class Counts: ", Counter(labels))
    # not use Path in following code:
    dataset_extracted ="/opt/ml/processing/"+"tmp"

    d_train = glob.glob(dataset_extracted+"/train/*/*.jpg")
    print("Total train files:", len(d_train))
    # print("D_train",d_train[:100])


    d_test = glob.glob(dataset_extracted+"/test/*/*.jpg")
    print("Total test files:", len(d_test))
    # print("D_test",d_test[:100])

    
    # resize and save on same location
    for p in d_train:
        img = read_image(p)
        img = transform(img)
        img.save(p)
        
    # resize and save on same location
    for p in d_test:
        img = read_image(p)
        img = transform(img)
        img.save(p)
        
    
    for path in ['train', 'test']:
        output_dir = git_path / "dataset" / path
        print(f"\t:: Creating Directory {output_dir}")
        output_dir.mkdir(parents=True, exist_ok=True)
        
    print(":: Writing train, test into Datasets")
    write_dataset(dataset_train, git_path / "dataset" / "train")
    write_dataset(dataset_test, git_path / "dataset" / "test")
     
    
if __name__=="__main__":
    parser = argparse.ArgumentParser()
    
    # setup git
    print(":: Configuring Git")
    configure_git()
    
    print(":: Cloning Git")
    repo = clone_dvc_git_repo()
    
    # Resize image 
    print(":: Resize Image")
    resize_image()
        
    print(":: copy data to train")
    subprocess.check_call('cp -r /opt/ml/processing/sagemaker-intel-classification/dataset/train/* /opt/ml/processing/dataset/train', shell=True)
    subprocess.check_call('cp -r /opt/ml/processing/sagemaker-intel-classification/dataset/test/* /opt/ml/processing/dataset/test', shell=True)
    
    # print(":: Sync Processed Data to Git & DVC")
    # sync_data_with_dvc(repo)

 