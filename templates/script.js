update = async () => {
    const data = await (await fetch('/update')).json()

    const thumbnail = document.getElementById("thumbnail");
    thumbnail.src = data.thumbnail;

    const title = document.getElementById("title");
    title.innerText = data.title;

    const played = document.getElementById("played");
    played.style.flexGrow = data.played;

    const remain = document.getElementById("remain");
    remain.style.flexGrow = data.remain;
}

setInterval(update, 1000)