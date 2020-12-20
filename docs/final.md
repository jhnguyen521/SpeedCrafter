---
layout: default
title: Final Report
---

## Summary

## Approaches

The approach that we originally wanted to take was to have our agent cycle through 5 different seeds to train on real chunks rather than an artificial environment as well as to encourage not overfitting. This approach would give us the best results in terms of generalization but would require a lot of repeated tuning and training as well as time put towards selecting a seed with a good training enviroinment. Due to time constraints and the oddities of working in a group via the internet as well as the lack of powerful equipment, we decided to simplify our approach.

We instead used a single seed which, although it would eventually overfit the agent, it would still be able to show that the agenta actually learns and, up to a certain extent, if training was stopped before overfitting began, the agent would still be able to generalize decently due to the nature of Soft Actor Critic (SAC) if it placed in a different environment. We also added some artificial elements to the seed such as making stone a little bit more easily accessible to speed up training.

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

## Evaluation

## References
RLLib?
