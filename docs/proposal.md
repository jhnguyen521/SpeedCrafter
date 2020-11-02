---
layout: default
title: Proposal
---

## Summary

For our project, we want to give our agent a recipe or list of resources which the agent must find and collect by exploring the world around it. The agent would be placed in a randomly-generated stage that somewhat mimics a normal world (e.g. ores would tend to spawn underground instead of near the surface), but smaller and less complex. The agent would be given limited information about its immediate surroundings given in the form of a three-dimensional grid and would have to explore to find additional resources. There would also be potential hazards in the area that our agent would have to be aware of and react accordingly. Our project has applications in problems that involve searching for objects in unfamiliar areas.

## AI/ML Algorithms
Because we plan on having a continous action space for our agent, we decided to work with policy gradient methods of reinforcement learning. We plan to train our agent using Soft-Actor Critic (SAC) due to it tending to perform well with generalization as well as the decreased need for tuning of hyperparameters.

## Evaluation Plan

A factor that will be evaluated is the agent's ability to collect all of the resources requested of the input. For every item collected, the agent would receive a reward for making progress in the task. The agent would also be evaluated on how well it manages to avoid potential obstacles in the form of punishment in the event that it runs into one. We could also help our agent optimize better by rewarding the agent for taking less actions.


## Appointment time
The appointment has been scheduled for **October 29** at **10 AM** (PDT).
