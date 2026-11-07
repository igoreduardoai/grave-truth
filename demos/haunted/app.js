const PRESETS = {
  eob: [
    { mode: "answer", label: "Patient responsibility", question: "What is the patient responsibility?" },
    { mode: "answer", label: "Pharmacy charge", question: "What is the pharmacy charge?" },
    { mode: "answer", label: "Two clauses", question: "What is the pharmacy charge and the patient responsibility?" },
    { mode: "answer", label: "Missing penalty", question: "What is the out-of-network penalty?" },
    { mode: "reject", label: "Pharmacy swapped", question: "The pharmacy charge is $42.15." },
    { mode: "reject", label: "Grounded responsibility", question: "The patient responsibility is $42.15." },
  ],
  lease: [
    { mode: "answer", label: "Security deposit", question: "What is the security deposit?" },
    { mode: "answer", label: "Rent and late fee", question: "What rent is due on the first day, and what late fee applies after the fifth day?" },
    { mode: "answer", label: "Late fee is not rent", question: "Is the late fee monthly rent?" },
    { mode: "answer", label: "Portuguese rent", question: "Qual é o valor do aluguel?" },
    { mode: "reject", label: "Late fee as rent", question: "The late fee is $1,850.00." },
    { mode: "reject", label: "Grounded late fee", question: "The late fee is $75.00." },
  ],
};

const VERDICT_TEXT = {
  cited: "Cited. The gold mark is the source clause.",
  accepted: "Accepted. The claim's figure sits in the marked clause.",
  not_found: "Ghost. No clause in this fixture matches the question.",
  rejected: "Ghost. That claim is not grounded in the clause that names the subject.",
};

const state = { app: "eob" };

const form = document.querySelector("#ask-form");
const questionBox = document.querySelector("#question");
const presets = document.querySelector("#presets");
const status = document.querySelector("#status");
const verdict = document.querySelector("#verdict");
const ghostHost = document.querySelector("#ghost-host");
const quote = document.querySelector("#quote");
const source = document.querySelector("#source");
const docId = document.querySelector("#doc-id");

document.querySelectorAll(".app-tab").forEach((button) => {
  button.addEventListener("click", () => selectApp(button.dataset.app));
});

form.addEventListener("submit", (event) => {
  event.preventDefault();
  const mode = new FormData(form).get("mode");
  ask(questionBox.value, mode);
});

function selectApp(app) {
  state.app = app;
  document.querySelectorAll(".app-tab").forEach((button) => {
    const on = button.dataset.app === app;
    button.classList.toggle("is-on", on);
    button.setAttribute("aria-selected", on ? "true" : "false");
  });
  renderPresets();
  loadDocument();
}

function renderPresets() {
  presets.replaceChildren();
  PRESETS[state.app].forEach((preset) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "preset";
    button.textContent = preset.label;
    button.addEventListener("click", () => {
      questionBox.value = preset.question;
      form.querySelector(`input[value="${preset.mode}"]`).checked = true;
      ask(preset.question, preset.mode);
    });
    presets.appendChild(button);
  });
}

async function loadDocument() {
  status.textContent = "";
  try {
    const response = await fetch(`/api/document?app=${state.app}`);
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "Could not load the fixture.");
    docId.textContent = payload.document_id;
    source.textContent = payload.document;
  } catch (error) {
    source.textContent = "The fixture did not load. Start python3 demos/haunted/server.py and open its localhost URL.";
    status.textContent = error.message;
  }
}

async function ask(question, mode) {
  status.textContent = "Asking the local library…";
  ghostHost.replaceChildren();
  quote.hidden = true;
  try {
    const response = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ app: state.app, question, mode }),
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "The local server rejected the request.");
    renderResult(payload);
    status.textContent = "";
  } catch (error) {
    verdict.className = "verdict";
    verdict.textContent = error.message;
    status.textContent = "No answer was invented.";
  }
}

function renderResult(payload) {
  const ghost = payload.ghost;
  verdict.className = `verdict ${ghost ? "ghost" : payload.verdict} ${payload.verdict}`;
  verdict.textContent = VERDICT_TEXT[payload.verdict] || payload.answer;
  ghostHost.replaceChildren();
  if (ghost) {
    const line = document.createElement("p");
    line.className = "ghost-claim";
    line.textContent = payload.question;
    ghostHost.appendChild(line);
  }
  if (payload.citations && payload.citations.length) {
    quote.hidden = false;
    quote.textContent = payload.citations.map((citation) => citation.span).join(" ");
  } else {
    quote.hidden = true;
    quote.textContent = "";
  }
  docId.textContent = payload.document_id || "";
  source.replaceChildren(renderSource(payload.document || "", payload.citations || []));
}

function renderSource(text, citations) {
  const marks = citations
    .filter((citation) => citation.start >= 0 && citation.end > citation.start && citation.end <= text.length)
    .filter((citation) => text.slice(citation.start, citation.end) === citation.span)
    .sort((a, b) => a.start - b.start);
  const frag = document.createDocumentFragment();
  let cursor = 0;
  marks.forEach((citation) => {
    if (citation.start < cursor) return;
    frag.append(text.slice(cursor, citation.start));
    const mark = document.createElement("mark");
    mark.className = "clause";
    mark.textContent = citation.span;
    frag.append(mark);
    cursor = citation.end;
  });
  frag.append(text.slice(cursor));
  return frag;
}

renderPresets();
loadDocument();
