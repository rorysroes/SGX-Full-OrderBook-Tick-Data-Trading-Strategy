## Modeling High-Frequency Limit Order Book Dynamics Using Machine Learning 

* Framework to capture the dynamics of high-frequency limit order books.

  <img src="./Graph/pipline.png" width="650">
  
#### Overview

In this project I used machine learning methods to capture the high-frequency limit order book dynamics and simple trading strategy to get the P&L outcomes.

* Feature Extractor

  * Rise Ratio
  
    <img src="./Graph/Price_B1A1.png" width="650">

  * Depth Ratio
  
    <img src="./Graph/depth.png" width="650">
    
    [Note] : [Feature_Selection] (Feature_Selection) 
 
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
   
   [Note] : [Model_Selection] (Model_Selection) 

 

