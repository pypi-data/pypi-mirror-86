import os
import h5py
import shutil
from tensorflow.keras.models import model_from_json
from cnn2snn import load_quantized_model, cnn2snn_objects


def _upgrade_model_with_legacy_quantizers(src_filepath, dst_filepath):
    """Replaces legacy quantizers (cnn2snn<=1.8.9) with new ones
    (cnn2snn>=1.8.10).

    The model configuration is retrieved and modified to replace the legacy
    quantizers "WeightQuantizer" and "TrainableWeightQuantizer" with the new
    "StdWeightQuantizer" and "TrainableStdWeightQuantizer". A new model
    with the weights of the source model is then saved.

    HDF5 and TF saved models are supported.

    Args:
        src_filepath: model filepath with legacy quantizers
        dst_filepath: filepath to save the upgraded model
    """

    if not dst_filepath:
        raise ValueError("The destination model filepath must not be empty")

    def _replace_legacy_quantizers(model_config):
        model_config = model_config.replace('"WeightQuantizer"',
                                            '"StdWeightQuantizer"')
        model_config = model_config.replace('"TrainableWeightQuantizer"',
                                            '"TrainableStdWeightQuantizer"')
        return model_config

    if h5py.is_hdf5(src_filepath):

        # Copy and open the h5 model file
        shutil.copy(src_filepath, dst_filepath)
        f = h5py.File(dst_filepath, mode='r+')

        # Get model configuration
        model_config = f.attrs.get('model_config')
        if model_config is None:
            raise ValueError('No model found in config file.')
        model_config = model_config.decode('utf-8')

        # Detect if there are legacy quantizers
        if ('"WeightQuantizer"' in model_config or
                '"TrainableWeightQuantizer"' in model_config):

            # Replace legacy quantizers with their new names
            model_config = _replace_legacy_quantizers(model_config)

            # Update model config in the h5py.File
            f.attrs['model_config'] = model_config.encode('utf8')
            f.close()

            print(f"Model upgraded and saved to {dst_filepath}")
        else:
            os.remove(dst_filepath)
            print("No legacy quantizers found. No operation is done")

    else:  # If model file is in TF/PB format

        # Get model configuration
        model = load_quantized_model(src_filepath)
        model_config = model.to_json()

        # Detect if there are legacy quantizers
        if ('"WeightQuantizer"' in model_config or
                '"TrainableWeightQuantizer"' in model_config):

            # Replace legacy quantizers with their new names
            model_config = _replace_legacy_quantizers(model_config)

            # Save new model with source weights
            new_model = model_from_json(model_config,
                                        custom_objects=cnn2snn_objects)
            new_model.set_weights(model.get_weights())
            new_model.save(dst_filepath)

            print(f"Model upgraded and saved to {dst_filepath}")
        else:
            print("No legacy quantizers found. No operation is done")
