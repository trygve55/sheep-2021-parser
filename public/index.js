function makeTable(list) {
    let table = document.getElementById('table');
    table.innerHTML = "";

    if (list.length > 0) {
        let tr = document.createElement('tr');
        let obj = list[0];
        Object.keys(obj).forEach(key => {
            if (key !== "rttSamples") {
                let td = document.createElement('td');
                td.innerHTML = key;
                tr.appendChild(td);
            }
        });
        table.appendChild(tr);
    }

    for (var i=0; i < list.length; i++) {
        let tr = document.createElement('tr');
        let obj = list[i];

        Object.keys(obj).forEach(key => {
            if (key !== "rttSamples") {
                let td = document.createElement('td');
                td.innerHTML = obj[key];
                tr.appendChild(td);
            }
        })

        table.appendChild(tr);
    }
}

function showState(state) {
    let stateDiv = document.getElementById('state');
    stateDiv.innerHTML = "";

    Object.keys(state).forEach(key => {
        let div = document.createElement('div');
        div.innerHTML = key + " : " + state[key];
        stateDiv.appendChild(div);
    });
}

document.addEventListener("DOMContentLoaded", function(event) {
    function update() {
        fetch('results')
          .then(response => response.json())
          .then(data => makeTable(data));


        fetch('state')
          .then(response => response.json())
          .then(data => showState(data));
    }

    update();

    setInterval(update, 1000);
});