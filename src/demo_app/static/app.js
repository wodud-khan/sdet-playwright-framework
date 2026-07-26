const form = document.querySelector("#order-form");
const result = document.querySelector("#order-result");
const formStatus = document.querySelector("#form-status");
const submitButton = form.querySelector("button[type='submit']");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  submitButton.disabled = true;
  formStatus.textContent = "Creating order…";
  result.hidden = true;

  const fields = new FormData(form);
  const payload = {
    customer_name: fields.get("customer_name"),
    item_name: fields.get("item_name"),
    quantity: Number(fields.get("quantity")),
    unit_price_cents: 2499,
  };

  try {
    const response = await fetch("/api/orders", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(payload),
    });
    const body = await response.json();

    if (!response.ok) {
      throw new Error(body.detail ?? `Request failed with status ${response.status}`);
    }

    result.querySelector("[data-testid='order-id']").textContent = body.id;
    result.querySelector("[data-testid='order-status']").textContent = body.status;
    result.querySelector("[data-testid='order-total']").textContent =
      `$${(body.total_cents / 100).toFixed(2)}`;
    form.dataset.lastOrderId = body.id;
    result.hidden = false;
    formStatus.textContent = "Order saved.";
  } catch (error) {
    formStatus.textContent = `Order could not be created: ${error.message}`;
  } finally {
    submitButton.disabled = false;
  }
});
