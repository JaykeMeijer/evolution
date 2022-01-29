import math
import random
from typing import Any, Dict, Iterable, List, Tuple, cast

import networkx as nx
import pygame

from beast.brain.neuron import Connection, InputNeuron, InputType, InternalNeuron, Neuron, OutputNeuron, OutputType
from beast.dna.dna import DNA
from beast.dna.gene import NeuronConnectionGene
from beast.interact import Action, InputSet, MoveForward, Noop, Turn
from util.math_helpers import get_direction, translate


class Brain:
    def __init__(self, dna: DNA):
        self.dna: DNA = dna
        self.neuron_connections: List[Connection] = [
            Connection(cast(NeuronConnectionGene, self.dna.get_gene("neuron_connection_1"))),
            Connection(cast(NeuronConnectionGene, self.dna.get_gene("neuron_connection_2"))),
            Connection(cast(NeuronConnectionGene, self.dna.get_gene("neuron_connection_3"))),
            Connection(cast(NeuronConnectionGene, self.dna.get_gene("neuron_connection_4"))),
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
        if inputs.all_none():
            return []

        actions: List[Action] = []
        for neuron in self.output_neurons.values():
            value = sum([
                self._get_incoming_connection_value(connection.neuron_1, inputs) * connection.strength
                for connection in neuron.incoming_connections
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
            return inputs.distance_to_nearest_mate if inputs.distance_to_nearest_mate else 0
        elif neuron.neuron_type == InputType.MATE_DIRECTION:
            return inputs.direction_of_nearest_mate if inputs.direction_of_nearest_mate else 0
        elif neuron.neuron_type == InputType.RANDOM_INPUT:
            return random.randint(0, 10)
        else:
            raise NotImplementedError(neuron.neuron_type)

    def _get_action_for_output_neuron(self, neuron: OutputNeuron, value: float) -> Action:
        if neuron.neuron_type == OutputType.MOVE_FORWARD:
            return MoveForward() if value != 0 else Noop()
        elif neuron.neuron_type == OutputType.TURN:
            return Turn(round(value))
        else:
            raise NotImplementedError(neuron.neuron_type)

    def get_graph(self) -> nx.DiGraph:
        G = nx.DiGraph()

        for n in self.neuron_connections:
            G.add_edge(n.neuron_1, n.neuron_2, strength=n.strength)

        return G


class BrainRenderer:
    NODE_SIZE = 10
    NEURON_COLORS = {
        InputNeuron: "red",
        InternalNeuron: "blue",
        OutputNeuron: "green"
    }
    IMGSIZE = 300
    MARGIN = 50
    FIGSIZE = (3, 3)
    DPI = 100

    def __init__(self):
        self.font = pygame.font.SysFont("Calibri", 8)

    def draw_brain(self, brain) -> pygame.surface.Surface:
        graph = brain.get_graph()

        colors = {node: self.NEURON_COLORS[type(node)] for node in graph.nodes()}
        labels = {node: node.neuron_type.name for node in graph.nodes()}
        edge_labels = {(n1, n2): f"{graph[n1][n2]['strength']:.2f}" for n1, n2 in graph.edges()}
        pos = nx.planar_layout(graph, scale=(self.IMGSIZE / 2) - self.MARGIN, center=(self.IMGSIZE/2, self.IMGSIZE/2))

        surface = pygame.Surface((self.IMGSIZE, self.IMGSIZE))
        surface.fill("white")
        self._draw_nodes(surface, graph.nodes(), pos, colors)
        self._draw_node_labels(surface, graph.nodes(), pos, labels)
        self._draw_edges(surface, graph.edges(), pos)
        self._draw_edge_labels(surface, graph.edges(), pos, edge_labels)
        return surface

    def _draw_nodes(
        self,
        surface: pygame.surface.Surface,
        nodes: Iterable[Neuron],
        pos: Dict[Neuron, Tuple[int, int]],
        colors: Dict[Any, str]
    ):
        for node in nodes:
            pygame.draw.circle(
                surface,
                colors[node],
                pos[node],
                self.NODE_SIZE,
            )

    def _draw_node_labels(
        self,
        surface: pygame.surface.Surface,
        nodes: Iterable[Any],
        pos: Dict[Any, Tuple[int, int]],
        labels: Dict[Any, str]
    ):
        for node in nodes:
            position = pos[node]
            label = self.font.render(labels[node], True, (0, 0, 0))
            surface.blit(label, (position[0] - label.get_width() / 2, position[1] + self.font.get_linesize()))

    def _draw_edges(
        self,
        surface: pygame.surface.Surface,
        edges: Iterable[Tuple[Any, Any]],
        pos: Dict[Any, Tuple[int, int]]
    ):
        for node1, node2 in edges:
            direction = get_direction(pos[node1], pos[node2])
            begin = translate(pos[node1], direction, self.NODE_SIZE + 1)
            end = translate(pos[node2], direction, -self.NODE_SIZE + 1)
            pygame.draw.aaline(surface, "black", begin, end)
            pygame.draw.polygon(
                surface,
                "black",
                (
                    (end),
                    (translate(end, direction + 135, 5)),
                    (translate(end, direction - 135, 5)),
                )
            )

    def _draw_edge_labels(
        self,
        surface: pygame.surface.Surface,
        edges: Iterable[Tuple[Any, Any]],
        pos: Dict[Any, Tuple[int, int]],
        labels: Dict[Tuple[Any, Any], str],
    ):
        for node1, node2 in edges:
            direction = get_direction(pos[node1], pos[node2])
            distance = math.dist(pos[node1], pos[node2])
            position = translate(pos[node1], direction, int(distance / 2))
            label = self.font.render(labels[(node1, node2)], True, (0, 0, 0))
            surface.blit(label, (position[0] - label.get_width() / 2, position[1] + self.font.get_linesize()))
