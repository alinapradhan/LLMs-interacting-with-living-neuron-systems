const waveCanvas = document.getElementById('waveCanvas');
const ctx = waveCanvas.getContext('2d');
const eegTrail = [];
const maxTrail = 220;
let autoTimer = null;

async function callApi(path, method = 'GET', body = null) {
  const res = await fetch(path, {
    method,
    headers: { 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : null,
  });
  return res.json();
}

function drawWave() {
  ctx.clearRect(0, 0, waveCanvas.width, waveCanvas.height);
  ctx.strokeStyle = '#2be6c9';
  ctx.lineWidth = 2;
  ctx.beginPath();

  eegTrail.forEach((v, i) => {
    const x = (i / (maxTrail - 1)) * waveCanvas.width;
    const y = waveCanvas.height / 2 - v * 36;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });

  ctx.stroke();
}

function pretty(obj) {
  if (!obj) return 'n/a';
  return `<pre>${JSON.stringify(obj, null, 2)}</pre>`;
}

function populateStates(states, current) {
  const select = document.getElementById('brainStateSelect');
  if (select.options.length) return;
  states.forEach((state) => {
    const opt = document.createElement('option');
    opt.value = state;
    opt.textContent = state;
    if (state === current) opt.selected = true;
    select.appendChild(opt);
  });
}

async function refresh() {
  const data = await callApi('/api/state');

  populateStates(data.available_states, data.neural_frame?.mental_state);
  document.getElementById('runningStatus').textContent = data.running ? 'Running' : 'Paused/Stopped';

  if (data.neural_frame?.eeg !== undefined) {
    eegTrail.push(data.neural_frame.eeg);
    if (eegTrail.length > maxTrail) eegTrail.shift();
  }

  drawWave();

  document.getElementById('signalMeta').innerHTML = `
    state=<b>${data.neural_frame?.mental_state || 'n/a'}</b>,
    firing_rate=<b>${data.neural_frame?.firing_rate_hz || 'n/a'} Hz</b>,
    burst=<b>${data.neural_frame?.burst || false}</b>
  `;

  document.getElementById('decoded').innerHTML = pretty(data.decoded);
  document.getElementById('aiThoughts').innerHTML = pretty(data.ai_output);
  document.getElementById('encoded').innerHTML = pretty(data.encoded_output);
  document.getElementById('memory').innerHTML = pretty(data.memory);

  const safe = data.safety?.safe;
  document.getElementById('safety').innerHTML = `
    <div class="${safe ? 'ok' : 'alert'}">${safe ? 'SAFE' : 'ALERT'}</div>
    ${pretty(data.safety)}
  `;

  document.getElementById('logs').textContent = (data.logs || []).join('\n');
}

async function replaySession() {
  const replay = await callApi('/api/replay');
  const frames = replay.frames || [];
  if (!frames.length) return;

  const logs = frames.slice(-25).map((f) => `replay tick=${f.tick} eeg=${f.eeg} intent=${f.intent}`);
  document.getElementById('logs').textContent = logs.join('\n');
}

function wireControls() {
  document.getElementById('startBtn').onclick = () => callApi('/api/control', 'POST', { action: 'start' });
  document.getElementById('pauseBtn').onclick = () => callApi('/api/control', 'POST', { action: 'pause' });
  document.getElementById('resetBtn').onclick = () => {
    eegTrail.length = 0;
    return callApi('/api/control', 'POST', { action: 'reset' });
  };
  document.getElementById('replayBtn').onclick = replaySession;
  document.getElementById('brainStateSelect').onchange = (e) => callApi('/api/brain_state', 'POST', { state: e.target.value });

  document.getElementById('autoBtn').onclick = async () => {
    if (autoTimer) {
      clearInterval(autoTimer);
      autoTimer = null;
      return;
    }

    const states = Array.from(document.getElementById('brainStateSelect').options).map((o) => o.value);
    let i = 0;
    await callApi('/api/auto_mode', 'POST', {});
    autoTimer = setInterval(() => {
      const state = states[i % states.length];
      callApi('/api/brain_state', 'POST', { state });
      i += 1;
    }, 2200);
  };
}

wireControls();
setInterval(refresh, 250);
refresh();
