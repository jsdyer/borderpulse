from common import ROOT,save,now
import source,json,argparse

def normalize(r,series):
 r=dict(r);r['series']=series;r['crossing_name']=r.get('crossing_name',source.LABELS.get(r['crossing'],r['crossing']))
 if series=='Current report':
  r.update(r.pop('travellers'));commercial=r['commercial'];r['commercial_wait']=commercial['raw'];r['source_url']=source.URLS['current.csv']
 if series=='Monthly service standard':
  r['id']='monthly:'+r['crossing']+':'+r['month'];r['local_time']=r['month'];r['status']='monthly percentage';r['wait']=str(r['service_standard_met_percent'])+'% within service standard';return r
 r['id']=series+':'+r['crossing']+':'+r['reported_at'];r['wait']='Not measurable' if r.get('lower') is None else str(r['lower'])+'–'+str(r['upper'])+' min' if r['lower']!=r['upper'] else str(r['lower'])+' min'
 return r

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--seed',action='store_true');parser.add_argument('--refresh-history',action='store_true');a=parser.parse_args()
 folder=ROOT/'data';folder.mkdir(exist_ok=True)
 if a.refresh_history or not (folder/'baseline.json').exists():
  if not a.seed:
   for file in ['current.csv','history.csv','border-2019q4.csv','border-reference.odt','changelog.txt']:source.get(file)
  data=source.border()
  static=[normalize(r,'2019 Q4 hourly archive') for r in data['observations']]+[normalize(r,'Monthly service standard') for r in data['monthly']]
  baseline={'records':static,'diagnostics':data['diagnostics'],'heatmap':data['heatmap'],'historical_period':data['historical_period']}
 else:
  if not a.seed:source.get('current.csv')
  current,missing=source.parse_current((source.ROOT/'current.csv').read_text(encoding='utf-8-sig'))
  previous=json.loads((folder/'current.json').read_text()) if (folder/'current.json').exists() else {}
  sources=[s for s in previous.get('sources',[]) if s['url']!=source.URLS['current.csv']]
  data={'current':current,'missing_current':missing,'sources':sources+[{'url':source.URLS['current.csv'],'sha256':source.sha('current.csv')}]}
  baseline=None
 rows=[normalize(r,'Current report') for r in data['current']]
 missing=data['missing_current']
 # Retained historical labels are not evidence of a current report.
 previous=json.loads((folder/'current.json').read_text()) if (folder/'current.json').exists() else {}
 absent={r['crossing']:r['crossing_name'] for r in previous.get('records',[]) if r['crossing'] not in {x['crossing'] for x in rows}}
 warnings=['The 2019 historical sample covers four BC crossings; it does not predict today’s quietest hour.','No delay is a 0–5 minute interval. Closed, missing and conflicting reports are excluded from wait statistics.','Source timezone labels are preserved exactly. An unusual seasonal label is not silently corrected.']
 missing_names=sorted(set(absent.values())|{source.LABELS[k] for k in missing})
 if missing_names:warnings.append('No current CBSA report for: '+', '.join(missing_names)+'. Historical records retain their dates; no current wait is inferred.')
 if baseline:(folder/'baseline.json').write_text(json.dumps(baseline,separators=(',',':'))+'\n')
 historypath=folder/'observations.json';history=json.loads(historypath.read_text()) if historypath.exists() else []
 known={r['id']:r for r in history}
 for r in rows:known[r['id']]={**r,'first_seen':known.get(r['id'],{}).get('first_seen',now())}
 historypath.write_text(json.dumps(sorted(known.values(),key=lambda r:r['reported_at']),separators=(',',':'))+'\n')
 save(rows,sources=data['sources'],coverage=f"{len(rows)} Canada-bound crossings in the current national CBSA feed · four BC crossings in the retained historical baseline · source timestamps shown per crossing",warnings=warnings,extra={'missing_current':missing,'baseline_file':'./data/baseline.json','observations_file':'./data/observations.json'})
if __name__=='__main__':main()
