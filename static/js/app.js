Dropzone.options.myAwesomeDropzone = {
  init: function () {
    this.on("success", function (file, response) {
      loadData()
        .then(() => loadLida())
        .then(() => loadDescription())
        .then(() => showQuestionSection());
    });
  },
};

async function loadData() {
  return fetch("/data_preview")
    .then((response) => response.text())
    .then((html) => {
      document.getElementById("data-preview").innerHTML = html;
      document.getElementById("data-preview").innerHTML += `<p>
          <small>The first 5 rows of the table.</small>
        </p>`;
    });
}

async function loadLida() {
  return fetch("/get_lida")
    .then((response) => response.json())
    .then((data) => {
      console.log(data);
      document.getElementById("lida-summary").innerText =
        data.summary.field_names;

      const fieldsContainer = document.getElementById("lida-fields");
      fieldsContainer.innerHTML = "";

      data.summary.fields.forEach((field, index) => {
        const fieldElement = document.createElement("div");
        fieldElement.innerHTML = `
            <h4>Field ${index + 1}: ${field.column}</h4>
            <p><strong>Description:</strong> ${
              field.properties.description || "No description provided"
            }</p>
            <p><strong>Data Type:</strong> ${field.properties.dtype}</p>
            <p><strong>Number of Unique Values:</strong> ${
              field.properties.num_unique_values
            }</p>
            <p><strong>Sample Values:</strong> ${field.properties.samples.join(
              ", "
            )}</p>
            <p><strong>Semantic Type:</strong> ${
              field.properties.semantic_type || "Not specified"
            }</p>
          `;
        fieldsContainer.appendChild(fieldElement);
      });

      const goalsContainer = document.getElementById("lida-goals");
      goalsContainer.innerHTML = "";
      data.goals.forEach((goal, index) => {
        const goalElement = document.createElement("div");
        goalElement.innerHTML = `
          <h3>Goal ${index + 1}</h3>
          <p><strong>Question:</strong> ${goal.question}</p>
          <p><strong>Rationale:</strong> ${goal.rationale}</p>
          <p><strong>Visualization:</strong> ${goal.visualization}</p>
        `;
        goalsContainer.appendChild(goalElement);
      });
    });
}

function loadDescription() {
  fetch("/get_description")
    .then((response) => response.json())
    .then((data) => {
      const container = document.getElementById("description-preview");
      container.innerHTML = "";

      Object.keys(data).forEach((key) => {
        const header = document.createElement("h4");
        header.textContent = key;

        const textDiv = document.createElement("div");
        textDiv.textContent = data[key];

        container.appendChild(header);
        container.appendChild(textDiv);
      });
    })
    .catch((err) => console.log("Error loading description: " + err));
}

function submitAgentQuestion() {
  const question = document.getElementById("agent-question-input").value;
  fetch("/process_agent_question", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question: question }),
  })
    .then((response) => response.json())
    .then((response) => {
      console.log(response);
      document.getElementById("ai-agent-response").innerText = response;
    })
    .catch((err) => console.log("Error processing question: " + err));
}

function submitQuestion() {
  const question = document.getElementById("ai-question-input").value;
  fetch("/process_pandasai_question", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ question: question }),
  })
    .then((response) => response.json())
    .then((response) => {
      if (response.type === "dataframe") {
        document.getElementById("ai-response").innerHTML = response.data;
      } else if (response.type === "text") {
        document.getElementById("ai-response").innerText = response.data;
      }
    })
    .catch((err) => console.log("Error processing question: " + err));
}

function showQuestionSection() {
  document.getElementById("ai-question-section").style.display = "block";
  document.getElementById("ai-agent-question-section").style.display = "block";
}
