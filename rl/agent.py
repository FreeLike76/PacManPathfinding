import tensorflow as tf
import tensorflow.keras as keras
import tensorflow.keras.layers as layers

import numpy as np

# experimenting...

class Agent:
    def __init__(self):
        self.model = None

    def get_action(self, walls, coins, p_pos, e_pos):
        """Returns an action"""
        pass

    def encode_state(self, walls, coins, p_pos, e_pos):
        _p_pos = np.zeros((32, 32))
        _p_pos[p_pos[0], p_pos[1]] = 1

        _e_pos = np.zeros((32, 32))
        for pos in e_pos:
            _e_pos[pos[0], pos[1]] = 1

        return np.stack([walls, coins, _p_pos, _e_pos], axis=-1)

    def train(self):
        """Function to train agent"""
        pass

    def create_model(self):
        """Create nn for the first time"""
        # game map      32x32   = 1024
        # coin map      32x32   = 1024
        # enemy pos     32x32   = 1024
        # player pos    32x32   = 1024

        x_in = layers.InputLayer(input_shape=(32, 32, 4))
        # 32x32x4
        x = layers.Conv2D(filters=8, kernel_size=(3, 3), padding="same")(x_in)
        x = layers.Activation("relu")(x)
        x = layers.MaxPool2D()(x)
        # 16x16x8
        x = layers.Conv2D(filters=16, kernel_size=(3, 3), padding="same")(x)
        x = layers.Activation("relu")(x)
        x = layers.MaxPool2D()(x)
        # 8x8x16
        x = layers.Conv2D(filters=32, kernel_size=(3, 3), padding="same")(x)
        x = layers.Activation("relu")(x)
        x = layers.MaxPool2D()(x)
        # 4x4x32
        x = layers.Conv2D(filters=64, kernel_size=(3, 3), padding="same")(x)
        x = layers.Activation("relu")(x)
        x = layers.MaxPool2D()(x)
        # 2x2x64
        x = layers.Conv2D(filters=128, kernel_size=(3, 3), padding="same")(x)
        x = layers.Activation("relu")(x)
        x = layers.MaxPool2D()(x)
        # 1x1x128
        x = layers.Flatten()(x)
        # 128
        x = layers.Dense(16)(x)
        x = layers.Activation("relu")(x)
        # 16
        x = layers.Dense(4)(x)
        x_out = layers.Activation("softmax")(x)
        # 4

        self.model = tf.keras.Model(inputs=x_in, outputs=x_out)
        #opt = tf.optimizers.Adam(learning_rate=learning_rate, decay=decay)
        #self.model.compile(optimizer=opt, loss=tf.losses.MeanSquaredError(), metrics=[tf.metrics.MeanSquaredError()])

    def load_model(self, path):
        pass