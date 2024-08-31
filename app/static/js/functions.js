
// Function that sends a post with an id to execute a query
function sendID(route, id) {
    return fetch(route, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({id: id})
    }).then(response => response.json())
    .then(data => {
        return data
    })
}

// Function to select an option in a select input box
function selectOption(element, option) {
    options = Array.from(element.options)
    option_element = options.find(item => item.text === option)
    option_element.selected = true
}

function addOption(containerSelector, selectSelector) {
    var container = document.querySelector(containerSelector)
    var select = document.querySelector(selectSelector)

    var id = select.value
    var nome = select.options[select.selectedIndex].text

    // Removing option from select so it cannot be selected again
    select.remove(select.selectedIndex)

    // Adding selected option to the container
    var newAssegnazione = document.createElement('span');
    newAssegnazione.setAttribute('appalto_nome', nome);
        newAssegnazione.innerHTML =  `
                <h5 class="nome_assegnazione">${nome}</h5>
                <button class="remove" type="button" appalto-id='${id}'>
                    <svg xmlns="http://www.w3.org/2000/svg" height="24px" viewBox="0 -960 960 960" width="24px" fill="#EA3323"><path d="m330-288 150-150 150 150 42-42-150-150 150-150-42-42-150 150-150-150-42 42 150 150-150 150 42 42ZM480-80q-82 0-155-31.5t-127.5-86Q143-252 111.5-325T80-480q0-83 31.5-156t86-127Q252-817 325-848.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 82-31.5 155T763-197.5q-54 54.5-127 86T480-80Zm0-60q142 0 241-99.5T820-480q0-142-99-241t-241-99q-141 0-240.5 99T140-480q0 141 99.5 240.5T480-140Zm0-340Z"/></svg>
                </button>`
        container.appendChild(newAssegnazione)
        newAssegnazione.querySelector('.remove').addEventListener('click', function(){
            // Adding this option to the select
            var option = document.createElement('option');
            option.value = this.getAttribute('appalto-id');
            option.text = this.parentNode.getAttribute('appalto_nome');
            select.appendChild(option);
            this.parentNode.remove();
        })

}

function addHiddenArray(itemSelector, arraySelector, attribute) {
    array = []
    document.querySelectorAll(itemSelector).forEach(item => {
        id = item.getAttribute(attribute)
        array.push(id)
    })
    array = JSON.stringify(array)
    document.querySelector(arraySelector).value = array
}
