"""
Copyright 2017-2018 Fizyr (https://fizyr.com)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import keras
from .common import evaluate


class Evaluate(keras.callbacks.Callback):
    """
    Evaluation callback for arbitrary datasets.
    """

    def __init__(
        self,
        generator,
        model,
        iou_threshold=0.5,
        score_threshold=0.01,
        max_detections=100,
        save_path=None,
        tensorboard=None,
        weighted_average=False,
        verbose=1
    ):
        """
        Evaluate a given dataset using a given model at the end of every epoch during training.

        Args:
            generator: The generator that represents the dataset to evaluate.
            iou_threshold: The threshold used to consider when a detection is positive or negative.
            score_threshold: The score confidence threshold to use for detections.
            max_detections: The maximum number of detections to use per image.
            save_path: The path to save images with visualized detections to.
            tensorboard: Instance of keras.callbacks.TensorBoard used to log the mAP value.
            weighted_average: Compute the mAP using the weighted average of precisions among classes.
            verbose: Set the verbosity level, by default this is set to 1.
        """
        self.generator = generator
        self.iou_threshold = iou_threshold
        self.score_threshold = score_threshold
        self.max_detections = max_detections
        self.save_path = save_path
        self.tensorboard = tensorboard
        self.weighted_average = weighted_average
        self.verbose = verbose
        self.active_model = model

        super(Evaluate, self).__init__()

    def on_epoch_end(self, epoch, logs=None):
        """
        Generate training metrics.

        Args:
            self: (todo): write your description
            epoch: (todo): write your description
            logs: (todo): write your description
        """
        logs = logs or {}

        # run evaluation
        average_precisions = evaluate(
            self.generator,
            self.active_model,
            iou_threshold=self.iou_threshold,
            score_threshold=self.score_threshold,
            max_detections=self.max_detections,
            visualize=False
        )

        # compute per class average precision
        total_instances = []
        precisions = []
        for label, (average_precision, num_annotations) in average_precisions.items():
            if self.verbose == 1:
                print('{:.0f} instances of class'.format(num_annotations),
                      self.generator.label_to_name(label), 'with average precision: {:.4f}'.format(average_precision))
            total_instances.append(num_annotations)
            precisions.append(average_precision)
        if self.weighted_average:
            self.mean_ap = sum([a * b for a, b in zip(total_instances, precisions)]) / sum(total_instances)
        else:
            self.mean_ap = sum(precisions) / sum(x > 0 for x in total_instances)

        if self.tensorboard is not None and self.tensorboard.writer is not None:
            import tensorflow as tf
            summary = tf.Summary()
            summary_value = summary.value.add()
            summary_value.simple_value = self.mean_ap
            summary_value.tag = "mAP"
            self.tensorboard.writer.add_summary(summary, epoch)

        logs['mAP'] = self.mean_ap

        if self.verbose == 1:
            print('mAP: {:.4f}'.format(self.mean_ap))
