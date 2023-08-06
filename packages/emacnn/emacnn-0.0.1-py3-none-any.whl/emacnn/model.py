import numpy as np
import tensorflow as tf


def _build_model(vocab_size, embedding_dim=256, rnn_units=1024, batch_size=64):
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Embedding(vocab_size, embedding_dim,
                                        batch_input_shape=[batch_size, None]))
    model.add(tf.keras.layers.LSTM(
        units=rnn_units,
        return_sequences=True,
        stateful=True,
        recurrent_initializer='glorot_uniform',
    ))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.LSTM(
        units=rnn_units,
        return_sequences=True,
        stateful=True,
    ))
    model.add(tf.keras.layers.Dropout(0.2))
    model.add(tf.keras.layers.Dense(vocab_size))
    return model


def train_model(training_dataset, validation_dataset, epochs, output_path):
    """Train a LSTM based model.

    Args:
        training_dataset: A Tensorflow dataset on which to train.
        validation_dataset: A Tensorflow dataset on which to validate.
        epochs: Number of epochs to train.
        output_path: Path at which to save the model.
    """

    checkpoint = tf.keras.callbacks.ModelCheckpoint(
        './checkpoints/cp-{epoch:04d}.ckpt',
        save_weights_only=True,
        monitor='loss',
        verbose=1,
    )

    callbacks = [
        checkpoint,
        tf.keras.callbacks.ProgbarLogger(count_mode='steps', stateful_metrics=None),
    ]

    model = _build_model(
        vocab_size=len((np.load('./data/processed/encoder.npy', allow_pickle=True)).flat[0]),  # TODO: Magic string
    )
    model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True))
    model.fit(training_dataset, epochs=epochs, validation_data=validation_dataset, callbacks=callbacks)
    model.save(output_path)


def predict_model(model_path, seed):
    """Use a trained model and a seed to generate a prediction.

    Args:
        model_path: Path to a trained model.
        seed: A word or phrase to get the prediction started.
    """

    output_length = 2000
    encoder = (np.load('./data/processed/encoder.npy', allow_pickle=True)).flat[0]  # TODO: Magic string
    decoder = dict((v, k) for k, v in encoder.items())  # TODO: Loading decoder.npy doesn't seem to work for decoding
    text_generated = []
    temperature = 1.0

    input_eval = [encoder[c] for c in seed]
    input_eval = tf.expand_dims(input_eval, 0)

    trained_model = tf.keras.models.load_model(model_path, compile=False)
    prediction_model = _build_model(
        vocab_size=len((np.load('./data/processed/encoder.npy', allow_pickle=True)).flat[0]),  # TODO: Magic string
        batch_size=1
    )
    prediction_model.set_weights(trained_model.get_weights())
    prediction_model.compile(optimizer='adam', loss=tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True))

    for i in range(output_length):
        predictions = prediction_model(input_eval)
        predictions = tf.squeeze(predictions, 0)  # remove the batch dimension

        predictions = predictions / temperature
        predicted_id = tf.random.categorical(predictions, num_samples=1)[-1, 0].numpy()

        input_eval = tf.expand_dims([predicted_id], 0)

        text_generated.append(decoder[predicted_id])

    return (seed + ''.join(text_generated))
