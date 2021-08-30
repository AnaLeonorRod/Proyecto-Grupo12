console.log('hola mundo desde cuest.js')
const url = window.location.href

const cuestBox = document.getElementById('quiz-box')
const scoreBox = document.getElementById('score-box')
const resultBox = document.getElementById('result-box')
const timerBox = document.getElementById('timer-box')

// Timer
const activateTimer = (time) => {
    if (time.toString().length < 2) {
        timerBox.innerHTML = `<b>0${time}:00</b>`
    } else {
        timerBox.innerHTML = `<b>${time}:00</b>`
    }

    let minutes = time - 1
    let seconds = 60
    let displaySeconds
    let displayMinutes

    const timer = setInterval(() => {
        seconds--
        if (seconds < 0) {
            seconds = 59
            minutes--
        }
        if (minutes.toString().length < 2) {
            displayMinutes = '0' + minutes
        } else {
            displayMinutes = minutes
        }
        if (seconds.toString().length < 2) {
            displaySeconds = '0' + seconds
        } else {
            displaySeconds = seconds
        }
        if (minutes === 0 && seconds === 0) {
            timerBox.innerHTML = "<b>00:00</b>"
            setTimeout(() => {
                clearInterval(timer)
                alert('Tiempo Finalizado')
                sendData()
            }, 500)
        }

        timerBox.innerHTML = `<b>${displayMinutes}:${displaySeconds}</b>`
    }, 1000)
}

// Obtener las preguntas con las respuestas correctas
$.ajax({
    type: 'GET',
    url: `${url}data`,
    success: function (response) {
        const data = response
            .data
            data
            .forEach(el => {
                for (const [pregunta, respuestas] of Object.entries(el)) {
                    cuestBox.innerHTML += `
                    <hr>
                    <div class="mb-2">
                        <b>${pregunta}</b>
                    </div>
                `
                    respuestas.forEach(respuesta => {
                        cuestBox.innerHTML += `
                        <div>
                            <input type="radio" class="ans" id="${pregunta}-${respuesta}" name="${pregunta}" value="${respuesta}">
                            <label for="${pregunta}">${respuesta}</label>
                        </div>
                    `
                    })
                }
            });
        activateTimer(response.time)

    },
    error: function (error) {
        console.log(error)
    }
})

const cuestForm = document.getElementById('quiz-form')
const csrf = document.getElementsByName('csrfmiddlewaretoken')

const sendData = () => {
    const elements = [...document.getElementsByClassName('ans')]
    const data = {}
    data['csrfmiddlewaretoken'] = csrf[0]
        .value
        elements
        .forEach(el => {
            if (el.checked) {
                data[el.name] = el.value
            } else {
                if (!data[el.name]) {
                    data[el.name] = null
                }
            }
        })

    // Muestra los resultados al finalizar el cuest o termina el tiempo
    $.ajax({
        type: 'POST',
        url: `${url}save/`,
        data: data,
        success: function (response) {
            console.log(response)
            const Resultados = response
                .Resultados
                console
                .log(Resultados)
            cuestForm
                .classList
                .add('not-visible')

            // Muesta puntaje obtenido al finalizar
            scoreBox.innerHTML = `Puntaje Obtenido: ${response
                .Puntaje}`

                Resultados
                .forEach(res => {
                    const resDiv = document.createElement("div")
                    for (const [pregunta, resp] of Object.entries(res)) {

                        resDiv.innerHTML += pregunta
                        const cls = ['container', 'p-3', 'text-light', 'h6']
                        resDiv
                            .classList
                            .add(...cls)

                        // Control de respuestas correctas, incorrectas o sin contestar
                        if (resp == 'no respondido') {
                            resDiv.innerHTML += ' - NO RESPONDIDO'
                            resDiv
                                .classList
                                .add('bg-danger')
                        } else {
                            const respuesta = resp['respondido']
                            const correcto = resp['respuesta_correcta']

                            if (respuesta == correcto) {
                                resDiv
                                    .classList
                                    .add('bg-success')
                                resDiv.innerHTML += ` - CORRECTO: ${respuesta}`
                            } else {
                                resDiv
                                    .classList
                                    .add('bg-danger')
                                resDiv.innerHTML += ` | RESPONDISTE: ${respuesta}`
                                resDiv.innerHTML += ` | RESPUESTA CORRECTA: ${correcto}`

                            }
                        }
                    }
                    resultBox.append(resDiv)
                })
        },
        error: function (error) {
            console.log(error)
        }
    })
}

cuestForm.addEventListener('submit', e => {
    e.preventDefault()

    sendData()
})