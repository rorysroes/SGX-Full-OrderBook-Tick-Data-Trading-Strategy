# SGX-OrderBook-Tick-Data-Trading-Strategy

#### Modeling High-Frequency Limit Order Book Dynamics Using Machine Learning 

* Framework to capture the dynamics of high-frequency limit order books.
  <img src="./Graph/pipline.png" width="650">

* Feature Extractor

  * Rise Ratio
  
  ![png](Graph/Price_B1A1.png)

  * Depth Ratio
  
  ![png](Graph/depth.png)
 
* Learning Model Trainer
  
  *  RandomForestClassifier
  *  ExtraTreesClassifier
  *  AdaBoostClassifier
  *  GradientBoostingClassifier
  *  SVM
  
*  Use best model to predict next 10 seconds

![png](Graph/CV_Best_Model.png)

*  Prediction outcome

![png](Graph/prediction.png)

* Profit & Loss

![png](Graph/P_L.png)

[Note] : Detail http://140.119.164.203/dm_team11/
 

