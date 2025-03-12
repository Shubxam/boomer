Agent Coding Guidelines: Bookmark Manager App

1. Project Context
	1. final outcome definition: A command-line and Telegram-based bookmark management system that automatically categorizes links, supports various import methods, and provides powerful search capabilities. The system uses local LLMs for classification to maintain privacy while enabling efficient bookmark organization.
	2. tech-stack/coding-guidelines requirements : refer to [Tech Spec](../tech-spec.md)
	3. project domain specific instructions / constraints
2. core principles: objectives that LLM must follow
	1. keep the task objective (why) in mind
	2. always immediately clarify when in doubt
	3. code readability and maintainability
	4. always reuse components / avoid redundent code
	5. writing optimized (readable) code (e.g. vectorized operations instead of loops)
	6. strict adherence to coding style [Tech Spec](../tech-spec.md)
	7. secure handling of sensitive info
	8. Documentation as Code
3. task execution framework: How to execute a given task
	1. perform task understanding and show understanding
	2. Development phase
		1. modular approach
		2. iterative development
		3. efficient error handling
	3. Validation Phase: self review for correctness and adherence to guidelines
	4. documentation
		1. documentation as a code approach
		2. file-level/module description in [architecture.md](../architecture.md)
		3. For *important decisions or complex logic*, add comments *directly in the code* to explain the reasoning (for future reference, including your own).
	5. testing
		1. For each function you write, also write a corresponding unit test.
		2. undertake testing best practices such that code is validated but not too much time is spent on it as this is not a production grade software and shipping is more important than perfection.
4. Post Completion Protocol
	1. Ask user if task was successfully completed
	2. update [architecture.md](../architecture.md) and other documentation if necessary
	3. add task details to a [agent-project-log.md](../agent-project-log.md) file
		1. purpose of file: documenting bugs/features/context/important decisions/retrospective analysis for future reference (knowledge sharing) of agent and other maintainers.
		2. where to log: project root folder
		3. when to log: after successful completion of each assigned task
		4. how to log
			1. add current timestamp with `date +"%Y-%m-%d %H:%M:%S"` bash command
			2. document in markdown format
			3. sort by date desc, i.e. append to top
		5. what to log:
			4. decision taken
			5. type: bug-fix / new-feature
			6. bug/issue solved
			7. learning done
			8. gotchas / reminders
		6. example
> 	## [YYYY-MM-DD HH:MM:SS] Task Summary
> 	- **Type**: 🐛 Bug Fix | ✨ New Feature
> 	- **Changes**: Brief technical description
> 	- **Decisions**: Architectural/security choices
> 	- **Gotchas**: "Beware of X when modifying Y"
> 	- **Learnings**: "Discovered Z about framework"
