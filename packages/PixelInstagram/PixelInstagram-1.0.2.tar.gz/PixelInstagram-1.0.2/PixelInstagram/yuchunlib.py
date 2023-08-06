import tensorflow as tf
import numpy as np
from PIL import Image
import os

WEIGHTS_INIT_STDEV = .1

CURRENT_PATH = os.path.abspath(__file__)

def net(image):
    conv1 = _conv_layer(image, 32, 9, 1)
    conv2 = _conv_layer(conv1, 64, 3, 2)
    conv3 = _conv_layer(conv2, 128, 3, 2)
    resid1 = _residual_block(conv3, 3)
    resid2 = _residual_block(resid1, 3)
    resid3 = _residual_block(resid2, 3)
    resid4 = _residual_block(resid3, 3)
    resid5 = _residual_block(resid4, 3)
    conv_t1 = _conv_tranpose_layer(resid5, 64, 3, 2)
    conv_t2 = _conv_tranpose_layer(conv_t1, 32, 3, 2)
    conv_t3 = _conv_layer(conv_t2, 3, 9, 1, relu=False)
    preds = tf.nn.tanh(conv_t3) * 150 + 255./2
    return preds


def _conv_layer(net, num_filters, filter_size, strides, relu=True):
    weights_init = _conv_init_vars(net, num_filters, filter_size)
    strides_shape = [1, strides, strides, 1]
    net = tf.nn.conv2d(input=net, filter=weights_init, strides=strides_shape, padding='SAME')
    net = _instance_norm(net)
    if relu:
        net = tf.nn.relu(net)
    return net


def _conv_tranpose_layer(net, num_filters, filter_size, strides):
    weights_init = _conv_init_vars(net, num_filters, filter_size, transpose=True)

    batch_size, rows, cols, in_channels = [i for i in net.get_shape()]
    new_rows, new_cols = int(rows * strides), int(cols * strides)
    # new_shape = #tf.pack([tf.shape(net)[0], new_rows, new_cols, num_filters])

    new_shape = [batch_size, new_rows, new_cols, num_filters]
    tf_shape = tf.stack(new_shape)
    strides_shape = [1,strides,strides,1]

    net = tf.nn.conv2d_transpose(net, weights_init, tf_shape, strides_shape, padding='SAME')
    net = _instance_norm(net)
    return tf.nn.relu(net)


def _residual_block(net, filter_size=3):
    tmp = _conv_layer(net, 128, filter_size, 1)
    return net + _conv_layer(tmp, 128, filter_size, 1, relu=False)


def _instance_norm(net):
    batch, rows, cols, channels = [i for i in net.get_shape()]
    var_shape = [channels]
    mu, sigma_sq = tf.nn.moments(x=net, axes=[1, 2], keep_dims=True)
    shift = tf.Variable(tf.zeros(var_shape))
    scale = tf.Variable(tf.ones(var_shape))
    epsilon = 1e-3
    normalized = (net-mu)/(sigma_sq + epsilon)**(.5)
    return scale * normalized + shift


def _conv_init_vars(net, out_channels, filter_size, transpose=False):
    _, rows, cols, in_channels = [i for i in net.get_shape()]
    if not transpose:
        weights_shape = [int(filter_size), int(filter_size), int(in_channels), int(out_channels)]
    else:
        weights_shape = [int(filter_size), int(filter_size), int(out_channels), int(in_channels)]

    weights_init = tf.Variable(tf.random.truncated_normal(shape=weights_shape, stddev=WEIGHTS_INIT_STDEV, seed=1),
                               dtype=tf.dtypes.float32)

    return weights_init


def ffwd(data_in, checkpoint_dir, device_t, batch_size):

    img_shape = data_in.shape
    g = tf.Graph()
    batch_size = batch_size
    soft_config = tf.compat.v1.ConfigProto(allow_soft_placement=True)
    soft_config.gpu_options.allow_growth = True

    with g.as_default(), g.device(device_t), tf.compat.v1.Session(config=soft_config) as sess:
        batch_shape = (batch_size,) + img_shape
        img_placeholder = tf.compat.v1.placeholder(tf.float32, shape=batch_shape, name='img_placeholder')
        preds = net(img_placeholder)
        saver = tf.compat.v1.train.Saver()
        if os.path.isdir(checkpoint_dir):
            ckpt = tf.train.get_checkpoint_state(checkpoint_dir)
            if ckpt and ckpt.model_checkpoint_path:
                saver.restore(sess, ckpt.model_checkpoint_path)
            else:
                raise Exception("No checkpoint found...")
        else:
            saver.restore(sess, checkpoint_dir)

        X = np.zeros(batch_shape, dtype=np.float32)
        img = data_in
        X[0] = img
        _preds = sess.run(preds, feed_dict={img_placeholder: X})
        img = np.clip(_preds[0], 0, 255).astype(np.uint8)
        img = Image.fromarray(img.astype('uint8')).convert('RGB')

    return img


def process(img, model="la_muse"):

    model = os.path.join(os.path.dirname(os.path.abspath(__file__)), "models", f"{model}.ckpt")
    img = np.array(img)
    result_img = ffwd(data_in=img, checkpoint_dir=model, device_t=None, batch_size=1)
    return result_img
