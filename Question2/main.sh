#!/bin/bash

gcc -o philos.e philos.c
for i in {1..1000}
do
    ./philos.e
done
