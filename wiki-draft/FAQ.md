## Will steerwright change a project's status by itself?

No. Status changes come from your answers on a review page or from a command you run. A review's suggested answer is a low-confidence guess, and an unanswered question stays unanswered.

## Does it edit askwright, chainwright or grindwright files?

No. It only reads them.

## My project has no grindwright ledger. Do the charts still work?

Partly. Without a ledger the project page uses git commits and log entries as a stand-in. That chart shows activity, not scope. Add items with `sw.py item` to give it scope.

## Why is the forecast a range?

It is a Monte Carlo run over past weekly throughput, so it gives 50, 85 and 95 % dates. One date would hide the uncertainty.

## Can other machines reach the pages?

No. They bind 127.0.0.1.

## How do I move the registry?

Set `STEERWRIGHT_HOME` to another folder.

## Does the weekly review run on a schedule?

No. Run `sw.py review NAME` when you want one.
