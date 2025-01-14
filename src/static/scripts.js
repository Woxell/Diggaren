const baseURL = 'http://127.0.0.1:5000/';
var currentRadioID = -1;

//Utförs när webbsidan laddas, för att bygga listan med radiostationer till vänster
async function buildRadioList() {
    const endpoint = baseURL + '/radio';
    const options = {
        method: "GET",
        headers: {
            "Accept": "application/json"
        }
    };
    const response = await fetch(endpoint, options);
    const radioJSON = await response.json();
    const radioList = document.querySelector("#stations");
    radioJSON.channels.forEach((channel) => {
        let listItem = document.createElement("li");
        let paragraphItem = document.createElement("span");
        let anchorItem = document.createElement("a");
        paragraphItem.innerHTML = " - " + channel.tagline;
        paragraphItem.id = "radioDescription";
        anchorItem.target = "_blank";
        anchorItem.innerHTML = channel.name;
        anchorItem.id = "radioLink";
        anchorItem.addEventListener("click", () => displayStation(channel));
        listItem.appendChild(anchorItem);
        listItem.appendChild(paragraphItem);
        radioList.appendChild(listItem);
    });
}

//Anropas vid klick på en radiostation i listan till vänster
async function displayStation(channelJson) {
    currentRadioID = channelJson.id;
    document.getElementById("currentRadio").innerHTML = channelJson.name;
    document.getElementById("player").querySelector('source').src = channelJson.liveaudio.url;
    document.getElementById("player").load();
    await updateCurrentlyPlaying(currentRadioID);
}

// Uppdatera info om låttitel, artist, start- och stopptider
async function updateCurrentlyPlaying(currentRadioID) {

    // Hämta låtdata
    const currentSongJson = await getCurrentSongJSON(currentRadioID);

    let currentArtist, currentTitle, currentStartTime, previousArtist, previousTitle, previousStartTime;

    // Kontrollera om nuvarande låtdata finns
    const currentSong = currentSongJson?.playlist?.song;
    if (currentSong) {
        currentArtist = currentSong.artist || "Okänd artist";
        currentTitle = currentSong.title || "Okänd titel";

        // Bearbeta starttid för nuvarande låt
        const startTimeUTC = currentSong.starttimeutc;
        if (startTimeUTC) {
            const timestamp = parseInt(startTimeUTC.replace("/Date(", "").replace(")/", ""));
            const startDate = new Date(timestamp);
            currentStartTime = startDate.toLocaleTimeString('sv-SE', {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
            });
        }
    }

    // Kontrollera om föregående låtdata finns
    const previousSong = currentSongJson?.playlist?.previoussong;
    if (previousSong) {
        previousArtist = previousSong.artist || "Okänd artist";
        previousTitle = previousSong.title || "Okänd titel";

        // Bearbeta starttid för föregående låt
        const previousStartTimeUTC = previousSong.starttimeutc;
        if (previousStartTimeUTC) {
            const timestamp = parseInt(previousStartTimeUTC.replace("/Date(", "").replace(")/", ""));
            const startDate = new Date(timestamp);
            previousStartTime = startDate.toLocaleTimeString('sv-SE', {
                hour: '2-digit',
                minute: '2-digit',
                second: '2-digit',
            });
        }
    }

    document.getElementById("currentArtist").innerHTML = currentArtist ? "Artist: " + currentArtist : "Detta låter inte bra...";
    document.getElementById("currentSong").innerHTML = currentTitle ? "Titel: " + currentTitle : "Någon som yappar kanske?";
    document.getElementById("currentTime").innerHTML = currentStartTime ? "Startade: " + currentStartTime :"";

    document.getElementById("previousArtist").innerHTML = "Föregående artist: " + previousArtist;
    document.getElementById("previousSong").innerHTML = "Föregående titel: " + previousTitle;
    document.getElementById("prevousSongStart").innerHTML = "Startade: " + previousStartTime;
}


//För ett givet radiostations-ID hämtas och returneras ett JSON-objekt
async function getCurrentSongJSON(channelID) {
    const endpoint = baseURL + "/radio/" + channelID;
    const options = {
        method: "GET",
        headers: {
            "Accept": "application/json"
        }
    };
    const response = await fetch(endpoint, options);
    return await response.json();
}

function searchCurrent() {
    let phrase = {
        artist: (document.getElementById("currentArtist").innerHTML).replace("Artist: ", ""),
        title: (document.getElementById("currentSong").innerHTML).replace("Titel: ", "")
    };
    if (phrase.artist.substring(0, 5) === "Ingen") {
        return;
    }
    search(phrase);
}

function searchPrevious() {
    let phrase = {
        artist: (document.getElementById("previousArtist").innerHTML).replace("Föregående artist: ", ""),
        title: (document.getElementById("previousSong").innerHTML).replace("Föregående titel: ", "")
    };
    if (phrase.artist || phrase.song) {
        search(phrase);
    }
}

async function search(phrase) {
    const endpoint = baseURL + "result";
    const options = {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(phrase)
    };
    await fetch(endpoint, options); //Behöver inte hantera response
    refreshSearchList();
}

async function refreshSearchList() {
    const endpoint = baseURL + "result";
    const options = {
        method: "GET",
        headers: {
            "Accept": "application/json"
        }
    };
    const response = await fetch(endpoint, options);
    const searches = await response.json();
    const searchList = document.querySelector("#searchResults");
    searchList.replaceChildren();
    searches.forEach((search) => {
        let listItem = document.createElement("li");
        let anchorItem = document.createElement("a");
        anchorItem.target = "_blank";
        anchorItem.innerHTML = search.artist + ": " + search.name;
        if (anchorItem.innerHTML.length > 60) { //Om resultat-texten är för lång, korta av efter 60 tecken
            anchorItem.innerHTML = anchorItem.innerHTML.substring(0, 60) + "...";
        }
        anchorItem.id = "searchLink";
        anchorItem.href = search.spotify_url;
        listItem.appendChild(anchorItem);
        searchList.appendChild(listItem);
    });
}

// När ny låt spelas ska låttitel, artistnamn osv uppdateras.
// Detta refreshas alltså varje 5:e sekund
async function infoRefresher() {
    while (true) {
        await new Promise(resolve => setTimeout(resolve, 5000));
        if (currentRadioID !== -1) {
            await updateCurrentlyPlaying(currentRadioID)
        }
    }
}

buildRadioList();
refreshSearchList();
infoRefresher();