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
import whale as wh

from easytransfer import layers
from .modeling_utils import PretrainedConfig, PreTrainedModel

T5_PRETRAINED_MODEL_ARCHIVE_MAP = {
    'pai-t5-base-zh': "t5/pai-t5-base-zh/model.ckpt",
    'pai-t5-2b-zh': "t5/pai-t5-2b-zh/model.ckpt",
}

T5_PRETRAINED_CONFIG_ARCHIVE_MAP = {
    'pai-t5-base-zh': "t5/pai-t5-base-zh/config.json",
    'pai-t5-2b-zh': "t5/pai-t5-2b-zh/config.json",
}


class T5Config(PretrainedConfig):
    """Configuration for `Transformer`.

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
        super(T5Config, self).__init__(**kwargs)
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
        self.q_head_weight = self.add_weight(
            shape=(self.hidden_size, self.hidden_size),
            initializer=self.initializer,
            dtype=tf.float32,
            name='query/kernel',
        )
        self.q_head_bias = self.add_weight(
            shape=(self.hidden_size,),
            initializer=self.initializer,
            dtype=tf.float32,
            name='query/bias',
        )
        self.k_head_weight = self.add_weight(
            shape=(self.hidden_size, self.hidden_size),
            initializer=self.initializer,
            dtype=tf.float32,
            name='key/kernel',
        )
        self.k_head_bias = self.add_weight(
            shape=(self.hidden_size,),
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

    def _abs_attn_core(self, q_head, k_head, v_head, attn_mask, training,
                       scale):
        attn_score = tf.einsum('bind,bjnd->bnij', q_head, k_head)
        attn_score = tf.multiply(attn_score, scale)

        attn_mask = tf.expand_dims(attn_mask, axis=[1])
        adder = (1.0 - tf.cast(attn_mask, tf.float32)) * -10000.0
        attn_score += adder

        attn_prob = tf.nn.softmax(attn_score)
        attn_prob = self.dropout(attn_prob, training=training)

        attn_vec = tf.einsum('bnij,bjnd->bind', attn_prob, v_head)
        return attn_vec

    def call(self, attention_input, attention_mask, kv=None, training=False):

        q_input = attention_input
        if kv is None:
            k_input = attention_input
            v_input = attention_input
        else:
            k_input = v_input = kv

        batch_size = tf.shape(attention_mask)[0]
        seq_length = tf.shape(attention_mask)[1]

        q_head_h = tf.einsum('bih,hx->bix', q_input, self.q_head_weight)
        q_head_h = tf.nn.bias_add(q_head_h, self.q_head_bias)

        k_head_h = tf.einsum('bih,hx->bix', k_input, self.k_head_weight)
        k_head_h = tf.nn.bias_add(k_head_h, self.k_head_bias)

        v_head_h = tf.einsum('bih,hx->bix', v_input, self.v_head_weight)
        v_head_h = tf.nn.bias_add(v_head_h, self.v_head_bias)

        q_head_h = tf.reshape(q_head_h, [batch_size, seq_length, self.num_attention_heads, self.attention_head_size])
        k_head_h = tf.reshape(k_head_h, [batch_size, seq_length, self.num_attention_heads, self.attention_head_size])
        v_head_h = tf.reshape(v_head_h, [batch_size, seq_length, self.num_attention_heads, self.attention_head_size])

        scale = 1 / (self.attention_head_size ** 0.5)
        attn_vec = self._abs_attn_core(q_head_h, k_head_h, v_head_h, attention_mask, training, scale)
        attn_vec = tf.reshape(attn_vec, [batch_size, seq_length, self.hidden_size])
        return attn_vec


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


class CrossAttention(layers.Layer):
    def __init__(self, config, **kwargs):
        super(CrossAttention, self).__init__(**kwargs)
        self.cross_attention = SelfAttention(config, name="cross")
        self.dense_output = dense_dropoutput_layernorm(config, name="output")

    def call(self, inputs, training=False):
        input_tensor, encoder_hidden_states, attention_mask = inputs
        self_outputs = self.cross_attention(input_tensor, attention_mask,
                                            encoder_hidden_states, training=training)
        attention_output = self.dense_output([self_outputs, input_tensor], training=training)
        return attention_output


class DecoderBlock(layers.Layer):
    def __init__(self, config, **kwargs):
        super(DecoderBlock, self).__init__(**kwargs)
        self.attention = Attention(config, name="decoder_attention")
        self.cross_attention = CrossAttention(config, name="decoder_cross_attention")
        # Use gelu_new, then match results
        self.intermediate = layers.Dense(
            units=config.intermediate_size,
            activation=layers.gelu_new,
            kernel_initializer=layers.get_initializer(config.initializer_range),
            name="intermediate/dense")

        self.output_1 = dense_dropoutput_layernorm(config, name="output_1")

        self.output_2 = dense_dropoutput_layernorm(config, name="output_2")

    def call(self, inputs, training=False):
        hidden_states, encoder_hidden_states, attention_mask, encoder_attention_mask = inputs
        attention_output = self.attention([hidden_states, attention_mask], training=training)

        cross_attention_output = self.cross_attention([hidden_states, encoder_hidden_states,
                                                       encoder_attention_mask])

        attention_output = self.output_1([attention_output, cross_attention_output], training=training)
        intermediate_output = self.intermediate(attention_output)
        layer_output = self.output_2([intermediate_output, attention_output], training=training)
        return layer_output, attention_output


class T5Encoder(layers.Layer):
    def __init__(self, config, **kwargs):
        super(T5Encoder, self).__init__(**kwargs)
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


class T5Decoder(layers.Layer):
    def __init__(self, config, **kwargs):
        super(T5Decoder, self).__init__(**kwargs)
        self.layer = [DecoderBlock(config, name="decoder_layer_{}".format(i)) for i in range(config.num_hidden_layers)]

    def call(self, inputs, training=False):
        hidden_states, encoder_hidden_states, attention_mask, encoder_attention_mask = inputs

        all_hidden_states = ()
        all_att_outputs = ()
        for i, layer_module in enumerate(self.layer):
            layer_output, att_output = layer_module([hidden_states,
                                                     encoder_hidden_states,
                                                     attention_mask,
                                                     encoder_attention_mask
                                                     ], training=training)
            hidden_states = layer_output
            all_hidden_states = all_hidden_states + (hidden_states,)
            all_att_outputs = all_att_outputs + (att_output,)

        final_outputs = []
        for hidden_states in all_hidden_states:
            final_outputs.append(hidden_states)

        return final_outputs, all_att_outputs


class T5EncoderWhale(layers.Layer):
    def __init__(self, config, **kwargs):
        super(T5EncoderWhale, self).__init__(**kwargs)
        self.layer = [EncoderBlock(config, name="layer_{}".format(i)) for i in range(config.num_hidden_layers)]

    def call(self, inputs, training=False):
        hidden_states, attention_mask = inputs

        all_hidden_states = ()
        all_att_outputs = ()
        assert len(self.layer) == 24
        for i in range(0, 6):
            layer_output, att_output = self.layer[i]([hidden_states, attention_mask], training=training)
            hidden_states = layer_output
            all_hidden_states = all_hidden_states + (hidden_states,)
            all_att_outputs = all_att_outputs + (att_output,)

        #with wh.stage():
        for i in range(6, 13):
            layer_output, att_output = self.layer[i]([hidden_states, attention_mask], training=training)
            hidden_states = layer_output
            all_hidden_states = all_hidden_states + (hidden_states,)
            all_att_outputs = all_att_outputs + (att_output,)

        with wh.stage():
            for i in range(13, 20):
                layer_output, att_output = self.layer[i]([hidden_states, attention_mask], training=training)
                hidden_states = layer_output
                all_hidden_states = all_hidden_states + (hidden_states,)
                all_att_outputs = all_att_outputs + (att_output,)

        #with wh.stage():
            for i in range(20, 24):
                layer_output, att_output = self.layer[i]([hidden_states, attention_mask], training=training)
                hidden_states = layer_output
                all_hidden_states = all_hidden_states + (hidden_states,)
                all_att_outputs = all_att_outputs + (att_output,)
            wh.current_scope_as_default()

        final_outputs = []
        for hidden_states in all_hidden_states:
            final_outputs.append(hidden_states)

        return final_outputs, all_att_outputs


class T5DecoderWhale(layers.Layer):
    def __init__(self, config, **kwargs):
        super(T5DecoderWhale, self).__init__(**kwargs)
        self.layer = [DecoderBlock(config, name="decoder_layer_{}".format(i)) for i in range(config.num_hidden_layers)]

    def call(self, inputs, training=False):
        hidden_states, encoder_hidden_states, attention_mask, encoder_attention_mask = inputs

        all_hidden_states = ()
        all_att_outputs = ()
        assert len(self.layer) == 24

        for i in range(0, 2):
            layer_output, att_output = self.layer[i]([hidden_states,
                                                      encoder_hidden_states,
                                                      attention_mask,
                                                      encoder_attention_mask
                                                      ], training=training)
            hidden_states = layer_output
            all_hidden_states = all_hidden_states + (hidden_states,)
            all_att_outputs = all_att_outputs + (att_output,)


        with wh.stage():
            for i in range(2, 7):
                layer_output, att_output = self.layer[i]([hidden_states,
                                                          encoder_hidden_states,
                                                          attention_mask,
                                                          encoder_attention_mask
                                                          ], training=training)
                hidden_states = layer_output
                all_hidden_states = all_hidden_states + (hidden_states,)
                all_att_outputs = all_att_outputs + (att_output,)


        #with wh.stage():
            for i in range(7, 13):
                layer_output, att_output = self.layer[i]([hidden_states,
                                                          encoder_hidden_states,
                                                          attention_mask,
                                                          encoder_attention_mask
                                                          ], training=training)
                hidden_states = layer_output
                all_hidden_states = all_hidden_states + (hidden_states,)
                all_att_outputs = all_att_outputs + (att_output,)

        with wh.stage():
            for i in range(13, 18):
                layer_output, att_output = self.layer[i]([hidden_states,
                                                          encoder_hidden_states,
                                                          attention_mask,
                                                          encoder_attention_mask
                                                          ], training=training)
                hidden_states = layer_output
                all_hidden_states = all_hidden_states + (hidden_states,)
                all_att_outputs = all_att_outputs + (att_output,)

        #with wh.stage():
            for i in range(18, 24):
                layer_output, att_output = self.layer[i]([hidden_states,
                                                          encoder_hidden_states,
                                                          attention_mask,
                                                          encoder_attention_mask
                                                          ], training=training)
                hidden_states = layer_output
                all_hidden_states = all_hidden_states + (hidden_states,)
                all_att_outputs = all_att_outputs + (att_output,)
            wh.current_scope_as_default()

        final_outputs = []
        for hidden_states in all_hidden_states:
            final_outputs.append(hidden_states)

        return final_outputs, all_att_outputs



class T5Backbone(layers.Layer):
    def __init__(self, config, **kwargs):

        self.embeddings = layers.BertEmbeddings(config, name="embeddings")

        if not kwargs.pop('enable_whale', False):
            self.encoder = T5Encoder(config, name="t5-encoder")
            self.decoder = T5Decoder(config, name="t5-decoder")
        else:
            tf.logging.info("**************Calling T5EncoderWhale and T5DecoderWhale **************")
            self.encoder = T5EncoderWhale(config, name="t5-encoder-whale")
            self.decoder = T5DecoderWhale(config, name="t5-decoder-whale")

        super(T5Backbone, self).__init__(config, **kwargs)

    def call(self, inputs,
             decoder_input_ids=None,
             input_mask=None,
             decoder_input_mask=None,
             segment_ids=None,
             decoder_segment_ids=None,
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

        if decoder_input_mask is None:
            decoder_input_mask = tf.ones(shape=[batch_size, seq_length], dtype=tf.int32)

        if segment_ids is None:
            segment_ids = tf.zeros(shape=[batch_size, seq_length], dtype=tf.int32)

        if decoder_segment_ids is None:
            decoder_segment_ids = tf.zeros(shape=[batch_size, seq_length], dtype=tf.int32)

        if decoder_input_ids is None:
            decoder_input_ids = input_ids

        embedding_output = self.embeddings([input_ids, segment_ids], training=training)
        attention_mask = layers.get_attn_mask_bert(input_ids, input_mask)
        encoder_outputs = self.encoder([embedding_output, attention_mask], training=training)

        decoder_embedding_output = self.embeddings([decoder_input_ids, decoder_segment_ids], training=training)
        decoder_attention_mask = layers.get_attn_mask_bert(decoder_input_ids, decoder_input_mask)

        encoder_hidden_states = encoder_outputs[0][-1]
        decoder_outputs = self.decoder([decoder_embedding_output,
                                        encoder_hidden_states,
                                        decoder_attention_mask,
                                        attention_mask
                                        ], training=training)

        return decoder_outputs, encoder_outputs


class T5PreTrainedModel(PreTrainedModel):
    config_class = T5Config
    pretrained_model_archive_map = T5_PRETRAINED_MODEL_ARCHIVE_MAP
    pretrained_config_archive_map = T5_PRETRAINED_CONFIG_ARCHIVE_MAP

    def __init__(self, config, **kwargs):
        super(T5PreTrainedModel, self).__init__(config, **kwargs)
        self.transformer = T5Backbone(config, name="t5", enable_whale=kwargs.get("enable_whale", False))
        self.mlm = layers.MLMHead(config, self.transformer.embeddings, name="cls/predictions")
        self.model_dim = config.hidden_size

    def call(self, inputs,
             masked_lm_positions=None,
             **kwargs):

        training = kwargs['mode'] == tf.estimator.ModeKeys.TRAIN
        tf.logging.info("********** T5PreTrainedModel ***********")
        if kwargs.get("output_features", True) == True:
            outputs = self.transformer(inputs, training=training)
            decoder_outputs = outputs[0]
            encoder_outputs = outputs[1]
            return decoder_outputs + encoder_outputs
        else:
            decoder_outputs, _ = self.transformer(inputs)
            sequence_output = decoder_outputs[0][-1] * (self.model_dim ** -0.5)
            input_shape = layers.get_shape_list(sequence_output)
            batch_size = input_shape[0]
            seq_length = input_shape[1]
            if masked_lm_positions is None:
                masked_lm_positions = tf.ones(shape=[batch_size, seq_length], dtype=tf.int64)

            mlm_logits = self.mlm(sequence_output, masked_lm_positions)
            return mlm_logits, _, _
