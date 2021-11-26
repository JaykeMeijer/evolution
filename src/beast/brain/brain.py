import math
import random
from typing import Dict, List, cast

from beast.brain.neuron import Connection, InputNeuron, InputType, Neuron, OutputNeuron, OutputType
from beast.dna.dna import DNA
from beast.dna.gene import NeuronConnectionGene
from beast.interact import Action, InputSet, MoveForward, Turn


class Brain:
    def __init__(self, dna: DNA):
        self.dna: DNA = dna
        self.neuron_connections: List[Connection] = [
            Connection(cast(NeuronConnectionGene, self.dna.get_gene("neuron_connection_1"))),
            Connection(cast(NeuronConnectionGene, self.dna.get_gene("neuron_connection_2"))),
        ]

        self.output_neurons: Dict[OutputType, OutputNeuron] = {}
        for connection in self.neuron_connections:
            if isinstance(connection.neuron_2, OutputNeuron):
                if connection.neuron_2.neuron_type in self.output_neurons:
                    self.output_neurons[connection.neuron_2.neuron_type].merge(connection.neuron_2)
                    connection.neuron_2 = self.output_neurons[connection.neuron_2.neuron_type]
                else:
                    self.output_neurons[connection.neuron_2.neuron_type] = connection.neuron_2

    def _get_output_neuron(self, neuron: OutputNeuron):
        if neuron.neuron_type not in self.output_neurons:
            self.output_neurons[neuron.neuron_type] = neuron
        return self.output_neurons[neuron.neuron_type]

    def step(self, inputs: InputSet) -> List[Action]:
        actions: List[Action] = []

        if inputs.all_none():
            return actions

        for neuron in self.output_neurons.values():
            value = sum([
                self._get_incoming_connection_value(connection.neuron_1, inputs) * connection.strength
                for connection in neuron.outgoing_connections
            ])
            actions.append(self._get_action_for_output_neuron(neuron, value))

        return actions

    def _get_incoming_connection_value(self, neuron: Neuron, inputs: InputSet):
        if isinstance(neuron, InputNeuron):
            return self._get_value_from_input_neuron(neuron, inputs)
        else:
            return sum([
                self._get_incoming_connection_value(connection.neuron_1, inputs) * connection.strength
                for connection in neuron.outgoing_connections
            ])

    def _get_value_from_input_neuron(self, neuron: InputNeuron, inputs: InputSet) -> float:
        if neuron.neuron_type == InputType.MATE_DISTANCE:
            # TODO cleanup
            if inputs.distance_to_nearest_mate:
                return 1 if inputs.distance_to_nearest_mate > 0 else -1
            else:
                return 0
        elif neuron.neuron_type == InputType.MATE_DIRECTION:
            return inputs.direction_of_nearest_mate if inputs.direction_of_nearest_mate else 0
        else:
            raise NotImplementedError(neuron.neuron_type)

    def _get_action_for_output_neuron(self, neuron: OutputNeuron, value: float) -> Action:
        if neuron.neuron_type == OutputType.MOVE_FORWARD:
            return MoveForward(round((value) * 5))
        elif neuron.neuron_type == OutputType.TURN:
            return Turn(round(value * 30))
        else:
            raise NotImplementedError(neuron.neuron_type)
