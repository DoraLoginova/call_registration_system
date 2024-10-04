const submitForm = async () => {
  const form = document.getElementById('application_form');

  form.onsubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData(form);

    try {
      let response = await fetch("http://localhost:8000/api/appeal", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(Object.fromEntries(formData))
      });

      
    } catch (e) {
      alert("Ошибка: " + e.message);
    }
  };
};

submitForm();