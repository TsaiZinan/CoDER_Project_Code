# PREPROCESSING-IMAGES-USING-BRIGHTENING-CLAHE-AND-RETINEX
 
## Author: Zinan Cai (Tsai), Thi Phuoc Hanh Nguyen, Khanh Nguyen

## Document Structure

```
PREPROCESSING-IMAGES-USING-BRIGHTENING-CLAHE-AND-RETINEX <br />
├── Image 
│   ├── data 
│   ├── mask 
│   ├── result_process 
│   ├── result_crop 
│   ├── result_canny 
│   └── result_noise 
├── Result
│   └── [current_time].csv
├── Preprocessing.py
├── crop.py
├── config_processing.json
└── config.json
```

**./Image <br />**
./Image/data: The place of original images. <br />
./Image/mask: The folder of mask images created by crop.py. <br />
./Image/result_process: The folder of images output by Preprocessing.py. <br />
./Image/result_crop: The folder of images after processed by crop method in crop.py. <br />
./Image/result_canny: The folder of images after processed by canny edge detection method in crop.py. <br />
./Image//result_niose: The folder of images after processed by noise reducing method in crop.py. <br />

**./Result <br />**
The folder of final result. <br />

**./Preprocessing.py <br />**
First main program of preprocessing. Fetch all the images in ./Image/data and output the processing image into ./Image/result_process. <br />

**./config_processing.json <br />**
Config file of Preprocessing.py. It storage the parameters of retinex and CLAHE. <br />

**./crop.py <br />**
Main program. Get the images in ./Image/result_process and output all different types of result into different floder (./Image/result_crop, ./Image/result_canny & ./Image//result_niose). Finally, it will general a csv file which included true posttive pixels calculation of each image in ./Image//result_nios. <br />

**./config.json <br />**
Config file of crop.py. <br />
Structure: <br />
```json
{
"image_number":{
              "crop_number":{
                           "x": "x coordinate of crop position",
                           "y": "y coordinate of crop position",
                           "height": "height of crop frame",
                           "width": "width of crop frame",
                           "mask": "coordinate of the whole mask in cropped image"
                           }
              }
}
```
Example:
```json
{
"07":{
        "0":{
            "x"       : 207,
            "y"       : 226,
            "height"  : 136,
            "width"   : 141,
            "mask"   : "[86,18],[86,45],[92,50],[107,51],[114,57],[100,71],[102,81],[118,97],[115,105],[101,103],[81,89],[69,89],[51,107],[43,97],[50,90],[49,75],[22,58],[22,51],[24,49],[56,52],[64,45],[73,19],[76,24],[66,47],[58,56],[27,52],[24,56],[53,72],[52,92],[48,98],[51,101],[68,85],[83,85],[104,100],[112,101],[113,97],[98,79],[97,69],[108,57],[87,50],[82,42],[82,23]"
        },
        "1":{
            "x"       : 331,
            "y"       : 1859,
            "height"  : 224,
            "width"   : 214,
            "mask"   : "[107,90],[125,109],[210,142],[199,145],[113,118],[105,125],[112,149],[123,173],[135,178],[135,199],[124,202],[121,199],[116,172],[99,149],[94,128],[80,115],[1,137],[1,129],[76,105],[81,87],[72,65],[72,48],[75,48],[88,75],[88,79],[94,85],[95,68],[107,44],[120,31],[149,16],[150,21],[130,33],[113,53],[107,66]"
        }
    }
}
```

## Steps:

1. Put all the images into ./Image/data folder. <br />
 <br />
 
2. Run the ./Preprocessing.py. You can change the parameter in ./config.json if you wish. <br />
 <br />
 
3. Mark all the targets you want to crop out and recoed the coordinates into ./config.json as "x", "y", "height" and "width". "image_number" and "crop_number" are needed to record as well. <br />
Example: <br />
![Imgur](https://i.imgur.com/DkmdrHu.jpg)
<br />

4. Run the ./crop.py. <br />
 <br />
 
5. The result will storaged into ./Result/[current_time].csv. First column is the filename. Second column is the calculation of white pixels in that image. The last one is the black pixels. <br />
Example:
```
00.00_crop_0_noise_reduce.jpg  2424  131646
00.00_crop_1_noise_reduce.jpg  2631  117507
00.00_crop_2_noise_reduce.jpg  2829  224142
00.00_crop_3_noise_reduce.jpg  4620  267387
00.00_crop_4_noise_reduce.jpg  3192  175092
00.00_crop_5_noise_reduce.jpg  2136  95043
00.01_crop_0_noise_reduce.jpg  2586  132060
00.01_crop_1_noise_reduce.jpg  2655  117621
00.01_crop_2_noise_reduce.jpg  2826  224253
```
 <br />
 
 ## Ps:
 If the program can't output the result images properly without any error, try rerun the crop.py few more times. </br>
 

