
def test(optim, weights=None):
    import tensorflow as tf
    import numpy as np

    tf.compat.v1.random.set_random_seed(14172)  # arbitrary seed
    np.random.seed(seed=14172)
    tf.config.optimizer.set_jit(True)
    tf.keras.backend.clear_session()
    from tensorflow.keras.mixed_precision import experimental as mixed_precision
    policy = tf.keras.mixed_precision.experimental.Policy("mixed_float16")
    mixed_precision.set_policy(policy)
    import mlvtk

    sess = tf.compat.v1.Session(
        config=tf.compat.v1.ConfigProto(log_device_placement=True)
    )
    import tensorflow_datasets as tfds
    from sklearn.preprocessing import label_binarize
    import numpy as np


    (x_train, y_train), (x_test, y_test) = tf.keras.datasets.cifar10.load_data()
    x_train = x_train.astype('float32') / 256
    x_test = x_test.astype('float32') / 256

    # Convert class vectors to binary class matrices.
    y_train = tf.keras.utils.to_categorical(y_train, num_classes=10)
    y_test = tf.keras.utils.to_categorical(y_test, num_classes=10)
    # construct standard 3 layer network
    #inputs = tf.keras.layers.Input(shape=(784))
    #dense_1 = tf.keras.layers.Dense(50, activation="elu")(inputs)
    #do = tf.keras.layers.Dropout(rate=0.1)(dense_1)
    #outputs = tf.keras.layers.Dense(
    #    np.unique(label_train, axis=0).size, activation="softmax"
    #)(
    #    do
    #)
    mod = [
    tf.keras.layers.Conv2D(32, (3, 3), padding='same', input_shape=x_train.shape[1:]),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.Conv2D(32, (3, 3)),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.Dropout(0.25),

    tf.keras.layers.Conv2D(64, (3, 3), padding='same'),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.Conv2D(64, (3, 3)),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.MaxPooling2D(pool_size=(2, 2)),
    tf.keras.layers.Dropout(0.25),

    tf.keras.layers.Flatten(),
    tf.keras.layers.Dense(512),
    tf.keras.layers.Activation('relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(10),
    tf.keras.layers.Activation('softmax')
    ]
    # create mlvtk model
    model = mlvtk.Model(model=mod)
    model.overwrite = True
    if optim == "adam":
        op = tf.keras.optimizers.Adam()
        model.checkpoint_path = "adam"
    if optim == "adamax":
        op = tf.keras.optimizers.Adamax()
        model.checkpoint_path = "adamax"
    if optim == "nadam":
        op = tf.keras.optimizers.Nadam()
        model.checkpoint_path = "nadam"
    model.compile(
        optimizer=op,
        loss=tf.keras.losses.CategoricalCrossentropy(),
        metrics=["accuracy"],
    )
    if weights is not None:
        model.set_weights(weights)
    else:
        weights = model.get_weights()
        model.initial_weights = weights
    history = model.fit(x_train, y_train, batch_size=256, epochs=10, validation_data=(x_test, y_test), shuffle=True)
    #history = model.fit(
    #    mnist_train_data,
    #    validation_data=mnist_test_data,
    #    epochs=6,
    #    verbose=1,
    #    steps_per_epoch=150,
    #)
    return model


def normalize():
    import mlvtk

    ms = test("adam")
    ma = test("adamax", ms.initial_weights)
    mad = test("nadam", ms.initial_weights)
    ct = mlvtk.base.CalcTrajectory.CalcTrajectory()
    ct.fit([ms, ma, mad])
    normalizer = mlvtk.base.FilterNorm.normalizer
    s = normalizer(ms, ct, alphas_size=50, betas_size=50, extension=1,
            verbose=False)
    return s
