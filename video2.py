import sys
import numpy as np
from flask import Flask, Response, render_template
from kafka import KafkaConsumer