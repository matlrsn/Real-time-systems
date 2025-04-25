# EDF non-preemptive
import numpy as np
import matplotlib.pyplot as plt
import random

# ------------------------------
# TASK DEFINITION
# ------------------------------

# Define the periodic task set with ID, Worst Case Execution Time (C), and Period (T)
tasks = [
    {"id": 1, "C": 2, "T": 10},
    {"id": 2, "C": 3, "T": 10},
    {"id": 3, "C": 2, "T": 20},
    {"id": 4, "C": 2, "T": 20},
    {"id": 5, "C": 2, "T": 40},
    {"id": 6, "C": 2, "T": 40},
    {"id": 7, "C": 3, "T": 80},
]

# ------------------------------
# EDF NON-PREEMPTIVE FUNCTION
# ------------------------------

def earliest_deadline_first_nonpreemptive(tasks, hyperperiod):
    """
    Non-preemptive EDF scheduler.
    At each time unit, if the processor is idle, choose the job with the earliest deadline.
    """
    schedule = [-1] * hyperperiod  # Initialize schedule as idle (-1)
    task_queue = []
    current_task = None
    remaining_time = 0

    for t in range(hyperperiod):
        # Release new jobs at their periods
        for task in tasks:
            if t % task["T"] == 0:
                task_queue.append({"id": task["id"], "C": task["C"], "deadline": t + task["T"], "release": t})

        # If no task is running, pick the next job with earliest deadline
        if remaining_time == 0:
            current_task = None
            task_queue.sort(key=lambda x: x["deadline"])
            if task_queue:
                current_task = task_queue.pop(0)
                remaining_time = current_task["C"]

        # Execute the selected task if any
        if current_task:
            schedule[t] = current_task["id"]
            remaining_time -= 1

    idle_time = schedule.count(-1)
    return schedule, idle_time

# ------------------------------
# UTILIZATION TEST
# ------------------------------

def utilization_test(tasks):
    """Check schedulability using total utilization U = Σ(C/T)."""
    return sum(task["C"] / task["T"] for task in tasks)

# Compute the hyperperiod (LCM of task periods)
hyperperiod = np.lcm.reduce([task["T"] for task in tasks])

# Check total utilization
utilization = utilization_test(tasks)
print(f"Total utilization sum: {utilization:.4f}")
if utilization <= 1:
    print("Schedulable as utilization ≤ 1")
else:
    print("Not schedulable as utilization > 1")

# ------------------------------
# EDF SCHEDULING AND VISUALIZATION
# ------------------------------

# Generate the EDF schedule and calculate idle time
schedule, idle_time = earliest_deadline_first_nonpreemptive(tasks, hyperperiod)

# Assign random colors to each task
colors = {task["id"]: (random.random(), random.random(), random.random()) for task in tasks}
colors[-1] = (0, 0, 0)  # Black for idle

# Plot the EDF schedule
plt.figure(figsize=(12, 4))
for t in range(hyperperiod):
    plt.plot(t, schedule[t], 'o', color=colors[schedule[t]], markersize=5)

# Add legend
legend_handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors[task["id"]], markersize=8, label=f'Task {task["id"]}') for task in tasks]
legend_handles.append(plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=colors[-1], markersize=8, label='Idle Time'))
plt.legend(handles=legend_handles, title="Task Legend")

plt.xlabel("Time")
plt.ylabel("Task ID")
plt.title("Non-Preemptive EDF Scheduling")
plt.grid(True)
plt.show()

print(f"Total processor idle time: {idle_time} time units out of {hyperperiod}")

#%% ------------------------------------------
# STATIC PRIORITY PERMUTATION SIMULATION
#---------------------------------------------

import itertools

# Function to simulate static-priority scheduling
def simulate_schedule(task_order, hyperperiod):
    schedule = [-1] * hyperperiod
    job_queue = []
    release_table = {task["id"]: [] for task in task_order}

    # Generate job releases for each task
    for task in task_order:
        for t in range(0, hyperperiod, task["T"]):
            release_table[task["id"]].append({"release_time": t, "C": task["C"], "id": task["id"]})

    # Flatten and sort jobs by release time and fixed priority
    for task in task_order:
        job_queue.extend(release_table[task["id"]])
    job_queue.sort(key=lambda job: (job["release_time"], [t["id"] for t in task_order].index(job["id"])))

    t = 0
    waiting_time = 0

    while t < hyperperiod and job_queue:
        for i, job in enumerate(job_queue):
            if job["release_time"] <= t:
                schedule[t:t + job["C"]] = [job["id"]] * job["C"]
                waiting_time += t - job["release_time"]
                t += job["C"]
                job_queue.pop(i)
                break
        else:
            t += 1  # CPU idle

    return schedule, waiting_time

# Try all static priority permutations and find best one
results = []
for i, perm in enumerate(itertools.permutations(tasks)):
    schedule, total_waiting = simulate_schedule(perm, hyperperiod)
    task_order_ids = [task["id"] for task in perm]
    print(f"Config {i + 1}: Order {task_order_ids}, Total Waiting Time = {total_waiting}")
    results.append((task_order_ids, schedule, total_waiting))

# Get best result (minimum total waiting)
best_order, best_schedule, best_waiting = min(results, key=lambda x: x[2])
print(f"\nBest Order: {best_order}, with Minimum Waiting Time = {best_waiting}")

# Plot best fixed-priority schedule
plt.figure(figsize=(14, 3))
plt.title(f"Best Schedule: Order {best_order}, Waiting Time = {best_waiting}")
plt.xlabel("Time")
plt.ylabel("Task ID")
plt.grid(True)
plt.yticks(range(1, 8))
for t, task_id in enumerate(best_schedule):
    if task_id != -1:
        plt.bar(t, 1, bottom=task_id - 0.5, width=1, align='center', color=f"C{task_id % 10}", edgecolor='black')
plt.tight_layout()
plt.show()

#%% ------------------------------------------
# EXHAUSTIVE JOB-LEVEL PERMUTATION SIMULATION
# -------------------------------------------

from itertools import permutations

# Define simplified task set for job-level simulation
tasks = {
    1: {"C": 2, "T": 10},
    2: {"C": 3, "T": 10},
    3: {"C": 2, "T": 20},
    #4: {"C": 2, "T": 20},
    #5: {"C": 2, "T": 40},
    #6: {"C": 2, "T": 40},
    #7: {"C": 3, "T": 80},
}

# Generate 3 jobs per task
jobs = []
for task_id, props in tasks.items():
    for j in range(3):
        jobs.append({
            "task_id": task_id,
            "job_id": j + 1,
            "arrival": j * props["T"],
            "C": props["C"],
            "T": props["T"],
            "name": f"T{task_id}_J{j + 1}",
        })

# Simulate every job permutation and check deadline violations
valid_schedules = []
for perm in permutations(jobs):
    time = 0
    schedule = []
    deadline_misses = []

    for job in perm:
        start = max(time, job["arrival"])
        finish = start + job["C"]
        response = finish - job["arrival"]
        deadline = job["arrival"] + job["T"]
        missed = finish > deadline

        schedule.append({
            "job": job["name"],
            "start": start,
            "finish": finish,
            "response_time": response,
            "deadline": deadline,
            "missed_deadline": missed
        })

        if missed:
            deadline_misses.append(job["name"])

        time = finish  # Non-preemptive

    valid_schedules.append({
        "schedule": schedule,
        "misses": deadline_misses,
        "total_response_time": sum(j["response_time"] for j in schedule)
    })

# Get best job-level schedule (min response time)
best_schedule = min(valid_schedules, key=lambda s: s["total_response_time"])

# Display results
print(f"\nBest Schedule — Total Response Time: {best_schedule['total_response_time']}")
for job in best_schedule["schedule"]:
    status = "Missed Deadline" if job["missed_deadline"] else "OK"
    print(f"  {job['job']}: start={job['start']} finish={job['finish']} "
          f"resp={job['response_time']} deadline={job['deadline']} {status}")
