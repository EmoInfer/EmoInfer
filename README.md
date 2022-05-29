# EmoInfer 1.0

We offer _EmoInfer_ as a tool to accelerate process-based research on emotions in the Learning Sciences and help educational stakeholders understand the interplay of cognition and affect in ecologically-valid learning situations. _EmoInfer_ provides a simple graphical user interface to streamline automatic annotation and analysis of videos with facial expressions of emotion. _EmoInfer_ can be applied to quantify and visualize the frequency and the temporal dynamics of emotions.

## Installation

**Dependencies:**
* OpenFace (installation instructions [here](https://github.com/TadasBaltrusaitis/OpenFace/wiki#installation))
* PyQt5 (installation instructions [here](https://pypi.org/project/PyQt5/))
* QtMultimedia (installation instructions [here](https://ports.macports.org/port/qt5-qtmultimedia/))


To run _EmoInfer_,

1. Go to the _'app.py'_ file and modify the variable _'OpenFacePath'_ to be the path of OpenFace in your local machine.

2. Run the following command ```python3 app.py``` in the head directory 


## Functionality and Use

**Facial Action Unit Extraction:** _EmoInfer_ provides options of using binary or continuous facial action unit extraction.
* To incorporate action units 53 (head up) and 54 (head down), the head pose threshold for pitch can be set (i.e., the rotation in radians around the X axis; 1 radian = 57.3 deg). 
* To incorporate action units 55 (head tilt left) and 56 (head tilt right), the head pose threshold for roll can be set (i.e., the rotation in radians around the Z axis; 1 radian = 57.3 deg).
* For continuous facial action units, a cutoff intensity above which a facial action unit is considered active needs to be specified (on a scale of 1 to 5). 
* Facial action units detected in the uploaded video(s) are saved per frame in a file called _'{filename}.csv'_ in the _'{HEAD}/processed'_ folder.


**Emotion Inference:** _EmoInfer_ infers emotions from the extracted facial action units, drawing on three culturally-generalizable coding schemes outlined in [Sinha et al., JLS, 2022](https://www.tandfonline.com/doi/full/10.1080/10508406.2021.1964506).
* After emotion extraction, a file named _'extracted/extracted.csv'_ is saved in the same directory, which has the details of the emotions inferred in each frame.


**Analysis:** _EmoInfer_ enables statistical analyses and visualizations of the emotions extracted in the video(s). More details on the analyses possible are outlined in the citation below.
* Images showing resultant graphs are saved in the head directory. 
* Overall statistics of the video(s) relevant to a particular coding scheme are saved in _'{coding scheme}.png'_.
* Emotion-specific results are saved in _'{coding scheme}{emotion}.png'_. 

**Sequencing:** _EmoInfer_ also supports the extraction of important sequences from the inferred emotions in the video. 
* Suggested methodological choices and the underlying rationale can be found [here](https://tinyurl.com/EmoInferSeq).


## Citation

If you use _EmoInfer_ in your work and/or publications, we ask you to kindly cite the following work(s).

**Overall system**

Sinha, T., & Dhandhania, S. 2022. Democratizing emotion research in learning sciences. _In Proceedings of Artificial Intelligence in Education_

**Empirical evidence based on the _EmoInfer_ pipeline**

Sinha, T. 2022. Enriching problem-solving followed by instruction with explanatory accounts of emotions. _Journal of the Learning Sciences_, 31 (2), 151-198, doi: 10.1080/10508406.2021.1964506


## Contact

**Dr. Tanmay Sinha**

Email: tanmay.sinha@gess.ethz.ch

**Sunidhi Dhandhania**

Email: sunidhi@iitk.ac.in
