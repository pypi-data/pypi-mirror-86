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

import pdb

import math
import tensorflow as tf

from easytransfer import layers
from .modeling_utils import PretrainedConfig, PreTrainedModel

CONVBERT_PRETRAINED_MODEL_ARCHIVE_MAP = {
    'pai-convbert-base-en': "convbert/pai-convbert-base-en/model.ckpt"
}

CONVBERT_PRETRAINED_CONFIG_ARCHIVE_MAP = {
    'pai-convbert-base-en': "convbert/pai-convbert-base-en/config.json"
}


class ConvBertConfig(PretrainedConfig):
    """Configuration for `FactorizedBert`.

    Args:

      vocab_size: Vocabulary size of `inputs_ids` in `BertModel`.
      factorized_size: internal size of matrix factorization
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
        super(ConvBertConfig, self).__init__(**kwargs)
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


class ConvBertEmbeddings(layers.Layer):
    """Construct the embeddings from word, position and token_type embeddings.
    """

    def __init__(self, config, **kwargs):
        super(ConvBertEmbeddings, self).__init__(**kwargs)

        self.vocab_size = config.vocab_size
        self.hidden_size = config.hidden_size
        self.initializer_range = config.initializer_range
        self.token_type_vocab_size = config.type_vocab_size
        self.max_position_embeddings = config.max_position_embeddings

        self.LayerNorm = layers.LayerNormalization
        self.dropout = layers.Dropout(config.hidden_dropout_prob)
        self.initializer = layers.get_initializer(self.initializer_range)

    def build(self, input_shape):
        """Build shared word embedding layer """
        self.word_embeddings = self.add_weight(
            "word_embeddings",
            dtype=tf.float32,
            shape=[self.vocab_size, self.hidden_size],
            initializer=self.initializer,
        )

        self.position_embeddings = self.add_weight(
            "position_embeddings",
            dtype=tf.float32,
            shape=[self.max_position_embeddings, self.hidden_size],
            initializer=self.initializer,
        )

        super(ConvBertEmbeddings, self).build(input_shape)

    def call(self, inputs, training=False):
        input_ids, token_type_ids = inputs

        input_embeddings = tf.gather(self.word_embeddings, input_ids)

        input_shape = layers.get_shape_list(input_embeddings)
        seq_length = input_shape[1]

        position_embeddings = tf.gather(self.position_embeddings, tf.range(0, seq_length))
        position_embeddings = tf.expand_dims(position_embeddings, 0)

        input_embeddings += position_embeddings

        output = self.LayerNorm(input_embeddings, name="LayerNorm")
        output = self.dropout(output, training=training)
        return output


class SelfAttention(layers.Layer):
    def __init__(self, config, **kwargs):
        super(SelfAttention, self).__init__(**kwargs)

        self.hidden_size = config.hidden_size
        self.num_hidden_layers = config.num_hidden_layers
        self.num_attention_heads = config.num_attention_heads
        assert config.hidden_size % config.num_attention_heads == 0
        self.attention_head_size = int(config.hidden_size / config.num_attention_heads)

        self.conv_kernel_size = 9
        self.initializer = layers.get_initializer(config.initializer_range)
        self.initializer_c = layers.get_initializer(1 / self.conv_kernel_size)
        self.dropout = layers.Dropout(config.attention_probs_dropout_prob)

    def build(self, input_shape):

        self.q_head_weight = self.add_weight(
            shape=(self.hidden_size, self.num_attention_heads, self.attention_head_size),
            initializer=self.initializer,
            dtype=tf.float32,
            name='query/kernel',
        )
        self.q_head_bias = self.add_weight(
            shape=(self.num_attention_heads, self.attention_head_size),
            initializer=self.initializer,
            dtype=tf.float32,
            name='query/bias',
        )

        self.k_head_weight = self.add_weight(
            shape=(self.hidden_size, self.num_attention_heads, self.attention_head_size),
            initializer=self.initializer,
            dtype=tf.float32,
            name='key/kernel',
        )

        self.k_head_bias = self.add_weight(
            shape=(self.num_attention_heads, self.attention_head_size),
            initializer=self.initializer,
            dtype=tf.float32,
            name='key/bias',
        )

        self.v_head_weight = self.add_weight(
            shape=(self.hidden_size, self.num_attention_heads, self.attention_head_size),
            initializer=self.initializer,
            dtype=tf.float32,
            name='value/kernel',
        )

        self.v_head_bias = self.add_weight(
            shape=(self.num_attention_heads, self.attention_head_size),
            initializer=self.initializer,
            dtype=tf.float32,
            name='value/bias',
        )

        super(SelfAttention, self).build(input_shape)

    def dot_product_attention(self, q_head, k_head, v_head, attn_mask, training):

        scale = 1 / (math.sqrt(float(self.attention_head_size)))
        logits = tf.matmul(q_head, k_head, transpose_b=True)
        logits = tf.multiply(logits, scale)
        attn_mask = tf.expand_dims(attn_mask, axis=[1])
        adder = (1.0 - tf.cast(attn_mask, tf.float32)) * -10000.0
        logits += adder

        attn_prob = tf.nn.softmax(logits)
        attn_prob = self.dropout(attn_prob, training=training)

        context_layer = tf.matmul(attn_prob, v_head)
        return context_layer

    def reshape_to_matrix(self, input_tensor):
        """Reshapes a >= rank 2 tensor to a rank 2 tensor (i.e., a matrix)."""
        ndims = input_tensor.shape.ndims
        if ndims < 2:
            raise ValueError("Input tensor must have at least rank 2. Shape = %s" %
                             (input_tensor.shape))
        if ndims == 2:
            return input_tensor

        width = input_tensor.shape[-1]
        output_tensor = tf.reshape(input_tensor, [-1, width])
        return output_tensor

    def reshape_for_conv(self, input_tensor, batch_size, num_attention_heads,
                         seq_length, width):
        output_tensor = tf.reshape(
            input_tensor, [batch_size, seq_length, num_attention_heads * width])
        return output_tensor

    def call(self, attention_input, attention_mask, kv=None, training=False):
        q_input = attention_input
        if kv is None:
            k_input = attention_input
            v_input = attention_input
        else:
            k_input = v_input = kv

        """
        q_head_h = tf.einsum("BFH,HND->BFND", q_input, self.q_head_weight)
        q_head_h += self.q_head_bias

        k_head_h = tf.einsum("BFH,HND->BFND", k_input, self.k_head_weight)
        k_head_h += self.k_head_bias

        v_head_h = tf.einsum("BFH,HND->BFND", v_input, self.v_head_weight)
        v_head_h += self.v_head_bias
        """

        from_tensor_2d = self.reshape_to_matrix(q_input)
        to_tensor_2d = self.reshape_to_matrix(k_input)

        # `query_layer` = [B*F, N*H]
        query_layer = tf.layers.dense(
            from_tensor_2d,
            self.num_attention_heads * self.attention_head_size,
            activation=None,
            name="query1",
            kernel_initializer=self.initializer)


        batch_size = tf.shape(attention_mask)[0]
        seq_length = tf.shape(attention_mask)[1]

        key_conv_attn_layer = self.reshape_for_conv(to_tensor_2d, batch_size, self.num_attention_heads,
                                               seq_length, self.attention_head_size)

        key_conv_attn_layer = tf.layers.separable_conv1d(key_conv_attn_layer,
                                              self.num_attention_heads * self.attention_head_size,
                                              self.conv_kernel_size,
                                              padding='same',
                                              activation=None,
                                              depthwise_initializer=self.initializer_c,
                                              pointwise_initializer=self.initializer,
                                              name="conv_attn_key")

        key_conv_attn_layer = self.reshape_to_matrix(key_conv_attn_layer)

        conv_attn_layer = tf.multiply(key_conv_attn_layer, query_layer)

        conv_kernel_layer = tf.layers.dense(
            conv_attn_layer,
            self.num_attention_heads * self.conv_kernel_size,
            activation=None,
            name="conv_attn_kernel",
            kernel_initializer=self.initializer)

        conv_kernel_layer = tf.reshape(conv_kernel_layer,
                                       [batch_size * seq_length * self.num_attention_heads,
                                        self.conv_kernel_size, 1])

        conv_kernel_layer = tf.nn.softmax(conv_kernel_layer, axis=1)

        paddings = tf.constant([[0, 0, ], [int((self.conv_kernel_size - 1) / 2), int((self.conv_kernel_size - 1) / 2)], [0, 0]])

        conv_out_layer = tf.layers.dense(
            to_tensor_2d,
            self.num_attention_heads * self.attention_head_size,
            activation=None,
            name="conv_attn_point",
            kernel_initializer=self.initializer)
        # [B,T, N*H]
        conv_out_layer = tf.reshape(conv_out_layer, [batch_size, seq_length, self.num_attention_heads * self.attention_head_size])

        conv_out_layer = tf.pad(conv_out_layer, paddings, "CONSTANT")
        # unfold [B,T, N*H, K]
        unfold_conv_out_layer = tf.stack(
            [tf.slice(conv_out_layer, [0, i, 0], [batch_size, seq_length, self.num_attention_heads * self.attention_head_size]) for i
             in range(self.conv_kernel_size)], -1)
        # following only work for gpu version
        # conv_out_layer = tf.reshape(conv_out_layer,[batch_size,to_seq_length,num_attention_heads * size_per_head,1])
        # unfold_conv_out_layer = tf.extract_image_patches(images=conv_out_layer, sizes=[1, conv_kernel_size, 1, 1], strides=[1, 1, 1, 1], rates=[1, 1, 1, 1], padding='SAME')

        conv_out_layer = tf.reshape(unfold_conv_out_layer,
                                    [batch_size * seq_length * self.num_attention_heads, self.attention_head_size, self.conv_kernel_size])

        conv_out_layer = tf.matmul(conv_out_layer, conv_kernel_layer)
        conv_out_layer = tf.reshape(conv_out_layer, [batch_size, seq_length, self.num_attention_heads, self.attention_head_size])
        return conv_out_layer


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
        self.hidden_size = config.hidden_size
        self.num_attention_heads = config.num_attention_heads
        self.attention_head_size = int(config.hidden_size / config.num_attention_heads)
        self.self_attention = SelfAttention(config, name="self")
        self.dropout = layers.Dropout(config.hidden_dropout_prob)
        self.LayerNorm = layers.LayerNormalization
        self.initializer = layers.get_initializer(config.initializer_range)

    def build(self, input_shape):
        self.weight = self.add_weight(
            shape=(self.num_attention_heads, self.attention_head_size, self.hidden_size),
            initializer=self.initializer,
            dtype=tf.float32,
            name='query/kernel',
        )
        self.bias = self.add_weight(
            shape=(self.hidden_size,),
            initializer=self.initializer,
            dtype=tf.float32,
            name='query/bias',
        )
        super(Attention, self).build(input_shape)

    def call(self, inputs, training=False):
        input_tensor, attention_mask = inputs
        attention_output = self.self_attention(input_tensor, attention_mask, training=training)
        attention_output = tf.einsum("BFND,NDH->BFH", attention_output, self.weight)
        attention_output += self.bias
        attention_output = self.dropout(attention_output, training=training)
        attention_output = self.LayerNorm(attention_output + input_tensor, name="LayerNorm")
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


class ConvBertEncoder(layers.Layer):
    def __init__(self, config, **kwargs):
        super(ConvBertEncoder, self).__init__(**kwargs)
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


class ConvBertBackbone(layers.Layer):
    def __init__(self, config, **kwargs):

        self.embeddings = ConvBertEmbeddings(config, name="embeddings")

        self.encoder = ConvBertEncoder(config, name="encoder")

        self.pooler = layers.Dense(
            units=config.hidden_size,
            activation='tanh',
            kernel_initializer=layers.get_initializer(config.initializer_range),
            name="pooler/dense")

        super(ConvBertBackbone, self).__init__(config, **kwargs)

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


class ConvBertPreTrainedModel(PreTrainedModel):
    config_class = ConvBertConfig
    pretrained_model_archive_map = CONVBERT_PRETRAINED_MODEL_ARCHIVE_MAP
    pretrained_config_archive_map = CONVBERT_PRETRAINED_CONFIG_ARCHIVE_MAP

    def __init__(self, config, **kwargs):
        super(ConvBertPreTrainedModel, self).__init__(config, **kwargs)
        self.bert = ConvBertBackbone(config, name="convbert")
        self.mlm = layers.MLMHead(config, self.bert.embeddings, name="cls/predictions")
        self.nsp = layers.NSPHead(config, name="cls/seq_relationship")

    def call(self, inputs,
             masked_lm_positions=None,
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

            mlm_logits = self.mlm(sequence_output, masked_lm_positions)
            nsp_logits = self.nsp(pooled_output)

            return mlm_logits, nsp_logits, pooled_output
