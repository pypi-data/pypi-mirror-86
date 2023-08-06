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
from .modeling_utils import PretrainedConfig, PreTrainedModel

LINFORMER_PRETRAINED_MODEL_ARCHIVE_MAP = {
    'pai-synthesizer-base-en': "synthesizer/pai-synthesizer-base-en/model.ckpt"
}

LINFORMER_PRETRAINED_CONFIG_ARCHIVE_MAP = {
    'pai-synthesizer-base-en': "synthesizer/pai-synthesizer-base-en/config.json"
}


class SynthesizerConfig(PretrainedConfig):
    """Configuration for `FactorizedBert`.

    Args:

      vocab_size: Vocabulary size of `inputs_ids` in `BertModel`.
      hidden_size: Size of the encoder layers and the pooler layer.
      num_hidden_layers: Number of hidden layers in the Transformer encoder.
      num_attention_heads: Number of attention heads for each attention layer in
        the Transformer encoder.
      intermediate_size: The size of the "intermediate" (i.e., feed-forward)
        layer in the Transformer encoder.
      hidden_dropout_prob: The dropout probability for all fully connected
        layers in the embeddings, encoder, and pooler.
      attention_probs_dropout_prob: The dropout ratio for the attention
        probabilities.
      max_position_embeddings: The maximum sequence length that this model might
        ever be used with. Typically set this to something large just in case
        (e.g., 512 or 1024 or 2048).
      type_vocab_size: The vocabulary size of the `token_type_ids` passed into
        `BertModel`.
      initializer_range: The stdev of the truncated_normal_initializer for
        initializing all weight matrices.

    """

    def __init__(self,
                 vocab_size,
                 hidden_size,
                 intermediate_size,
                 num_hidden_layers,
                 num_attention_heads,
                 max_position_embeddings,
                 type_vocab_size,
                 hidden_dropout_prob=0.1,
                 attention_probs_dropout_prob=0.1,
                 initializer_range=0.02,
                 **kwargs):
        super(SynthesizerConfig, self).__init__(**kwargs)
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.intermediate_size = intermediate_size
        self.num_hidden_layers = num_hidden_layers
        self.num_attention_heads = num_attention_heads
        self.max_position_embeddings = max_position_embeddings
        self.type_vocab_size = type_vocab_size
        self.hidden_dropout_prob = hidden_dropout_prob
        self.attention_probs_dropout_prob = attention_probs_dropout_prob
        self.initializer_range = initializer_range

class SelfAttention(layers.Layer):
    def __init__(self, config, **kwargs):
        super(SelfAttention, self).__init__(**kwargs)

        self.hidden_size = config.hidden_size
        self.num_hidden_layers = config.num_hidden_layers
        self.num_attention_heads = config.num_attention_heads
        assert config.hidden_size % config.num_attention_heads == 0
        self.attention_head_size = int(config.hidden_size / config.num_attention_heads)

        self.initializer = layers.get_initializer(config.initializer_range)
        self.dropout = layers.Dropout(config.attention_probs_dropout_prob)

    def build(self, input_shape):

        self.w1 = self.add_weight(
            shape=(self.hidden_size, self.hidden_size),
            initializer=self.initializer,
            dtype=tf.float32,
            name='query/kernel',
        )

        self.b1 = self.add_weight(
            shape=(self.hidden_size,),
            initializer=self.initializer,
            dtype=tf.float32,
            name='query/bias',
        )

        self.w2 = self.add_weight(
            shape=(self.hidden_size, 512),
            initializer=self.initializer,
            dtype=tf.float32,
            name='key/kernel',
        )

        self.b2 = self.add_weight(
            shape=(512,),
            initializer=self.initializer,
            dtype=tf.float32,
            name='key/bias',
        )

        self.v_head_weight = self.add_weight(
            shape=(self.hidden_size, self.hidden_size),
            initializer=self.initializer,
            dtype=tf.float32,
            name='value/kernel',
        )

        self.v_head_bias = self.add_weight(
            shape=(self.hidden_size,),
            initializer=self.initializer,
            dtype=tf.float32,
            name='value/bias',
        )

        super(SelfAttention, self).build(input_shape)

    def _abs_attn_core(self, tmp, v_head, attn_mask, training,
                       scale):

        attn_score = tf.multiply(tmp, scale)
        adder = (1.0 - tf.cast(attn_mask, tf.float32)) * -10000.0
        attn_score += adder
        attn_prob = tf.nn.softmax(attn_score)
        attn_prob = self.dropout(attn_prob, training=training)
        attn_vec = tf.einsum('bij,bjd->bid', attn_prob, v_head)
        return attn_vec

    def call(self, attention_input, attention_mask, kv=None, training=False):

        tmp1 = tf.einsum('bnm,md->bnd', attention_input, self.w1)
        tmp1 = tf.nn.relu(tf.nn.bias_add(tmp1, self.b1))

        tmp2 = tf.einsum('bnm,md->bnd', tmp1, self.w2)
        tmp2 = tf.nn.bias_add(tmp2, self.b2)

        v_head_h = tf.einsum('bnm,md->bnd', attention_input, self.v_head_weight)
        v_head_h = tf.nn.bias_add(v_head_h, self.v_head_bias)

        scale = 1 / (self.attention_head_size ** 0.5)

        attn_vec = self._abs_attn_core(tmp2, v_head_h, attention_mask, training, scale)
        return attn_vec

class dense_dropoutput_layernorm(layers.Layer):
    def __init__(self, config, **kwargs):
        super(dense_dropoutput_layernorm, self).__init__(**kwargs)
        self.dense = layers.Dense(
            config.hidden_size, kernel_initializer=layers.get_initializer(config.initializer_range), name="dense"
        )
        self.LayerNorm = layers.LayerNormalization
        self.dropout = layers.Dropout(config.hidden_dropout_prob)

    def call(self, inputs, training=False):
        hidden_states, input_tensor = inputs
        hidden_states = self.dense(hidden_states)
        hidden_states = self.dropout(hidden_states, training=training)
        hidden_states = self.LayerNorm(hidden_states + input_tensor, name="LayerNorm")
        return hidden_states

class Attention(layers.Layer):
    def __init__(self, config, **kwargs):
        super(Attention, self).__init__(**kwargs)
        self.self_attention = SelfAttention(config, name="self")
        self.dense_output = dense_dropoutput_layernorm(config, name="output")

    def call(self, inputs, training=False):
        input_tensor, attention_mask = inputs
        self_outputs = self.self_attention(input_tensor, attention_mask, training=training)
        attention_output = self.dense_output([self_outputs, input_tensor], training=training)
        return attention_output

class EncoderBlock(layers.Layer):
    def __init__(self, config, **kwargs):
        super(EncoderBlock, self).__init__(**kwargs)
        self.attention = Attention(config, name="attention")
        # Use gelu_new, then match results

        self.intermediate = layers.Dense(
            units=config.intermediate_size,
            activation=layers.gelu_new,
            kernel_initializer=layers.get_initializer(config.initializer_range),
            name="intermediate/dense")

        self.bert_output = dense_dropoutput_layernorm(config, name="output")

    def call(self, inputs, training=False):
        hidden_states, attention_mask = inputs
        attention_output = self.attention([hidden_states, attention_mask], training=training)
        intermediate_output = self.intermediate(attention_output)
        layer_output = self.bert_output([intermediate_output, attention_output], training=training)
        return layer_output, attention_output

class SynthesizerEncoder(layers.Layer):
    def __init__(self, config, **kwargs):
        super(SynthesizerEncoder, self).__init__(**kwargs)
        self.layer = [EncoderBlock(config, name="layer_{}".format(i)) for i in range(config.num_hidden_layers)]

    def call(self, inputs, training=False):
        hidden_states, attention_mask = inputs

        all_hidden_states = ()
        all_att_outputs = ()
        for i, layer_module in enumerate(self.layer):
            layer_output, att_output = layer_module([hidden_states, attention_mask], training=training)
            hidden_states = layer_output
            all_hidden_states = all_hidden_states + (hidden_states,)
            all_att_outputs = all_att_outputs + (att_output,)

        final_outputs = []
        for hidden_states in all_hidden_states:
            final_outputs.append(hidden_states)

        return final_outputs, all_att_outputs

class SynthesizerBackbone(layers.Layer):
    def __init__(self, config, **kwargs):

        self.embeddings = layers.BertEmbeddings(config, name="embeddings")

        self.encoder = SynthesizerEncoder(config, name="encoder")

        self.pooler = layers.Dense(
            units=config.hidden_size,
            activation='tanh',
            kernel_initializer=layers.get_initializer(config.initializer_range),
            name="pooler/dense")

        super(SynthesizerBackbone, self).__init__(config, **kwargs)

    def call(self, inputs,
             input_mask=None,
             segment_ids=None,
             training=False):

        if isinstance(inputs, (tuple, list)):
            input_ids = inputs[0]
            input_mask = inputs[1] if len(inputs) > 1 else input_mask
            segment_ids = inputs[2] if len(inputs) > 2 else segment_ids
        else:
            input_ids = inputs

        input_shape = layers.get_shape_list(input_ids)
        batch_size = input_shape[0]
        seq_length = input_shape[1]

        if input_mask is None:
            input_mask = tf.ones(shape=[batch_size, seq_length], dtype=tf.int32)

        if segment_ids is None:
            segment_ids = tf.zeros(shape=[batch_size, seq_length], dtype=tf.int32)

        embedding_output = self.embeddings([input_ids, segment_ids], training=training)
        attention_mask = layers.get_attn_mask_bert(input_ids, input_mask)
        encoder_outputs = self.encoder([embedding_output, attention_mask], training=training)
        pooled_output = self.pooler(encoder_outputs[0][-1][:, 0])
        outputs = (encoder_outputs[0][-1], pooled_output)
        return outputs


class SynthesizerPreTrainedModel(PreTrainedModel):
    config_class = SynthesizerConfig
    pretrained_model_archive_map = LINFORMER_PRETRAINED_MODEL_ARCHIVE_MAP
    pretrained_config_archive_map = LINFORMER_PRETRAINED_CONFIG_ARCHIVE_MAP

    def __init__(self, config, **kwargs):
        super(SynthesizerPreTrainedModel, self).__init__(config, **kwargs)
        self.bert = SynthesizerBackbone(config, name="synthesizer")
        self.mlm = layers.MLMHead(config, self.bert.embeddings, name="cls/predictions")
        self.nsp = layers.NSPHead(config, name="cls/seq_relationship")

    def call(self, inputs,
             masked_lm_positions=None,
             **kwargs):
        tf.logging.info("********** SynthesizerPreTrainedModel ***********")
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

            mlm_logits = self.mlm(sequence_output, masked_lm_positions)
            nsp_logits = self.nsp(pooled_output)

            return mlm_logits, nsp_logits, pooled_output
