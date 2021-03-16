const shortenNamesBtn = document.querySelector("#shortcutButton")
const actorsNames = document.querySelectorAll(".actor-name")

shortenNamesBtn.addEventListener("click", () => {
    for (let actor of actorsNames){
        let nameSplit = actor.textContent.split(" ")
        nameSplit[0] = `${nameSplit[0].slice(0,1)}.`
        actor.textContent = nameSplit.join(" ")
    }
})
