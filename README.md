# EEL5718 Lab2
Yumeng Zhang, Yuxuan Zhang, Xiyun Guo

## Video recordings are uploaded to "releases"

#### >>> [LINK TO RECORDINGS AND DRAWINGS](https://github.com/zhangyx1998/EEL5718-Labs/releases/tag/Lab2-Submission-1) <<<

##  [`Linear`](linear.py) Topology - Xiyun Guo

> This Python script defines a low-level mininet linear topology.
>
> _Code Written By Yuxuan Zhang_

+ Usage:

    ```sh
    sudo ./linear.py
    # optional:
    #   -N <number of nodes>
    #   --interactive
    ```

## [`Tree`](tree.py) Topology - Yumeng Zhang

> This Python script defines a mininet tree topology named 'MyTreeTopo'.

+ Description:

    This topology consists of seven switches (s1, s2_1, s2_2, s3_1, s3_2, s4_1, s4_2) and eight hosts (h1, h2, h3, h4, h5, h6, h7, h8).

    Starting from s1, the switches create a hierarchical branching structure, and the hosts are connected to the switches as follows:
    h1 and h2 connect to s2_1;
    h3 and h4 connect to s3_1;
    h5 and h6 connect to s4_1;
    h7 and h8 connect to s4_2.

+ Usage:

    ```sh
    sudo mn --custom mytreetopo.py --topo mytreetopo
    ```

## [`Mesh`](mesh.py) Topology - Yuxuan Zhang

> This Python script defines a low-level mininet mesh topology.

+ Usage:

    ```sh
    sudo ./mesh.py
    # optional:
    #   -N <number of nodes>
    #   --interactive
    ```

