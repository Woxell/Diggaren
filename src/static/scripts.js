const baseURL = "http://unicorns.idioti.se/";

async function listUnicorns() {
    const options = {
        method: "GET",
        headers: {
            "Accept": "application/json"
        }
    };
    const response = await fetch(baseURL, options);
    const unicorns = await response.json();
    const unicornList = document.querySelector("#unicorns");
    unicornList.replaceChildren();
    unicorns.forEach((unicorn) => {
        let listItem = document.createElement("li");
        listItem.setAttribute("name", "unicorn_" + unicorn.id);
        listItem.setAttribute("value", unicorn.id);
        listItem.innerHTML = unicorn.name;
        listItem.addEventListener("click", fetchThenDisplayUnicorn);
        unicornList.appendChild(listItem);
    });
}

async function fetchThenDisplayUnicorn(event) {
    const url = baseURL + event.target.value;
    const options = {
        method: "GET",
        headers: {
            "Accept": "application/json"
        }
    };
    const response = await fetch(url, options);
    const unicorn = await response.json();
    displayUnicorn(unicorn);
}

function displayUnicorn(unicorn) {
    const date = new Date(unicorn.spottedWhen);
    const legibleDate = date.toLocaleString("sv-SE", {
        year: "numeric",
        month: "2-digit",
        day: "2-digit"
    });
    const sighting = `Av: ${unicorn.reportedBy}, ${legibleDate} i ${unicorn.spottedWhere.name}`;
    const image = document.createElement("img");
    image.setAttribute("src", unicorn.image);

    document.querySelector("#unicornName").innerHTML = unicorn.name;
    document.querySelector("#unicornImage").replaceChildren(image);
    document.querySelector("#unicornInfo").innerHTML = unicorn.description;
    document.querySelector("#unicornSighting").innerHTML = sighting;

    document.querySelector("#existingUnicorn input[name=id]").value = unicorn.id;
    document.querySelector("#existingUnicorn input[name=name]").value = unicorn.name;
    document.querySelector("#existingUnicorn input[name=reportedBy]").value = unicorn.reportedBy;
    document.querySelector("#existingUnicorn input[name='spottedWhere.name']").value = unicorn.spottedWhere.name;
    document.querySelector("#existingUnicorn input[name='spottedWhere.lat']").value = unicorn.spottedWhere.lat;
    document.querySelector("#existingUnicorn input[name='spottedWhere.lon']").value = unicorn.spottedWhere.lon;
    document.querySelector("#existingUnicorn input[name=spottedWhen]").value = legibleDate;
    document.querySelector("#existingUnicorn input[name=image]").value = unicorn.image;
    document.querySelector("#existingUnicorn [name=description]").value = unicorn.description;
    hideForms();
}

async function postUnicorn() {
    /*
     * Skapa enhörningar genom den nya funktionen
     */
    const unicorn = buildUnicorn("newUnicorn");

    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(unicorn)
    };

    await fetch(baseURL, options);
    hideForms();
}

async function putUnicorn() {
    /*
     * Skapa enhörningar genom den nya funktionen
     */
    const unicorn = buildUnicorn("existingUnicorn");

    const url = baseURL + unicorn.id;
    const options = {
        method: "PUT",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(unicorn)
    };

    await fetch(url, options);
    hideForms();
}

/*
 * Det här är en enkel funktion. Se bara till att ta bort rätt enhörning.
 */
async function deleteUnicorn() {
    /*
     * Hämta enhörningens id och lägg till det i URL:en
     */
    const url = baseURL + document.querySelector("#existingUnicorn input[name=id]").value;
    const options = {
        method: "DELETE"
    };

    await fetch(url, options);
}

function buildUnicorn(formName) {
    const unicorn = {};
    unicorn.id = document.querySelector(`#${formName} input[name=id]`).value;
    unicorn.name = document.querySelector(`#${formName} input[name=name]`).value;
    unicorn.description = document.querySelector(`#${formName} [name=description]`).value;
    unicorn.reportedBy = document.querySelector(`#${formName} input[name=reportedBy]`).value;
    unicorn.spottedWhere = {
        name: document.querySelector(`#${formName} input[name='spottedWhere.name']`).value,
        lat: document.querySelector(`#${formName} input[name='spottedWhere.lat']`).value,
        lon: document.querySelector(`#${formName} input[name='spottedWhere.lon']`).value
    };
    unicorn.spottedWhen = document.querySelector(`#${formName} input[name=spottedWhen]`).value + " 00:00:00";
    unicorn.image = document.querySelector(`#${formName} input[name=image]`).value;

    if (unicorn.id == "") {
        delete(unicorn.id);
    }

    return unicorn;
}

function hideForms() {
    document.querySelectorAll("form").forEach((form) => {
        form.style.display = "none";
    });
}

function showAddForm() {
    hideForms();
    document.querySelector("#newUnicorn").style.display = "block";
}

function showUpdateForm() {
    hideForms();
    document.querySelector("#existingUnicorn").style.display = "block";
}

document.querySelector("#addUnicorn").addEventListener("click", showAddForm);
document.querySelector("#updateUnicorn").addEventListener("click", showUpdateForm);
document.querySelector("#postUnicorn").addEventListener("click", postUnicorn);
document.querySelector("#putUnicorn").addEventListener("click", putUnicorn);
/*
 * Koppla deleteUnicorn() till knappen #deleteUnicorn
 */
document.querySelector("#deleteUnicorn").addEventListener("click", deleteUnicorn);
hideForms();
listUnicorns();