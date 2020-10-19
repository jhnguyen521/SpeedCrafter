---
layout: default
title: Proposal
---

## Summary

The basic idea behind our project is relatively simple. We want our agent to gather resources for a recipe and craft an item or multiple items as fast as possible. The agent would be placed in an environment in which it must find resources and create specific items. The agent would be given limited information about its immediate surroundings given in the form of a three-dimensional grid and a list of recipes to craft and then output a set of actions which would optimize the time taken to craft those recipes. The agent would have to explore in order to find additional resources. The crux of the problem is that the fastest way to collect a resource or craft a recipe individually may not be the best way when attempting to craft multiple recipes. An example of this would be attempting to gather stone. One might simply dig through dirt to reach stone with their bare hands, but depending on the amount of dirt, it might be faster to instead first craft a shovel and then begin digging. Our project has applications in optimization problems where the fastest or most efficient solution is desired while having incomplete information.

## AI/ML Algorithms

## Evaluation Plan

One factor that will be evaluated is the agent's efficiency in gathering the required resources. This can be things like the time taken to gather all of the resources, the total distance traveled, the number of blocks broken, and/or the amount of damage taken by the player. One possible approach to improving the efficiency is to test different mining methods, such as which Y-level the agent mines at or the pattern that they mine in.

The project will also be evaluated on the complexity of the tasks performed. To ensure that the AI is generalized enough, it can be tested with different types of resources such as ores, dirt, plants, or a combination of them. A particularly impressive result would include things such as killing mobs and finding structures, such as obtaining Blaze Rods (which involve obtaining obsidian to build a Nether Portal, finding a Nether Fortress and killing blazes without dying).
