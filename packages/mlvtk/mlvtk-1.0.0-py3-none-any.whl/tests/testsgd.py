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

    (mnist_train, label_train), (mnist_test, label_test) = tfds.as_numpy(
        tfds.load(
            "mnist",
            split=["train", "test"],
            batch_size=-1,
            as_supervised=True,
            data_dir="datasets",
        )
    )

    label_train_binarized = label_binarize(label_train, classes=np.unique(label_train))
    label_test_binarized = label_binarize(label_test, classes=np.unique(label_train))

    mnist_train_data = (
        tf.data.Dataset.from_tensor_slices(
            (mnist_train.reshape(mnist_train.shape[0], -1), label_train_binarized)
        )
        .shuffle(buffer_size=30)
        .batch(batch_size=30)
        .repeat()
    )
    mnist_test_data = (
        tf.data.Dataset.from_tensor_slices(
            (mnist_test.reshape(mnist_test.shape[0], -1), label_test_binarized)
        )
        .shuffle(buffer_size=30)
        .batch(batch_size=30)
    )

    # construct standard 3 layer network
    inputs = tf.keras.layers.Input(shape=(784))
    dense_1 = tf.keras.layers.Dense(50, activation="elu")(inputs)
    do = tf.keras.layers.Dropout(rate=0.1)(dense_1)
    outputs = tf.keras.layers.Dense(
        np.unique(label_train, axis=0).size, activation="softmax"
    )(
        do
    )  
    # create mlvtk model
    model = mlvtk.Model(inputs=inputs, outputs=outputs)
    model.overwrite = True
    if optim == "sgd1":
        op = tf.keras.optimizers.SGD(learning_rate=0.003)
        model.checkpoint_path = "sgd1"
    if optim == "sgd2":
        op = tf.keras.optimizers.SGD(learning_rate=0.001)
        model.checkpoint_path = "sgd2"
    if optim == "sgd3":
        op = tf.keras.optimizers.SGD(learning_rate=0.005)
        model.checkpoint_path = "sgd3"
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
    history = model.fit(
        mnist_train_data,
        validation_data=mnist_test_data,
        epochs=6,
        verbose=1,
        steps_per_epoch=150,
    )
    return model


def normalize():
    import mlvtk

    ms = test("sgd1")
    ma = test("sgd2", ms.initial_weights)
    mad = test("sgd3", ms.initial_weights)
    ct = mlvtk.base.CalcTrajectory.CalcTrajectory()
    ct.fit([ms, ma, mad])
    normalizer = mlvtk.base.FilterNorm.normalizer
    s = normalizer(ms, ct, alphas_size=50, betas_size=50, extension="std",
            verbose=False)
    return s
