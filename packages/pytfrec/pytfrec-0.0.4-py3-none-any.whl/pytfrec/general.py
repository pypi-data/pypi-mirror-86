import collections
from functools import partial
import tensorflow as tf


def get_examples(tfrec_path, example_numbers=1):
    """Just for inspect tfrec files
    https://stackoverflow.com/questions/42394585/how-to-inspect-a-tensorflow-tfrecord-file/42402484#42402484"""
    raw_dataset = tf.data.TFRecordDataset(tfrec_path)

    result = []
    for raw_record in raw_dataset.take(example_numbers):
        example = tf.train.Example()
        example.ParseFromString(raw_record.numpy())
        result.append(example)
    return result


def get_file_names(tfrecs_dir: str, validation_data_ratio: float) -> tuple:
    file_names = tf.io.gfile.glob(f'{tfrecs_dir}/*.tfrec')
    data_number = len(file_names)
    split_index = int(data_number * (1 - validation_data_ratio))
    train_file_names = file_names[:split_index]
    validation_file_names = file_names[split_index:]
    return train_file_names, validation_file_names


def augment_data(dataset, augmentation_function, normalize=True):
    for minibatch in dataset:
        images = minibatch[0].numpy()
        labels = minibatch[1].numpy()
        distribution = collections.Counter(labels)
        max_dist = max(distribution.values())
        add_dict = {}
        for i in distribution:
            add_dict[i] = (max_dist - distribution[i]) // distribution[i]
        batch_increase = sum([add_dict[i] * distribution[i] for i in add_dict])
        new_img_shape = (images.shape[0] + batch_increase, *images.shape[1:])
        new_lbl_shape = (labels.shape[0] + batch_increase, )
        new_images = np.empty(new_img_shape)
        new_labels = np.empty(new_lbl_shape)
        index = 0
        for i, j in zip(images, labels):
            new_images[index] = i
            new_labels[index] = j
            index += 1
            for _ in range(add_dict[j]):
                new_images[index] = augmentation_function(i)
                new_labels[index] = j
                index += 1
        if normalize:
            new_images = np.clip(new_images / 255.0, 0, 1)
        else:
            new_images = np.clip(new_images, 0.0, 255.0)
        yield (new_images, new_labels)


class AugmentedDataGenerator(tf.keras.utils.Sequence):
    def __init__(self,
                 dataset,
                 augmentation_function,
                 minibatchs_num,
                 normalize=True):
        self.dataset = dataset
        self.augmentation_function = augmentation_function
        self.normalize = normalize
        self.augemented_generator = augment_data(dataset,
                                                 augmentation_function,
                                                 normalize)
        self.minibatchs_num = minibatchs_num

    def __len__(self):
        return self.minibatchs_num

    def __getitem__(self, index):
        return next(self.augemented_generator)

    def on_epoch_end(self):
        self.augemented_generator = augment_data(self.dataset,
                                                 self.augmentation_function,
                                                 self.normalize)


def aug_func(img):
    img = tf.image.random_flip_left_right(img)
    img = tf.image.random_flip_up_down(img)
    img = tf.image.random_brightness(img, max_delta=0.8)
    img = tf.image.random_contrast(img, lower=0.6, upper=1.4)
    img = tf.image.random_saturation(img, lower=0.6, upper=1.4)
    return img