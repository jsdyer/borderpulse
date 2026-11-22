# Border Pulse

Canada-bound waits, kept in context. Compare reported crossing conditions, older hourly patterns and monthly service-standard results.

Open https://coolcode.ca/borderpulse/

<!-- coolcode:guide -->
Choose a crossing and distinguish current reports, the 2019 Q4 hourly sample and newer monthly service-standard percentages. No delay means up to five minutes; missing and conflicting observations are excluded from wait statistics.
<!-- /coolcode:guide -->

## Sources and interpretation

All CBSA measurements here describe traffic entering Canada. Peace Arch is called Douglas in the feed; Sumas is Abbotsford-Huntingdon. U.S.-bound conditions are not mixed into these figures.

The archived timestamped sample covers October–December 2019. It can describe that historical period, not predict today’s quietest hour. The newer April 2019–October 2025 file contains monthly service-standard percentages, not minute waits.

The official dictionary defines No delay as five minutes or less. Its interval is preserved as 0–5 minutes; medians and 90th percentiles have lower/upper bounds. Closed, missing and conflicting duplicate reports are excluded rather than treated as zero.

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
