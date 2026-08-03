from flask import Flask, jsonify, request
import time
import math
import random
import threading
import os
from datetime import datetime

app = Flask(__name__)

request_count = 0
memory_storage = []
lock = threading.Lock()


@app.route("/")
def home():
    return jsonify({
        "message": "Heavy Load Testing Flask Application",
        "hostname": os.uname().nodename,
        "time": datetime.now().isoformat(),
        "requests": request_count
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "UP",
        "pod": os.uname().nodename
    })


# CPU intensive workload
@app.route("/cpu")
def cpu_test():

    global request_count

    with lock:
        request_count += 1

    start = time.time()

    result = 0

    # Heavy mathematical calculations
    for i in range(1, 8000000):
        result += math.sqrt(i) * math.sin(i)

    duration = time.time() - start

    print(
        f"CPU TEST COMPLETED | Time: {duration:.2f}s | Pod: {os.uname().nodename}"
    )

    return jsonify({
        "task": "CPU intensive calculation",
        "result": result,
        "execution_time": duration,
        "pod": os.uname().nodename
    })


# Memory stress test
@app.route("/memory")
def memory_test():

    global request_count

    with lock:
        request_count += 1

    size = int(request.args.get("size", 50))

    data = []

    for i in range(size):
        data.append(
            "X" * 1024 * 1024
        )

    memory_storage.append(data)

    print(
        f"MEMORY LOAD CREATED {size}MB | Pod: {os.uname().nodename}"
    )

    return jsonify({
        "message": "Memory allocated",
        "allocated_MB": size,
        "total_memory_objects": len(memory_storage),
        "pod": os.uname().nodename
    })


# Artificial latency testing
@app.route("/delay")
def delay():

    seconds = int(request.args.get("seconds", 10))

    print(
        f"Sleeping for {seconds} seconds"
    )

    time.sleep(seconds)

    return jsonify({
        "message": "Delay completed",
        "delay_seconds": seconds,
        "pod": os.uname().nodename
    })


# Random mixed workload
@app.route("/stress")
def stress():

    global request_count

    with lock:
        request_count += 1


    workload = random.choice(
        [
            "cpu",
            "memory",
            "delay"
        ]
    )


    if workload == "cpu":

        result = 0

        for i in range(1,5000000):
            result += math.sqrt(i)

        return jsonify({
            "workload":"CPU",
            "result":result
        })


    elif workload == "memory":

        temp = []

        for i in range(30):
            temp.append(
                "LOAD"*100000
            )

        return jsonify({
            "workload":"MEMORY",
            "created":"30MB+"
        })


    else:

        time.sleep(5)

        return jsonify({
            "workload":"DELAY",
            "wait":"5 seconds"
        })



@app.route("/stats")
def stats():

    return jsonify({

        "total_requests":request_count,

        "memory_objects":
        len(memory_storage),

        "hostname":
        os.uname().nodename

    })



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        threaded=True
    )
