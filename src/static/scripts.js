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

//Uppdatera info om låttitel, artist, osv...
async function updateCurrentlyPlaying(currentRadioID) {
    try {
        const currentSongJson = await getCurrentSongJSON(currentRadioID);
        document.getElementById("currentArtist").innerHTML = "Artist: " + currentSongJson.playlist.song.artist;
        document.getElementById("currentSong").innerHTML = "Titel: " + currentSongJson.playlist.song.title;
    } catch (e) {
        document.getElementById("currentArtist").innerHTML = 'Ingen låt spelas';
        document.getElementById("currentSong").innerHTML = 'Någon som yappar kanske?';

    }
    try {
        const currentSongJson = await getCurrentSongJSON(currentRadioID);
        document.getElementById("previousArtist").innerHTML = "Föregående artist: " + currentSongJson.playlist.previoussong.artist;
        document.getElementById("previousSong").innerHTML = "Föregående titel: " + currentSongJson.playlist.previoussong.title;
    } catch (e) {
        document.getElementById("previousArtist").innerHTML = "";
        document.getElementById("previousSong").innerHTML = "";
    }
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
    const searches  = await response.json();
    const searchList = document.querySelector("#searchResults");
    searchList.replaceChildren();
    searches.forEach((search) =>{
        let listItem = document.createElement("li");
        let anchorItem = document.createElement("a");
        anchorItem.target = "_blank";
        anchorItem.innerHTML = search.artist+": "+search.name;
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