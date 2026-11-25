import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from source import wait_value,timestamp
class SourceTests(unittest.TestCase):
 def test_no_delay_is_censored_not_exact_zero(self):self.assertEqual(wait_value('No Delay')['upper'],5);self.assertIsNone(wait_value('Closed')['lower'])
 def test_source_zone_keeps_repeated_fall_hour_distinct(self):self.assertNotEqual(timestamp('2019-11-03 01:00 PDT')['reported_at'],timestamp('2019-11-03 01:00 PST')['reported_at'])
 def test_unknown_wait_category_fails(self):
  with self.assertRaises(ValueError):wait_value('no one knows')
 def test_hour_and_minute_waits_are_converted_without_losing_source_text(self):
  for raw,minutes in [('1 hour, 5 minutes',65),('2 hours, 1 minute',121),('1 hour',60),('2 hours 30 minutes',150),(' 1 HOUR,  5 MINUTES ',65),('24 hours',1440),('15 minutes',15),('0',0)]:
   with self.subTest(raw=raw):
    self.assertEqual(wait_value(raw),{'status':'numeric','lower':minutes,'upper':minutes,'raw':raw})
 def test_invalid_or_excessive_waits_still_fail(self):
  for raw in ['1 hour, 60 minutes','24 hours, 1 minute','25 hours','1441 minutes','-1 hour','1.5 hours','1 hour,','1 hour and a bit']:
   with self.subTest(raw=raw),self.assertRaises(ValueError):wait_value(raw)

class CurrentFeedTests(unittest.TestCase):
 def feed(self, names):
  header='Customs Office;; Location;; Last updated;; Commercial Flow - Canada bound;; Commercial Flow - U.S. bound;; Travellers Flow - Canada bound;; Travellers Flow - U.S. bound;;'
  return header+'\n'+'\n'.join(n+';; BC/WA;; 2026-11-24 03:00 PDT;; No Delay;; --;; No Delay;; --;;' for n in names+['Other '+str(i) for i in range(20)])
 def test_missing_crossing_does_not_invent_report_or_drop_other_reports(self):
  from source import parse_current
  rows,missing=parse_current(self.feed(['Douglas','Pacific Highway','Abbotsford-Huntingdon']))
  self.assertEqual(len(rows),23);self.assertEqual(missing,['aldergrove'])
 def test_current_feed_accepts_hour_waits_for_both_traffic_types(self):
  from source import parse_current
  text=self.feed(['Douglas']).replace('No Delay;; --;; No Delay','1 hour, 5 minutes;; --;; 2 hours, 10 minutes')
  rows,_=parse_current(text)
  self.assertEqual(rows[0]['commercial']['lower'],65)
  self.assertEqual(rows[0]['travellers']['lower'],130)
 def test_duplicate_crossing_or_wrong_header_fails(self):
  from source import parse_current
  for text in (self.feed(['Douglas','Douglas']),self.feed(['Douglas']).replace('Customs Office','Changed header')):
   with self.assertRaises(ValueError):parse_current(text)
 def test_empty_or_truncated_feed_fails(self):
  from source import parse_current
  for text in ('',self.feed(['Douglas']).splitlines()[0]+'\nDouglas;; BC/WA'):
   with self.assertRaises(ValueError):parse_current(text)

class NationalTests(unittest.TestCase):
 def test_real_national_source_and_added_crossing(self):
  from source import parse_current
  raw=(Path(__file__).parent/'fixtures/current-national.csv').read_text(encoding='utf-8-sig')
  rows,_=parse_current(raw)
  self.assertGreaterEqual(len(rows),20)
  self.assertEqual({r['province'] for r in rows},{'NB','QC','ON','MB','SK','AB','BC'})
  rows,_=parse_current(raw+'Future Crossing;; Town, NB/State, ME;; 2026-11-25 03:00 AST;; Closed;; --;; 12 minutes;; --;;\n')
  self.assertEqual(rows[-1]['crossing'],'future-crossing')
  self.assertEqual(rows[-1]['travellers']['lower'],12)
 def test_national_source_offsets(self):
  self.assertEqual(timestamp('2026-11-25 02:00 AST')['reported_at'],'2026-11-25T06:00:00Z')
  self.assertEqual(timestamp('2026-11-25 02:00 NST')['reported_at'],'2026-11-25T05:30:00Z')
