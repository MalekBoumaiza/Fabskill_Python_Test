

import pandas as pd
import numpy as np
import json
from flask import *

_app = Flask(__name__)


#load .csv files into dataframes
#jobs
df_jobs = pd.read_csv("jobs.csv")
df_jobs = pd.DataFrame(df_jobs,columns=['JobId','custom_title'])

#user_job_cand
df_users = pd.read_csv("users.csv")
df_users = pd.DataFrame(df_users,columns=['UserId','User_fname','User_lname'])

#users
df_user_job_cand = pd.read_csv("user_job_cand.csv")
df_user_job_cand = pd.DataFrame(df_user_job_cand,columns=['UserId','JobId'])


@_app.route('/getApplicationPerUser', methods=['GET'])
def getApplicationPerUser():
    
    if 'userID' in request.args:
        id = int(request.args['userID'])
        if id in df_users['UserId']:
          jobs = df_user_job_cand.loc[df_user_job_cand['UserId'] == id, 'JobId'].tolist()
          result = df_jobs.loc[df_jobs['JobId'].isin(jobs)]
        else:
          return "Error: invalid userID. retry with another one"
    else:
        return "Error: No userID field provided. Please specify a userID."
    
    if result.empty:
      return "NONE!"
    else:
      return result.to_json(orient = 'records', indent=2)

@_app.route('/getApplicationPerJob', methods=['GET'])
def getApplicationPerJob():
    
    if 'jobID' in request.args:
        id = int(request.args['jobID'])
        if id in df_jobs['JobId']:
          users = df_user_job_cand.loc[df_user_job_cand['JobId'] == id, 'UserId'].tolist()
          result = df_users.loc[df_users['UserId'].isin(users)]
        else:
          return "Error: invalid jobID. retry with another one"
    else:
        return "Error: No jobID field provided. Please specify a jobID."
    if result.empty:
      return "NONE!"
    else:
      return result.to_json(orient = 'records', indent=2)


if __name__ == "__main__":
    _app.run()



