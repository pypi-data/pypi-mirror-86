# NiaAML

NiaAML is an automated machine learning Python framework based on nature-inspired algorithms for optimization. The name comes from the automated machine learning method of the same name [[1]](#1). Its goal is to efficiently compose the best possible classification pipeline for the given task using components on the input. The components are divided into three groups: feature seletion algorithms, feature transformation algorithms and classifiers. The framework uses nature-inspired algorithms for optimization to choose the best set of components for the classification pipeline on the output and optimize their parameters. We use <a href="https://github.com/NiaOrg/NiaPy">NiaPy framework</a> for the optimization process which is a popular Python collection of nature-inspired algorithms. The NiaAML framework is easy to use and customize or expand to suit your needs.

## Installation

Install NiaAML with pip:

```sh
pip install niaaml
```

## Components

In the following sections you can see a list of currently implemented components divided into groups: classifiers, feature selection algorithms and feature transformation algorithms. At the end you can also see a list of currently implemented fitness functions for the optimization process. All of the components are passed into the optimization process using their class names. Let's say we want to choose between Adaptive Boosting, Bagging and Multi Layer Perceptron classifiers, Select K Best and Select Percentile feature selection algorithms and Normalizer as the feature transformation algorithm (may not be selected during the optimization process).

```python
PipelineOptimizer(
    data=...,
    classifiers=['AdaBoost', 'Bagging', 'MultiLayerPerceptron'],
    feature_selection_algorithms=['SelectKBest', 'SelectPercentile'],
    feature_transform_algorithms=['Normalizer']
)
```

For a full example see the [Examples section](#examples).

### Classifiers

* Adaptive Boosting (AdaBoost),
* Bagging (Bagging),
* Extremely Randomized Trees (ExtremelyRandomizedTrees),
* Linear SVC (LinearSVC),
* Multi Layer Perceptron (MultiLayerPerceptron),
* Random Forest Classifier (RandomForestClassifier).

### Feature Selection Algorithms

* Select K Best (SelectKBest),
* Select Percentile (SelectPercentile),
* Variance Threshold (VarianceThreshold).

#### Nature-Inspired

* Bat Algorithm (BatAlgorithm),
* Differential Evolution (DifferentialEvolution),
* Self-Adaptive Differential Evolution (jDEFSTH),
* Grey Wolf Optimizer (GreyWolfOptimizer),
* Particle Swarm Optimization (ParticleSwarmOptimization).

### Feature Transformation Algorithms

* Normalizer (Normalizer),
* Standard Scaler (StandardScaler).

### Fitness Functions

* Accuracy (Accuracy),
* Cohen's kappa (CohenKappa),
* F1-Score (F1),
* Precision (Precision).

## Optimization Process And Parameter Tuning

In NiaAML there are two types of optimization. Goal of the first type is to find an optimal set of components (feature selection algorithm, feature transformation algorithm and classifier). The next step is to find optimal parameters for the selected set of components and that is the goal of the second type of optimization. Each component has an attribute `_params`, which is a dictionary of parameters and their possible values.

```python
self._params = dict(
    n_estimators = ParameterDefinition(MinMax(min=10, max=111), np.uint),
    algorithm = ParameterDefinition(['SAMME', 'SAMME.R'])
)
```

An individual in the second type of optimization is a real-valued vector that has a size equal to the sum of number of keys in all three dictionaries (classifier's _params, feature transformation algorithm's _params and feature selection algorithm's _params) and a value of each dimension is in range [0.0, 1.0]. The second type of optimization maps real values from the individual's vector to those parameter definitions in the dictionaries. Each parameter's value can be defined as a range or array of values. In the first case, a value from vector is mapped from one iterval to another and in the second case, a value from vector falls into one of the bins that represent an index of the array that holds possible parameter's values.

Let's say we have a classifier with 3 parameters, feature selection algorithm with 2 parameters and feature transformation algorithm with 4 parameters. Size of an individual in the second type of optimization is 9. Size of an individual in the first type of optimization is always 3 (1 classifier, 1 feature selection algorithm and 1 feature transform algorithm).

In some cases we may want to tune a parameter that needs additional information for setting its range of values, so we cannot set the range in the initialization method. In that case we should set its value in the dictionary to None and define it later in the process. The parameter will be a part of parameter tuning process as soon as we define its possible values. For example, see [Select K Best Feature Selection](niaaml/preprocessing/feature_selection/select_k_best.py) and its parameter `k`.

## Examples

NiaAML framework currently supports only numeric features on the input. **However, we are planning to add support for categorical features too.**

### Example of Usage

Load data and try to find the optimal pipeline for the given components. The example below uses the Particle Swarm Algorithm as the optimization algorithm. You can find a list of all available algorithms in the <a href="https://niapy.readthedocs.io/en/stable/">NiaPy's documentation</a>.

```python
from niaaml import PipelineOptimizer, Pipeline
from niaaml.data import BasicDataReader
import numpy

# dummy random data
data_reader = BasicDataReader(
    x=numpy.random.uniform(low=0.0, high=15.0, size=(50, 3)),
    y=numpy.random.choice(['Class 1', 'Class 2'], size=50)
)

pipeline_optimizer = PipelineOptimizer(
    data=data_reader,
    classifiers=['AdaBoost', 'Bagging', 'MultiLayerPerceptron', 'RandomForest', 'ExtremelyRandomizedTrees', 'LinearSVC'],
    feature_selection_algorithms=['SelectKBest', 'SelectPercentile', 'ParticleSwarmOptimization', 'VarianceThreshold'],
    feature_transform_algorithms=['Normalizer', 'StandardScaler']
)
pipeline = pipeline_optimizer.run('Accuracy', 20, 20, 400, 400, 'ParticleSwarmAlgorithm', 'ParticleSwarmAlgorithm')
```

You can save a result of the optimization process as an object to a file for later use.

```python
pipeline.export('pipeline.ppln')
```

And also load it from a file and use the pipeline.

```python
loaded_pipeline = Pipeline.load('pipeline.ppln')

# some features (can be loaded using DataReader object instances)
x = numpy.array([[0.35, 0.46, 5.32], [0.16, 0.55, 12.5]], dtype=float)
y = loaded_pipeline.run(x)
```

You can also save a user-friendly representation of a pipeline to a text file.

```python
final_pipeline.export_text('pipeline.txt')
```

This is a very simple example with dummy data. It is only intended to give you a basic idea on how to use the framework.

### Example of a Pipeline Component Implementation

NiaAML framework is easily expandable as you can implement components by overriding the base classes' methods. To implement a classifier you should inherit from the [Classifier](niaaml/classifiers/classifier.py) class and you can do the same with [FeatureSelectionAlgorithm](niaaml/preprocessing/feature_selection/feature_selection_algorithm.py) and [FeatureTransformAlgorithm](niaaml/preprocessing/feature_transform/feature_transform_algorithm.py) classes. All of the mentioned classes inherit from the [PipelineComponent](niaaml/pipeline_component.py) class.

Take a look at the [Classifier](niaaml/classifiers/classifier.py) class and the implementation of the [AdaBoost](niaaml/classifiers/ada_boost.py) classifier that inherits from it.

### Fitness Functions

NiaAML framework also allows you to implement your own fitness function. All you need to do is implement the [FitnessFunction](niaaml/fitness/fitness_function.py) class.

Take a look at the [Accuracy](niaaml/fitness/accuracy.py) implementation.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/lukapecnik"><img src="https://avatars0.githubusercontent.com/u/23029992?s=460&u=d1c802fd8c82af0a020b1e21af80a34d6e28fb10&v=4?s=100" width="100px;" alt=""/><br /><sub><b>Luka Pečnik</b></sub></a><br /><a href="https://github.com/lukapecnik/NiaAML/commits?author=lukapecnik" title="Code">💻</a> <a href="https://github.com/lukapecnik/NiaAML/commits?author=lukapecnik" title="Documentation">📖</a> <a href="https://github.com/lukapecnik/NiaAML/pulls?q=is%3Apr+reviewed-by%3Alukapecnik" title="Reviewed Pull Requests">👀</a> <a href="https://github.com/lukapecnik/NiaAML/issues?q=author%3Alukapecnik" title="Bug reports">🐛</a> <a href="#example-lukapecnik" title="Examples">💡</a></td>
    <td align="center"><a href="https://github.com/firefly-cpp"><img src="https://avatars2.githubusercontent.com/u/1633361?v=4?s=100" width="100px;" alt=""/><br /><sub><b>firefly-cpp</b></sub></a><br /><a href="https://github.com/lukapecnik/NiaAML/commits?author=firefly-cpp" title="Code">💻</a> <a href="https://github.com/lukapecnik/NiaAML/issues?q=author%3Afirefly-cpp" title="Bug reports">🐛</a></td>
  </tr>
</table>

<!-- markdownlint-restore -->
<!-- prettier-ignore-end -->

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind are welcome!

## Licence

This package is distributed under the MIT License. This license can be found online at <http://www.opensource.org/licenses/MIT>.

## Disclaimer

This framework is provided as-is, and there are no guarantees that it fits your purposes or that it is bug-free. Use it at your own risk!

## References

<a id="1">[1]</a> Iztok Fister Jr., Milan Zorman, Dušan Fister, Iztok Fister. <a href="https://link.springer.com/chapter/10.1007%2F978-981-15-2133-1_13">Continuous optimizers for automatic design and evaluation of classification pipelines</a>. In: Frontier applications of nature inspired computation. Springer tracts in nature-inspired computing, pp.281-301, 2020.