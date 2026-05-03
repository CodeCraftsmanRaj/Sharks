const output = document.getElementById('output');

function show(data) {
  output.textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
}

async function callApi(path, payload = null, method = 'POST') {
  const options = { method, headers: { 'Content-Type': 'application/json' } };
  if (payload) options.body = JSON.stringify(payload);
  const res = await fetch(path, options);
  const json = await res.json();
  if (!res.ok) throw new Error(JSON.stringify(json));
  return json;
}

function formToPayload(form) {
  const data = new FormData(form);
  const payload = {};
  for (const [k, v] of data.entries()) {
    if (v === '') continue;
    const asNum = Number(v);
    payload[k] = Number.isFinite(asNum) && v.trim() !== '' && !isNaN(asNum) && /^(marks|budget|work_experience|family_income|tuition_cost|living_cost_per_year|duration_years)$/.test(k)
      ? asNum
      : v;
  }
  return payload;
}

document.getElementById('healthBtn').addEventListener('click', async () => {
  try {
    show(await callApi('/health', null, 'GET'));
  } catch (e) {
    show(e.message);
  }
});

[
  ['profileForm', '/api/profile'],
  ['mentorForm', '/api/mentor'],
  ['roiForm', '/api/roi'],
  ['loanForm', '/api/loan-eligibility'],
  ['waSendForm', '/api/whatsapp/send'],
  ['docForm', '/api/documents/process'],
].forEach(([id, path]) => {
  document.getElementById(id).addEventListener('submit', async (e) => {
    e.preventDefault();
    try {
      const payload = formToPayload(e.target);
      show(await callApi(path, payload));
    } catch (err) {
      show(err.message);
    }
  });
});
