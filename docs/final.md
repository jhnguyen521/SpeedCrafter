---
layout: default
title: Final Report
---

## Video
<iframe width="560" height="315" src="https://www.youtube.com/embed/mEVgjwE8kqI" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="margin:auto; display:block;"></iframe>

## Summary
The goal of our project is to create an agent that is able to gather resources and craft items in a normally-generated Minecraft world. The agent is spawned in a 29x29 chunk created with the default world generator, containing resources such as wood, dirt and stone. Information about the agent's surroundings is given in the form of a 5x5x5 grid centered on its current location. The user inputs an item to craft through the command line, which is transformed into a list of resources that is given to the agent.

Due to its limited sight range, the agent must explore the world around it and break blocks to collect resources. Reinforcement learning is used to train the agent to do so in an efficient manner (i.e. collecting the resources with fewer steps). We used the Soft-Actor Critic algorithm as it works well on continuous action spaces and requires less hyperparameter tuning than algorithms such as Q-learning.

<div style="text-align:center"><img src='https://raw.githubusercontent.com/jhnguyen521/SpeedCrafter/main/img/arena.png' width='750px' height='500px'/></div>
<div style="text-align:center"><small>The agent's environment</small></div>

## Approaches

The approach that we originally wanted to take was to have our agent cycle through 5 different seeds to train on real chunks rather than an artificial environment as well as to prevent overfitting. This approach would give us the best results in terms of generalization but would require a lot of repeated tuning and training as well as time put towards selecting a seed with a good training enviroinment. Due to time constraints and the oddities of working in a group via the internet as well as the lack of powerful equipment, we decided to simplify our approach.

We instead used a single seed which, although it would eventually overfit the agent, would still be able to show that the agent actually learns and, up to a certain extent, if training was stopped before overfitting began, the agent would still be able to generalize decently due to the nature of Soft Actor Critic (SAC) if it was placed in a different environment. Training was mainly done with a stone pickaxe as the input because it forces the agent to explore the whole environment vertically and dig through dirt rather than simply finding things on the surface as it gathers both stone and wood.

### Rewarding the agent
In order for the agent to learn, it is extremely important to reward the agent properly to encourage certain behaviors and actions. The most basic reward that we gave to the agent was rewarding it for when it mines and collects a resource that it still needs. We rewarded the agent with a flat 100 for collecting a needed resource, -1 for collecting a resource that it doesn't need as to encourage it to not break everything in sight, and 1000 for collecting all resources needed and crafting an item. We also gave it a -1 reward for every action it took to push the agent to optimize its actions. What's interesting to note is that because stone is below dirt, the agent would have to lose rewards for mining towards it, but it will receive a greater overall reward if it goes for it. This alone, however, is not enough to efficiently train the agent. As stated in our problem statement, an important aspect of the project is exploration. If the agent, for whatever reason, ends up never collecting a needed resource, it will never know that it needs to collect those resources in the first place. To solve this problem, we encouraged the agent to have a greedy approach in collecting resources. Upon finding a resource in its observation space, we help the agent simplify this space by calculating the coordinates of the nearest resource and provide the agent with the distance from it. We then reward the agent +-1 depending on whether it gets closer or further from that resource. Upon collecting any resource, the agent will then try to explore until it can find a resource in its observation space and repeats the process.

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
<div style="text-align:center"> <img src='https://raw.githubusercontent.com/jhnguyen521/SpeedCrafter/main/img/final_return_graph.png'/> </div>

## References

* [OpenAI documentation about Soft Actor-Critic](https://spinningup.openai.com/en/latest/algorithms/sac.html)
* [paperswithcode.com](https://paperswithcode.com/method/soft-actor-critic)
* [Malmo documentation](https://microsoft.github.io/malmo/0.30.0/Documentation/index.html)
* [Ray RLlib documentation](https://docs.ray.io/en/latest/rllib.html)
* Code from Assignment 2
