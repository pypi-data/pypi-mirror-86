#!/usr/bin/env python
# ******************************************************************************
# Copyright 2019 Brainchip Holdings Ltd.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ******************************************************************************

# Tensorflow imports
import tensorflow as tf
from tensorflow.python.keras import backend as K
from tensorflow.keras import layers
from tensorflow.keras.utils import serialize_keras_object
from tensorflow.python.keras.utils import conv_utils
from tensorflow.python.ops import math_ops
from tensorflow.python.ops import nn
from tensorflow.python.ops import sparse_ops
from tensorflow.python.ops import standard_ops, gen_math_ops
from tensorflow.python.eager import context
from .quantization_ops import get as get_quantizer
from .quantization_ops import WeightFloat, ceil_through


def _check_unsupported_args(kwargs, unsupported_args):
    """Raises error if unsupported argument are present in kwargs.

    For now, 4 arguments are unsupported: 'data_format', 'activation',
        'dilation_rate', 'depth_mutiplier', 'activity_regularizer'.

    Args:
        kwargs (dictionary): keyword arguments to check.
        unsupported_args: list of unsupported arguments.

    """
    for kwarg in kwargs:
        if kwarg in unsupported_args:
            raise TypeError("Unsupported argument in quantized layers:", kwarg)


class QuantizedConv2D(layers.Conv2D):
    """A quantization-aware Keras convolutional layer.

    Inherits from Keras Conv2D layer, applying a quantization on weights during
    the forward pass.

    """
    unsupported_args = {
        'data_format', 'activation', 'dilation_rate', 'activity_regularizer'
    }

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=(1, 1),
                 padding='valid',
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 quantizer=WeightFloat(),
                 **kwargs):
        """Creates a quantization-aware convolutional layer.

        Args:
            filters (integer): the number of filters.
            kernel_size (tuple of integer): the kernel spatial dimensions.
            strides (integer, or tuple of integers, optional): strides of the
                convolution along height and width.
            padding (str, optional): one of 'valid' or 'same'.
            use_bias (boolean, optional): whether the layer uses a bias vector.
            kernel_initializer (str, or a :obj:`tf.keras.initializer`, optional):
                initializer for the weights matrix.
            bias_initializer (str, or a :obj:`tf.keras.initializer`, optional):
                initializer for the bias vector.
            kernel_regularizer (str, or a :obj:`tf.keras.regularizer`, optional):
                regularization applied to the weights.
            bias_regularizer (str, or a :obj:`tf.keras.regularizer`, optional):
                regularization applied to the bias.
            kernel_constraint (str, or a :obj:`tf.keras.constraint`, optional):
                constraint applied to the weights.
            bias_constraint (str, or a :obj:`tf.keras.constraint`, optional):
                constraint applied to the bias.
            quantizer (:obj:`cnn2snn.WeightQuantizer`, optional): the quantizer
                to apply during the forward pass.

        """
        _check_unsupported_args(kwargs, self.unsupported_args)
        self.quantizer = get_quantizer(quantizer)
        super(QuantizedConv2D,
              self).__init__(filters=filters,
                             kernel_size=kernel_size,
                             strides=strides,
                             padding=padding,
                             use_bias=use_bias,
                             kernel_initializer=kernel_initializer,
                             bias_initializer=bias_initializer,
                             kernel_regularizer=kernel_regularizer,
                             bias_regularizer=bias_regularizer,
                             kernel_constraint=kernel_constraint,
                             bias_constraint=bias_constraint,
                             **kwargs)

    def call(self, inputs):
        """Evaluates input Tensor.

        This applies the quantization on weights, then evaluates the input
        Tensor and produces the output Tensor.

        Args:
            inputs(:obj:`tensorflow.Tensor`): input Tensor.

        Returns:
            :obj:`tensorflow.Tensor`: output Tensor.

        """
        outputs = self._convolution_op(inputs,
                                       self.quantizer.quantize(self.kernel))
        if self.use_bias:
            outputs = nn.bias_add(outputs, self.bias, data_format='NHWC')

        return outputs

    def get_config(self):
        config = super().get_config()
        config['quantizer'] = serialize_keras_object(self.quantizer)
        for kwarg in self.unsupported_args:
            config.pop(kwarg, None)
        return config


class QuantizedDepthwiseConv2D(layers.DepthwiseConv2D):
    """A quantization-aware Keras depthwise convolutional layer.

    Inherits from Keras DepthwiseConv2D layer, applying a quantization on
    weights during the forward pass.

    """
    unsupported_args = {
        'data_format', 'activation', 'depth_multiplier', 'activity_regularizer'
    }

    def __init__(self,
                 kernel_size,
                 strides=(1, 1),
                 padding='valid',
                 use_bias=True,
                 depthwise_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 depthwise_regularizer=None,
                 bias_regularizer=None,
                 depthwise_constraint=None,
                 bias_constraint=None,
                 quantizer=WeightFloat(),
                 **kwargs):
        """Creates a quantization-aware depthwise convolutional layer.

        Args:
            kernel_size (a tuple of integer): the kernel spatial dimensions.
            strides (integer, or tuple of integers, optional): strides of the
                convolution along height and width.
            padding (str, optional): One of 'valid' or 'same'.
            use_bias (boolean, optional): whether the layer uses a bias vector.
            depthwise_initializer (str, or a :obj:`tf.keras.initializer`, optional):
                initializer for the weights matrix.
            bias_initializer (str, or a :obj:`tf.keras.initializer`, optional):
                initializer for the bias vector.
            depthwise_regularizer (str, or a :obj:`tf.keras.initializer`, optional):
                regularization applied to the weights.
            bias_regularizer (str, or a :obj:`tf.keras.initializer`, optional):
                regularization applied to the bias.
            depthwise_constraint (str, or a :obj:`tf.keras.initializer`, optional):
                constraint applied to the weights.
            bias_constraint (str, or a :obj:`tf.keras.initializer`, optional):
                constraint applied to the bias.
            quantizer (:obj:`cnn2snn.WeightQuantizer`, optional): the quantizer
                to apply during the forward pass.

        """
        _check_unsupported_args(kwargs, self.unsupported_args)
        self.quantizer = get_quantizer(quantizer)
        super(QuantizedDepthwiseConv2D,
              self).__init__(kernel_size=kernel_size,
                             strides=strides,
                             padding=padding,
                             use_bias=use_bias,
                             depthwise_initializer=depthwise_initializer,
                             bias_initializer=bias_initializer,
                             depthwise_regularizer=depthwise_regularizer,
                             bias_regularizer=bias_regularizer,
                             depthwise_constraint=depthwise_constraint,
                             bias_constraint=bias_constraint,
                             **kwargs)

    def call(self, inputs):
        """Evaluates input Tensor.

        This applies the quantization on weights, then evaluates the input
        Tensor and produces the output Tensor.

        Args:
            inputs (:obj:`tensorflow.Tensor`): input Tensor.

        Returns:
            :obj:`tensorflow.Tensor`: output Tensor.

        """
        # We don't support biases
        return K.depthwise_conv2d(inputs,
                                  self.quantizer.quantize(
                                      self.depthwise_kernel),
                                  strides=self.strides,
                                  padding=self.padding,
                                  dilation_rate=self.dilation_rate,
                                  data_format=self.data_format)

    def get_config(self):
        config = super().get_config()
        config['quantizer'] = serialize_keras_object(self.quantizer)
        for kwarg in self.unsupported_args:
            config.pop(kwarg, None)
        return config


class QuantizedDense(layers.Dense):
    """A quantization-aware Keras dense layer.

    Inherits from Keras Dense layer, applying a quantization on weights during
    the forward pass.

    """
    unsupported_args = {'activation', 'activity_regularizer'}

    def __init__(self,
                 units,
                 use_bias=True,
                 kernel_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 kernel_regularizer=None,
                 bias_regularizer=None,
                 kernel_constraint=None,
                 bias_constraint=None,
                 quantizer=WeightFloat(),
                 **kwargs):
        """Creates a quantization-aware dense layer.

        Args:
            units (integer): the number of neurons.
            use_bias (boolean, optional): whether the layer uses a bias vector.
            kernel_initializer (str, or a :obj:`tf.keras.initializer`, optional):
                initializer for the weights matrix.
            bias_initializer (str, or a :obj:`tf.keras.initializer`, optional):
                initializer for the bias vector.
            kernel_regularizer (str, or a :obj:`tf.keras.regularizer`, optional):
                regularization applied to the weights.
            bias_regularizer (str, or a :obj:`tf.keras.regularizer`, optional):
                regularization applied to the bias.
            kernel_constraint (str, or a :obj:`tf.keras.constraint`, optional):
                constraint applied to the weights.
            bias_constraint (str, or a :obj:`tf.keras.constraint`, optional):
                constraint applied to the bias.
            quantizer (:obj:`cnn2snn.WeightQuantizer`, optional): the quantizer
                to apply during the forward pass.

        """
        _check_unsupported_args(kwargs, self.unsupported_args)
        self.quantizer = get_quantizer(quantizer)
        super(QuantizedDense,
              self).__init__(units=units,
                             use_bias=use_bias,
                             kernel_initializer=kernel_initializer,
                             bias_initializer=bias_initializer,
                             kernel_regularizer=kernel_regularizer,
                             bias_regularizer=bias_regularizer,
                             kernel_constraint=kernel_constraint,
                             bias_constraint=bias_constraint,
                             **kwargs)

    def call(self, inputs):
        """Evaluates input Tensor.

        This applies the quantization on weights, then evaluates the input
        Tensor and produces the output Tensor.

        Args:
            inputs (:obj:`tensorflow.Tensor`): input Tensor.

        Returns:
            :obj:`tensorflow.Tensor`: output Tensor.

        """
        kernel = self.quantizer.quantize(self.kernel)
        rank = len(inputs.shape)
        if rank > 2:
            # Broadcasting is required for the inputs.
            outputs = standard_ops.tensordot(inputs, kernel, [[rank - 1], [0]])
            # Reshape the output back to the original ndim of the input.
            if not context.executing_eagerly():
                shape = inputs.shape.as_list()
                output_shape = shape[:-1] + [self.units]
                outputs.set_shape(output_shape)
        else:
            inputs = math_ops.cast(inputs, self._compute_dtype)
            if K.is_sparse(inputs):
                outputs = sparse_ops.sparse_tensor_dense_matmul(inputs, kernel)
            else:
                outputs = gen_math_ops.mat_mul(inputs, kernel)
        if self.use_bias:
            outputs = nn.bias_add(outputs, self.bias)
        return outputs

    def get_config(self):
        config = super().get_config()
        config['quantizer'] = serialize_keras_object(self.quantizer)
        for kwarg in self.unsupported_args:
            config.pop(kwarg, None)
        return config


class QuantizedSeparableConv2D(layers.SeparableConv2D):
    """A quantization-aware Keras separable convolutional layer.

    Inherits from Keras SeparableConv2D layer, applying a quantization on
    weights during the forward pass.

    """
    unsupported_args = {
        'data_format', 'activation', 'dilation_rate', 'depth_multiplier',
        'activity_regularizer'
    }

    def __init__(self,
                 filters,
                 kernel_size,
                 strides=(1, 1),
                 padding='valid',
                 use_bias=True,
                 depthwise_initializer='glorot_uniform',
                 pointwise_initializer='glorot_uniform',
                 bias_initializer='zeros',
                 depthwise_regularizer=None,
                 pointwise_regularizer=None,
                 bias_regularizer=None,
                 depthwise_constraint=None,
                 pointwise_constraint=None,
                 bias_constraint=None,
                 quantizer=WeightFloat(),
                 quantizer_dw=None,
                 **kwargs):
        """Creates a quantization-aware separable convolutional layer.

        Args:
            filters (integer): the number of filters.
            kernel_size (tuple of integer): the kernel spatial dimensions.
            strides (integer, or tuple of integers, optional): strides of the
                convolution along height and width.
            padding (str, optional): One of 'valid' or 'same'.
            use_bias (boolean, optional): Whether the layer uses a bias vector.
            depthwise_initializer (str, or a :obj:`tf.keras.initializer`, optional):
                initializer for the depthwise kernel.
            pointwise_initializer (str, or a :obj:`tf.keras.initializer`, optional):
                initializer for the pointwise kernel.
            bias_initializer (str, or a :obj:`tf.keras.initializer`, optional):
                initializer for the bias vector.
            depthwise_regularizer (str, or a :obj:`tf.keras.regularizer`, optional):
                regularization applied to the depthwise kernel.
            pointwise_regularizer (str, or a :obj:`tf.keras.regularizer`, optional):
                regularization applied to the pointwise kernel.
            bias_regularizer (str, or a :obj:`tf.keras.regularizer`, optional):
                regularization applied to the bias.
            depthwise_constraint (str, or a :obj:`tf.keras.constraint`, optional):
                constraint applied to the depthwise kernel.
            pointwise_constraint (str, or a :obj:`tf.keras.constraint`, optional):
                constraint applied to the pointwise kernel.
            bias_constraint (str, or a :obj:`tf.keras.constraint`, optional):
                constraint applied to the bias.
            quantizer (:obj:`cnn2snn.WeightQuantizer`): the quantizer to apply
                during the forward pass.

        """
        _check_unsupported_args(kwargs, self.unsupported_args)
        self.quantizer = get_quantizer(quantizer)
        if quantizer_dw is None:
            # If no depthwise quantizer provided, use the pointwise quantizer
            # Note: this is compatible with legacy models
            self.quantizer_dw = get_quantizer(
                serialize_keras_object(self.quantizer))
        else:
            self.quantizer_dw = get_quantizer(quantizer_dw)

        super(QuantizedSeparableConv2D,
              self).__init__(filters=filters,
                             kernel_size=kernel_size,
                             strides=strides,
                             padding=padding,
                             use_bias=use_bias,
                             depthwise_initializer=depthwise_initializer,
                             pointwise_initializer=pointwise_initializer,
                             bias_initializer=bias_initializer,
                             depthwise_regularizer=depthwise_regularizer,
                             pointwise_regularizer=pointwise_regularizer,
                             bias_regularizer=bias_regularizer,
                             depthwise_constraint=depthwise_constraint,
                             pointwise_constraint=pointwise_constraint,
                             bias_constraint=bias_constraint,
                             **kwargs)

    def call(self, inputs):
        """Evaluates input Tensor.

        This applies the quantization on weights, then evaluates the input
        Tensor and produces the output Tensor.

        Args:
            inputs (:obj:`tensorflow.Tensor`): input Tensor.

        Returns:
            :obj:`tensorflow.Tensor`: a Tensor.

        """
        strides = (1,) + self.strides + (1,)
        outputs = nn.separable_conv2d(
            inputs,
            self.quantizer_dw.quantize(self.depthwise_kernel),
            self.quantizer.quantize(self.pointwise_kernel),
            strides=strides,
            padding=self.padding.upper(),
            rate=self.dilation_rate,
            data_format=conv_utils.convert_data_format(self.data_format,
                                                       ndim=4))

        if self.use_bias:
            outputs = nn.bias_add(outputs,
                                  self.bias,
                                  data_format=conv_utils.convert_data_format(
                                      self.data_format, ndim=4))

        return outputs

    def get_config(self):
        config = super().get_config()
        config['quantizer_dw'] = serialize_keras_object(self.quantizer_dw)
        config['quantizer'] = serialize_keras_object(self.quantizer)
        for kwarg in self.unsupported_args:
            config.pop(kwarg, None)
        return config


class QuantizedActivation(layers.Layer):
    """Base class for quantized activation layers.

    This base class must be overloaded as well as the three @property
    functions:

    - `threshold`
    - `step_height`
    - `step_width`

    These @property functions must return TensorFlow objects (e.g. tf.Tensor
    or tf.Variable) of scalar values. The `.numpy()` method must be callable on
    them. They can be fixed at initialization or can be trainable variables.

    The CNN2SNN toolkit only support linear quantized activation as defined in
    the `quantized_activation` function.
    """

    def __init__(self, bitwidth, **kwargs):
        """Creates a QuantizedActivation for the specified bitwidth.

        The bitwidth defines the number of quantization levels on which the
        activation will be quantized. For instance, a 4-bit quantization gives
        15 activation levels. More generally, a n-bit quantization gives 2^n-1
        levels.

        Args:
            bitwidth (integer): the quantization bitwidth
        """
        if bitwidth <= 0:
            raise ValueError("Activation 'bitwidth' must be greater than zero."
                             f" Receives 'bitwidth' {bitwidth}.")

        self.bitwidth_ = bitwidth
        self.levels = 2.**bitwidth - 1
        super().__init__(**kwargs)

    def quantized_activation(self, x):
        """Evaluates the quantized activations for the specified input Tensor.

        The quantization is defined by three parameters:

        - the activation threshold, 'threshold'
        - the quantization step size, 'step_height'
        - the step width, 'step_width'

        For any potential x, the activation output is as follows:

        - if x <= threshold, activation is zero
        - if threshold < x <= threshold + step_width, activation is
          step_height
        - if threshold + step_width < x <= threshold + 2*step_width,
          activation is 2*step_height
        - and so on...
        - if x > threshold + levels*step_width, activation is
          levels*step_height

        Args:
            x (:obj:`tensorflow.Tensor`): the input values.

        """
        act = ceil_through((x - self.threshold) / self.step_width)
        clip_act = tf.clip_by_value(act, 0, self.levels)
        return self.step_height * clip_act

    def call(self, inputs):
        return self.quantized_activation(inputs)

    @property
    def bitwidth(self):
        return self.bitwidth_

    @property
    def threshold(self):
        raise NotImplementedError()

    @property
    def step_height(self):
        raise NotImplementedError()

    @property
    def step_width(self):
        raise NotImplementedError()

    def get_config(self):
        config = super().get_config()
        config.update({'bitwidth': self.bitwidth_})
        return config


class ActivationDiscreteRelu(QuantizedActivation):
    """A discrete ReLU Keras Activation.

    Activations will be quantized and will have 2^bitwidth values in the range
    [0,6].

    """

    def __init__(self, bitwidth=1, **kwargs):
        """Creates a discrete ReLU for the specified bitwidth.

        Args:
            bitwidth (int): the activation bitwidth.

        """

        super().__init__(bitwidth, **kwargs)

        relumax = min(self.levels, 6)
        self.step_height_ = tf.constant(relumax / self.levels)

    @property
    def threshold(self):
        return 0.5 * self.step_height_

    @property
    def step_height(self):
        return self.step_height_

    @property
    def step_width(self):
        return self.step_height_


class QuantizedReLU(QuantizedActivation):
    """A Trainable Quantized ReLU Keras Activation.

    Activations will be clipped to a trainable range, and quantized to a number
    of values defined by the bitwidth: N = (2^bitwidth - 1) values plus zero

    More specifically, this class uses two trainable variables:

    - threshold represents the lower bound of the activation range,
    - step_height represents the step between two quantized activation values.

    The activation range is therefore [threshold, tN_k], with:

        tN_k = threshold + N * step_height = (2^bitwidth - 1) * step_height

    In other words:

    - inputs below threshold will result in no activation
    - inputs between threshold and threshold + tN_k will be ceiled to the nearest
      threshold + n * step_height, and result in a activation of n * step_height
    - inputs above threshold + tN_k will result in a activation of N * step_height

    """

    def __init__(self, bitwidth=1, **kwargs):
        """Creates a QuantizedReLU for the specified bitwidth.

        Args:
            bitwidth (int): the activation bitwidth.

        """
        super().__init__(bitwidth, **kwargs)

        # To be compatible with models trained with ActivationDiscreteRelu, we
        # keep the same rule for the initial value of the activation range
        # relumax and we deduce the initial values of the threshold and
        # step_height from it
        relumax = min(self.levels, 6)
        step_height_initializer = relumax / self.levels
        # Create lower bound variable and initialize it
        threshold_initializer = step_height_initializer / 2.
        self.threshold_ = tf.Variable(name=f"{self.name}/threshold",
                                      initial_value=threshold_initializer,
                                      dtype=tf.float32,
                                      trainable=True)
        # We will actually train the rescaled step, whose value is more
        # consistent between different bitwidth values
        step_initializer = (2.**self.bitwidth) * step_height_initializer / 16
        self.step_ = tf.Variable(name=f"{self.name}/step",
                                 initial_value=step_initializer,
                                 dtype=tf.float32,
                                 trainable=True)

    @property
    def step_height(self):
        return self.step_width

    @property
    def threshold(self):
        return self.threshold_

    @property
    def step_width(self):
        return 16 * self.step_ / 2.**self.bitwidth


# A helper to instantiate a Conv2D layer to which a modifier is assigned
def conv2d(filters, kernel_size, modifier=None, **kwargs):
    layer = QuantizedConv2D(filters, kernel_size, quantizer=modifier, **kwargs)
    return layer


# A helper to instantiate a Dense layer to which a modifier is assigned
def dense(units, modifier=None, **kwargs):
    layer = QuantizedDense(units, quantizer=modifier, **kwargs)
    return layer


# A helper to instantiate a Depthwise Conv2D layer to which a modifier is assigned
def depthwise_conv2d(kernel_size, modifier=None, **kwargs):
    layer = QuantizedDepthwiseConv2D(kernel_size, quantizer=modifier, **kwargs)
    return layer


def separable_conv2d(filters, kernel_size, modifier=None, **kwargs):
    layer = QuantizedSeparableConv2D(filters,
                                     kernel_size,
                                     quantizer=modifier,
                                     **kwargs)
    return layer


def batchNormalization(*args, **kwargs):
    return layers.BatchNormalization(*args, **kwargs)


def maxPooling2D(*args, **kwargs):
    return layers.MaxPooling2D(*args, **kwargs)


def activationFloat(type='relu'):
    return lambda **kwargs: layers.Activation(type, **kwargs)


def activationDiscreteRelu(bitwidth=1, **kwargs):
    return ActivationDiscreteRelu(bitwidth, **kwargs)


def activationDiscreteReluBits(bitwidth=1):
    return lambda **kwargs: activationDiscreteRelu(bitwidth, **kwargs)
