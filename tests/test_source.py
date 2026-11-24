import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from source import wait_value,timestamp
class SourceTests(unittest.TestCase):
 def test_no_delay_is_censored_not_exact_zero(self):self.assertEqual(wait_value('No Delay')['upper'],5);self.assertIsNone(wait_value('Closed')['lower'])
 def test_source_zone_keeps_repeated_fall_hour_distinct(self):self.assertNotEqual(timestamp('2019-11-03 01:00 PDT')['reported_at'],timestamp('2019-11-03 01:00 PST')['reported_at'])
 def test_unknown_wait_category_fails(self):
  with self.assertRaises(ValueError):wait_value('no one knows')

class CurrentFeedTests(unittest.TestCase):
 def feed(self, names):
  header='Customs Office;; Location;; Last updated;; Commercial Flow - Canada bound;; Commercial Flow - U.S. bound;; Travellers Flow - Canada bound;; Travellers Flow - U.S. bound;;'
  return header+'\n'+'\n'.join(n+';; BC/WA;; 2026-11-24 03:00 PDT;; No Delay;; --;; No Delay;; --;;' for n in names+['Other '+str(i) for i in range(20)])
 def test_missing_crossing_does_not_invent_report_or_drop_other_reports(self):
  from source import parse_current
  rows,missing=parse_current(self.feed(['Douglas','Pacific Highway','Abbotsford-Huntingdon']))
  self.assertEqual(len(rows),3);self.assertEqual(missing,['aldergrove'])
 def test_duplicate_crossing_or_wrong_header_fails(self):
  from source import parse_current
  for text in (self.feed(['Douglas','Douglas']),self.feed(['Douglas']).replace('Customs Office','Changed header')):
   with self.assertRaises(ValueError):parse_current(text)
 def test_empty_or_truncated_feed_fails(self):
  from source import parse_current
  for text in ('',self.feed(['Douglas']).splitlines()[0]+'\nDouglas;; BC/WA'):
   with self.assertRaises(ValueError):parse_current(text)
