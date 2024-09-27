export function submitForm(form) {
  form.onsubmit = async (e) => {
    e.preventDefault()
    try {
      let response = await fetch("http://localhost:8000/api/appeal", {
        method: "POST",
        body: new FormData(form),
      })

    } catch (e) {
      alert("Ошибка", e)
    }
  }
}
