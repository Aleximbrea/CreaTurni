function delete_record(route, id) {
        fetch(route, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({id: id})
        })  .then(response => response.json())
            .then(data => {
                if(data==true) {
                    window.location.reload();
                }
            })
    }

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
