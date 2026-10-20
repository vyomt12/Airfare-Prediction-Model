const $ = id => document.getElementById(id);
const form = $('fare-form');
let data;
const names = {ATL:'Atlanta',LAX:'Los Angeles',JFK:'New York JFK',LGA:'New York LaGuardia',EWR:'Newark',ORD:'Chicago O’Hare',MDW:'Chicago Midway',SFO:'San Francisco',SEA:'Seattle',BOS:'Boston',MIA:'Miami',DFW:'Dallas / Fort Worth',DAL:'Dallas Love Field',DEN:'Denver',LAS:'Las Vegas',PHX:'Phoenix',IAD:'Washington Dulles',DCA:'Washington Reagan',BWI:'Baltimore',MCO:'Orlando',TPA:'Tampa',SAN:'San Diego',SJC:'San Jose',OAK:'Oakland',PDX:'Portland',PHL:'Philadelphia',DTW:'Detroit',MSP:'Minneapolis',IAH:'Houston Intercontinental',HOU:'Houston Hobby',CLT:'Charlotte',AUS:'Austin',BNA:'Nashville',SLC:'Salt Lake City',FLL:'Fort Lauderdale',ABQ:'Albuquerque'};
const currency = value => new Intl.NumberFormat('en-US',{style:'currency',currency:'USD',maximumFractionDigits:2}).format(value);
function option(code) {
  const el = document.createElement('option'); el.value = code;
  el.textContent = names[code] ? `${code} · ${names[code]}` : code;
  return el;
}
function updateDestinations(preferred = $('destination').value) {
  const destinations = data.routes[$('origin').value] || [];
  $('destination').replaceChildren(...destinations.map(option));
  if (destinations.includes(preferred)) $('destination').value = preferred;
}
function markPending() {
  $('fare-amount').textContent = '—';
  $('record-count').textContent = '—';
  $('training-period').textContent = '—';
  $('result-description').textContent = 'Select “Estimate average fare” to update your result.';
  $('result-origin').textContent = $('origin').value;
  $('result-destination').textContent = $('destination').value;
  $('result-quarter').textContent = `Q${new FormData(form).get('quarter')} · ${$('year').value}`;
  $('form-error').hidden = true;
}
$('origin').addEventListener('change', () => { if (data) updateDestinations(); });
form.addEventListener('input', markPending);
form.addEventListener('change', markPending);
$('swap').addEventListener('click', () => {
  if (!data) return;
  const origin = $('origin').value, destination = $('destination').value;
  if (!(data.routes[destination] || []).includes(origin)) {
    $('form-error').textContent = 'The dataset stores this airport pair in one order. Your current selection already uses that order.';
    $('form-error').hidden = false;
    return;
  }
  $('origin').value = destination; updateDestinations(origin); markPending();
});
function setBusy(busy) {
  for(const element of form.elements)element.disabled=busy;
  $('estimate-button').textContent=busy?'Calculating in Python…':'Estimate average fare ↗';
  $('result').setAttribute('aria-busy',String(busy));
}
async function showEstimate() {
  if (!data) return;
  const route={origin:$('origin').value,destination:$('destination').value,year:Number($('year').value),quarter:Number(new FormData(form).get('quarter'))};
  const controller=new AbortController();
  const timeout=setTimeout(()=>controller.abort(),30000);
  setBusy(true); $('form-error').hidden=true;
  try {
    const response=await fetch('/api/predict',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(route),signal:controller.signal});
    const result=await response.json();
    if(!response.ok)throw new Error(result.error || 'Unable to calculate a fare. Try again.');
    $('result-origin').textContent=route.origin;
    $('result-destination').textContent=route.destination;
    $('result-quarter').textContent=`Q${route.quarter} · ${route.year}`;
    $('fare-amount').textContent=currency(result.estimate);
    $('result-description').textContent=`Calculated by your original Python model using matching Q${route.quarter} records.`;
    $('record-count').textContent=result.count;
    const years=result.history.map(([year])=>year);
    $('training-period').textContent=`${Math.min(...years)}–${Math.max(...years)}`;
  } catch(error) {
    markPending();
    $('form-error').textContent=error.name==='AbortError'?'The prediction took too long. Please try again.':error.message;
    $('form-error').hidden=false;
    $('result-description').textContent='No estimate available for this selection.';
  } finally {
    clearTimeout(timeout); setBusy(false);
  }
}
form.addEventListener('submit',event=>{event.preventDefault();showEstimate();});
try {
  const response=await fetch('/api/routes');
  if (!response.ok)throw new Error('Unable to load routes.');
  data=await response.json();
  const origins=Object.keys(data.routes).sort();
  $('origin').replaceChildren(...origins.map(option));
  $('origin').value=origins.includes('ATL')?'ATL':origins[0];updateDestinations('LAX');
  $('dataset-footer').textContent=`${data.records.toLocaleString()} records · ${data.minYear}–${data.maxYear}`;
  $('estimate-button').disabled=false;
  await showEstimate();
} catch(error) {
  $('form-error').textContent='Unable to connect to the Python server. Please reload the page.';
  $('form-error').hidden=false;
  $('result-description').textContent='The server is unavailable. Please try again.';
  $('estimate-button').textContent='Server unavailable'; $('estimate-button').disabled=true;
}
