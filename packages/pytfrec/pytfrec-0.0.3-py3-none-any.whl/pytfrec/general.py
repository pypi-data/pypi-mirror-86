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