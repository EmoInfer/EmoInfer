# GUIEmotionAnalysis

**Dependencies:** To run _EmoInfer_, 
* [OpenFace](https://github.com/TadasBaltrusaitis/OpenFace/wiki#installation) must be installed on the machine.
* PyQt5 and QtMultimedia should be installed


To run the app,

1. Go to the _'app.py'_ file and modify the variable _'OpenFacePath'_ to be the path of OpenFace in your local machine.

2. Run the following command in the head directory:

```python3 app.py```

**Emotion Extraction:** There are options of binary/continuous extractions in the app and one can toggle the hyperparameters.
* First, facial action units are detected in the video and saved per frame in a file called _'{filename}.csv'_ in the _'{HEAD}/processed'_ folder.
* After emotion extraction, a file named _'extracted.csv'_ is saved in the same directory which has details of the emotions detected in the frame according to 3 coding schemes.

**Analysis:** This enables to statistically analyse the emotions extracted in the video. Images showing resultant graphs are saveed in the head directory itself.Overall statistics of the video according to the coding scheme is saved in _'{coding scheme}.png'_ and the emotion-wise results are saved in _'{coding scheme}{emotion}.png'_.

**Sequencing:** This phase extracts important sequences from emotion sequences occuring in the video. 
