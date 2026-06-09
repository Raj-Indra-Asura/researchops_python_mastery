# Reflection - Week 04 CLI and Packaging

## End-of-Month-1 reflection prompts

### Looking back at the whole month
- Four weeks ago, what could you not build yet that you can build now?
- Which Month 1 idea felt most abstract at first but now feels concrete?
- Where do you notice the biggest difference between "writing Python" and "shipping software"?
- What part of Month 1 gave you the strongest sense that ResearchOps is becoming a real product?
- Which Week 1, 2, or 3 concept did Week 4 finally make click for you?

### The full Month 1 project in your own words
- Explain ResearchOps as if you were describing it to a new teammate on day one.
- What does the current `researchops scan` command do from input to output?
- What code path does the command follow from the shell to `find_pdfs()` to terminal output?
- Which parts of the project belong to interface, logic, and packaging?
- What does the user experience look like when the directory is valid, empty, or missing?

### What Week 4 taught you specifically
- What is a CLI, in your own words?
- Why is Typer a good fit for this stage of the course?
- What is the difference between `typer.Argument(...)` and `typer.Option(...)`?
- Why does `--verbose` belong in the callback rather than a single command?
- Why is `app.add_typer()` important even before every subcommand group is fully implemented?
- Why are exit codes part of the product contract, not a minor implementation detail?
- Why does a well-packaged command feel different from running a loose script?

### Thin-handler reflection
- Where does the current CLI stay thin?
- Where would it be tempting to put too much logic into `cli/main.py`?
- Why would that temptation become a problem later?
- How would shared services help both the CLI and a future API?
- What would break first if every command owned its own business logic?

### Packaging reflection
- What does `researchops = "researchops.cli.main:app"` mean, piece by piece?
- What confused you most about entry points at first?
- What did you learn about reinstalling after metadata changes?
- Why are optional dependency groups useful in a growing project like ResearchOps?
- Which optional groups make the architecture feel modular to you?

### Testing reflection
- What do `result.output` and `result.exit_code` each tell you?
- Which CLI test in `tests/e2e/test_cli.py` feels most important, and why?
- What kinds of CLI behaviors are easy to test with `CliRunner`?
- What kinds of things would still need deeper integration testing later?
- How has your idea of "testing" changed across Month 1?

### Failure and debugging reflection
- Which failure in the break-it lab taught you the most?
- Which bug felt like a packaging bug rather than a Python bug?
- Which bug proved that visible output and exit codes are different concerns?
- Which bug taught you to be more careful with broad exception handling?
- Which debugging habit do you want to carry into Month 2?

### Confidence and readiness
- What part of Week 4 feels solid enough that you could teach it?
- What part still feels shaky and needs another pass through the notes?
- What command-line concepts now feel natural?
- What packaging concepts still feel mechanical rather than intuitive?
- On a scale from 1-10, how confident are you that you could add one more command on your own?
- What would raise that confidence score by two points?

### Month 2 bridge
- What feels ready for Month 2?
- Which habits from Month 1 do you want to keep unchanged?
- Which habits do you want to improve before the project grows more complex?
- How do you expect SQLite, persistence, and application services to change the CLI design?
- Why is it useful that Month 1 ends with a tested, installable interface before adding more infrastructure?

### Final synthesis prompts
- In 8-12 sentences, summarize how Month 1 transformed ResearchOps from a scaffold into a usable tool.
- In 5-8 sentences, explain why CLI design, packaging, and testing belong in the same chapter.
- In 5-8 sentences, explain what you can now build that you could not build at the start of the month.
- In 5-8 sentences, explain what you feel most ready to tackle next.
