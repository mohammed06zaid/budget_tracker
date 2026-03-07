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

    card.innerHTML = `
      <div class="expense-left">
        <div class="expense-category">
          ${getCategoryIcon(expense.Kategorie)} ${expense.Kategorie}
        </div>
        <div class="expense-date">
          📅 ${expense.Datum}
        </div>
      </div>
      <div class="expense-amount">
        ${expense.Ausgabe} €
      </div>
    `;

    const deleteBtn = document.createElement("button");
    deleteBtn.textContent = "🗑 Ausgabe Löschen";
    deleteBtn.classList.add("delete-expense-btn"); 
    card.appendChild(deleteBtn);

    deleteBtn.addEventListener("click", 
       () => {
        fetch(`expenses/${expense.id}`,{method: "DELETE"})

        .then(res=> {
          if(res.ok){
            card.remove();
          }else{
            alert("Fehler beim Löschen der Ausgabe.");
          }
        })
        .catch(error => {
          console.error("Fehler", error);
          alert("Fehler beim Löschen der Ausgabe.");
        });
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


  // register fun 
  registerForm.addEventListener("submit", async (e)=>{
    e.preventDefault();

    const username = document.getElementById("username").value; 
    const password = document.getElementById("password").value;

    const response = await fetch("/register",{
      method : "POST",
      headers : { "Content-Type": "application/json" },
      body: JSON.stringify({username, password})
    });

    const result = await response.json();
    
    if(response.ok){
      window.location.href = "/index";
    }else{
      alert(result.error);
    }


  });


});
