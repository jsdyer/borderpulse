export default {
  "title": "Border Pulse",
  "intro": "Canada-bound waits, kept in context. Compare reported crossing conditions, older hourly patterns and monthly service-standard results.",
  "eyebrow": "LOWER MAINLAND CROSSINGS / CANADA-BOUND",
  "accent": "#356959",
  "tint": "#e2efe7",
  "method": [
    "All CBSA measurements here describe traffic entering Canada. Peace Arch is called Douglas in the feed; Sumas is Abbotsford-Huntingdon. U.S.-bound conditions are not mixed into these figures.",
    "The archived timestamped sample covers October–December 2019. It can describe that historical period, not predict today’s quietest hour. The newer April 2019–October 2025 file contains monthly service-standard percentages, not minute waits.",
    "The official dictionary defines No delay as five minutes or less. Its interval is preserved as 0–5 minutes; medians and 90th percentiles have lower/upper bounds. Closed, missing and conflicting duplicate reports are excluded rather than treated as zero.",
    "The current feed is checked every 30 minutes. Unchanged report timestamps are not counted as new observations. Each crossing’s source timestamp and supplied PST/PDT offset remain visible; retrieval time is not report time."
  ],
  "id": "borderpulse",
  "explorer-title": "Follow the record.",
  "cadence": "Every 30 minutes automated collection. Source dates and capture dates are shown separately.",
  "facets": [
    {
      "key": "crossing_name",
      "label": "Crossing"
    },
    {
      "key": "series",
      "label": "Series"
    },
    {
      "key": "status",
      "label": "Report status"
    }
  ],
  "columns": [
    {
      "key": "crossing_name",
      "label": "Crossing"
    },
    {
      "key": "local_time",
      "label": "Source-local time"
    },
    {
      "key": "series",
      "label": "Series"
    },
    {
      "key": "wait",
      "label": "Traveller wait / result"
    },
    {
      "key": "status",
      "label": "Status"
    },
    {
      "key": "reported_at",
      "label": "Reported (UTC)"
    }
  ],
  "related": [
    {
      "label": "Transit Receipt",
      "url": "https://coolcode.ca/transitreceipt/"
    },
    {
      "label": "Tide Receipt",
      "url": "https://coolcode.ca/tidereceipt/"
    }
  ],
  "defaults": {
    "crossing_name": "Peace Arch (Douglas)",
    "series": "Current report"
  }
};
