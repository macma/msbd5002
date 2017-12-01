#!/usr/bin/python
import psycopg2
import sys
import pprint
import numpy as np
import svm as svm
import os
import datetime

totalVideoLength = 19228.14


def timedelta_total_seconds(timedelta):
    return (
        timedelta.microseconds + 0.0 +
        (timedelta.seconds + timedelta.days * 24 * 3600) * 10 ** 6) / 10 ** 6


def createFeatures(records, istrain):
	cacheUserId = ''
	cacheSessionId = ''
	cacheVideoId = ''
	# 63 videos
	# print(timedelta_total_seconds(records[5][9] - records[3][9]))  # /135.95
	# print((records[5][9] - records[3][9]))  # /135.95
	# for i in range(len(records)):

	f = np.zeros(64)  # 63videos, 1 total second, 1 total session, 1
	userlist = []
	usercounter = 0
	userlabel = 0
	featurelist = []
	labellist = []
	for i in range(len(records)):
		if(records[i][1] <> cacheUserId):
			cacheUserId = records[i][1]
			usercounter = usercounter + 1
			f = np.zeros(64)
			if(istrain):
				userlabel = records[i][11]
				labellist.append(float(userlabel))
		# f[records[i][0]] = f[records[i][0]] + records[i][0]
		if(i <> len(records) - 1):
			if(records[i][1] == records[i + 1][1] and  # user_id
                                # session_id
                                records[i][3] == records[i + 1][3] and
                                records[i][8] <> 'speed_change_video' and
                                records[i][8] <> 'seek_video'):
				dura = timedelta_total_seconds(records[i + 1][9] - records[i][9])
				f[records[i][0]] = f[records[i][0]] + dura / float(records[i][10])
				f[63] = f[63] + dura / totalVideoLength
		if(i == len(records) - 1 or records[i][1] <> records[i + 1][1]):
			userinfo = (usercounter, f, int(userlabel), cacheUserId)  # (records[i][1], f)
			userlist.append(userinfo)
			featurelist.append(map(lambda x: float(x), f))
	print 'features count: ', len(featurelist)
	if(istrain):
		print featurelist[0]
		return {"featureList":featurelist,"labelList":labellist}
	else:
		return {"featureList":featurelist, "userList":userlist}

	# print f[2]


def main():
	print 'program start:', datetime.datetime.now()
	#Define our connection string
	conn_string = "host='52.74.79.13' dbname='sammy' user='sammy' password='sammy'"

	# print the connection string we will use to connect
	print "Connecting to database\n	->%s" % (conn_string)

	# get a connection, if a connect cannot be made an exception will be
	# raised here
	conn = psycopg2.connect(conn_string)

	# conn.cursor will return a cursor object, you can use this cursor to
	# perform queries
	cursor = conn.cursor()
	print "Connected!\n"

	cursor.execute("select vi.vid, tf.*, vi.duration, tl.grade from train_features tf inner join \
	video_info vi on tf.video_id = vi.video_id \
	inner join train_label tl on tl.user_id = tf.user_id \
	 order by user_id, event_time;")

	# where tf.user_id in ('ff930d24cbdeb11e6dde8ceb0da5ac64', 'eee1df0fff33a37873990992bed20e82') \
	records = cursor.fetchall()
	print('fetch train data done, ', datetime.datetime.now())
	svm_trainset = createFeatures(records, True)


	cursor.execute("select vi.vid, tf.*, vi.duration from test_features tf inner join \
	video_info vi on tf.video_id = vi.video_id \
	 order by user_id, event_time;")
	# where tf.user_id in ('a74fe6d4812fa93a1afa1a6a334ebdda', '4ab9d6eadf7510198f468d10fc29f689', '55654c092cd47b64ec9860f6a9cf3b40') \
	records = cursor.fetchall()
	print('fetch test data done, ', datetime.datetime.now())
	svm_testset = createFeatures(records, False)

	svm.train(svm_trainset['featureList'], svm_trainset['labelList'])
	svm.classify(svm_testset['featureList'], svm_testset['userList'])

	print('program finish', datetime.datetime.now())
if __name__ == "__main__":
	main()
