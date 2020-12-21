---
layout: default
title: Final Report
---

## Video
<iframe width="560" height="315" src="https://www.youtube.com/embed/mEVgjwE8kqI" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen style="margin:auto; display:block;"></iframe>

## Summary
The goal of our project is to create an agent that is able to gather resources and craft items in a normally-generated Minecraft world. The agent is spawned in a 29x29 chunk created with the default world generator, containing resources such as wood, dirt and stone. Information about the agent's surroundings is given in the form of a 5x5x5 grid centered on its current location. The user inputs an item to craft through the command line, which is transformed into a list of resources that is given to the agent. At any given point, the agent has the choice of turning left or right, looking up or down, moving forward, and breaking the block in front of it.

Due to its limited sight range, the agent must explore the world around it and break blocks to collect resources. Reinforcement learning is used to train the agent to do so in an efficient manner (i.e. collecting the resources with fewer steps). We used the Soft-Actor Critic algorithm as it works well on continuous action spaces and requires less hyperparameter tuning than algorithms such as Q-learning.

<div style="text-align:center"><img src='https://raw.githubusercontent.com/jhnguyen521/SpeedCrafter/main/img/arena.png' width='750px' height='500px'/></div>
<div style="text-align:center"><small>The agent's environment</small></div>

## Approaches

The baseline for our project is an agent that simply takes random actions. It sometimes obtained the desired resources before exceeding a maximum of 200 steps, but would take a long time to do so and gather lots of unnecessary resources such as dirt in the process.

The approach that we originally wanted to take was to have our agent cycle through 5 different seeds to train on real chunks rather than an artificial environment as well as to prevent overfitting. This approach would give us the best results in terms of generalization but would require a lot of repeated tuning and training as well as time put towards selecting a seed with a good training enviroinment. Due to time constraints and the oddities of working in a group via the internet as well as the lack of powerful equipment, we decided to simplify our approach.

We instead used a single seed which, although it would eventually overfit the agent, would still be able to show that the agent actually learns and, up to a certain extent, if training was stopped before overfitting began, the agent would still be able to generalize decently due to the nature of Soft Actor Critic (SAC) if it was placed in a different environment. Training was mainly done with a stone pickaxe as the input because it forces the agent to explore the whole environment vertically and dig through dirt rather than simply finding things on the surface as it gathers both stone and wood.

Crafting recipes were stored in a JSON file, and the list of resources to collect was determined via a script that recursively simplifies recipes into raw ingredients. This also generated a list of Malmo crafting commands, which were sent to the agent once all resources have been collected.

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

The agent is evaluated in its ability in finding resources as well as how efficient it is at doing so. A small penalty of -1 is incurred every time a command is sent to the agent, as well as when it collects dirt (a common item that's not used in any recipes). Collecting a required resource has a reward of 100, and collecting all of the resources adds an additional reward of 1000. This is intended to reward the agent for completing recipes and encourage it to do so in fewer steps. 

Some ingridients are also underground, and the observation space is only 5 * 5 * 5, which means that the agent can only see 2 blocks below it. Therefore, sometimes the penalty will be larger because the agent will give up some rewards to reach a bigger reward. For example, when the users want to craft a stone pickaxe, the agent has to dig some dirts (each dirt = -1 penalties) in order to get the stone underground, which has a larger reward. 

#### Return with Higher Learning Rate 
<div style="text-align:center"> <img src='https://github.com/jhnguyen521/SpeedCrafter/blob/main/img/high_learning.png'/> </div>

The first time we trained, the model had a higher learning rate. A higher learning rate means that the model requires less training epochs and adapts to rapid changes. The model would stuck at a local minima, so when the steps increases, the model did not learning anything, so the return decreased drastically.

#### Final Returns
<div style="text-align:center"> <img src='https://raw.githubusercontent.com/jhnguyen521/SpeedCrafter/main/img/final_return_graph.png'/> </div>

After lowering the learning rate, the model had more training epochs and was continuously learning as the steps increased, so we can see from the graph that even though the graph fluctuated and went up and down, overall, the return increased. 

| Steps | Returns |
| ----- | ------- |
| 0     | 0.0     |
| 2500  | 1333.0  |
| 5000  | 1175.0  |
| 7500  | 47.0    |
| 10000 | 430.0   |
| 12500 | -46.0   |
| 15000 | 1434.0  |
| 17500 | 377.0   |
| 20000 | 173.0   |

## References
* [OpenAI documentation about Soft Actor-Critic](https://spinningup.openai.com/en/latest/algorithms/sac.html)
* [paperswithcode.com](https://paperswithcode.com/method/soft-actor-critic)
* [Malmo documentation](https://microsoft.github.io/malmo/0.30.0/Documentation/index.html)
* [Ray RLlib documentation](https://docs.ray.io/en/latest/rllib.html)
* Code from Assignment 2
