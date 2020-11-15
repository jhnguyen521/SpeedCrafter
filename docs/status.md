---
layout: default
title: Status
---

<iframe width="560" height="315" src="https://www.youtube.com/embed/EtwqYYouHnY" frameborder="0" allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>


## Summary
For our project, we want to give our agent a recipe or list of resources which the agent must find and collect by exploring the world around it. The agent would be placed in a normally-generated world with a given world seed. The agent would be given limited information about its immediate surroundings in the form of a three-dimensional grid and would have to explore to find additional resources. It would also need to be aware of and react to potential hazards in the area. Our project has applications in problems that involve searching for objects in unfamiliar areas.

## Approach

### Entropy reinforcement maximum learning: soft actor critic (SAC)


We will use entropy reinforcement maximum learning: soft actor critic (SAC), which is an off-policy, independent of the agent’s action algorithm. The agent will try to maximize the expected award as well as entropy. Since the agent tries to maximize the entropy, the agent will take more random actions and therefore is encouraged to explore more possibilities. The algorithm prefers the most random action that receives the highest reward.

Reward functions:
<img src='https://raw.githubusercontent.com/jhnguyen521/SpeedCrafter/main/img/reward_f.png' title='Reward function' />
                                                                                                                  

 
H() = entropy measure, α = how important the entropy is (weight of entropy, temperature parameter) 


SAC uses three main network:
<img src='https://raw.githubusercontent.com/jhnguyen521/SpeedCrafter/main/img/3functions.png' title='threefunctions' />

 
Soft state value function aims to minimize the mean squared error 
<img src='https://raw.githubusercontent.com/jhnguyen521/SpeedCrafter/main/img/soft_state.png' title='soft state Q' />


Soft Q function aims to minimize the soft Bellman residual
<img src='https://raw.githubusercontent.com/jhnguyen521/SpeedCrafter/main/img/soft_q.png' title='soft state Q' />

 
Pseudo algorithm

<img src='https://raw.githubusercontent.com/jhnguyen521/SpeedCrafter/main/img/algorithm.png' title='algorithm' />

### Solving the Problem

To solve our problem, we will combine RL along with other algorithms to help the agent complete the task. We will be using RL primarily for the exploring and searching aspect of the AI and creating algorithms for the AI to actually perform the crafting upon collecting all items due to crafting recipes being pre-defined. Regarding the environment, we will be alternating between a few pre-defined world seeds in order to help train the agent to be able to generalize in different environments.


## Evaluation

The agent will be evaluated in its efficiency in finding resources to craft as well as whether it actually is able to craft the request item or not. Each action taken will incur some sort of small negative reward such as -1 in order to encourage the agent to complete the task with fewer actions. We would also reward it as it works towards completing the task for conditions such as collecting a needed item or getting closer to a needed resource. This is known as reward shaping and it will be an extremely important part in training the agent. In order to incentivize the agent to maximize later rewards, we will gradually give larger rewards as the agent progresses.

## Remaining Goals and Challenges

Regarding remaining goals and challenges, we are still deciding what kind of neural network may be best for our application and train the agent using it to gather resources. We also need to implement algorithms to actually use the collected resources and craft the requested item. Reward shaping will definitely be a large challenge in optimizing our neural network because we need to create some method for rewarding the agent for getting closer to certain objectives while being careful about possible ways the agent could take advantage of the reward system while not performing desired actions.

## Resources Used
Resources that were helpful included the following:
* Malmo documentation
External Libraries:
https://github.com/haarnoja/sac

