import streamlit as st
import pandas as pd

import streamlit as st
# Include PIL, load_image before main()
import torch
from matplotlib import pyplot as plt
import cv2
from PIL import Image
import os
import pandas as pd
import html
from apps.displayhtml import display_html

def load_image(image_file):
    img = Image.open(image_file)
    return img

def save_uploadedfile(uploadedfile):
         with open(os.path.join("images",uploadedfile.name),"wb") as f:
                 f.write(uploadedfile.getbuffer())
         return st.success("Saved File:{} to images".format(uploadedfile.name))

def show_images(uploadedfile):
    from IPython.display import Image #this is to render predictions
    Image(filename=os.path.join("images",uploadedfile.name), width=1000)

def my_round(n):
        lower = (n//100)*100;
        upper = lower+100;
        if (n-lower)<(upper-n):
                return int(lower)
        return int(upper)
global str
def group_html_tags(df,requiredboxes):
    group = {}
    i=0
    #print(df,"================")
    for column in df:
        #print("acolumn",column)
        listcolumn = {}
        list_columns = []
        for rownum,(indx,value) in enumerate(df[column].items()):
            #print('value ',value)
            if(value ==1):
                column = int(column)
                new_df = requiredboxes[( requiredboxes['xminnew'] ==indx) & (requiredboxes['yminnew'] ==column) ]
                #listcolumn[indx] = new_df.iloc[0,0]
                function_name    = new_df.iloc[0,0]

                # Get class from globals and create an instance
                func =  globals()[function_name]
                listcolumn[indx] = func()
                #print("aaac index",indx)
                group[i] = listcolumn
        i +=1
    return group
def Checkbox():
    return '<label >Check Box </label> <input type="checkbox" id="vehicle1" name="vehicle1" value="Bike" class="myinput">'
def TextBox():
    return '<label >Text Box </label> <input type="text" id="fname" name="fname" class="textfield">'
def Button():
    return ' <button type="button" class="button">Click Me!</button> '
def Select():
    return '<div class="select"><select><option>Option 1</option><option>Option 2</option><option>Option 3</option><option>Option 4</option><option>Option 5</option></select></div>'

def app():
    st.subheader("Image")
    image_file = st.file_uploader("Upload Images", type=["png","jpg","jpeg"])
    #print(image_file)

    #Model
    model = torch.hub.load('yolov5', 'custom', path='yolov5/train/best.pt', source='local')  # local repo

    if image_file is not None:

        file_details = {"filename":image_file.name, "filetype":image_file.type,"filesize":image_file.size}
        save_uploadedfile(image_file)

        #print(file_details['filename'])

        # Images
        image_name =os.path.join("images",file_details['filename'])
        img = cv2.imread(image_name)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY )
        # Inference
        results = model(img, size=328)  # includes NMS

        # Results
        #results.print()  
        results.show()  # or .show()
        results.save()  # or .show()

        #results = results.xyxy[0]  # img1 predictions (tensor)
        boxes = results.pandas().xyxy[0]  # img1 predictions (pandas)
        #print("Boxes -----------------------------",boxes)
        #show_images(image_file)
        boxes['xminnew'] = boxes.apply(lambda x: my_round(x.xmin), axis=1)
        boxes['yminnew'] = boxes.apply(lambda x: my_round(x.ymin), axis=1)
        requiredboxes =  boxes[boxes.columns[-3:]]
        #print("==================",requiredboxes.head())
        dfb = requiredboxes.set_index('xminnew')
        df = pd.get_dummies(dfb.yminnew, prefix='', prefix_sep='').groupby(axis=1, level=0).max()
        df = df.sort_index()
        #print(df.head())
        #print ("df ====data===========")

        #columns = requiredboxes.groupby(['xminnew']).size().reset_index(name='columns_counts')
        #columns
        #number_row = requiredboxes.groupby(['yminnew']).size().reset_index(name='row_counts')
        #requiredboxes.info()



        complete_info =     group_html_tags(df,requiredboxes)
        #print (complete_info)
        #print ("dfb====complete_info===========")

        olddf = pd.DataFrame(data=complete_info)
        olddf = olddf.fillna(' ').T
        #print("Ddshdhdh",olddf)
        #print ("dNew===============")

        olddf = olddf.sort_index(axis=1)
        html_old = olddf.to_html(header=False,index=False,na_rep='&nbsp;',border=0)

        decoded_old = html.unescape(html_old)
        #print("saasas")
        #print(decoded_old)
        #print("decoded_old")
        #new_ext = ".html"
        #name_without_ext = os.path.splitext(image_name)[0]
        #name_without_ext2 = os.path.splitext(image_name)[0]
        #os.rename(image_name, name_without_ext + ".html")
        #os.rename(image_name, name_without_ext2 + "_output.html")
        #print(image_name)
        default_file     = "default.html"
        output_file      = "output.html"
        default_filename = os.path.join("html",default_file)
        output_filename  = os.path.join("html",output_file)
        from pathlib import Path
        my_file = Path(output_filename)
        if my_file.exists():
                my_file.unlink()

        input_file = open(default_filename, 'r')
        output_file = open(output_filename, 'w')
        #print(decoded_old)
        lines = input_file.readlines()


        for index, line in enumerate(lines):
            output_file.write(line)
            if line.strip() == '<body>':
                output_file.write(decoded_old)
            
        output_file.close()
        input_file.close()
        #st.download_button('Download file', output_file)
        display_html()



