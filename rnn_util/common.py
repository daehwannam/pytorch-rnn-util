# Copyright (c) 2019 Daehwan Nam
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


import torch.nn as nn
import torch


def no_dropout(x): return x


no_dropout.p = 0


def no_layer_norm(x): return x


def get_indicator(length_tensor, max_length=None):
    lengths_size = length_tensor.size()

    flat_lengths = length_tensor.view(-1, 1)

    if not max_length:
        max_length = length_tensor.max()
    unit_range = torch.arange(max_length)
    # flat_range = torch.stack([unit_range] * flat_lengths.size()[0],
    #                          dim=0)
    flat_range = unit_range.repeat(flat_lengths.size()[0], 1)
    flat_indicator = flat_range < flat_lengths

    return flat_indicator.view(lengths_size + (-1, 1))


def create_lstm_cell_init_state(hidden_size, init_state_learned=True):
    """
    :param hidden_size: 
    :param init_state_learned: 
    :returns: init_state is a input of lstm cells. _init_state is saved as a parameter of model (such as self._init_state)
    """
    init_hidden = nn.Parameter(torch.zeros(1, hidden_size), init_state_learned)
    init_cell = nn.Parameter(torch.zeros(1, hidden_size), init_state_learned)

    init_state = (init_hidden, init_cell)
    _init_state = nn.ParameterList(init_state)

    return init_state, _init_state


def repeat_lstm_cell_state(state, batch_size):
    # s is either hidden or cell
    return tuple(
        s.repeat(batch_size, 1)
        for s in state)


def create_lstm_init_state(num_layers, num_directions, hidden_size, init_state_learned=True):
    """
    :param hidden_size: 
    :param init_state_learned: 
    :returns: init_state is a input of lstm cells. _init_state is saved as a parameter of model (such as self._init_state)
    """
    init_hidden = nn.Parameter(torch.zeros(
        num_layers * num_directions, 1, hidden_size), init_state_learned)
    init_cell = nn.Parameter(torch.zeros(num_layers * num_directions,
                                         1, hidden_size), init_state_learned)

    init_state = (init_hidden, init_cell)
    _init_state = nn.ParameterList(init_state)

    return init_state, _init_state


def repeat_lstm_state(state, batch_size):
    # s is either hidden or cell
    return tuple(
        s.repeat(1, batch_size, 1)
        for s in state)


# def enable_cuda(model, arg):
#     if is_cuda_enabled(model):
#         arg = arg.cuda()
#     else:
#         arg = arg.cpu()
#     return arg


def is_cuda_enabled(model):
    return next(model.parameters()).is_cuda


def get_module_device(model):
    return next(model.parameters()).device
