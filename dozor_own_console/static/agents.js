function fetchAgents() {
  fetch('/agents') // URL сервера
    .then(response => response.json())
    .then(data => {
      displayAgents(data);
    })
    .catch(error => {
      console.error('Ошибка при получении списка агентов', error);
    });
}

// Отображение списка агентов на странице
function displayAgents(data) {
  const agentsList = document.getElementById('agents-list');

  // Перебираем список агентов и добавляем их на страницу
  data.forEach(agent => {
    const agentElement = document.createElement('div');
    const agentNameElement = document.createElement('span');
    agentNameElement.textContent = agent.ip;

    // Обработчик события при нажатии на имя сканера
    agentNameElement.addEventListener('click', () => {
      getAgentType(agent.id)
        .then(agentType => {
          if (agentType === 'network_scanner') {
            window.open(`/network_scanner.html?agentId=${agent.ip}`, '_blank');
          } else if (agentType === 'endpoint_scanner') {
            window.open(`/endpoint_scanner.html?agentId=${agent.ip}`, '_blank');
          }
        });
    });

    agentElement.appendChild(agentNameElement);
    agentElement.appendChild(document.createTextNode(` (${agent.status})`));
    agentsList.appendChild(agentElement);
  });
}

// Отправка запроса на сервер для получения типа сканера
function getAgentType(agentId) {
  return fetch(`/agents/${agentId}/type`) // URL сервера
    .then(response => response.json())
    .then(data => {
      return data.agentType;
    })
    .catch(error => {
      console.error('Ошибка при получении типа сканера', error);
    });
}

document.addEventListener('DOMContentLoaded', function() {
  fetchAgents();
  var modal = document.getElementById("add-agent-modal");
  var btn = document.getElementById("add-agent-btn");
  var span = document.getElementById("close-modal-btn");
  var cancelBtn = document.getElementById("cancel-add-agent-btn");

  btn.onclick = function() {
    modal.style.display = "block";
  }

  span.onclick = function() {
    modal.style.display = "none";
  }

  cancelBtn.onclick = function() {
    modal.style.display = "none";
  }

  window.onclick = function(event) {
    if (event.target === modal) {
      modal.style.display = "none";
    }
  }
});


document.getElementById('agent-form').addEventListener('submit', (event) => {
  event.preventDefault();
  
  const ip = document.getElementById('agent-ip').value;
  const description = document.getElementById('agent-description').value;
  const scannerType = document.getElementById('scanner-type').value;

  if (!ip || !description || !scannerType) {
    alert('Пожалуйста, заполните все поля.');
    return;
  }

  // Отправка данных на сервер
  fetch('/agents', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      ip: ip,
      description: description,
      scanner_type: scannerType
    })
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Ошибка добавления агента');
    }
    return response.json();
  })
  .then(data => {
    console.log('Агент добавлен:', data);
    document.getElementById('add-agent-modal').style.display = 'none';
    fetchAgents();
  })
  .catch(error => {
    console.error('Ошибка:', error);
  });
});
