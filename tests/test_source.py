import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
from source import wait_value,timestamp
class SourceTests(unittest.TestCase):
 def test_no_delay_is_censored_not_exact_zero(self):self.assertEqual(wait_value('No Delay')['upper'],5);self.assertIsNone(wait_value('Closed')['lower'])
 def test_source_zone_keeps_repeated_fall_hour_distinct(self):self.assertNotEqual(timestamp('2019-11-03 01:00 PDT')['reported_at'],timestamp('2019-11-03 01:00 PST')['reported_at'])
 def test_unknown_wait_category_fails(self):
  with self.assertRaises(ValueError):wait_value('no one knows')
