===========================================
Exp script for var cue learning experiment
===========================================

Contains:
#########

* main experiment script: (latest version as of 21/11/18) exp2.5.2.py
* audio/ subfolder: contains audio files for default speaker and experiment instructions
* audio_speakers/ subfolder: contains audio files for individual speakers and all speaker intros
* images/ subfolder: contains images used in the experiment
* postquest subfolder: contains postquest.html, postquest.js, sendTrialData.php (generates post experiment questionnaire in browser)

To run 
######
1) navigate to experiment directory in terminal

2) ::

    $ python exp2.5.2.py <condition (1-6> <pptID>


Experiment generates
#####################
1) participant datafile - this will be stored in the data/ subfolder (this folder is created if it doesn't already exist)

2) a recordings directory associated with each participant

Notes
-----
Place cuelearning folder on Desktop the experiment is being run on

