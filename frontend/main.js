const submitForm  = async () => {
const form = document.getElementById('application_form')

  const formData = new FormData(form)
  const fetchParams = JSON.stringify(Object.fromEntries(formData));
  form.onsubmit = async (e) => {
    e.preventDefault()
    try {
      let response = await fetch("http://localhost:8000/api/appeal", {
        method: "POST",
        body: fetchParams,
      })

    } catch (e) {
      alert("Ошибка", e)
    }
  }
}