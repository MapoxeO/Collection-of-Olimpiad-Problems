CODEC = "utf-8"

if __name__ == "__main__":
    import os
    tasks = [ file for file in os.listdir("src/tasks") if file.endswith(".tex") and file.rstrip(".tex").isnumeric() ]
    sortedTasks = sorted( ( int(task.rstrip(".tex")), task ) for task in tasks )

    # Doing cache for simple access to the tasks
    python_cache_path = '__compile/python_cache'
    if not os.path.exists(python_cache_path):
        os.makedirs(python_cache_path)
    with open(f"{python_cache_path}/tasks.pre", "w", encoding=CODEC) as out:
            for _, task in sortedTasks:
                out.write(f"{task}\n")

    with open("src/precompiled/tasks.tex", "w", encoding=CODEC) as out:
        out.write(r"\section{Все задачи}")
        for _, task in sortedTasks:
            out.write(rf"\input{{src/tasks/{task}}}" + "\n")