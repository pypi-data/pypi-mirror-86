# coding=utf-8
# Copyright (c) 2019 Alibaba PAI team.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import tensorflow as tf
from easytransfer import layers
from .modeling_utils import PreTrainedModel
from .modeling_bert import BertConfig, BertBackbone

SENTIMENTBERT_PRETRAINED_MODEL_ARCHIVE_MAP = {
    'pai-sentimentbert-base-zh': "sentimentbert/pai-sentimentbert-base-zh/model.ckpt"
}

SENTIMENTBERT_PRETRAINED_CONFIG_ARCHIVE_MAP = {
    'pai-sentimentbert-base-zh': "sentimentbert/pai-sentimentbert-base-zh/config.json",
}

class SentimentBertPreTrainedModel(PreTrainedModel):
    config_class = BertConfig
    pretrained_model_archive_map = SENTIMENTBERT_PRETRAINED_MODEL_ARCHIVE_MAP
    pretrained_config_archive_map = SENTIMENTBERT_PRETRAINED_CONFIG_ARCHIVE_MAP

    def __init__(self, config, **kwargs):
        super(SentimentBertPreTrainedModel, self).__init__(config, **kwargs)

        self.bert = BertBackbone(config, name="bert")
        self.mlm = layers.MLMHead(config, self.bert.embeddings, name="cls/predictions")

    def call(self, inputs,
             masked_lm_positions=None,
             masked_senti_positions=None,
             **kwargs):

        training = kwargs['mode'] == tf.estimator.ModeKeys.TRAIN

        if kwargs.get("output_features", True) == True:
            outputs = self.bert(inputs, training=training)
            sequence_output = outputs[0]
            pooled_output = outputs[1]
            return sequence_output, pooled_output
        else:
            outputs = self.bert(inputs, training=training)
            sequence_output = outputs[0]
            pooled_output = outputs[1]
            input_shape = layers.get_shape_list(sequence_output)
            batch_size = input_shape[0]
            seq_length = input_shape[1]
            if masked_lm_positions is None:
                masked_lm_positions = tf.ones(shape=[batch_size, seq_length], dtype=tf.int64)

            if masked_senti_positions is None:
                masked_senti_positions = tf.ones(shape=[batch_size, seq_length], dtype=tf.int64)

            mlm_logits = self.mlm(sequence_output, masked_lm_positions)
            senti_pol_logits = self.mlm(sequence_output, masked_senti_positions)

            return mlm_logits, senti_pol_logits, pooled_output





