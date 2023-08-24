import tensorflow as tf
import os

# Variables for image resizing
IMG_WIDTH = 100
IMG_HEIGHT = 100

def main():
    """
    Load data from image files and train a convolutional neural network to 
    classify them according to the category the picture belongs to.
    
    Optionally the fit model can be saved as an .h5 file for later use
    """
    training, validation = data_load()
    model = get_model()
    
    # Train the model and use a validation set to test accuracy
    model.fit(
        training, 
        steps_per_epoch=8,
        epochs=50,
        verbose=1,
        validation_data=validation
    )
    
    # Save model to file
    filename = "human-horse-classifier.h5"
    model.save(filename)
    print(f"Model saved to {filename}.")
    

def data_load():
    """
    Loads data from local files into memory through a generator that changes 
    pictures' configurations to add variety to training purposes and avoid overfitting.

    Returns:
        TrainingData: Images loaded into memory for the training set, 
            resized and normalized
        ValidationData: Images loaded into memory for the validation 
            set used for accuracy testing, resized and normalized
    """
    
    # Paths for the data
    TrainPath = "horse-or-human\\train"
    ValidationPath = "horse-or-human\\validation"
    
    # Create generator object that changes configurations of input images
    TrainingDataGenerator = tf.keras.preprocessing.image.ImageDataGenerator(
      rescale=1./255,
      rotation_range=20,
      width_shift_range=0.2,
      height_shift_range=0.2,
      shear_range=0.2,
      zoom_range=0.2,
      horizontal_flip=True,
      fill_mode='nearest'
    )
    
    # Use generator to load images
    TrainingData = TrainingDataGenerator.flow_from_directory(
        TrainPath,
        target_size=(IMG_WIDTH, IMG_HEIGHT),
        batch_size=128,
        class_mode="binary"
    )

    # Create generator object that changes configurations of input images    
    ValidationDataGenerator = tf.keras.preprocessing.image.ImageDataGenerator(
      rescale=1./255,
    )
    
    # Use generator to load images
    ValidationData = ValidationDataGenerator.flow_from_directory(
        ValidationPath,
        target_size=(IMG_WIDTH, IMG_HEIGHT),
        class_mode="binary"
    )
    
    return TrainingData, ValidationData
    
    
def get_model():
    """
    Creates the architecture of the CNN with multiple convolutional layers 
    and compiles it according to binary crossentropy.  
    Optimizer is preconfigured but can be swapped in the first line.

    Returns:
        model: A compiled convolutional model.
    """
    OPTIMIZER = tf.keras.optimizers.Adam(lr=0.001)
    
    model = tf.keras.models.Sequential([
        # Use convolution to simplify data and feature extraction
        tf.keras.layers.Conv2D(64, (3, 3), activation="relu", input_shape = (IMG_WIDTH, IMG_HEIGHT, 3)),
        # Pooling to decrease dimensions and
        tf.keras.layers.MaxPooling2D((3, 3)),
        tf.keras.layers.Conv2D(128, (3, 3), activation="tanh"),
        tf.keras.layers.MaxPooling2D((2, 2)),
        tf.keras.layers.Conv2D(128, (3, 3), activation="relu"),
        tf.keras.layers.MaxPooling2D((2, 2)),
        # Vectorize resulting data
        tf.keras.layers.Flatten(),
        tf.keras.layers.Dense(256, activation = "relu"),
        # Using dropouts to avoid model being over reliant on just a few neurons
        tf.keras.layers.Dense(512, activation = "relu"),
        # One output that indicates wether output is 0 for human, 1 for horse
        tf.keras.layers.Dense(1, activation="sigmoid")        
    ])
    
    # Compile the model using binary crossentropy as loss function 
    # due to there only being two output values possible
    model.compile(
        optimizer = OPTIMIZER,
        loss="binary_crossentropy",
        metrics =["accuracy"]
    )
    
    return model
    
    
if __name__ == "__main__":
    main()