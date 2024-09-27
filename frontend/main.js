import './style.css'
import javascriptLogo from './javascript.svg'
import viteLogo from '/vite.svg'
import { submitForm } from './script.js'

document.querySelector('#app').innerHTML = `
  <div class="message">
  <h1>Регистрация обращения</h1>
  <form id="application_form">
    <label for="last_name">Фамилия:</label>
    <input type="text" id="last_name" name="last_name" required>

    <label for="first_name">Имя:</label>
    <input type="text" id="first_name" name="first_name" required>

    <label for="patronymic">Отчество:</label>
    <input type="text" id="patronymic" name="patronymic" required>

    <label for="phone">Телефон:</label>
    <input type="tel" id="phone" name="phone" required>

    <label for="message">Обращение:</label>
    <textarea id="message" name="message" required></textarea>

    <button type="submit">Отправить</button>
  </form>
  </div>
`

submitForm(document.querySelector('#application_form'))

