import click
import tensorflow as tf

import emacnn.data
import emacnn.features
import emacnn.model


# Resolves some cuDNN error
# See https://github.com/tensorflow/tensorflow/issues/36508#issuecomment-584898603
physical_devices = tf.config.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(physical_devices[0], enable=True)


@click.group()
def emac():
    pass


@emac.command('slurp', short_help='Slurp the closed captions from a YouTube channel\'s uploads')
@click.option('--api-key', '-k', 'api_key', envvar='EMACNN_API_KEY',
              help='A YouTube API key')
@click.option('--playlist-id', '-p', 'playlist_id', default='UUC1FVUSiw7X2L5QoPEG_dkw', envvar='EMACNN_PLAYLIST_ID',
              help='A YouTube playlist ID')
@click.option('--data-path', '-d', 'data_path', default='./data/raw/uploads.csv',
              help='Path to a csv file for holding YouTube API data')
def slurp(api_key, playlist_id, data_path):
    """Slurp the closed captions from a YouTube channel's uploads."""

    emacnn.data.get_captions(
        api_key=api_key,
        playlist_id=playlist_id,
        uploads_path=data_path,
    )


@emac.command('train', short_help='Train a neural network based on data from `emacnn slurp`')
@click.option('--generate', '-g', 'generate', help='Generate new random datasets', is_flag=True)
@click.option('--input-path', '-i', 'input_path', default='./data/raw/uploads.csv',
              help='Path to a csv file to generate datasets from', show_default=True)
@click.option('--data-path', '-d', 'data_path', default='./data/processed',
              help='Path to a dir to store EmacNN data', show_default=True)
@click.option('--training-path', '-t', 'training_path', default='/training',
              help='Subdir of data_path containing the training dataset', show_default=True)
@click.option('--validation-path', '-t', 'validation_path', default='/validation',
              help='Subdir of data_path containing the validation dataset', show_default=True)
@click.option('--epochs', '-e', 'epochs', default=19,
              help='Number of epochs to train', show_default=True)
@click.option('--model-path', '-m', 'model_path', default='./models/emacnn',
              help='Path at which to save the trained model', show_default=True)
def train(generate, input_path, data_path, training_path, validation_path, epochs, model_path):
    """Train a neural network based on data from `emacnn slurp`."""
    # TODO: Add a resume option, provide a checkpoint file to resume from

    if generate:
        emacnn.features.generate_datasets(input_path, data_path)

    try:
        emacnn.model.train_model(
            training_dataset=tf.data.experimental.load(
                data_path + training_path,
                (
                    tf.TensorSpec(shape=(64, 100), dtype=tf.int32),  # TODO: Magic numbers
                    tf.TensorSpec(shape=(64, 100), dtype=tf.int32),  # TODO: Magic numbers
                ),
                compression='GZIP',
            ),
            validation_dataset=tf.data.experimental.load(
                data_path + validation_path,
                (
                    tf.TensorSpec(shape=(64, 100), dtype=tf.int32),  # TODO: Magic numbers
                    tf.TensorSpec(shape=(64, 100), dtype=tf.int32),  # TODO: Magic numbers
                ),
                compression='GZIP',
            ),
            epochs=epochs,
            output_path=model_path,
        )
    except TypeError:
        raise click.ClickException('Unable to load training or validation datatset.')


@ emac.command('vlog', short_help='Generate a script of Eric\'s rambling')
@click.option('--model-path', '-m', 'model_path', default='./models/emacnn',
              help='Path to a trained model', show_default=True)
@click.option('--seed', '-s', 'seed', default='hello lovely world',
              help='Word or phrase to start generation', show_default=True)
def vlog(model_path, seed):
    """Generate a video script."""

    click.echo(emacnn.model.predict_model(model_path, seed))
