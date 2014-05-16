pymsdb
======

Pymsdb is python implementation of mono soft debugger client. It implements only 2.1 protocol version features (debugger-agent.c version: https://github.com/mono/mono/blob/e66f1611cf18ba117454a223a565af905a06756f/mono/mini/debugger-agent.c). It can be considered as the analogue for Mono.Debugger.Soft assembly.

The main goal of this project is to make available debugging mono programs (Unity3D scripts particularly) inside of editors using Python for their plugins.