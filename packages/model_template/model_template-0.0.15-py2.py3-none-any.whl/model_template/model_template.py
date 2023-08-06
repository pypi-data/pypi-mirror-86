"""
A package to run any machine learning model in production
"""
import pickle
import logging

import numpy as np

from abc import ABC
from tqdm import tqdm
from .pre_process import preprocess
from sklearn.feature_extraction.text import HashingVectorizer

try:
    from pre_processing import CorpusHandler as ch
except Exception:
    pass

# logging.config.fileConfig(logger_path)
# logger = logging.getLogger('template_logger')

logger = logging.getLogger(__name__)


class ModelTemplate(ABC):

    def model_output(self, data, binary):
        """
        Return the output of model, if you are running a neural network
        return the values off the last layer, don't use binarizer or return
        the final classification in this function
        """

        if binary:
            output = self.binary.predict(data)
            if output[0] == 0:
                return output, True

        # output = self.model.predict_proba(data)
        output = self.model.predict(data)

        return output, False

    def recover_label(self, model_output):
        """
        Recover the label
        """
        new_preds = []
        for each in model_output:
            new_list = np.asarray([0 for temp in range(len(each))])
            new_list[np.where(each == 1)] = 1
            if new_list.sum() == 0:
                new_list[-1] = 1
            new_preds.append(np.asarray(new_list))
        return new_preds


class ModelPieces(ModelTemplate):

    def __init__(self, model_path, tfidf_path):
        super().__init__()
        self.model = self.load_model(model_path)
        self.tfidf = self.load_tfidf(tfidf_path)

    def load_tfidf(self, tfidf_path):

        tfidf = pickle.load(open(tfidf_path, "rb"))
        return tfidf

    def load_model(self, model_path):
        """
        Function that implements load model, is recommended load
        the model with training step off
        """

        model = pickle.load(open(model_path, "rb"))
        return model

    def parse_data(self, data):
        """
        Treats the data to be inserted into the model
        """

        parsed_data = ch.preprocess(data,
                                    disabled=["spellchecker",
                                              "to_st_named_entities",
                                              "lemmatize"])
        parsed_data = ' '.join(parsed_data)

        vectorized_data = self.tfidf.transform([parsed_data])

        return vectorized_data

    def inference(self, document):

        inference = self.predict(document)

        return inference

    def predict(self, data, binary=False):
        """
        Run the model and return the prediction
        """

        logger.info('Make prediction')

        logger.debug('Parsing data')
        data = self.parse_data(data)
        logger.debug('Data parsed')

        logger.debug('Getting output from model')
        output, is_bin = self.model_output(data, binary)
        logger.debug('Output taked successfully')

        if is_bin:
            return output

        logger.info('Finish prediction')

        return output


class ModelThemes(ModelTemplate):

    def __init__(self, path, binary_path=None):
        super().__init__()
        self.model, self.binary = self.load_model(path, binary_path)
        self.pre_process = True

    def set_cpu_predictor(self, model):
        for model_index in range(len(model.estimators_)):
            booster = model.estimators_[model_index].get_booster()
            booster.set_param({'predictor': 'cpu_predictor'})
            model.estimators_[model_index].booster = booster
        return model

    def load_model(self, path, binary_path):

        model_file = open(path, "rb")
        model = pickle.loads(model_file.read())
        model = self.set_cpu_predictor(model)
        model_file.close()

        if binary_path:
            binary_model_file = open(binary_path, "rb")
            binary_model = pickle.loads(binary_model_file.read())
            binary_model_file.close()
        else:
            binary_model = None

        return model, binary_model

    def parse_data(self, data):
        """
        Treats the data to be inserted into the model
        """

        if(self.pre_process):
            parsed_data = [preprocess(data[0])]
        else:
            parsed_data = data

        emb = HashingVectorizer(n_features=2**14).fit_transform(parsed_data)

        return emb

    def inference(self, process, pre_process=True):

        self.pre_process = pre_process
        process_aux = process.copy()

        for i, document in enumerate(process_aux):
            process_aux[i] = ' '.join(document)

        process_aux = [' '.join(process_aux)]

        inference = self.predict(process_aux, binary=bool(self.binary))
        return inference

    def predict(self, data, binary=False):
        """
        Run the model and return the prediction
        """

        logger.info('Make prediction')

        logger.debug('Parsing data')
        data = self.parse_data(data)
        logger.debug('Data parsed')

        logger.debug('Getting output from model')
        output, is_bin = self.model_output(data, binary)
        logger.debug('Output taked successfully')

        if is_bin:
            return output

        print(output)

        logger.debug('Transforming output in label')
        prediction = self.recover_label(output)
        logger.debug('The result label is: [%s]' % prediction)

        logger.info('Finish prediction')

        return prediction


class GpamTokenizer:
    def __init__(self, vocab, texts):
        self.vocab = vocab
        self.texts = texts
        self.dict_vocab = {}

    def list_2_dict(self):
        id = 1
        for word in self.vocab:
            self.dict_vocab[word] = id
            id += 1

    def return_tokens(self, text):
        return text.split(" ")

    def transform_tokens(self, tokens):
        result_transform = []
        for token in tokens:
            try:
                id = self.dict_vocab[token]
                result_transform.append(id)
            except Exception:
                continue

        return result_transform

    def pad_vector(self, texts, num):
        reshape_v = []

        for each in tqdm(texts):
            if len(each) >= num:
                reshape_v.append(each[0:num])
            else:
                zeros = num - len(each)
                temp = each
                v_zeros = [0 for each in range(zeros)]
                temp.extend(v_zeros)
                reshape_v.append(temp)

        return reshape_v

    def tokenizer_with_vocab(self, num):
        self.list_2_dict()
        result_texts = []
        for i in tqdm(range(len(self.texts))):
            tokens = self.return_tokens(self.texts[i])
            result_transform = self.transform_tokens(tokens)
            result_texts.append(result_transform)

        result = self.pad_vector(result_texts, num)

        return np.matrix(result)


def binarize_pred(preds):
    new_preds = []
    for each in preds:
        num = max(each)
        new_list = np.asarray([0 for temp in range(len(each))])
        new_list[np.where(each == num)[0][0]] = 1
        new_preds.append(np.asarray(new_list))
    return new_preds
