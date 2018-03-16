import numpy as np
import tensorflow as tf


class Network(object):

    def __init__(self, sizes):
        """The list ``sizes`` contains the number of neurons in the
        respective layers of the network.  For example, if the list
        was [2, 3, 1] then it would be a three-layer network, with the
        first layer containing 2 neurons, the second layer 3 neurons,
        and the third layer 1 neuron.  The biases and weights for the
        network are initialized randomly, using a Gaussian
        distribution with mean 0, and variance 1.  Note that the first
        layer is assumed to be an input layer, and by convention we
        won't set any biases for those neurons, since biases are only
        ever used in computing the outputs from later layers."""
        self._num_layer = len(sizes)
        if self._num_layer >= 3:
            self._sizes = sizes

            # used for tensor flow
            self._weights = [tf.Variable(tf.cast(tf.random_normal([y, x]), tf.float64)) for x, y in zip(sizes[:-1], sizes[1:])]
            self._biases = [tf.Variable(tf.cast(tf.random_normal([y, 1]), tf.float64)) for y in sizes[1:]]

            self._input_network = tf.placeholder(tf.float64, shape=[sizes[0], None])
            self._output_network = tf.placeholder(tf.float64, shape=[sizes[self._num_layer - 1], None])

            # used for normal computations
            self._np_weights = [np.zeros((y, x)) for x, y in zip(sizes[:-1], sizes[1:])]
            self._np_biases = [np.zeros((y, 1)) for y in sizes[1:]]
        else:
            raise ValueError("This network works only with >= 3 layers")

    def _model_for_nn(self, keep_prob):
        """
        :param keep_prob: list of dropouts of len = self._num_layer - 2 (only for hidden layers)
        :return: output_model: a 1D-narray with two items

        OBS! len(self._weights) and len(self._biases) = self._num_layer - 1
        """

        # compute first layer
        y = tf.nn.dropout(
            tf.nn.relu(tf.matmul(self._weights[0], self._input_network) + self._biases[0]),
            keep_prob=keep_prob[0])

        # compute all hidden layers
        for step in range(1, self._num_layer - 2):
            y = tf.nn.dropout(
                tf.nn.relu(tf.matmul(self._weights[step], y) + self._biases[step]),
                keep_prob=keep_prob[step])

        # compute last layer
        return tf.matmul(self._weights[self._num_layer - 2], y) + self._biases[self._num_layer - 2]

    def model_output(self, input_model):
        # compute first layer
        y = np.dot(self._np_weights[0], input_model) + self._np_biases[0]

        # compute all the other layers
        for step in range(1, self._num_layer - 1):
            y = np.dot(self._np_weights[step], y) + self._np_biases[step]

        return y

    def _loss(self, regularization_loss_step, keep_prob):
        """
        :param regularization_loss_step: hyper-parameter to twick the loss
        :param keep_prob: list of dropouts of len = self._num_layer - 1 (last layer does not have dropout)
        :return: a scalar: loss
        """
        y_ = self._model_for_nn(keep_prob)
        # loss = tf.reduce_mean(
        #     tf.nn.softmax_cross_entropy_with_logits(labels=self._output_network, logits=y_)
        # )

        loss = np.sum((y_ - self._output_network) ** 2) / tf.cast(tf.size(y_), tf.float64)

        regularizes_loss = np.sum(np.array(
            [tf.nn.l2_loss(w) for w in self._weights]
        ))
        return loss + regularization_loss_step * regularizes_loss

    def _optimization(self, minimize_step, regularization_loss_step, keep_prob):
        """
        :param minimize_step: hyper-parameter for the gradient descent optimizer
        :param regularization_loss_step: hyper-parameter to twick the loss
        :param keep_prob: list of dropouts of len = self._num_layer - 1 (last layer does not have dropout)
        :return: train step for the weights
        """
        return tf.train.GradientDescentOptimizer(minimize_step).minimize(self._loss(regularization_loss_step, keep_prob))

    def session_train(self, minimize_step, regularization_loss_step, keep_prob, input_nn, output_nn):
        """
        :param minimize_step: hyper-parameter for the gradient descent optimizer
        :param regularization_loss_step: hyper-parameter to twick the loss
        :param keep_prob: list of dropouts of len = self._num_layer - 1 (last layer does not have dropout)
        :param input_nn: input for the placeholder
        :param output_nn: output for the placeholder
        :return: None
        """

        with tf.Session() as sess:
            sess.run(tf.global_variables_initializer())

            # optimize the variables
            train_step = self._optimization(minimize_step, regularization_loss_step, keep_prob)
            train_step.run(feed_dict={self._input_network: np.transpose(input_nn),
                                      self._output_network: np.transpose(output_nn)})

            # print accuracy
            # correct_prediction = tf.equal(tf.arg_max(tf.transpose(self._model_for_nn(keep_prob)), 1),
            #                              tf.arg_max(output_nn, 1))
            # accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
            # print("Accuracy: {}".format(accuracy.eval(feed_dict={self._input_network: np.transpose(input_nn),
            #                               self._output_network: np.transpose(output_nn)})))

            loss = tf.reduce_mean(self._loss(regularization_loss_step, keep_prob))

            print("Loss: {}".format(loss.eval(feed_dict={self._input_network: np.transpose(input_nn),
                                                         self._output_network: np.transpose(output_nn)})))

            # save weights
            self._np_weights = np.array(sess.run(self._weights))
            self._np_biases = np.array(sess.run(self._biases))

    def print_loss(self, input_nn, output_nn):
        loss = np.sum((np.transpose(np.array(output_nn)) - self.model_output(np.transpose(np.array(input_nn)))) ** 2) / len(input_nn)
        print("PRINT LOSS: {}".format(loss))
