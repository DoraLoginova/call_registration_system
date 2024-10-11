const submitForm = async () => {
  const form = document.getElementById('application_form');

  form.onsubmit = async (e) => {
    e.preventDefault();    //останавливает стандартное поведение браузера (перезагрузку страницы при отправке формы)

    const formData = new FormData(form);

    try {
      let response = await fetch("http://localhost:8000/api/appeal", {
        method: "POST",
        headers: {
          "Content-Type": "application/json", // задаёт заголовок запроса Content-Type, который указывает на то, что данные, которые отправляются на сервер, будут в формате JSON
        },
        body: JSON.stringify(Object.fromEntries(formData))
      }); // Поле body указывает данные, которые отправляются на сервер. Здесь мы преобразуем объект FormData в обычный объект с помощью Object.fromEntries(),
      // а затем сериализуем его в формат JSON с помощью JSON.stringify(), чтобы сервер мог его правильно обработать

      
    } catch (e) {
      alert("Ошибка: " + e.message);
    }
  };
};

submitForm();