const baseURL = 'https://diggaren.fly.dev/';
var currentRadioID = -1;

//Utförs när webbsidan laddas, för att bygga listan med radiostationer till vänster
async function buildRadioList() {
    const endpoint = baseURL + 'channels';
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
    let currentArtist, currentTitle, currentStartTime;
    let previousArtist, previousTitle, previousStartTime;

    // Nuvarande låt
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

    // Föregående låt
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
    document.getElementById("currentTime").innerHTML = currentStartTime ? "Startade: " + currentStartTime : "";

    document.getElementById("previousArtist").innerHTML = "Föregående artist: " + previousArtist;
    document.getElementById("previousSong").innerHTML = "Föregående titel: " + previousTitle;
    document.getElementById("prevousSongStart").innerHTML = "Startade: " + previousStartTime;
}

//För ett givet radiostations-ID hämtas och returneras ett JSON-objekt
async function getCurrentSongJSON(channelID) {
    const endpoint = baseURL + "radio/" + channelID;
    const options = {
        method: "GET",
        headers: {
            "Accept": "application/json"
        }
    };
    const response = await fetch(endpoint, options);
    return await response.json();
}

// Initierar en sökning baserad på den nuvarande låten
function searchCurrent() {
    let phrase = {
        artist: document.getElementById("currentArtist").innerHTML.replace("Artist: ", ""),
        title: document.getElementById("currentSong").innerHTML.replace("Titel: ", "")
    };
    // Om artist saknas, avbryt
    if (phrase.artist.substring(0, 5) === "Ingen") {
        return;
    }
    search(phrase);
}

// Initierar en sökning baserad på den föregående låten
function searchPrevious() {
    let phrase = {
        artist: document.getElementById("previousArtist").innerHTML.replace("Föregående artist: ", ""),
        title: document.getElementById("previousSong").innerHTML.replace("Föregående titel: ", "")
    };
    if (phrase.artist || phrase.song) {
        search(phrase);
    }
}

// Skickar en GET-förfrågan med sökparametrarna till API:et
async function search(phrase) {
    if (!phrase.artist || !phrase.title || phrase.artist === "Okänd artist" || phrase.title === "Okänd titel") {
        return;
    }

    const endpoint = `${baseURL}result?title=${encodeURIComponent(phrase.title)}&artist=${encodeURIComponent(phrase.artist)}`;
    const options = {
        method: "GET",
        headers: {
            "Accept": "application/json"
        }
    };

    await fetch(endpoint, options); // //Behöver inte hantera response
    refreshSearchList();
}

// Hämtar de senast sparade sökningarna och uppdaterar listan i gränssnittet
async function refreshSearchList() {
    const endpoint = baseURL + "result";
    const options = {
        method: "GET",
        headers: {
            "Accept": "application/json"
        }
    };

    const response = await fetch(endpoint, options);
    const data = await response.json();

    const searchList = document.querySelector("#searchResults");
    searchList.replaceChildren();

    if (data.saved_searches) {
        data.saved_searches.forEach((search) => {
            let listItem = document.createElement("li");
            let anchorItem = document.createElement("a");
            anchorItem.target = "_blank";
            anchorItem.innerHTML = search.artist + ": " + search.name;

            // Om texten är för lång, förkorta den
            if (anchorItem.innerHTML.length > 60) {
                anchorItem.innerHTML = anchorItem.innerHTML.substring(0, 60) + "...";
            }

            anchorItem.id = "searchLink";
            anchorItem.href = search.spotify_url;
            listItem.appendChild(anchorItem);
            searchList.appendChild(listItem);
        });
    }
}

// När ny låt spelas ska låttitel, artistnamn osv uppdateras.
// Detta refreshas alltså varje 5:e sekund
async function infoRefresher() {
    while (true) {
        await new Promise(resolve => setTimeout(resolve, 5000));
        if (currentRadioID !== -1) {
            await updateCurrentlyPlaying(currentRadioID);
        }
    }
}

buildRadioList();
refreshSearchList();
infoRefresher();
