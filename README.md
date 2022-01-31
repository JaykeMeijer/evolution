# Evolution

Evolution is an evolution simulation. "Beasts" can move around and reproduce, however this takes energy. When the energy of a beast reaches 0, he dies.

Reproduction mimicks that of real life. Each beast has a genetic code, similar to DNA. When two beasts reproduce, the new beast will be a combination of their
genetic code, with possibly some random mutations.

The "brain" of the beasts uses inputs such as distance to others, objects etc, as some kind of basic neural network.

Inspired by / loosely based on https://www.youtube.com/watch?v=N3tRFayqVtk and https://www.youtube.com/watch?v=myJ7YOZGkv0

# TODO

Evolution:
- Add food, moving towards food (gives energy)
- Add fighting / eating eachother: bigger is better, fighting gene
- Add speed as genetic parameter

## Would be cool

Evolution:
- Add items to environment - obstacles, dangers
- Add environment factors that suite certain beasts, for example:
  - forest limits speed of larger beasts
  - temperature effects energy usage (perhaps have a "fur" gene that decreases energy usage in cold, but decreases speed in warmth
- Add aging, disease
- Implement species: Certain max distance between genes. If distance is too large, there's a different species, which
  prevents reproduction and cannibalism

Simulation:
- Highlight families of beasts
- Show family tree

## Other

- Use own rendering (like in brain) for fast quad tree render

# Balancing mechanisms

Implemented:

- Larger beasts turn slower (defined in `Beast._apply_action`)
- Larger beasts have higher energy consumption (defined in `Beast.__init__`)

To be added:

- Larger beasts have larger energy storage
- Larger beasts win in a fight ?
