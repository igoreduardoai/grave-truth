const PRESETS = {
  eob: [
    {
      label: "Patient responsibility",
      question: "What is the patient responsibility?",
      answer: "",
    },
    {
      label: "Cited and ghost",
      question: "What is the pharmacy charge?",
      answer: "The patient responsibility is $42.15. The pharmacy charge is $180.00.",
    },
    {
      label: "Missing penalty",
      question: "What is the out-of-network penalty?",
      answer: "",
    },
    {
      label: "Grounded pharmacy",
      question: "",
      answer: "The pharmacy charge is $18.40.",
    },
  ],
  lease: [
    {
      label: "Security deposit",
      question: "What is the security deposit?",
      answer: "",
    },
    {
      label: "Late fee swapped",
      question: "What is the late fee?",
      answer: "The late fee is $1,850.00. The late fee is $75.00.",
    },
    {
      label: "Portuguese rent",
      question: "Qual é o valor do aluguel?",
      answer: "",
    },
  ],
  paste: [
    {
      label: "Postcard",
      document: "The demo clinic collected a souvenir copay of $3.00. The gift shop sold a postcard for $1.25.",
      question: "How much is the postcard?",
      answer: "The souvenir copay is $3.00. The postcard costs $9.00.",
    },
  ],
};

const VERDICT_TEXT = {
  cited: "Cited. The gold mark is the clause that states it.",
  accepted: "Accepted. The claim's figure sits in the marked clause.",
  not_found: "Ghost. No clause in this document matches the question.",
  rejected: "Ghost. That claim is not grounded in the clause that names the subject.",
  mixed: "Mixed. Cited claims stay lit. Ghost claims have no supporting clause.",
  conflict: "Conflict. These clauses name different figures for the same subject. Neither figure is selected.",
};

const form = document.querySelector("#ask-form");
const questionBox = document.querySelector("#question");
const answerBox = document.querySelector("#answer");
const documentBox = document.querySelector("#document");
const pasteField = document.querySelector("#paste-field");
const presets = document.querySelector("#presets");
const status = document.querySelector("#status");
const verdict = document.querySelector("#verdict");
const questionResult = document.querySelector("#question-result");
const claimsList = document.querySelector("#claims");
const ghostHost = document.querySelector("#ghost-host");
const quote = document.querySelector("#quote");
const quoteLabel = document.querySelector("#quote-label");
const source = document.querySelector("#source");
const docId = document.querySelector("#doc-id");

document.querySelectorAll('input[name="app"]').forEach((input) => {
  input.addEventListener("change", () => {
    if (input.checked) selectApp(input.value);
  });
});

form.addEventListener("submit", (event) => {
  event.preventDefault();
  ask();
});

form.addEventListener("keydown", (event) => {
  if (event.key === "Enter" && (event.ctrlKey || event.metaKey)) {
    event.preventDefault();
    ask();
  }
});

function selectedApp() {
  const picked = document.querySelector('input[name="app"]:checked');
  return picked ? picked.value : "eob";
}

function selectApp(app) {
  pasteField.hidden = app !== "paste";
  renderPresets();
  if (app === "paste") {
    docId.textContent = "pasted-document";
    source.textContent = documentBox.value || "Paste a synthetic document, then check it.";
    return;
  }
  loadDocument();
}

function renderPresets() {
  const app = selectedApp();
  presets.replaceChildren();
  PRESETS[app].forEach((preset) => {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "preset";
    button.textContent = preset.label;
    button.addEventListener("click", () => {
      if (preset.document !== undefined) documentBox.value = preset.document;
      questionBox.value = preset.question || "";
      answerBox.value = preset.answer || "";
      ask();
    });
    presets.appendChild(button);
  });
}

documentBox.addEventListener("input", () => {
  if (selectedApp() === "paste" && !claimsList.childElementCount && !questionResult.childElementCount) {
    source.textContent = documentBox.value || "Paste a synthetic document, then check it.";
  }
});

async function loadDocument() {
  const app = selectedApp();
  if (app === "paste") return;
  status.textContent = "";
  try {
    const response = await fetch(`/api/document?app=${app}`);
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "Could not load the fixture.");
    docId.textContent = payload.document_id;
    source.textContent = payload.document;
  } catch (error) {
    source.textContent = "The fixture did not load. Start python3 demos/haunted/server.py and open its localhost URL.";
    status.textContent = error.message;
  }
}

async function ask() {
  const app = selectedApp();
  const body = {
    app,
    question: questionBox.value,
    answer: answerBox.value,
  };
  if (app === "paste") body.document = documentBox.value;
  status.textContent = "Checking with the local library…";
  ghostHost.replaceChildren();
  quote.hidden = true;
  quoteLabel.hidden = true;
  try {
    const response = await fetch("/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || "The local server rejected the request.");
    renderResult(payload);
    status.textContent = "";
    verdict.focus();
  } catch (error) {
    verdict.className = "verdict";
    verdict.textContent = error.message;
    questionResult.replaceChildren();
    claimsList.replaceChildren();
    ghostHost.replaceChildren();
    quote.hidden = true;
    quoteLabel.hidden = true;
    quote.textContent = "";
    if (selectedApp() === "paste") {
      const pasted = documentBox.value.trim();
      docId.textContent = pasted ? "pasted-document" : "";
      source.textContent = pasted || "Paste a synthetic document, then check it.";
    }
    status.textContent = "No answer was invented.";
    verdict.focus();
  }
}

function renderResult(payload) {
  const ghost = payload.ghost;
  verdict.className = `verdict ${ghost ? "ghost" : ""} ${payload.verdict || ""}`.trim();
  verdict.textContent = VERDICT_TEXT[payload.verdict] || payload.answer || "";
  renderQuestion(payload.question_result);
  renderClaims(payload.claims || []);
  if (!(payload.claims || []).length && payload.ghost) {
    const line = document.createElement("p");
    line.className = "ghost-claim";
    line.textContent = payload.question || payload.answer || "";
    ghostHost.append(line);
  }
  const citations = collectCitations(payload);
  const showQuote = citations.length > 0 && !(payload.claims || []).length;
  quote.hidden = !showQuote;
  quoteLabel.hidden = !showQuote;
  quote.textContent = showQuote ? citations.map((citation) => citation.span).join(" ") : "";
  docId.textContent = payload.document_id || "";
  source.replaceChildren(renderSource(payload.document || "", citations));
}

function renderQuestion(result) {
  questionResult.replaceChildren();
  if (!result) return;
  const block = document.createElement("div");
  block.className = `library ${result.ghost ? "ghost" : "cited"}`;
  const heading = document.createElement("h3");
  heading.textContent = "Library answer";
  const badge = document.createElement("span");
  badge.className = result.ghost ? "badge ghost" : "badge cited";
  badge.textContent = result.ghost ? "Ghost" : "Cited";
  const text = document.createElement("p");
  text.textContent = result.answer;
  if (result.ghost) text.className = "ghost-claim";
  block.append(heading, badge, text);
  questionResult.append(block);
}

function renderClaims(claims) {
  claimsList.replaceChildren();
  ghostHost.replaceChildren();
  claims.forEach((claim) => {
    const item = document.createElement("li");
    item.className = claim.ghost ? "claim is-ghost" : "claim is-cited";
    const badge = document.createElement("span");
    badge.className = claim.ghost ? "badge ghost" : "badge cited";
    badge.textContent = claim.ghost ? "Ghost" : "Cited";
    const text = document.createElement("p");
    text.textContent = claim.text;
    if (claim.ghost) text.className = "ghost-claim";
    item.append(badge, text);
    if (claim.ghost) {
      const reason = document.createElement("p");
      reason.className = "ghost-reason";
      reason.textContent = "No clause in this document states this claim.";
      item.append(reason);
    } else if (claim.citations && claim.citations.length) {
      const ref = document.createElement("p");
      ref.className = "clause-ref";
      ref.textContent = claim.citations.map((citation) => citation.span).join(" ");
      item.append(ref);
    }
    claimsList.append(item);
  });
}

function collectCitations(payload) {
  const all = [];
  if (payload.question_result && payload.question_result.citations) {
    all.push(...payload.question_result.citations);
  }
  if (payload.citations) all.push(...payload.citations);
  const seen = new Set();
  return all.filter((citation) => {
    const key = `${citation.start}:${citation.end}:${citation.span}`;
    if (seen.has(key)) return false;
    seen.add(key);
    return true;
  });
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
