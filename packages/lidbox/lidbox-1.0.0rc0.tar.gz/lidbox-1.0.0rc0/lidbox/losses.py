import tensorflow as tf


class SparseAngularProximity(tf.keras.losses.Loss):
    """
    Angular proximity loss function as described by Gelly, G., Gauvain, J. (2017) Spoken Language Identification Using LSTM-Based Angular Proximity. Proc. Interspeech 2017, 2566-2570, DOI: 10.21437/Interspeech.2017-1334.
    URL: https://www.isca-speech.org/archive/Interspeech_2017/pdfs/1334.PDF

    NOTE: should only be called with sparse true labels from range [0, N) and language vectors of shape [batch_size, D].
    NOTE: delta_weight is not in the paper
    """
    def __init__(self, N, D, delta_weight=1.0, name="AP", **kwargs):
        super().__init__(name=name, **kwargs)
        tf.debugging.assert_greater_equal(N, 1, message="Must have at least 1 class")
        tf.debugging.assert_greater_equal(D, N, message="Language vector dimension cannot be less than number of classes")
        tf.debugging.assert_positive(delta_weight, message="Non-positive delta weight would cause correct classifications to have larger loss values than incorrect classifications.")

        self.delta_weight = tf.constant(delta_weight, tf.float32)
        # Generate reference directions as one-hot encoding of classes -> all are orthogonal
        self.c_T = tf.transpose(tf.math.l2_normalize(tf.one_hot(tf.range(N), D), axis=1))
        # Generate inverse one-hot encoding for masking out sigmoids in equation 3 for l == l_prime pairs
        # I.e. all ones except for diagonal of zeros
        self.zero_mask = tf.one_hot(tf.range(N), N, on_value=0.0, off_value=1.0)

    def call(self, y_true_sparse, y_pred):
        """
        Compute loss for a batch of true labels (shape [batch_size, 1]) and predicted language vectors (shape [batch_size, D]).
        """
        y_pred = tf.convert_to_tensor(y_pred)
        # offsets between predictions and all reference directions
        theta_l_prime = self.theta(y_pred)
        # offset for true directions
        theta_l = tf.gather(theta_l_prime, y_true_sparse, batch_dims=1)
        # equation 3
        deltas = tf.expand_dims(theta_l, -1) - theta_l_prime
        sigmoids = tf.math.sigmoid(self.delta_weight * deltas)
        # mask out all sigmoids computed on deltas where l == l_prime
        mask = tf.gather(self.zero_mask, y_true_sparse, batch_dims=0)
        L_l = tf.math.reduce_sum(mask * sigmoids, axis=1)
        return L_l

    def theta(self, z):
        """
        Compute angular offset (equation 1 in paper) between given language vector z and all reference directions.
        Returns a vector [batch_size, N] of angular offsets for all classes.
        Highest probability language hypothesis is obtained by taking the argmin of the angular offsets (equation 2).
        """
        c_dot_zT = tf.tensordot(z, self.c_T, axes=1, name="AP.theta.dot")
        return tf.math.acos(c_dot_zT, name="AP.theta.acos")

    def predict(self, z):
        return -self.theta(z)


if __name__ == "__main__":
    import time
    import numpy as np
    import tensorflow as tf
    tf.config.set_visible_devices([], "GPU")

    num_labels = 3
    num_langvec_dims = 100

    def noisy_langvec(i, dim):
        v = np.random.normal(0, 0, size=dim)
        v[i] = 1.0
        return v

    # Sparse true classes
    y_true_sparse = np.array([0, 1, 1, 1, 0, 2, 1, 2], np.int32)

    # Test predictions, starting with 0 errors, up to all wrong
    pred_test_cases = [
        [0, 1, 1, 1, 0, 2, 1, 2],
        [0, 1, 1, 2, 0, 2, 1, 2],
        [1, 1, 1, 2, 0, 2, 1, 2],
        [1, 2, 1, 2, 0, 2, 1, 2],
        [1, 2, 0, 2, 0, 2, 1, 2],
        [1, 2, 0, 2, 1, 2, 1, 2],
        [1, 2, 0, 2, 1, 1, 1, 2],
        [1, 2, 0, 2, 1, 1, 0, 2],
        [1, 2, 0, 2, 1, 1, 0, 1],
    ]

    for pred in pred_test_cases:
        # L2-normalized language vectors
        y_pred = np.stack([noisy_langvec(i, num_langvec_dims) for i in pred])
        y_pred = tf.constant(y_pred, tf.float32)
        y_pred = tf.math.l2_normalize(y_pred, axis=1)

        pred = np.array(pred, np.int32)
        print("testing {} correct out of {}"
              .format((pred == y_true_sparse).sum(), y_true_sparse.size))

        begin = time.perf_counter()

        loss = SparseAngularProximity(N=num_labels, D=num_langvec_dims)(y_true_sparse, y_pred)

        end = time.perf_counter() - begin
        print("ap loss: {}, took {:.6f} sec".format(loss, end))
