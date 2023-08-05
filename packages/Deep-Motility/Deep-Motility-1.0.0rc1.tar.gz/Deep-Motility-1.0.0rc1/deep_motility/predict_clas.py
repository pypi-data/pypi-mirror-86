from fastai.vision.all import *
import fastai
import os 
from imutils import paths
import shutil
import tqdm
import urllib.request


#------------Download weights--------------------------------------

weights = str(Path.home())+f"{os.sep}.deep-motilidad{os.sep}models{os.sep}"+ "motilidadResNet50.pkl"


url = "https://www.dropbox.com/s/56ebyizjhozirwi/motilidadResNet50.pkl?dl=1"
if  not os.path.exists(weights):
    os.makedirs(os.path.dirname(weights), exist_ok=True)
    urllib.request.urlretrieve(url, filename=weights)


learn=load_learner(fname=weights)



def predict_classification(input_folder, output_folder):
    
    os.makedirs(output_folder+"/complete",exist_ok=True)
    os.makedirs(output_folder+"/incomplete",exist_ok=True)
    
    for img in os.listdir(input_folder):
        prediction=learn.predict(input_folder+img)[0]
        if(prediction=='Complete'):
            shutil.copy(input_folder+img,output_folder+"complete/"+img)
        else:
            shutil.copy(input_folder+img,output_folder+"incomplete/"+img)
