#!/usr/bin/python3
from datetime import datetime
from dateutil.tz import tzutc
from kubernetes import client, config

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

v1 = client.CoreV1Api()
pod_list = v1.list_pod_for_all_namespaces(watch=False)
for pod in pod_list.items:
    sorted_status = sorted(
        pod.status.conditions,
        key=lambda x: x.last_transition_time or datetime.min.replace(tzinfo=tzutc()),
    )
    last_status = sorted_status[-1]
    for container in pod.spec.containers:
        print(pod.metadata.namespace, container.name, container.image)
    # print("%s\t%s\t%s" % (i.status.pod_ip, i.metadata.namespace, i.metadata.name))
    # print(i['spec']['containers'])


node_list = v1.list_node()
for node in node_list.items:
    print(node)
