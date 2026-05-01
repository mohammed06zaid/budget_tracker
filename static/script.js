// Warten, bis HTML geladen ist
document.addEventListener("DOMContentLoaded", () => {

  const form = document.getElementById("expense-form");
  const container = document.getElementById("expenses");
  const themeBtn = document.getElementById("toggle-theme");
  const ctx = document.getElementById("expensesChart");
  const max = document.getElementById("max-value");
  const min = document.getElementById("min-value");
  const registerForm = document.getElementById("register-form"); 

  /* ---------------- DARK MODE ---------------- */
  themeBtn.addEventListener("click", () => {
    document.body.classList.toggle("dark");
  });

  /* --------- HILFSFUNKTION: ICON --------- */
  function getCategoryIcon(category) {
    switch (category) {
      case "Food": return "🍔";
      case "Transport": return "🚌";
      case "Rent": return "🏠";
      case "Shopping": return "🛍️";
      default: return "💰";
    }
  }

  /* --------- HILFSFUNKTION: CARD --------- */
  function createExpenseCard(expense) {
    const card = document.createElement("div");
    card.className = "expense-card";
 
    // Bug #3 fix: API gibt category/amount/date zurück (nicht Kategorie/Ausgabe/Datum)
    const category = expense.category || expense.Kategorie || "–";
    const amount   = expense.amount   || expense.Ausgabe   || "–";
    const date     = expense.date     || expense.Datum     || "–";
    const id       = expense.id;
 
    card.innerHTML = `
      <div class="expense-left">
        <div class="expense-category">
          ${getCategoryIcon(category)} ${category}
        </div>
        <div class="expense-date">
          📅 ${date}
        </div>
      </div>
      <div class="expense-amount">
        ${amount} €
      </div>
    `;
 
    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "🗑 Ausgabe Löschen";
    deleteBtn.classList.add("delete-expense-btn"); 
    card.appendChild(deleteBtn);
 
  deleteBtn.addEventListener("click", async () => {
    console.log("Lösche expense ID:", id); // Debug
    try {
        const res = await fetch(`/expenses/${id}`, { method: "DELETE" });
        const data = await res.json();
        if (res.ok) {
            card.remove();
            console.log(data.message);
        } else {
            alert("Fehler beim Löschen der Ausgabe: " + data.error);
        }
    } catch (error) {
        console.error("Fehler", error);
        alert("Fehler beim Löschen der Ausgabe.");
    }
  });
 
    return card;
  }

  /* --------- AUSGABEN LADEN --------- */
  function loadExpenses() {
    fetch("/expenses")
      .then(res => res.json())
      .then(data => {
        container.innerHTML = "";

        data.forEach(expense => {
          const card = createExpenseCard(expense);
          container.appendChild(card);
        });
      })
      .catch(err => console.error("Fehler beim Laden:", err));
  }

  loadExpenses();

  /* --------- FORMULAR ABSCHICKEN --------- */
  form.addEventListener("submit", (e) => {
    e.preventDefault();

    const expense = {
      ausgabe: document.getElementById("amount").value,
      kategorie: document.getElementById("category").value,
      datum: document.getElementById("date").value
    };

    fetch("/expenses", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(expense)
    })
      .then(res => res.json())
      .then(data => {
        const card = createExpenseCard(data);
        container.prepend(card); // neueste oben
        form.reset();
        
      })
      .catch(err => console.error("Fehler:", err));
  });


  if (ctx) {
    console.log("Canvas gefunden:", ctx);
  } else {
    console.error("Canvas nicht gefunden!");
  }

  fetch("/expenses/categories")
  .then(res => res.json())
  .then(data => {

    const labels = Object.keys(data);
    const values = Object.values(data); 

    
      new Chart(ctx, {
        type: "bar", // Balkendiagramm
        data: {
          labels:labels ,
          datasets: [{
            label: "Ausgaben (€)",
            data: values,
            backgroundColor: "#6366f1"
          }]
        },
        options: {
          responsive: true,
          plugins: {
            legend: { display: true }
          }
        

        
        }
});
  })
  .catch(err => console.error(err));


  fetch("/expenses/max_min")
  .then(res => res.json())
  .then(data =>{
    max.textContent = data.max + " €";
    min.textContent = data.min + " €";
  })

  .catch(err => {
    console.error("Fehler:", err);
  });


  const btn = document.getElementById("salary-submit");

  btn.addEventListener("click", (e) => {
    e.preventDefault();

    const incom = document.getElementById("salary-input").value;

    // Validate input
    if (!incom || isNaN(incom) || Number(incom) <= 0) {
      alert("Bitte geben Sie ein gültiges Einkommen ein.");
      return;
    }

    console.log("Einkommen:", incom);

    fetch("/income", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ income: incom }),
    })
      .then((response) => {
        if (!response.ok) {
          return response.json().then((errorData) => {
            throw new Error(errorData.error || "Fehler beim Speichern des Einkommens.");
          });
        }
        return response.json();
      })
      .then((data) => {
        alert(data.message || "Einkommen erfolgreich gespeichert.");
      })
      .catch((error) => {
        console.error("Fehler:", error);
        alert(error.message || "Es gab ein Problem beim Speichern des Einkommens.");
      });
  });

  setInterval(() => {
    fetch("/expenses/status")
    .then(res => res.json())
    .then(data => {
      if(data.error){
        document.getElementById("remaining-salary").textContent = "Bitte Einkommen eingeben!";
        return;
      }
      document.getElementById("remaining-salary").textContent = data.remaining_budget + " €";
    });
  }, 3000);


  // register fun - only attach if the form exists; do not override normal POST
  if (registerForm) {
    // Let the form submit normally so the Flask route handles the POST.
    // If you prefer AJAX registration, implement it here and send form-encoded
    // or JSON matching the server expectations.
  }

});


// ===== CHATBOT (Budget Assistant) =====

document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn    = document.getElementById("chat-toggle-btn");
  const closeBtn     = document.getElementById("chat-close-btn");
  const chatWindow   = document.getElementById("chat-window");
  const chatMessages = document.getElementById("chat-messages");
  const chatInput    = document.getElementById("chat-input");
  const sendBtn      = document.getElementById("chat-send-btn");

  // Gesprächsverlauf – wird bei jedem Request mitgeschickt
  let chatHistory = [];

  // --- Chat öffnen / schließen ---
  toggleBtn.addEventListener("click", () => {
    chatWindow.classList.toggle("chat-hidden");
    if (!chatWindow.classList.contains("chat-hidden")) {
      chatInput.focus();
    }
  });

  closeBtn.addEventListener("click", () => {
    chatWindow.classList.add("chat-hidden");
  });

  // --- Nachricht im Fenster anzeigen ---
  function appendMessage(text, role) {
    const msg = document.createElement("div");
    msg.classList.add("chat-msg", role);
    msg.textContent = text;
    chatMessages.appendChild(msg);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return msg;
  }

  // --- Lade-Indikator (drei blinkende Punkte) ---
  function showLoading() {
    const msg = document.createElement("div");
    msg.classList.add("chat-msg", "bot", "loading");
    msg.innerHTML = "<span>●</span><span>●</span><span>●</span>";
    chatMessages.appendChild(msg);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    return msg;
  }

  // --- Nachricht an /chat senden ---
  async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return; // Leere Nachrichten ignorieren

    appendMessage(text, "user");
    chatInput.value = "";
    sendBtn.disabled = true;

    const loadingMsg = showLoading();

    try {
      const response = await fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: text, history: chatHistory }),
      });

      const data = await response.json();
      loadingMsg.remove();

      if (response.ok) {
        appendMessage(data.reply, "bot");
        // Verlauf für den nächsten Request speichern
        chatHistory.push({ role: "user",      content: text       });
        chatHistory.push({ role: "assistant", content: data.reply });
      } else {
        appendMessage("Fehler: " + (data.error || "Unbekannter Fehler."), "error");
      }
    } catch (err) {
      loadingMsg.remove();
      appendMessage("Backend nicht erreichbar. Bitte versuche es später.", "error");
    } finally {
      sendBtn.disabled = false;
      chatInput.focus();
    }
  }

  // --- Button-Klick und Enter-Taste ---
  sendBtn.addEventListener("click", sendMessage);
  chatInput.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
  });
});

// ===== ENDE CHATBOT =====
