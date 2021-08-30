console.log('hola mundo desde main.js')

const modalBtns = [...document.getElementsByClassName('modal-button')]
const modalBody = document.getElementById('modal-body-confirm')
const startBtn = document.getElementById('start-button')

const url = window.location.href

// Datos sobre los cuest de main.html
modalBtns.forEach(modalBtn=> modalBtn.addEventListener('click', ()=>{
    const pk = modalBtn.getAttribute('data-pk')
    const numPreguntas = modalBtn.getAttribute('data-preguntas')
    const categoria = modalBtn.getAttribute('data-cuest')
    const dificultad = modalBtn.getAttribute('data-dificultad')
    const tiempo = modalBtn.getAttribute('data-tiempo')

    // PopUp con los datos del cuest seleccionado
    modalBody.innerHTML = `
        <div class="h5 mb-3">Está seguro que desea empezar con "<b>${categoria}</b>"?</div>
        <div class="text-muted">
            <ul>
                <li>Dificultad: <b>${dificultad}</b></li>
                <li>Número de Preguntas: <b>${numPreguntas}</b></li>
                <li>Tiempo: <b>${tiempo} min</b></li>
            </ul>
        </div>
    `

    startBtn.addEventListener('click', ()=>{
        window.location.href = url + pk
    })
}))