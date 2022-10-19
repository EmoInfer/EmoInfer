# EmoInfer 1.0

We offer _EmoInfer_ as a tool to accelerate process-based research on emotions in the Learning Sciences and help educational stakeholders understand the interplay of cognition and affect in ecologically-valid learning situations. _EmoInfer_ provides a simple graphical user interface to streamline automatic annotation and analysis of videos with facial expressions of emotion. _EmoInfer_ can be applied to quantify and visualize the frequency and the temporal dynamics of emotions.

## Installation

**Dependencies:**
* OpenFace (installation instructions [here](https://github.com/TadasBaltrusaitis/OpenFace/wiki#installation))
* PyQt5 (installation instructions [here](https://pypi.org/project/PyQt5/))
* QtMultimedia (installation instructions [here](https://ports.macports.org/port/qt5-qtmultimedia/))
* Typing-Extensions (installation instructions [here](https://pypi.org/project/typing-extensions/), in some cases an additional ```--upgrade``` may be needed)

To run _EmoInfer_,

1. Go to the _'app.py'_ file and modify the variable _'OpenFacePath'_ to be the path of OpenFace in your local machine.

2. Run the following command ```python3 app.py``` in the head directory.

3. Upload one or multiple videos for which to extract emotion incidence and dynamics.


## Functionality and Use

![EmoInferREADME drawio](https://user-images.githubusercontent.com/48733306/181459962-473db2b8-7f54-4212-a8c6-baf55ee28a81.png)


**1. Facial Action Unit Extraction:** _EmoInfer_ provides options of using binary or continuous facial action unit extraction.
* To incorporate action units 53 (head up) and 54 (head down), the head pose threshold for pitch can be set (i.e., the rotation in radians around the X axis; 1 radian = 57.3 deg). 
* To incorporate action units 55 (head tilt left) and 56 (head tilt right), the head pose threshold for roll can be set (i.e., the rotation in radians around the Z axis; 1 radian = 57.3 deg).
* For continuous facial action units, a cutoff intensity above which a facial action unit is considered active needs to be specified (on a scale of 1 to 5). 
  * We recommend conducting sensitivity analyses to set this cutoff for your data. For ecologically-valid learning situations, facial action unit intensities can be expected to be moderate on average. Individual differences (e.g., some students maybe more expressive than others or take longer to return to baseline facial configurations), however may affect this cutoff.
* Facial action units detected in the uploaded video(s) are saved per frame in _'{filename}.csv'_ in the _'{HEAD}/processed'_ folder.


**2. Emotion Inference:** _EmoInfer_ infers emotions from the extracted facial action units, drawing on three culturally-generalizable coding schemes outlined in [Sinha et al., JLS, 2022](https://www.tandfonline.com/doi/full/10.1080/10508406.2021.1964506).
* After emotion extraction, a file called _'extracted__{filename}_.csv'_ is saved in the _'{HEAD}/extracted'_ folder, with the details of emotions inferred in each frame.


**3. Analysis:** _EmoInfer_ enables statistical analyses and visualizations of the emotions extracted in the video(s). More details on the analyses possible are outlined in the citation below.
* Images showing resultant graphs are saved in the _'{HEAD}/images'_ folder.
* Overall statistics of the video(s) relevant to a particular coding scheme are saved in the _'{HEAD}/images/{coding scheme}/{video id}'_ folder.
* Emotion-specific results are saved in _'{HEAD}/images/{coding scheme}/{video id}/{emotion}.png'_. 
* Time granularity: The time granularity of the analysis can be modified to 'n' frames. A threshold of 50% is used for inferring the presence of an emotion in a bucket of 'n' frames. The modified file of extracted emotions is saved in the _'{HEAD}/extracted'_ folder as _'extracted__{filename}\__{time_granularity}.csv'_ . Each row in this file can be read off as an aggregate of the k_th_ block of 'n' frames, where 'k' corresponds to the frame-id.

**4. Sequencing:** _EmoInfer_ also supports the extraction of important sequences from the inferred emotions in the video. 
* After the extraction of emotion sequences, three files are saved in the _'{HEAD}/sequencing/{coding scheme}/{video id}'_ folder, with the details of emotion sequences inferred for each coding scheme and video.
  * _'final_sequences.txt'_: sequences of multiple lengths

  * _'final_mult_sequences.txt'_: sequences comprising multiple emotions

  * _'final_uniq_sequences.txt'_: sequences for every unique emotion
* Suggested methodological choices and the underlying rationale can be found [here](https://tinyurl.com/EmoInferSeq).
* The last used setting for time granularity from the Analysis tab is reflected in the sequencing as well.


## Note

* Steps 3 (analysis) and 4 (sequencing) use the intermediate files generated from steps 1 (facial action unit extraction) and 2 (emotion inference). As long as those intermediate files have been generated apriori, steps 3 and 4 do not need to be performed synchronously. This allows, for example, picking up previously unfinished analyses at a later point in time. For asynchronous analyses, simply upload the corresponding video file to _EmoInfer_ and directly proceed with steps 3 or 4.
* Steps 3 and 4 are independent of each other and can be performed in any order.
* We recommend using python 3.7.3 and above to run _EmoInfer_. 

## Citation

If you use _EmoInfer_ in your work and/or publications, we ask you to kindly cite the following work(s).

**Overall system**

Sinha, T., Dhandhania, S. 2022. Democratizing emotion research in learning sciences. In: Rodrigo, M.M., Matsuda, N., Cristea, A.I., Dimitrova, V. (eds) _Artificial Intelligence in Education_. Lecture Notes in Computer Science, vol 13356. Springer, Cham. doi: 10.1007/978-3-031-11647-6_27

**Empirical evidence motivating development of the _EmoInfer_ pipeline**

Sinha, T. 2022. Enriching problem-solving followed by instruction with explanatory accounts of emotions. _Journal of the Learning Sciences_, 31 (2), 151-198, doi: 10.1080/10508406.2021.1964506


## Contact

**Dr. Tanmay Sinha**

Email: tanmay.sinha@gess.ethz.ch

**Sunidhi Dhandhania**

Email: sunidhi@iitk.ac.in
