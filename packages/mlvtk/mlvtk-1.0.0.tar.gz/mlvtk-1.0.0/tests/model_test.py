import tensorflow as tf
import numpy as np
from . import Model




sequential_model_base_truth = tf.keras.Sequential([tf.keras.layers.Dense(1,),
    tf.keras.layers.Dense(1,), tf.keras.layers.Dense(1)])
sequential_model_base_truth.build(input_shape=(None, 1))

i = tf.keras.layers.Input(shape=(1))
d = tf.keras.layers.Dense(1)(tf.keras.layers.Dense(1,)(tf.keras.layers.Dense(1)(i)))
functional_model_base_truth = tf.keras.Model(inputs=i, outputs=d)

print("\n\n\n\nBASE TRUTH MODEL SUMMARIES")
sequential_model_base_truth.summary()
print("\n\n\n")
functional_model_base_truth.summary()


def test_sequential():
    tf.random.set_seed(1234)
    model = Model(sequential_model_base_truth)
    model.overwrite=True
    model.summary()
    n = np.concatenate([np.concatenate([new.get_weights()[0].flatten(),
        new.get_weights()[1]]) for new in model.layers]) # [1:] to skip empty input layer
    o = np.concatenate([np.concatenate([original.get_weights()[0].flatten(), original.get_weights()[1]]) for original in sequential_model_base_truth.layers])

    print(n, "\n\n\n")
    print(o, "\n\n\n")
    assert sum([np.all(n == o)]) 

    x_train = np.random.rand(3)
    y_train = np.array([0, 1, 0])

    x_val = np.random.rand(3)
    y_val = np.array([0, 1, 0])

    sequential_model_base_truth.compile(optimizer=tf.keras.optimizers.SGD(),
            loss='binary_crossentropy')
    histo = sequential_model_base_truth.fit(x=x_train, y=y_train,
            validation_data=(x_val, y_val), steps_per_epoch=2)
    
    sequential_model_base_truth.reset_states()
    tf.random.set_seed(1234)
    model.reset_states()
    model.compile(optimizer=tf.keras.optimizers.SGD(), loss='binary_crossentropy')

    hist = model.fit(x=x_train, y=y_train, validation_data=(x_val, y_val))

    
    assert abs(hist.history.get('val_loss')[0] -
            histo.history.get('val_loss')[0]) < .1




def test_functional():
    model = Model(functional_model_base_truth)
    model.summary()
    n = np.concatenate([np.concatenate([new.get_weights()[0].flatten(), new.get_weights()[1]]) for new in model.layers[1:]])
    o = np.concatenate([np.concatenate([original.get_weights()[0].flatten(), original.get_weights()[1]]) for original in functional_model_base_truth.layers[1:]])

    assert sum([np.all(n == o)]) 

