# -*- coding: utf-8 -*-
""""""  # for sphinx auto doc purposes
"""
| ----------------------------------------------------------------------------------------------------------------------
| Date                : September 2018
| Copyright           : © 2018 - 2020 by Tinne Cahy (Geo Solutions) and Ann Crabbé (KU Leuven)
| Email               : acrabbe.foss@gmail.com
| Acknowledgements    : Translated from LNNS 1.0 A neural network simulator [C++ software]
|                       Ghent University, Laboratory of Forest Management and Spatial Information Techniques
|                       Lieven P.C. Verbeke
|
| This file is part of the QGIS Neural Network MLP Classifier plugin and mlp-image-classifier python package.
|
| This program is free software: you can redistribute it and/or modify it under the terms of the GNU General Public
| License as published by the Free Software Foundation, either version 3 of the License, or any later version.
|
| This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied
| warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.
|
| You should have received a copy of the GNU General Public License (COPYING.txt). If not see www.gnu.org/licenses.
| ----------------------------------------------------------------------------------------------------------------------
"""
import argparse
from os.path import abspath, splitext

from lnns.interfaces import tuple_int_cli
from lnns.interfaces import run_algorithm_pattern
from lnns.core.network import Network


def create_parser():
    parser = argparse.ArgumentParser(description=str(Network.__doc__))

    parser.add_argument('pattern_predict_path', type=str,
                        help="Pattern text file that includes the values to predict,'number_of_patterns', "
                             "'number_of_inputs' and 'number_of_outputs.'")
    parser.add_argument('pattern_train_path', type=str,
                        help="Pattern text file that includes the network training values, 'number_of_patterns', "
                             "'number_of_inputs' and 'number_of_outputs.'")
    parser.add_argument('-n', '--no_data_value', type=int, default=-1,
                        help='Value that describes pixels with no data in the classes_data file (default: -1).')
    # optional
    parser.add_argument('-l', '--hidden_layer_size', type=tuple_int_cli, default=(10,),
                        help='Hidden layer size with length = n_layers - 2, comma separated values. The ith element '
                             'represents the number of neurons in the ith hidden layer. (default: 10,)')
    parser.add_argument('-a', '--activation', type=str, choices=['identity', 'logistic', 'tanh', 'relu'],
                        help='Activation function for the MLPClassifier (default: logistic).', default='logistic')
    parser.add_argument('-i', '--iterations', type=int,
                        help='Maximum number of iterations (default: 200).', default=200)
    parser.add_argument('-t', '--test_size', type=float, default=0.33,
                        help='Portion of test pixels used to evaluate the trained network (default: 0.33).')
    parser.add_argument('-p', '--probability_of_class', type=int,
                        help='class for which you would like the probability image (default: None).', default=None)
    parser.add_argument('-o', '--output',
                        help="Output predicted file (default: in same folder with extension '_predict.prn'")
    parser.add_argument('-g', '--output_graph',
                        help="Output error graph (default: in same folder with extension '_error.PNG'")
    return parser


def run_network(args):
    """
    Documentation: mlpclassifier-pattern -h
    """
    full_path_predict = abspath(args.pattern_predict_path)
    output_file = abspath(args.output) if args.output else splitext(full_path_predict)[0] + "_predict.prn"
    graph_file = abspath(args.output_graph) if args.output_graph else splitext(full_path_predict)[0] + "_error.PNG"

    run_algorithm_pattern(pattern_train=abspath(args.pattern_train_path),
                          pattern_predict=full_path_predict,
                          no_data_value=args.no_data_value,
                          hidden_layer_size=args.hidden_layer_size,
                          activation=args.activation,
                          iterations=args.iterations,
                          test_size=args.test_size,
                          probability_of_class=args.probability_of_class,
                          output_path=output_file,
                          plot_path=graph_file)

    print("Predicted output: {}".format(output_file))
    print("Network error decline: {}".format(graph_file))


def main():
    parser = create_parser()
    run_network(parser.parse_args())


if __name__ == '__main__':
    main()
