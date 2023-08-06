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

import os
import json
from tensorflow.python.platform import gfile
from .modeling_adabert import AdaBERTStudent

def get_pretrained_model(pretrain_model_name_or_path, **kwargs):
    if "/" not in pretrain_model_name_or_path:
        model_type = pretrain_model_name_or_path.split("-")[1]
        if model_type == 'bert':
            from .modeling_bert import BertPreTrainedModel
            return BertPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == "roberta":
            from .modeling_roberta import RobertaPreTrainedModel
            return RobertaPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == "sentimentbert":
            from .modeling_sentimentbert import SentimentBertPreTrainedModel
            return SentimentBertPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == 'albert':
            from .modeling_albert import AlbertPreTrainedModel
            return AlbertPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == 'imagebert':
            from .modeling_imagebert import ImageBertPreTrainedModel
            return ImageBertPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == 'videobert':
            from .modeling_videobert import VideoBertPreTrainedModel
            return VideoBertPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == "linformer":
            from .modeling_linformer import LinFormerPreTrainedModel
            return LinFormerPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == "xformer":
            from .modeling_xformer import XFormerPreTrainedModel
            return XFormerPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == "synthesizer":
            from .modeling_synthesizer import SynthesizerPreTrainedModel
            return SynthesizerPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == "factorizer":
            from .modeling_factorizer import FactorizerPreTrainedModel
            return FactorizerPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == "mca":
            from .modeling_memory_compressed_attention import McaPreTrainedModel
            return McaPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == "bigbird":
            from .modeling_bigbird import BigbirdPreTrainedModel
            return BigbirdPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == "blockbert":
            from .modeling_blockbert import BlockBertPreTrainedModel
            return BlockBertPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == "randombert":
            from .modeling_randombert import RandomBertPreTrainedModel
            return RandomBertPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == "t5":
            from .modeling_t5 import T5PreTrainedModel
            return T5PreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == "convbert":
            from .modeling_convbert import ConvBertPreTrainedModel
            return ConvBertPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == "vanillabert":
            from .modeling_vanillabert import VanillaBertPreTrainedModel
            return VanillaBertPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        else:
            raise NotImplementedError
    else:
        config_path = os.path.join(os.path.dirname(pretrain_model_name_or_path), "config.json")
        if "oss" in config_path:
            with gfile.GFile(config_path, mode='r') as reader:
                text = reader.read()
        else:
            with open(config_path, "r") as reader:
                text = reader.read()
        json_config = json.loads(text)
        model_type = json_config["model_type"]
        assert model_type is not None, "you must specify model_type in config.json when pass pretrained_model_path"
        if model_type == 'bert':
            from .modeling_bert import BertPreTrainedModel
            return BertPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == "roberta":
            from .modeling_roberta import RobertaPreTrainedModel
            return RobertaPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == "sentimentbert":
            from .modeling_sentimentbert import SentimentBertPreTrainedModel
            return SentimentBertPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == 'albert':
            from .modeling_albert import AlbertPreTrainedModel
            return AlbertPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == 'imagebert':
            from .modeling_imagebert import ImageBertPreTrainedModel
            return ImageBertPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == 'videobert':
            from .modeling_videobert import VideoBertPreTrainedModel
            return VideoBertPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == "linformer":
            from .modeling_linformer import LinFormerPreTrainedModel
            return LinFormerPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == "xformer":
            from .modeling_xformer import XFormerPreTrainedModel
            return XFormerPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == "synthesizer":
            from .modeling_synthesizer import SynthesizerPreTrainedModel
            return SynthesizerPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == "factorizer":
            from .modeling_factorizer import FactorizerPreTrainedModel
            return FactorizerPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == "mca":
            from .modeling_memory_compressed_attention import McaPreTrainedModel
            return McaPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == "bigbird":
            from .modeling_bigbird import BigbirdPreTrainedModel
            return BigbirdPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == "blockbert":
            from .modeling_blockbert import BlockBertPreTrainedModel
            return BlockBertPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == "randombert":
            from .modeling_randombert import RandomBertPreTrainedModel
            return RandomBertPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == "t5":
            from .modeling_t5 import T5PreTrainedModel
            return T5PreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == "convbert":
            from .modeling_convbert import ConvBertPreTrainedModel
            return ConvBertPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        elif model_type == "vanillabert":
            from .modeling_vanillabert import VanillaBertPreTrainedModel
            return VanillaBertPreTrainedModel.get(pretrain_model_name_or_path, **kwargs)
        else:
            raise ValueError("model_type should be in bert, roberta, sentimentbert, albert, imagebert, videobert")

def get_config_path(model_type, pretrain_model_name_or_path):
    if model_type == 'bert':
        from .modeling_bert import BertPreTrainedModel
        config_path = BertPreTrainedModel.pretrained_config_archive_map[
            pretrain_model_name_or_path]
    elif model_type == "roberta":
        from .modeling_roberta import RobertaPreTrainedModel
        config_path = RobertaPreTrainedModel.pretrained_config_archive_map[
            pretrain_model_name_or_path]
    elif model_type == "sentimentbert":
        from .modeling_sentimentbert import SentimentBertPreTrainedModel
        config_path = SentimentBertPreTrainedModel.pretrained_config_archive_map[
            pretrain_model_name_or_path]
    elif model_type == 'albert':
        from .modeling_albert import AlbertPreTrainedModel
        config_path = AlbertPreTrainedModel.pretrained_config_archive_map[
            pretrain_model_name_or_path]
    elif model_type == 'imagebert':
        from .modeling_imagebert import ImageBertPreTrainedModel
        config_path = ImageBertPreTrainedModel.pretrained_config_archive_map[
            pretrain_model_name_or_path]
    elif model_type == 'videobert':
        from .modeling_videobert import VideoBertPreTrainedModel
        config_path = VideoBertPreTrainedModel.pretrained_config_archive_map[
            pretrain_model_name_or_path]
    elif model_type == "linformer":
        from .modeling_linformer import LinFormerPreTrainedModel
        config_path = LinFormerPreTrainedModel.pretrained_config_archive_map[
            pretrain_model_name_or_path]
    elif model_type == "xformer":
        from .modeling_xformer import XFormerPreTrainedModel
        config_path = XFormerPreTrainedModel.pretrained_config_archive_map[
            pretrain_model_name_or_path]
    elif model_type == "synthesizer":
        from .modeling_synthesizer import SynthesizerPreTrainedModel
        config_path = SynthesizerPreTrainedModel.pretrained_config_archive_map[
            pretrain_model_name_or_path]
    elif model_type == "factorizer":
        from .modeling_factorizer import FactorizerPreTrainedModel
        config_path = FactorizerPreTrainedModel.pretrained_config_archive_map[
            pretrain_model_name_or_path]
    elif model_type == "mca":
        from .modeling_memory_compressed_attention import McaPreTrainedModel
        config_path = McaPreTrainedModel.pretrained_config_archive_map[
            pretrain_model_name_or_path]
    elif model_type == "bigbird":
        from .modeling_bigbird import BigbirdPreTrainedModel
        config_path = BigbirdPreTrainedModel.pretrained_config_archive_map[
            pretrain_model_name_or_path]
    elif model_type == "blockbert":
        from .modeling_blockbert import BlockBertPreTrainedModel
        config_path = BlockBertPreTrainedModel.pretrained_config_archive_map[
            pretrain_model_name_or_path]
    elif model_type == "randombert":
        from .modeling_randombert import RandomBertPreTrainedModel
        config_path = RandomBertPreTrainedModel.pretrained_config_archive_map[
            pretrain_model_name_or_path]
    elif model_type == "t5":
        from .modeling_t5 import T5PreTrainedModel
        config_path = T5PreTrainedModel.pretrained_config_archive_map[
            pretrain_model_name_or_path]
    elif model_type == "convbert":
        from .modeling_convbert import ConvBertPreTrainedModel
        config_path = ConvBertPreTrainedModel.pretrained_config_archive_map[
            pretrain_model_name_or_path]
    elif model_type == "vanillabert":
        from .modeling_vanillabert import VanillaBertPreTrainedModel
        config_path = VanillaBertPreTrainedModel.pretrained_config_archive_map[
            pretrain_model_name_or_path]
    else:
        raise ValueError("model_type should be in bert, roberta, albert, imagebert, videobert")

    return config_path