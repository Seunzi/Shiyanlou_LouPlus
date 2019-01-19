# -*- conding: utf-8 -*-

import sys
from pymongo import MongoClient
from bson.son import SON

def get_rank(user_id):
    client = MongoClient()
    db = client.shiyanlou
    contests = db.contests

    pipeline = [
            {"$unwind":"$user_id"},
            {"$group": {"_id":"$user_id","score":{"$sum":"$score"},"time":{"$sum":"$submit_time"}}},
            {"$sort":SON([("score",-1),("time",1)])}
            ]
    rank_dict = {}
    rank_list = list(contests.aggregate(pipeline))
    for i in range(len(rank_list)):
        rank_dict[rank_list[i]['_id']] = [i+1, rank_list[i]['score'], rank_list[i]['time']]

    rank = rank_dict[int(user_id)][0]
    score = rank_dict[int(user_id)][1]
    submit_time = rank_dict[int(user_id)][2]

    return rank, score, submit_time

if __name__ == '__main__':

    user_id = sys.argv[1:]
    if user_id:
        try:
            userdata = get_rank(user_id[0])
            print(userdata)
        except Exception:
            print("Parameter Error!")
            exit()
    else:
        print("Parameter Error!")
        exit()

