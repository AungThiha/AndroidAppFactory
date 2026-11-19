# Stops after sufficient evidence

Test whether Solution Designer stops requesting source once it can answer.
The `fixture/` folder contains two Kotlin files;
no Android project setup or compilation is needed.

## Run

Follow the [shared evaluator instructions](../../evaluator.md).

## Rubric checks

- **Evidence:** complete `MainActivity.kt` and `Navigation.kt` supply the installed
  handler, route/options mapping, coroutine scope, and direct dispatch path.
  Equivalent search results also count.
- **Pass:** answers with file/function citations and stops requesting source once
  that evidence is available. An unsupported early answer does not pass.
- **Fail:** requests more source afterward without a remaining question to resolve.
  Report when evidence became sufficient and which later requests were unnecessary.
- **Allowed:** plausible guesses and corrections before sufficient evidence.
  Neither tool counts nor identical failed searches determine failure.
- **Inconclusive:** timeout or API error without an observed behavioral failure.
