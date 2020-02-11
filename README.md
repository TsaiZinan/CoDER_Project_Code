# PREPROCESSING-IMAGES-USING-BRIGHTENING-CLAHE-AND-RETINEX
 

## Document Structure

PREPROCESSING-IMAGES-USING-BRIGHTENING-CLAHE-AND-RETINEX
├── Image
    ├── data
    ├── mask
    ├── result_process
    ├── result_crop
    ├── result_canny
    └── result_noise    
├── Result
    └── [current_time].csv
├── Preprocessing.py
├── crop.py
├── config_processing.json
└── config.json


./Image
./Image/data: The place of original images.
./Image/mask: The folder of mask images created by crop.py.
./Image/result_process: The folder of images output by Preprocessing.py.
./Image/result_crop: The folder of images after processed by crop method in crop.py.
./Image/result_canny: The folder of images after processed by canny edge detection method in crop.py.
./Image//result_niose: The folder of images after processed by noise reducing method in crop.py.

./Result
The folder of final result.

./Preprocessing.py
First main program of preprocessing. Fetch all the images in ./Image/data and output the processing image into ./Image/result_process.

./config_processing.json
Config file of Preprocessing.py. It storage the parameters of retinex and CLAHE.

./crop.py
Main program. Get the images in ./Image/result_process and output all different types of result into different floder (./Image/result_crop, ./Image/result_canny & ./Image//result_niose). Finally, it will general a csv file which included true posttive pixels calculation of each image in ./Image//result_nios.

./config.json
Config file of crop.py.
Structure:
{
"image_number"{
              "crop_number"{
                           "x": x coordinate of crop position
                           "y": y coordinate of crop position
                           "height": height of crop frame
                           "width": width of crop frame
                           "mask": "coordinate of the whole mask in cropped image"
                                   Example: "[1,1],[2,4],[9,2]"
                           }
              }
}
