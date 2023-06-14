# Human or Horse?
### You can try to test the model running the colab file in this subdirectory!

This is a subdirectory dedicated to a Convolutional Neural Network model created with the main goal of detecting a myriad of filters from human and horse images with different patterns and ultimately classify a test set according to previously learned image data.

The motivation behind the project was to further understand how computer vision works as I was currently learning how to apply machine learning algorithms and models in Arduino microcontrollers with embedded systems.

## How was the model built?
The model was created mainly using `tensorflow` and its architecture follows a Sequential structure. It consists of a few *Convolutional* and *Max-pooling* layers followed by a series of *Dense* layers, which ultimately output the result using a `sigmoid` activation function.

## How was the model trained?
-  The model resizes every input image from the training set, as well as the validation set, to a given size for the sake of consistency.
-  On every `epoch` that the model goes through new data is pumped in and variation is added in order to increase learning generalization.
-  After every training `epoch` newly trained weights are tested against the validation set.
-  The loss function used for compiling the neural network was `binary_crossentropy` since there are only two possible results; on the other hand, the optimizer used was `adam` and a learning rate of *0.001* was applied throughout the training process, which seemed to produce the best results.

## Results obtained
Overall the accuracy during training reached a value of approximately *99%* after around 30 `epochs`, which is not surprising; the main takeaway however being that the current model had a validation accuracy of around *75%*, which is pretty decent for the amount of available training data utilized.

The model seemed to struggle with certain cases in which the input didn't show clear differences, such as those in which the human or the horse were almost fully horizontal or vertical. The expectation is that increasing `shear` and `rotation` and retraining with new parameters should give a more accurate classification model.
