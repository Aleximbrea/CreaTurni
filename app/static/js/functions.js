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
