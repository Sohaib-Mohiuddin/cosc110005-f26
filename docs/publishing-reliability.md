# Publishing reliability

## Observed failure

Week 9 was tracked on main. The [first run](https://github.com/Sohaib-Mohiuddin/cosc110005-f26/actions/runs/42672690839) passed all Python and browser checks and uploaded its artifact, but never created the deployment job. The [next run](https://github.com/Sohaib-Mohiuddin/cosc110005-f26/actions/runs/42673825739) created no jobs. Both report a workflow-level GitHub internal server error. Retrying failed jobs was rejected because the latter run had no re-runnable jobs.

The existing week discovery and release-aware checks correctly included week 9. This incident required recovery from publishing infrastructure failure, rather than another numbered-week exception.

## Delivery slices

1. Add current-commit metadata and verify the live inventory and latest-week links after deployment.
2. Add a recovery workflow triggered by completed publication runs, a periodic schedule, or manual dispatch. Only trusted main runs can influence its decision; active work and newer commits take priority.
3. Bound retries, retain all validation gates, and verify the failure cases with isolated API fixtures. Infrastructure errors can recover after an hourly cooldown; repeatedly failing source validation requires a fix.
4. Publish the implementation to main, observe Actions, and verify the actual week 9 page, downloads, and helper-module Python execution in the live site.

The source records implementation and local checks before publication. The delivery response records the final workflow and live-check results. No untracked classroom files are released by this change.

## Local gate evidence

All 36 Python checks and all three Chromium browser suites pass. Recovery fixtures cover jobless failures, missing deployment jobs, hourly retry limits, repeated validation failures, active/healthy runs, untrusted or old heads, and main advancing during recovery. Live-verification fixtures check the commit, exact material inventory, newest-week navigation, and project-relative filenames. Both workflow files parse successfully. A read-only evaluation against the actual jobless week 9 run correctly requests recovery.

The recovery workflow subsequently dispatched a replacement publication automatically. CI also exposed a resize-focus timing failure: the browser could clear focus after its media event, losing the remembered navigation owner. Focus is now retained until it moves to another control or the user clicks into page content; handoff can wait one layout frame. Navigation checks cover ordinary pointer blur as well as resize recovery and print focused-control diagnostics on failure.
