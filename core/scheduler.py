from datetime import date, timedelta

WEIGHT = {"High": 3, "Medium": 2, "Low": 1}

def make_schedule(tasks, hours_per_day, block=2):
    """
    tasks: list of dicts with keys subject, deadline (date), priority, hours_needed
    Returns (plan, unscheduled)
    """
    if not tasks:
        return [], {}

    remaining = {t["subject"]: float(t["hours_needed"]) for t in tasks}
    plan = []
    day = date.today()
    last_day = max(t["deadline"] for t in tasks)

    while day <= last_day:
        free = float(hours_per_day)

        live = [t for t in tasks
                if remaining[t["subject"]] > 0 and t["deadline"] >= day]

        # higher score = more urgent
        live.sort(key=lambda t: -(WEIGHT[t["priority"]] /
                                  max((t["deadline"] - day).days, 1)))

        for t in live:
            if free <= 0:
                break
            hours = min(block, free, remaining[t["subject"]])
            plan.append({"date": day, "subject": t["subject"], "hours": hours})
            remaining[t["subject"]] -= hours
            free -= hours

        day += timedelta(days=1)

    unscheduled = {k: v for k, v in remaining.items() if v > 0}
    return plan, unscheduled