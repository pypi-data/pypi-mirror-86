"""Based on notebook from: https://keras.io/examples/keras_recipes/tfrecord/"""

import tensorflow as tf
import matplotlib.pyplot as plt
from pytfrec.general import *
from functools import partial

def decode_image(image, image_size, channels, normalize_scale):
    image = tf.io.decode_jpeg(image, channels=channels)
    image = tf.image.resize(image, image_size)
    image = tf.cast(image, tf.float32)
    image = image / normalize_scale
    return image


def read_tfrecord(example, image_size, channels, labeled, normalize_scale):
    # Features may have different names in case of error chack that
    tfrecord_format = {'image': tf.io.FixedLenFeature([], tf.string)}
    if labeled:
        tfrecord_format['target'] = tf.io.FixedLenFeature([], tf.int64)

    example = tf.io.parse_single_example(example, tfrecord_format)
    image = decode_image(example["image"], image_size, channels, normalize_scale)
    if labeled:
        label = tf.cast(example["target"], tf.int32)
        return image, label
    return image


def load_dataset(filenames, image_size, channels, labeled, ordered, normalize_scale):
    ignore_order = tf.data.Options()
    ignore_order.experimental_deterministic = ordered  # disable order, increase speed
    dataset = tf.data.TFRecordDataset(
        filenames)  # automatically interleaves reads from multiple files
    dataset = dataset.with_options(
        ignore_order
    )  # uses data as soon as it streams in, rather than in its original order
    map_func = partial(read_tfrecord,
                       image_size=image_size,
                       channels=channels,
                       labeled=labeled,
                       normalize_scale=normalize_scale)
    dataset = dataset.map(map_func,
                          num_parallel_calls=tf.data.experimental.AUTOTUNE)
    # returns a dataset of (image, label) pairs if labeled=True or just images if labeled=False
    return dataset


def get_dataset_from_file_names(filenames,
                                image_size,
                                batch_size,
                                channels=3,
                                labeled=True,
                                ordered=False,
                                normalize_scale=255):
    dataset = load_dataset(filenames,
                           image_size,
                           channels,
                           labeled=labeled,
                           ordered=ordered,
                           normalize_scale=normalize_scale)
    dataset = dataset.shuffle(2048)
    dataset = dataset.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
    dataset = dataset.batch(batch_size)
    return dataset


def get_datasets(tfrecs_dir: str,
                 image_size: tuple,
                 batch_size: int,
                 validation_data_ratio=0,
                 channels=3,
                 labeled=True,
                 ordered=False,
                 normalize_scale=255):
    datasets = {}
    train_file_names, validation_file_names = get_file_names(
        tfrecs_dir, validation_data_ratio)
    datasets['train'] = get_dataset_from_file_names(train_file_names, image_size, batch_size,
                                                    channels=channels,
                                                    labeled=labeled,
                                                    ordered=ordered,
                                                    normalize_scale=normalize_scale)
    assert type(validation_data_ratio) == float
    assert validation_data_ratio >= 0
    if validation_data_ratio:
        datasets['validation'] = get_dataset_from_file_names(
            validation_file_names, image_size, batch_size, channels, labeled,
            ordered)
    return datasets


def show_batch(image_batch, label_batch, batch_size, columns=3):
    plt.figure(figsize=(10, 10))
    for n in range(batch_size):
        ax = plt.subplot(batch_size // columns + 1, columns, n + 1)
        plt.imshow(image_batch[n] / 255.0)
        plt.title(label_batch[n])
        plt.axis("off")