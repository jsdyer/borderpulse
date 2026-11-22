from common import ROOT,save,now
import source,json,argparse

def normalize(r,series):
 r=dict(r);r['series']=series;r['crossing_name']=source.LABELS[r['crossing']]
 if series=='Current report':r.update(r.pop('travellers'));r.pop('commercial',None)
 if series=='Monthly service standard':
  r['id']='monthly:'+r['crossing']+':'+r['month'];r['local_time']=r['month'];r['status']='monthly percentage';r['wait']=str(r['service_standard_met_percent'])+'% within service standard';return r
 r['id']=series+':'+r['crossing']+':'+r['reported_at'];r['wait']='Not measurable' if r.get('lower') is None else str(r['lower'])+'–'+str(r['upper'])+' min' if r['lower']!=r['upper'] else str(r['lower'])+' min'
 return r

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--seed',action='store_true');a=parser.parse_args()
 if not a.seed:
  for file in ['current.csv','history.csv','border-2019q4.csv','border-reference.odt','changelog.txt']:source.get(file)
 data=source.border();rows=[normalize(r,'Current report') for r in data['current']]
 if len(rows)!=4:raise ValueError('Expected all four crossing entries')
 static=[normalize(r,'2019 Q4 hourly archive') for r in data['observations']]+[normalize(r,'Monthly service standard') for r in data['monthly']]
 folder=ROOT/'data';folder.mkdir(exist_ok=True)
 baseline={'records':static,'diagnostics':data['diagnostics'],'heatmap':data['heatmap'],'historical_period':data['historical_period']}
 (folder/'baseline.json').write_text(json.dumps(baseline,separators=(',',':'))+'\n')
 historypath=folder/'observations.json';history=json.loads(historypath.read_text()) if historypath.exists() else []
 known={r['id']:r for r in history}
 for r in rows:known[r['id']]={**r,'first_seen':known.get(r['id'],{}).get('first_seen',now())}
 historypath.write_text(json.dumps(sorted(known.values(),key=lambda r:r['reported_at']),separators=(',',':'))+'\n')
 save(rows,sources=data['sources'],coverage='Four Canada-bound crossings · hourly historical sample Oct–Dec 2019 · monthly performance Apr 2019–Oct 2025 · current source timestamps shown per crossing',warnings=['The heatmap uses a 2019 historical sample; it does not predict today’s quietest hour.','No delay is a 0–5 minute interval. Closed, missing and conflicting reports are excluded from wait statistics.'],extra={'baseline_file':'./data/baseline.json','observations_file':'./data/observations.json'})
if __name__=='__main__':main()
