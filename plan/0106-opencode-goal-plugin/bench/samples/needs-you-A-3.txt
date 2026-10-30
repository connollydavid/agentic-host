

**ACTION:** host-lifecycle goal repair

**CONTEXT:** Following reconciliation of receipt vs. missing status line (plan/0001-smoke).

**OBJECTIVE:** Restore host lifecycle integrity and ensure goal closure.

**EXECUTION PLAN:**

1.  **Verify Host State:** Check current host status endpoint to confirm the missing status line.
2.  **Inject Missing Data:** Update the status line with the correct lifecycle state based on the landed receipt.
3.  **Update Lifecycle Goal:** Re-sync the goal status from `INCOMPLETE` to `REPAIRED`.
4.  **Validate Closure:** Confirm that the receipt and status line now match for a complete closure.
5.  **Log Completion:** Record the repair action in the `plan/0001-smoke` log.

**STATUS:** READY TO EXECUTE.