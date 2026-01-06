def extract_arguments_in_braces(s) -> list[str]:
	result = []
	count = 0
	left, right = 1, len(s)
	for i in range(len(s)):
		if s[i] not in "{}":
			continue
		if s[i] == "{":
			count += 1
			if count == 1:
				left = i + 1
		elif s[i] == "}":
			count -= 1
			if count == 0:
				right = i
				result.append(s[left:right])
	return result

class TCategory:
	def __init__(self, identifier, name):
		self.id = identifier
		self.name = name

def get_categories() -> list[TCategory]:
	categories = []
	with open("src/categories_list.txt", "r", encoding=CODEC) as file:
		for line in file:
			identifier, name, *_ = filter(lambda item: item != "", line.strip().split('\t'))
			categories.append(TCategory(identifier, name))
	return categories

class TTask:
	def __init__(self, task_file):
		with open(f"src/tasks/{task_file}", "r", encoding=CODEC) as file:
			lines = file.read()
			task_args = extract_arguments_in_braces(lines)
			self.file = task_file
			self.number = int(task_file.rstrip(".tex"))
			self.categories = extract_arguments_in_braces(task_args[0].strip())
			self.problem = task_args[1].strip()
			self.solution = task_args[2].strip()
			self.answer = task_args[3].strip()

CODEC = "utf-8"

def main():
	categories = get_categories()

	tasks = []
	with open("__compile/python_cache/tasks.pre", "r", encoding=CODEC) as file:
		for line in file:
			task_file = line.strip()
			task = TTask(task_file)
			tasks.append(task)

	for category in categories:
		with open(f"src/precompiled/categories/{category.id}.tex", "w", encoding=CODEC) as out:
			out.write(rf"\hypertarget{{category:{category.id}}}{{}}" + "\n")
			out.write(rf"\section{{{category.name}}}" + "\n")
			tasksByCategory = list(filter(lambda item: category.id in item.categories, tasks))
			print(category.id.ljust(40), list(map(lambda item: int(item.file.rstrip('.tex')), tasksByCategory)))
			for order, task in enumerate(tasksByCategory, 1):
				out.write(rf"\hyperlink{{{category.id}:{order}}} {{\large{{\textbf{{ Задача {order}({task.number})}}}}}}" + "\n")
				out.write(task.problem + r"\\[4mm]" + "\n")
			out.write(r"\clearpage")
	
	with open("src/precompiled/categories.tex", "w", encoding=CODEC) as out:
		for category in categories:
			out.write(rf"\input{{src/precompiled/categories/{category.id}.tex}}" + "\n")

	with open("src/precompiled/commands.tex", "w", encoding=CODEC) as out:
		out.write(
r"""\newcommand{\newtaskref}[1] {
	\stepcounter{task#1}
	\hyperlink{category:#1}
	{%
	""")
		for order, category in enumerate(categories):
			out.write( (r'\else' if order > 0 else '') +
					   rf"\ifnum \pdfstrcmp{{#1}}{{{category.id}}} = 0%" + "\n" +
					   f"{category.name}%\n")
		out.write(r"\else ХУИТА " + r"\fi" * len(categories))
		out.write(r"""
	}%
	\hypertarget{#1:\arabic{task#1}}{}
}""")

	with open("src/precompiled/settings.tex", "w", encoding=CODEC) as out:
		for category in categories:
			out.write(rf"\newtaskcounter{{{category.id}}}" + "\n")

if __name__ == "__main__":
	main()