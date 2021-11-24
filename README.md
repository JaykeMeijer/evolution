# Evolution

Evolution is an evolution simulation. "Beasts" can move around and reproduce, however this takes energy. When the energy of a beast reaches 0, he dies.

Reproduction mimicks that of real life. Each beast has a genetic code, similar to DNA. When two beasts reproduce, the new beast will be a combination of their
genetic code, with possibly some random mutations.

Currently, the "brain" of the beasts selects random actions. However, the plan is to use inputs such as distance to others, objects etc, and some kind of
basic neural network.

Inspired by / loosely based on https://www.youtube.com/watch?v=N3tRFayqVtk and https://www.youtube.com/watch?v=myJ7YOZGkv0

# TODO

Evolution:
- Implement brain and non-random moves
- Add food, moving towards food (gives energy)
- Add fighting / eating eachother: bigger is better, fighting genome
- Add speed as genetic parameter

Simulation:
- Optimize vincinity detection for reproduction (look at quad trees, r trees)
- Click on beast for stats

# Would be cool

Evolution:
- Add items to environment - obstacles, dangers
- Add environment factors that suite certain beasts, eg forest limits size
- Add aging, disease

Simulation:
- Highlight families of beasts
- Show family tree
