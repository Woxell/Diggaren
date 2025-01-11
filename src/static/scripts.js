const srURL = '';
var currentRadioID = -1;

//Anropas vid klick på en radiostation i listan till vänster
async function displayStation(channelJson) {
    currentRadioID = channelJson.id;
    document.getElementById("currentRadio").innerHTML = channelJson.name;
    document.getElementById("player").querySelector('source').src = channelJson.liveaudio.url;
    document.getElementById("player").load();
    document.getElementById("addToSpotify").value = currentRadioID;
    await updateCurrentlyPlaying(currentRadioID);
}

//Uppdatera info om låttitel, artist, osv...
async function updateCurrentlyPlaying(currentRadioID) {
    try {
        const currentSongJson = await getCurrentSong(currentRadioID);
        document.getElementById("currentArtist").innerHTML = "Artist: " + currentSongJson.playlist.song.artist;
        document.getElementById("currentSong").innerHTML = "Titel: " + currentSongJson.playlist.song.title;
    } catch (e) {
        document.getElementById("currentArtist").innerHTML = 'Ingen låt spelas';
        document.getElementById("currentSong").innerHTML = 'Någon som yappar kanske?';
    }
}

//För ett givet radiostations-ID hämtas och returneras ett JSON-objekt
async function getCurrentSong(channelID) {
    const endpoint = 'https://api.sr.se/api/v2/playlists/rightnow?channelid=' + channelID + '&format=json';
    const options = {
        method: "GET",
        headers: {
            "Accept": "application/json"
        }
    };
    const response = await fetch(endpoint, options);
    return await response.json();
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

infoRefresher();