---
layout: default
title: Final Report
---

## Summary
The goal of our project is to create an agent that is able to gather resources and craft items in a normally-generated Minecraft world. The agent is spawned in a 29x29 chunk created with the default world generator, which has usual resources such as wood, dirt and stone. Information about its surroundings is given in the form of a 5x5x5 grid centered on its current location. Due to the limited sight range, the agent must explore the world around it to find resources, and reinforcement learning is used to allow it to do so in an efficient manner.

<img src='https://raw.githubusercontent.com/jhnguyen521/SpeedCrafter/main/img/arena.png' title='Agent's world' />

## Approaches

The approach that we originally wanted to take was to have our agent cycle through 5 different seeds to train on real chunks rather than an artificial environment as well as to prevent overfitting. This approach would give us the best results in terms of generalization but would require a lot of repeated tuning and training as well as time put towards selecting a seed with a good training enviroinment. Due to time constraints and the oddities of working in a group via the internet as well as the lack of powerful equipment, we decided to simplify our approach.

We instead used a single seed which, although it would eventually overfit the agent, would still be able to show that the agent actually learns and, up to a certain extent, if training was stopped before overfitting began, the agent would still be able to generalize decently due to the nature of Soft Actor Critic (SAC) if it was placed in a different environment. Training was mainly done with a stone pickaxe as the input because it forces the agent to explore the whole environment vertically and dig through dirt rather than simply finding things on the surface as it gathers both stone and wood.

### Rewarding the agent
In order for the agent to learn, it is extremely important to reward the agent properly to encourage certain behaviors and actions. The most basic reward that we gave to the agent was rewarding it for when it mines and collects a resource that it still needs. We rewarded the agent with a flat 100 for collecting a needed resource, -1 for collecting dirt as to encourage it to not break everything in sight, and 1000 for collecting all resources needed and crafting an item. We also gave it a -1 reward for every action it took to push the agent to optimize its actions. This alone, however, is not enough to efficiently train the agent. As stated in our problem statement, an important aspect of the project is exploration. If the agent, for whatever reason, ends up never collecting a needed resource, it will never know that it needs to collect those resources in the first place. To solve this problem, we encouraged the agent to have a greedy approach in collecting resources. Upon finding a resource in its observation space, we help the agent simplify this space by calculating the coordinates of the nearest resource and provide the agent with the distance from it. We then reward the agent +-1 depending on whether it gets closer or further from that resource. Upon collecting any resource, the agent will then try to explore until it can find a resource in its observation space and repeats the process.

#### Getting Resource Coordinates
Because the agent's observation space is a 5x5x5 matrix around it, the coordinates of the resource respective to the agent is not the same respective to the world. Thus, we calculate the coordinates respect to the world in order for the agent to be able to calculate its distance from it:
```python
p = [int(self.pos[0] - (int(self.obs_size/2)-obs_coord[0])),
     int(self.pos[1] - (int(self.obs_size/2)-obs_coord[1])),
     int(self.pos[2] - (int(self.obs_size/2)-obs_coord[2]))]
```
Once we have these coordinates, we can calculate the distance between the agent and the resource with simple matrix math.
The mission finishes either when the agent hits 200 steps or the agent collects enough resources to craft the item.

## Evaluation
The agent is evaluated in its ability in finding resources as well as how efficient it is at doing so. A small penalty of -1 is incurred every time a command is sent to the agent, as well as when it collects dirt (a common item that's not used in any recipes). Collecting a required resource has a reward of 100, and collecting all of the resources adds an additional reward of 1000. This is intended to reward the agent for completing recipes and encourage it to do so in fewer steps. 

<!--
TODO: distance-based reward
This is known as reward shaping and it will be an extremely important part in training the agent. In order to incentivize the agent to maximize later rewards, we will gradually give larger rewards as the agent progresses.-->

## References
RLLib?
