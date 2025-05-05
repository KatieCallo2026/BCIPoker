def ask_scale(pid, phase, time_sec):
    rating = input(f"Participant {pid} - {phase.upper()} phase @ {time_sec}s\nRate your stress (1–5): ")
    return {"phase": phase, "time_sec": time_sec, "rating": int(rating)}
