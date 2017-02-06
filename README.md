## Modeling High-Frequency Limit Order Book Dynamics Using Machine Learning 

* Framework to capture the dynamics of high-frequency limit order books.

  <img src="./Graph/pipline.png" width="650">
  
#### Overview

In this project I implemented machine learning methods to capture the high-frequency limit order book dynamics and used simple trading strategy to get the P&L outcomes.


* Feature Extractor

  * Rise Ratio
  
    <img src="./Graph/Price_B1A1.png" width="650">

  * Depth Ratio
  
    <img src="./Graph/depth.png" width="650">
 
* Learning Model Trainer
  
  *  RandomForestClassifier
  *  ExtraTreesClassifier
  *  AdaBoostClassifier
  *  GradientBoostingClassifier
  *  SVM
  
*  Use best model to predict next 10 seconds

   <img src="./Graph/CV_Best_Model.png" width="650">

*  Prediction outcome

   <img src="./Graph/prediction.png" width="650">

*  Profit & Loss

   <img src="./Graph/P_L.png" width="650">

[Note] : Detail http://140.119.164.203/dm_team11/
 

