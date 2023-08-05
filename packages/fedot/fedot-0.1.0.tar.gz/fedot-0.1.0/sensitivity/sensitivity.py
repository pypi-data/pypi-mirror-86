from fedot.core.composer.chain import Chain
from SALib.analyze.sobol import analyze as sobol_analyze
from SALib.sample import saltelli
from SALib.sample.morris import sample as morris_sample
from typing import List
from copy import deepcopy

from fedot.core.models.data import InputData
from fedot.core.models.model import Model


class SensitiityAnalyze:
    def __init__(self):
        self.sa_method = None

    def analyze(self):
        pass

    def save_history(self):
        pass

    def visualize(self):
        pass


class ModelAnalyze(SensitiityAnalyze):
    def __init__(self, model: Model, param_space: dict, data: InputData, method: str):
        super().__init__()
        self.model = model
        self.param_space = param_space
        self.data = data

        if method == 'sobol':
            self.sa_method = self.sobol_analyze

    def analyze(self):
        self.sa_method()

    def sobol_analyze(self):
        # TODO Model.params (now params are custom)
        problem = _create_problem_for_sobol_method(self.model.params)
        problem_samples = make_saltelly_sample(problem, num_of_samples=100)
        conveted_samples = _convert_sample_to_dict(problem, problem_samples)
        response_matrix = self.get_model_response_matrix(conveted_samples)
        sobol_indecies = sobol_method(problem, response_matrix)

        return sobol_indecies

    def get_model_response_matrix(self, samples):
        model_response_matrix = []
        for sample in samples:
            self.model.custom_params = sample

            fitted_model, _ = self.model.fit(self.data)
            prediction = self.model.predict(fitted_model=fitted_model,
                                            data=self.data)
            model_response_matrix.append(prediction)

        return model_response_matrix


def sobol_method(problem, model_response) -> dict:
    sobol_indices = sobol_analyze(problem, model_response, print_to_console=True)

    return sobol_indices


def morris_method(problem, model_response) -> dict:
    pass


def make_saltelly_sample(problem, num_of_samples=100):
    params_samples = saltelli.sample(problem, num_of_samples)
    params_samples = _convert_sample_to_dict(problem, params_samples)

    return params_samples


def make_moris_sample(problem, num_of_samples=100):
    params_samples = morris_sample(problem, num_of_samples, num_levels=4)
    params_samples = _convert_sample_to_dict(problem, params_samples)

    return params_samples


def _create_problem_for_sobol_method(params: dict):
    problem = {
        'num_vars': len(params),
        'names': list(params.keys()),
        'bounds': list()
    }

    for key, bounds in params.items():
        if bounds[0] is not str:
            bounds = list(bounds)
            problem['bounds'].append([bounds[0], bounds[-1]])
        else:
            problem['bounds'].append(bounds)
    return problem


def _convert_sample_to_dict(problem, samples) -> List[dict]:
    converted_samples = []
    names_of_params = problem['names']
    for sample in samples:
        new_params = {}
        for index, value in enumerate(sample):
            new_params[names_of_params[index]] = value
        converted_samples.append(new_params)

    return converted_samples


def _convert_model_input_for_moris_method(data: InputData):
    pass


class ChainAnalyze:
    def __init__(self, chain: Chain, train_data: InputData, test_data: InputData):
        self.chain = chain
        self.train_data = train_data
        self.test_data = test_data

    def analyze(self):
        results_predicted = []
        samples = self.sample()
        for chain_sample in samples:
            chain_sample.fit(self.train_data)
            predicted = chain_sample.predict(self.test_data)


    def sample(self):
        chain_samples = []
        for index in range(1, len(self.chain.nodes)):
            chain_sample = deepcopy(self.chain)
            chain_sample.delete_node(chain_sample.nodes[index])
            chain_samples.append(chain_sample)

        return chain_samples


