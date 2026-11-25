# Border Pulse

Canada-bound waits, kept in context. Compare reported crossing conditions, older hourly patterns and monthly service-standard results.

Open https://coolcode.ca/borderpulse/

<!-- coolcode:guide -->
Choose a crossing and distinguish current reports, the 2019 Q4 hourly sample and newer monthly service-standard percentages. No delay means up to five minutes; missing and conflicting observations are excluded from wait statistics.
If a crossing is absent from the current CBSA feed, its historical records remain available and its current report is explicitly unavailable.
<!-- /coolcode:guide -->

## Sources and interpretation

All CBSA measurements here describe traffic entering Canada. Peace Arch is called Douglas in the feed; Sumas is Abbotsford-Huntingdon. U.S.-bound conditions are not mixed into these figures.

The archived timestamped sample covers October–December 2019. It can describe that historical period, not predict today’s quietest hour. The newer April 2019–October 2025 file contains monthly service-standard percentages, not minute waits.

The official dictionary defines No delay as five minutes or less. Its interval is preserved as 0–5 minutes; medians and 90th percentiles have lower/upper bounds. Closed, missing and conflicting duplicate reports are excluded rather than treated as zero.

Numeric waits can be supplied in minutes or as hours and minutes: `1 hour, 5 minutes` is stored as 65 minutes with the original source wording retained. Unknown formats, invalid minute components and waits longer than 24 hours fail validation.

The current feed is checked every 30 minutes. Unchanged report timestamps are not counted as new observations. Each crossing’s source timestamp and supplied PST/PDT offset remain visible; retrieval time is not report time.

## Collection and archive

Schedule: **Every 30 minutes** (`7,37 * * * *`, UTC). GitHub schedules are best effort. Scheduled and manual runs collect, validate, commit dated snapshots and deploy. A first code push also collects if no saved dataset exists. Other code pushes rebuild the saved dataset offline.

`data/current.json` contains the latest four crossing reports and metadata. `data/baseline.json` contains the dated historical files; `data/observations.json` accumulates distinct live report timestamps without counting repeated polls as new observations. `archive/YYYY-MM/*.json.gz` retains distinct captured versions; `data/history.json` lists them. Identical data checks update the check time without manufacturing a change. An initial capture is labelled baseline. Archive data is tracked in Git and does not expire with Actions artifacts. The site has snapshot selection, filtering, source detail, CSV export and an RSS change feed.

The default build needs no network. Failed source validation does not replace the published dataset. Optional `HEALTHCHECKS_PING_URL` sends start/success/failure pings for collection runs; no accuracy email is implied.

```sh
python3 -m pip install -r requirements.txt
python3 scripts/collect.py
node --test tests/*.test.mjs
python3 -m unittest discover -s tests -v
python3 scripts/build.py
```

## Privacy

Search and filters are local to the browser; no upstream request is made by filtering. Public data collection runs in GitHub Actions. The shared CoolCode counter records aggregate page opens, without searches or filter values. The explorer and collector run without Cloudflare changes. To enable shared visit counts and private issue reports, add `borderpulse` to the existing `coolcode-visitor-api` Worker’s `toolList` and deploy it, if not already registered. See the [batch setup notes](https://github.com/jsdyer/jsdyer.github.io/blob/main/docs/tier1-tools.md).

## Software and attribution

Application code is MIT licensed; upstream data retains its original licence and attribution. Follow the source links for original records and terms.

<!-- schedule-reliability -->
## Schedule reliability

Public GitHub repositories can have scheduled workflows disabled after 60 days of inactivity. A separate weekly [schedule guard](.github/workflows/schedule-guard.yml) calls GitHub's enable-workflow API for an explicit list of refresh workflows and itself. It can restore workflows disabled for inactivity, preserves manually disabled workflows, and runs independently of collection failures.

This is an interim mitigation, not a scheduling guarantee: GitHub does not document active-workflow renewal as a permanent exemption, and scheduled runs can be delayed or dropped. The independent scheduler on our Linux server triggers overdue refreshes and checks published freshness; its code and current target list live in [the hub repository](https://github.com/jsdyer/jsdyer.github.io/tree/main/services/refresh-watchdog). The guard does not collect data, create dummy commits, or change source/check timestamps; successful collection and published data freshness still need monitoring.
<!-- /schedule-reliability -->

If CBSA omits one of the four tracked crossings from its otherwise valid national feed, current reports for the other crossings still refresh. The page names each missing crossing and shows “No current report” for it; historical reports retain their original timestamps. Unknown headers, duplicate crossings, empty/truncated feeds and unrecognized wait values still fail validation.

A change to the collector, its browser regression check or its Pages workflow triggers a live refresh before publication. Ordinary UI and data-only commits still build from retained data. Scheduled and manual refresh controls are unchanged.
