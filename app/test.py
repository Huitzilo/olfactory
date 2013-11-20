#!/usr/bin/env python
# encoding: utf-8
'''
'''
import json
from hallem import data

h = data.Hallem()

job_id = 1
response = h.response
data_names = h.or_list
feature_names = h.odorant_list

js = [{"job_id": job_id, "number_data": response.shape[0], "number_features": response.shape[1],
       "data_names": data_names.tolist(), "feature_names": feature_names.tolist()}]

print json.dumps(js)