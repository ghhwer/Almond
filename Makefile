build:
	docker build containers/base-image/java/. -t almond/base-java
	docker build containers/base-image/python_java/. -t almond/base-java-python
	docker build containers/hadoop/base-hadoop/. -t almond/hadoop-base
	docker build containers/hadoop/namenode/. -t almond/namenode
	docker build containers/hadoop/datanode/. -t almond/datanode
	docker build containers/hadoop/resourcemanager/. -t almond/resourcemanager
	docker build containers/hadoop/nodemanager/. -t almond/nodemanager
	docker build containers/hadoop/historyserver/. -t almond/historyserver
	docker build containers/spark/base-spark/. -t almond/spark-base
	docker build containers/spark/spark/. -t almond/spark
	docker build containers/spark/notebook/. -t almond/notebook
