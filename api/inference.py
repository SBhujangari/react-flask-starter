import tensorflow as tf
import efficientnet.tfkeras as efn
from PIL import Image
import numpy as np
import os
# Comment following line when proving something
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

#filename='/home/stanleyzheng/Desktop/hackitbetter/COVID-19 Radiography Database/COVID-19/0a6c60063b4bae4de001caaba306d1_jumbo.jpeg'
filename='/home/stanleyzheng/Desktop/hackitbetter/COVID-19 Radiography Database/NORMAL/CR.1.2.840.113564.192168196.2020033016123149069.1203801020003.png'
def predict(filename):
    filename = filename.replace(" ", "_")
    filename = filename.replace('(', '')
    filename = filename.replace(')', '')
    using_laptop=True

    if using_laptop:
        gpus = tf.config.experimental.list_physical_devices('GPU')
        tf.config.experimental.set_memory_growth(gpus[0], True)

    EFNS = [efn.EfficientNetB0, efn.EfficientNetB1, efn.EfficientNetB2, efn.EfficientNetB3, 
            efn.EfficientNetB4, efn.EfficientNetB5, efn.EfficientNetB6, efn.EfficientNetB6]

    def build_model(dim=256, ef=0):
        inp = tf.keras.layers.Input(shape=(dim,dim,3))
        base = EFNS[ef](input_shape=(dim,dim,3),weights='noisy-student',include_top=False) #Change imagnet to noisy-student here
        base.trainable = False # freeze model
        x = base(inp)
        x = tf.keras.layers.GlobalAveragePooling2D()(x)
        x = tf.keras.layers.Dense(3,activation='sigmoid')(x)
        model = tf.keras.Model(inputs=inp,outputs=x)
        opt = tf.keras.optimizers.Adam(learning_rate=0.001)
        loss = tf.keras.losses.BinaryCrossentropy(label_smoothing=0.05)
        model.compile(optimizer=opt,loss=loss,metrics=['AUC'])
        return model

    def sigmoid(x):
        return 1 / (1 + math.exp(-x))

    def softmax(x):
        e_x = np.exp(x - np.max(x))
        return e_x / e_x.sum()

    #cache? and use spinner?
    model = build_model(dim=224, ef=0)
    model.load_weights('model.hdf5')

    x = Image.open(filename)
    x = x.convert('RGB')
    x = x.resize((224, 224))
    x = np.asarray(x)
    x = np.expand_dims(x, axis=0)/255.

    image = tf.keras.preprocessing.image.img_to_array(Image.open(filename).convert('RGB').resize((224, 224)))
    label = model.predict(x)
    maxlabel = np.argmax(label)
    prob = label[0][maxlabel]*1.2
    if maxlabel == 0:
        label = 'Normal'
    elif maxlabel == 1:
        label = 'Viral Pneumonia or other pneumonia'
    elif maxlabel == 2:
        label = 'COVID-19'
    else:
        prob = 1
        label = 'Unknown or equal labels'

    return prob, label

#predict(filename)