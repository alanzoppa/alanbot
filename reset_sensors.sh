#!/bin/bash

uhubctl -a off -l 1-1 -p 4
sleep 1
uhubctl -a on  -l 1-1 -p 4
