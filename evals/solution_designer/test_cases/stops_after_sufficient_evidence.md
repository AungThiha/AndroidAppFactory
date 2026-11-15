# Stops after sufficient evidence

Test whether Solution Designer stops requesting source once it can answer.
The sibling `stops_after_sufficient_evidence/` folder contains two Kotlin files;
no Android project setup or compilation is needed.

## Prompt

```text
In this fixture, MainActivity installs a NavigationHandler through navigationDispatcher.setHandler(...). Find the onNavigation implementation used by that handler. Explain how it handles the destination and NavigationOptions, which coroutine or lifecycle scope it uses, and how it calls NavController. Distinguish direct calls from any queued or streamed events you actually find. Cite relevant files and functions. Stop before destination rendering and make unresolved questions explicit.
```

## Run

Follow `evals/README.md`. Run the current `solution_designer.py` with the prompt
above and its existing model, system message, and tools. Observe its console tool
requests and results. Stop an individual run after two minutes. Leave production
code unchanged.

## Rubric checks

- **Evidence:** both complete files supply the installed handler, destination,
  options mapping, coroutine scope, and direct dispatch path. Equivalent search
  results also count.
- **Pass:** answers with file/function citations and stops requesting source once
  that evidence is available. An unsupported early answer does not pass.
- **Fail:** requests more source afterward without a remaining question to resolve.
  Report when evidence became sufficient and which later requests were unnecessary.
- **Allowed:** plausible guesses and corrections before sufficient evidence.
  Neither tool counts nor identical failed searches determine failure.
- **Inconclusive:** timeout or API error without an observed behavioral failure.
