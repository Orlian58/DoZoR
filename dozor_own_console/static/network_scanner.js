let scanEnabled = false;
const urlParams = new URLSearchParams(window.location.search);
const agentId = urlParams.get('agentId');

function toggleScan(agentId) {
  scanEnabled = !scanEnabled;
  
  updateScanButton();
  
  const action = scanEnabled ? 'start' : 'stop';
  
  fetch(`/agents/${agentId}/${action}`, {
    method: 'POST'
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Ошибка команды сканирования');
    }
    return response.json();
  })
  .then(data => {
    displayLog('Статус сканирования: ' + data.status);
  })
  .catch(error => {
    console.error('Ошибка:', error);
  });
}

function updateScanButton() {
  const startButton = document.getElementById("start-scan-btn");
  const stopButton = document.getElementById("stop-scan-btn");

  if (scanEnabled) {
    startButton.style.display = 'none';
    stopButton.style.display = 'inline-block';
  } else {
    startButton.style.display = 'inline-block';
    stopButton.style.display = 'none';
  }
}

function displayLog(log) {
  const logOutput = document.getElementById("logs-output");
  const logElement = document.createElement("p");
  logElement.textContent = log;
  logOutput.appendChild(logElement);
  logOutput.scrollTop = logOutput.scrollHeight;
}

document.getElementById('start-scan-btn').addEventListener('click', () => toggleScan(agentId));
document.getElementById('stop-scan-btn').addEventListener('click', () => toggleScan(agentId));

document.getElementById('fetch-logs-btn').addEventListener('click', () => {
  const datePicker = document.getElementById('date-picker');
  datePicker.style.display = datePicker.style.display === 'none' ? 'block' : 'none';
});

document.getElementById('date-picker').addEventListener('change', (event) => {
  const date = event.target.value;
  if (date) {
    fetchLogsByDate(agentId, date);
  }
});

async function fetchLogsByDate(agentId, date) {
  try {
    const response = await fetch(`/agents/${agentId}/logs?date=${date}`);
    if (!response.ok) {
      throw new Error('Ошибка при получении логов по выбранной дате');
    }
    const logs = await response.json();
    const logOutput = document.getElementById("logs-output");
    logOutput.innerHTML = '';
    logs.forEach((log) => {
      displayLog(log.message);
    });
  } catch (error) {
    console.error('Ошибка:', error);
  }
}