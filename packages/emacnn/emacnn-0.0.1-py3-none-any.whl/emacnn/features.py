import csv

import numpy as np
import tensorflow as tf


def _generate_char_encoding(vocab, output_path):
    encoder = {u: i for i, u in enumerate(vocab)}
    np.save(output_path + '/encoder.npy', encoder)
    decoder = np.array(vocab)
    np.save(output_path + '/decoder.npy', decoder)
    return encoder, decoder


def generate_datasets(input_path, output_path):
    """Generate Tensorflow datasets from csv caption data.

    Args:
        input_path: Path to csv formatted caption data.
        output_path: Path at which to store generated datasets.
    """

    with open(input_path) as uploads_file:
        uploads_reader = csv.reader(uploads_file)
        text = ' '.join(upload[2] for upload in uploads_reader)

    vocab = sorted(set(text))
    encoder, decoder = _generate_char_encoding(vocab, output_path)
    seq_length = 100  # TODO: Magic numbers

    text_as_int = [encoder[c] for c in text]
    # Create training examples / targets
    char_dataset = tf.data.Dataset.from_tensor_slices(text_as_int)
    # Build sequences from the character dataset
    sequences = char_dataset.batch(seq_length + 1, drop_remainder=True)
    # Build text dataset of input texts and expected output texts
    dataset = sequences.map(lambda chunk: (chunk[:-1], chunk[1:]))

    # Shuffle text dataset and batch the shuffled inputs and outputs
    BATCH_SIZE = 64  # TODO: Magic numbers
    BUFFER_SIZE = 10000
    dataset = dataset.shuffle(BUFFER_SIZE, reshuffle_each_iteration=False).batch(BATCH_SIZE, drop_remainder=True)

    def _is_validation(x, y):
        return x % 4 == 0

    def _is_training(x, y):
        return not _is_validation(x, y)

    def _recover(x, y):
        return y

    # Break the shuffled dataset into 75% training, 25% validation
    training_dataset = dataset.enumerate().filter(_is_training).map(_recover)
    validation_dataset = dataset.enumerate().filter(_is_validation).map(_recover)

    tf.data.experimental.save(
        training_dataset,
        path=output_path + '/training',
        compression='GZIP',
    )
    tf.data.experimental.save(
        validation_dataset,
        path=output_path + '/validation',
        compression='GZIP',
    )

    return training_dataset, validation_dataset
