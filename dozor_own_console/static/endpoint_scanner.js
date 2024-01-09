let antivirusScanEnabled = false;
let logCollectionEnabled = false;

function toggleAntivirusScan(agentId) {
  antivirusScanEnabled = !antivirusScanEnabled;
  sendCommand('antivirus_scan', antivirusScanEnabled, agentId);
}

function toggleLogCollection(agentId) {
  logCollectionEnabled = !logCollectionEnabled;
  sendCommand('log_collection', logCollectionEnabled, agentId);
}

function sendCommand(command, enable, agentId) {
  fetch(`/agent=${agentId}/${command}/${enable ? 'start' : 'stop'}`, {
    method: 'POST'
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Ошибка команды ' + command);
    }
    return response.json();
  })
  .then(data => {
    displayLog('Статус команды ' + command + ': ' + data.status);
  })
  .catch(error => {
    console.error('Ошибка:', error);
  });
}

function displayLog(log) {
  const logContainer = document.getElementById("log-container");
  logContainer.innerHTML += `<p>${log}</p>`;
}

document.getElementById('start-antivirus-btn').addEventListener('click', () => toggleAntivirusScan(agentId));
document.getElementById('collect-logs-btn').addEventListener('click', () => toggleLogCollection(agentId));