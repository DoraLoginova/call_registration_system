export function submitForm(form) {
  form.onsubmit = async (e) => {
    e.preventDefault()
    try {
      let response = await fetch("http://127.0.0.1:8000/api/products/", {
        method: "POST",
        body: new FormData(form),
      })

    } catch (e) {
      alert("Ошибка", e)
    }
  }
}
